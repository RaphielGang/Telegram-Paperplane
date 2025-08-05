#!/usr/bin/env python3
"""
Test script to verify Paperplane setup
"""

import os
import sys
from pathlib import Path

def test_requirements():
    """Test if all required packages can be imported"""
    print("🧪 Testing package imports...")
    
    required_packages = [
        'telethon',
        'pymongo',
        'redis',
        'aiohttp',
        'python-dotenv',
        'Pillow',
        'requests'
    ]
    
    failed_imports = []
    
    for package in required_packages:
        try:
            if package == 'python-dotenv':
                import dotenv
            elif package == 'Pillow':
                import PIL
            else:
                __import__(package)
            print(f"  ✅ {package}")
        except ImportError as e:
            print(f"  ❌ {package}: {e}")
            failed_imports.append(package)
    
    return len(failed_imports) == 0

def test_config():
    """Test configuration file"""
    print("\n🔧 Testing configuration...")
    
    config_path = Path("config.env")
    if not config_path.exists():
        print("  ❌ config.env not found")
        print("  💡 Run: python setup.py")
        return False
    
    print("  ✅ config.env exists")
    
    # Load and check required variables
    from dotenv import load_dotenv
    load_dotenv("config.env")
    
    required_vars = ['API_KEY', 'API_HASH']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
            print(f"  ❌ {var} not set")
        else:
            print(f"  ✅ {var} is set")
    
    optional_vars = ['STRING_SESSION', 'MONGO_DB_URI']
    for var in optional_vars:
        if os.environ.get(var):
            print(f"  ✅ {var} is set")
        else:
            print(f"  ⚠️  {var} not set (optional but recommended)")
    
    return len(missing_vars) == 0

def test_userbot_module():
    """Test if userbot module can be imported"""
    print("\n🤖 Testing userbot module...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, str(Path.cwd()))
        
        # Try to import userbot
        import userbot
        print("  ✅ userbot module imported successfully")
        return True
    except Exception as e:
        print(f"  ❌ Failed to import userbot: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Paperplane Setup Test")
    print("=" * 50)
    
    tests = [
        ("Package Requirements", test_requirements),
        ("Configuration", test_config),
        ("Userbot Module", test_userbot_module)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup looks good.")
        print("\n📋 Next steps:")
        print("1. Generate string session: python generate_string_session.py")
        print("2. Set up MongoDB and update MONGO_DB_URI")
        print("3. Run the bot: python -m userbot")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())