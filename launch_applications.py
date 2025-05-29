#!/usr/bin/env python3
"""
CSM Applications Launcher
Main entry point for all CSM applications
"""

import sys
import os
import torch
from typing import Dict, Callable

def get_device_info():
    """Get available device information"""
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
        return f"🎮 CUDA GPU: {gpu_name} ({gpu_memory:.1f}GB)"
    elif torch.backends.mps.is_available():
        return "🍎 Apple Metal (MPS)"
    else:
        return "💻 CPU (will be slow for large models)"

def show_banner():
    """Display application banner"""
    print("=" * 60)
    print("🎭 CSM Applications Suite")
    print("   Conversational Speech Model Applications")
    print("=" * 60)
    print(f"📱 Device: {get_device_info()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"🔥 PyTorch: {torch.__version__}")
    print("=" * 60)

def show_applications():
    """Display available applications"""
    apps = {
        "1": {
            "name": "🎭 Character Chat",
            "description": "Create AI characters with consistent voices",
            "module": "applications.character_chat.run",
            "function": "main"
        },
        "2": {
            "name": "📚 Story Generator", 
            "description": "Convert stories to audio narration",
            "module": "applications.story_generator.run",
            "function": "main"
        },
        "3": {
            "name": "🎮 Voice Game",
            "description": "Generate game dialogue (Coming Soon)",
            "module": "applications.voice_game.run",
            "function": "main"
        },
        "4": {
            "name": "🔧 Configuration",
            "description": "Configure application settings",
            "module": "applications.config.run",
            "function": "main"
        },
        "5": {
            "name": "🧪 Quick Test",
            "description": "Run a quick CSM test",
            "module": "applications.quick_test",
            "function": "main"
        }
    }
    
    print("\n📋 Available Applications:")
    print("-" * 40)
    for key, app in apps.items():
        print(f"{key}. {app['name']}")
        print(f"   {app['description']}")
        print()
    
    return apps

def run_application(choice: str, apps: Dict):
    """Run the selected application"""
    if choice not in apps:
        print(f"❌ Invalid choice: {choice}")
        return
    
    app = apps[choice]
    print(f"\n🚀 Starting {app['name']}...")
    print("-" * 40)
    
    try:
        # Dynamic import and execution
        module_name = app['module']
        function_name = app['function']
        
        # Import the module
        module = __import__(module_name, fromlist=[function_name])
        
        # Get the function and run it
        func = getattr(module, function_name)
        func()
        
    except ModuleNotFoundError as e:
        print(f"❌ Application not yet implemented: {app['name']}")
        print(f"   Module '{module_name}' not found")
        if "voice_game" in module_name:
            print("   🔧 Voice Game is coming soon!")
        elif "config" in module_name:
            print("   🔧 Configuration system is coming soon!")
    except Exception as e:
        print(f"❌ Error running {app['name']}: {e}")
        print("💡 Make sure you have:")
        print("   - Sufficient GPU memory")
        print("   - Hugging Face access (run 'huggingface-cli login')")
        print("   - Required dependencies installed")

def main():
    """Main launcher function"""
    show_banner()
    
    # Check for required environment
    try:
        import torch
        import torchaudio
        import transformers
        print("✅ Core dependencies found")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return
    
    while True:
        apps = show_applications()
        
        print("💡 Enter 'q' to quit")
        choice = input("\n🎯 Select an application (1-5): ").strip().lower()
        
        if choice == 'q' or choice == 'quit':
            print("\n👋 Goodbye!")
            break
            
        if choice in apps:
            run_application(choice, apps)
            input("\n⏸️  Press Enter to continue...")
        else:
            print(f"❌ Invalid choice: {choice}")

if __name__ == "__main__":
    main() 