"""
Test script to verify Downloads folder detection works correctly.
"""
import os
import sys
import ctypes
from ctypes import wintypes


def get_downloads_folder():
    """Get user's Downloads folder path."""
    if os.name == 'nt':  # Windows
        try:
            CSIDL_DOWNLOADS = 0x0028
            buffer = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
            ctypes.windll.shell32.SHGetFolderPathW(0, CSIDL_DOWNLOADS, 0, 0, buffer)
            downloads_path = buffer.value
            return downloads_path
        except Exception as e:
            print(f"Error getting Downloads folder: {e}")
            return None
    else:
        return os.path.expanduser("~/Downloads")


def main():
    print("="*70)
    print("DOWNLOADS FOLDER DETECTION TEST")
    print("="*70)
    print()
    
    # Test Downloads folder detection
    downloads = get_downloads_folder()
    
    if downloads:
        print(f"✅ Downloads folder detected: {downloads}")
        print()
        
        # Check if folder exists
        if os.path.exists(downloads):
            print(f"✅ Downloads folder exists")
        else:
            print(f"❌ Downloads folder does not exist!")
        
        # Check if writable
        try:
            test_file = os.path.join(downloads, ".testtrace_test.tmp")
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            print(f"✅ Downloads folder is writable")
        except Exception as e:
            print(f"❌ Downloads folder is NOT writable: {e}")
    else:
        print("❌ Could not detect Downloads folder")
    
    print()
    print("="*70)
    print("TEST COMPLETE")
    print("="*70)
    print()
    
    if downloads and os.path.exists(downloads):
        print("✅ Reports will be saved to:", downloads)
        print()
        print("When you generate a report, look for it in your Downloads folder!")
    else:
        print("⚠️ Warning: Downloads folder detection failed")
        print("Reports may save to fallback location")


if __name__ == "__main__":
    main()
