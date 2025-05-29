"""Configuration management interface"""

from .settings import get_config

def show_config_menu():
    """Display configuration management menu"""
    config_manager = get_config()
    
    while True:
        print("\n🔧 CSM Configuration Manager")
        print("=" * 40)
        print("1. 📋 View Current Configuration")
        print("2. 🎵 Audio Settings")
        print("3. 🖥️  Device Settings")
        print("4. 📁 Output Settings")
        print("5. 🎨 UI Settings")
        print("6. 💾 Save Configuration")
        print("7. 📤 Export Configuration")
        print("8. 📥 Import Configuration")
        print("9. 🔄 Reset to Defaults")
        print("0. ❌ Exit")
        
        choice = input("\n🎯 Select option (0-9): ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            config_manager.show_current_config()
        elif choice == "2":
            edit_audio_settings(config_manager)
        elif choice == "3":
            edit_device_settings(config_manager)
        elif choice == "4":
            edit_output_settings(config_manager)
        elif choice == "5":
            edit_ui_settings(config_manager)
        elif choice == "6":
            config_manager.save_config()
        elif choice == "7":
            export_config(config_manager)
        elif choice == "8":
            import_config(config_manager)
        elif choice == "9":
            if confirm_action("Reset all settings to defaults?"):
                config_manager.reset_to_defaults()
                config_manager.save_config()
        else:
            print("❌ Invalid choice")
        
        if choice != "0":
            input("\n⏸️  Press Enter to continue...")

def edit_audio_settings(config_manager):
    """Edit audio settings"""
    print("\n🎵 Audio Settings")
    print("-" * 30)
    
    current = config_manager.config.audio
    
    # Sample rate
    print(f"Current sample rate: {current.sample_rate} Hz")
    new_sample_rate = input("New sample rate (24000, 22050, 16000) [Enter to keep current]: ").strip()
    if new_sample_rate and new_sample_rate.isdigit():
        config_manager.update_audio_settings(sample_rate=int(new_sample_rate))
    
    # Max audio length
    print(f"Current max length: {current.max_audio_length_ms} ms")
    new_length = input("New max length in ms [Enter to keep current]: ").strip()
    if new_length and new_length.isdigit():
        config_manager.update_audio_settings(max_audio_length_ms=int(new_length))
    
    # Quality
    print(f"Current quality: {current.quality}")
    new_quality = input("New quality (low, medium, high) [Enter to keep current]: ").strip().lower()
    if new_quality in ["low", "medium", "high"]:
        config_manager.update_audio_settings(quality=new_quality)
    
    # Output format
    print(f"Current format: {current.output_format}")
    new_format = input("New format (wav, flac, mp3) [Enter to keep current]: ").strip().lower()
    if new_format in ["wav", "flac", "mp3"]:
        config_manager.update_audio_settings(output_format=new_format)
    
    # Watermark
    print(f"Current watermark: {current.use_watermark}")
    watermark_choice = input("Use watermark? (y/n) [Enter to keep current]: ").strip().lower()
    if watermark_choice in ["y", "yes"]:
        config_manager.update_audio_settings(use_watermark=True)
    elif watermark_choice in ["n", "no"]:
        config_manager.update_audio_settings(use_watermark=False)

def edit_device_settings(config_manager):
    """Edit device settings"""
    print("\n🖥️  Device Settings")
    print("-" * 30)
    
    current = config_manager.config.device
    
    # Preferred device
    print(f"Current device: {current.preferred_device}")
    print(f"Actual device: {config_manager.get_device_preference()}")
    new_device = input("Preferred device (auto, cuda, mps, cpu) [Enter to keep current]: ").strip().lower()
    if new_device in ["auto", "cuda", "mps", "cpu"]:
        config_manager.update_device_settings(preferred_device=new_device)
    
    # Batch size
    print(f"Current batch size: {current.batch_size}")
    new_batch = input("New batch size [Enter to keep current]: ").strip()
    if new_batch and new_batch.isdigit():
        config_manager.update_device_settings(batch_size=int(new_batch))
    
    # Memory optimization
    print(f"Current memory optimization: {current.memory_optimization}")
    mem_choice = input("Use memory optimization? (y/n) [Enter to keep current]: ").strip().lower()
    if mem_choice in ["y", "yes"]:
        config_manager.update_device_settings(memory_optimization=True)
    elif mem_choice in ["n", "no"]:
        config_manager.update_device_settings(memory_optimization=False)
    
    # Model compilation
    print(f"Current model compilation: {current.compile_model}")
    compile_choice = input("Compile model? (y/n) [Enter to keep current]: ").strip().lower()
    if compile_choice in ["y", "yes"]:
        config_manager.update_device_settings(compile_model=True)
    elif compile_choice in ["n", "no"]:
        config_manager.update_device_settings(compile_model=False)

def edit_output_settings(config_manager):
    """Edit output settings"""
    print("\n📁 Output Settings")
    print("-" * 30)
    
    current = config_manager.config.output
    
    # Output directory
    print(f"Current directory: {current.output_directory}")
    new_dir = input("New output directory [Enter to keep current]: ").strip()
    if new_dir:
        config_manager.update_output_settings(output_directory=new_dir)
    
    # Save transcripts
    print(f"Current save transcripts: {current.save_transcripts}")
    transcript_choice = input("Save transcripts? (y/n) [Enter to keep current]: ").strip().lower()
    if transcript_choice in ["y", "yes"]:
        config_manager.update_output_settings(save_transcripts=True)
    elif transcript_choice in ["n", "no"]:
        config_manager.update_output_settings(save_transcripts=False)
    
    # Save metadata
    print(f"Current save metadata: {current.save_metadata}")
    metadata_choice = input("Save metadata? (y/n) [Enter to keep current]: ").strip().lower()
    if metadata_choice in ["y", "yes"]:
        config_manager.update_output_settings(save_metadata=True)
    elif metadata_choice in ["n", "no"]:
        config_manager.update_output_settings(save_metadata=False)
    
    # Auto cleanup
    print(f"Current auto cleanup: {current.auto_cleanup}")
    cleanup_choice = input("Auto cleanup old files? (y/n) [Enter to keep current]: ").strip().lower()
    if cleanup_choice in ["y", "yes"]:
        config_manager.update_output_settings(auto_cleanup=True)
    elif cleanup_choice in ["n", "no"]:
        config_manager.update_output_settings(auto_cleanup=False)
    
    # Max files
    print(f"Current max files: {current.max_output_files}")
    new_max = input("New max files [Enter to keep current]: ").strip()
    if new_max and new_max.isdigit():
        config_manager.update_output_settings(max_output_files=int(new_max))

def edit_ui_settings(config_manager):
    """Edit UI settings"""
    print("\n🎨 UI Settings")
    print("-" * 30)
    
    current = config_manager.config.ui
    
    # Show progress
    print(f"Current show progress: {current.show_progress}")
    progress_choice = input("Show progress bars? (y/n) [Enter to keep current]: ").strip().lower()
    if progress_choice in ["y", "yes"]:
        config_manager.update_ui_settings(show_progress=True)
    elif progress_choice in ["n", "no"]:
        config_manager.update_ui_settings(show_progress=False)
    
    # Verbose logging
    print(f"Current verbose logging: {current.verbose_logging}")
    verbose_choice = input("Use verbose logging? (y/n) [Enter to keep current]: ").strip().lower()
    if verbose_choice in ["y", "yes"]:
        config_manager.update_ui_settings(verbose_logging=True)
    elif verbose_choice in ["n", "no"]:
        config_manager.update_ui_settings(verbose_logging=False)
    
    # Confirm actions
    print(f"Current confirm actions: {current.confirm_destructive_actions}")
    confirm_choice = input("Confirm destructive actions? (y/n) [Enter to keep current]: ").strip().lower()
    if confirm_choice in ["y", "yes"]:
        config_manager.update_ui_settings(confirm_destructive_actions=True)
    elif confirm_choice in ["n", "no"]:
        config_manager.update_ui_settings(confirm_destructive_actions=False)
    
    # Theme
    print(f"Current theme: {current.theme}")
    new_theme = input("New theme (default, dark, light) [Enter to keep current]: ").strip().lower()
    if new_theme in ["default", "dark", "light"]:
        config_manager.update_ui_settings(theme=new_theme)

def export_config(config_manager):
    """Export configuration to file"""
    filename = input("Export filename [config_export.json]: ").strip()
    if not filename:
        filename = "config_export.json"
    
    if not filename.endswith('.json'):
        filename += '.json'
    
    try:
        config_manager.export_config(filename)
    except Exception as e:
        print(f"❌ Export failed: {e}")

def import_config(config_manager):
    """Import configuration from file"""
    filename = input("Import filename: ").strip()
    
    if not filename:
        print("❌ No filename provided")
        return
    
    try:
        config_manager.import_config(filename)
        print("✅ Configuration imported successfully")
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
    except Exception as e:
        print(f"❌ Import failed: {e}")

def confirm_action(message: str) -> bool:
    """Confirm a potentially destructive action"""
    response = input(f"⚠️  {message} (y/n): ").strip().lower()
    return response in ["y", "yes"]

def main():
    """Main configuration interface"""
    print("🔧 CSM Configuration System")
    print("=" * 50)
    
    try:
        show_config_menu()
        print("\n👋 Configuration management complete!")
    except KeyboardInterrupt:
        print("\n\n👋 Configuration management cancelled")
    except Exception as e:
        print(f"\n❌ Error in configuration system: {e}")

if __name__ == "__main__":
    main() 