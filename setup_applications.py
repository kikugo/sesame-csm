#!/usr/bin/env python3
"""
CSM Applications Setup Script
Helps users set up their environment for running CSM applications
"""

import os
import sys
import subprocess
import torch

def print_banner():
    """Print setup banner"""
    print("=" * 60)
    print("🔧 CSM Applications Setup")
    print("   Environment preparation for CSM applications")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10+ required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("💡 Please upgrade Python to 3.10 or later")
        return False
    else:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        ("torch", "PyTorch"),
        ("torchaudio", "TorchAudio"),
        ("transformers", "Transformers"),
        ("huggingface_hub", "Hugging Face Hub"),
        ("moshi", "Moshi")
    ]
    
    missing = []
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"✅ {name} - Installed")
        except ImportError:
            print(f"❌ {name} - Missing")
            missing.append(package)
    
    return missing

def install_dependencies(missing_packages):
    """Install missing dependencies"""
    if not missing_packages:
        return True
        
    print(f"\n📥 Installing missing packages: {', '.join(missing_packages)}")
    print("⚠️  This may take several minutes...")
    
    try:
        # Install from requirements.txt if it exists
        if os.path.exists("requirements.txt"):
            print("📋 Installing from requirements.txt...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        else:
            print("📦 Installing individual packages...")
            for package in missing_packages:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("💡 Try running manually: pip install -r requirements.txt")
        return False

def check_device_compatibility():
    """Check device compatibility"""
    print("\n🖥️  Checking device compatibility...")
    
    if torch.cuda.is_available():
        gpu_count = torch.cuda.device_count()
        for i in range(gpu_count):
            gpu_name = torch.cuda.get_device_name(i)
            gpu_memory = torch.cuda.get_device_properties(i).total_memory / 1024**3
            print(f"✅ CUDA GPU {i}: {gpu_name} ({gpu_memory:.1f}GB)")
        
        if gpu_memory < 4:
            print("⚠️  GPU has less than 4GB memory - consider using CPU mode")
        elif gpu_memory < 8:
            print("⚠️  GPU has less than 8GB memory - some features may be slow")
        else:
            print("✅ GPU memory sufficient for all features")
            
    elif torch.backends.mps.is_available():
        print("✅ Apple Metal (MPS) available")
        print("💡 MPS should work well for most features")
    else:
        print("⚠️  Only CPU available")
        print("💡 CPU mode will work but be significantly slower")

def check_huggingface_access():
    """Check Hugging Face access"""
    print("\n🤗 Checking Hugging Face access...")
    
    try:
        from huggingface_hub import HfApi
        api = HfApi()
        
        # Try to access user info (requires login)
        try:
            user_info = api.whoami()
            print(f"✅ Logged in as: {user_info['name']}")
            return True
        except Exception:
            print("❌ Not logged in to Hugging Face")
            print("💡 Run: huggingface-cli login")
            return False
            
    except ImportError:
        print("❌ Hugging Face Hub not available")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ["outputs", "config"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created: {directory}/")
        else:
            print(f"✅ Exists: {directory}/")

def test_basic_functionality():
    """Test basic PyTorch functionality"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        # Test PyTorch
        x = torch.randn(2, 3)
        y = x + 1
        print("✅ PyTorch basic operations work")
        
        # Test device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        x = x.to(device)
        print(f"✅ Device operations work on {device}")
        
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def show_next_steps():
    """Show next steps to user"""
    print("\n🎯 Next Steps:")
    print("-" * 30)
    print("1. 🤗 Login to Hugging Face:")
    print("   huggingface-cli login")
    print()
    print("2. 🧪 Test your setup:")
    print("   python launch_applications.py")
    print("   → Select '5. Quick Test'")
    print()
    print("3. 🎭 Start with Character Chat or Story Generator")
    print()
    print("4. 🔧 Configure settings for your hardware:")
    print("   → Select '4. Configuration' in the launcher")
    print()
    print("💡 Tips:")
    print("  • Check outputs/ folder for generated files")
    print("  • Use CPU mode if you have GPU memory issues")
    print("  • All applications work offline after initial model download")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check and install dependencies
    missing = check_dependencies()
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        install_choice = input("📥 Install missing dependencies? (y/n): ").strip().lower()
        
        if install_choice in ['y', 'yes']:
            if not install_dependencies(missing):
                print("❌ Setup failed - could not install dependencies")
                sys.exit(1)
        else:
            print("⚠️  Setup incomplete - dependencies not installed")
            print("💡 Install manually: pip install -r requirements.txt")
            sys.exit(1)
    
    # Check device compatibility
    check_device_compatibility()
    
    # Check Hugging Face access
    hf_ok = check_huggingface_access()
    
    # Create directories
    create_directories()
    
    # Test basic functionality
    if not test_basic_functionality():
        print("❌ Setup failed - basic functionality test failed")
        sys.exit(1)
    
    # Show results
    print("\n🎉 Setup Summary:")
    print("=" * 30)
    print("✅ Python version compatible")
    print("✅ Dependencies installed")
    print("✅ Directories created")
    print("✅ Basic functionality works")
    
    if hf_ok:
        print("✅ Hugging Face access configured")
    else:
        print("⚠️  Hugging Face login required")
    
    # Show next steps
    show_next_steps()
    
    print("\n🚀 Setup complete! Ready to run CSM applications.")

if __name__ == "__main__":
    main() 