"""Configuration management for CSM applications"""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class AudioSettings:
    """Audio generation settings"""
    sample_rate: int = 24000
    max_audio_length_ms: int = 10000
    output_format: str = "wav"
    quality: str = "high"  # low, medium, high
    use_watermark: bool = False

@dataclass
class DeviceSettings:
    """Device and performance settings"""
    preferred_device: str = "auto"  # auto, cuda, mps, cpu
    batch_size: int = 1
    memory_optimization: bool = True
    compile_model: bool = False

@dataclass
class OutputSettings:
    """Output and file management settings"""
    output_directory: str = "outputs"
    save_transcripts: bool = True
    save_metadata: bool = True
    auto_cleanup: bool = False
    max_output_files: int = 100

@dataclass
class UISettings:
    """User interface settings"""
    show_progress: bool = True
    verbose_logging: bool = False
    confirm_destructive_actions: bool = True
    theme: str = "default"

@dataclass
class CSMConfig:
    """Complete CSM application configuration"""
    audio: AudioSettings
    device: DeviceSettings
    output: OutputSettings
    ui: UISettings
    version: str = "1.0"

class ConfigManager:
    """
    Manage application configuration
    """
    
    def __init__(self, config_file: str = "config/csm_config.json"):
        """
        Initialize configuration manager
        
        Args:
            config_file (str): Path to configuration file
        """
        self.config_file = config_file
        self.config = self._load_or_create_default()
    
    def _load_or_create_default(self) -> CSMConfig:
        """Load existing config or create default"""
        if os.path.exists(self.config_file):
            try:
                return self.load_config()
            except Exception as e:
                print(f"⚠️  Error loading config: {e}")
                print("🔧 Creating default configuration...")
        
        return self._create_default_config()
    
    def _create_default_config(self) -> CSMConfig:
        """Create default configuration"""
        return CSMConfig(
            audio=AudioSettings(),
            device=DeviceSettings(),
            output=OutputSettings(),
            ui=UISettings()
        )
    
    def load_config(self) -> CSMConfig:
        """
        Load configuration from file
        
        Returns:
            CSMConfig: Loaded configuration
        """
        with open(self.config_file, 'r') as f:
            data = json.load(f)
        
        return CSMConfig(
            audio=AudioSettings(**data.get("audio", {})),
            device=DeviceSettings(**data.get("device", {})),
            output=OutputSettings(**data.get("output", {})),
            ui=UISettings(**data.get("ui", {})),
            version=data.get("version", "1.0")
        )
    
    def save_config(self):
        """Save configuration to file"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        
        # Convert dataclasses to dict
        config_dict = {
            "audio": asdict(self.config.audio),
            "device": asdict(self.config.device),
            "output": asdict(self.config.output),
            "ui": asdict(self.config.ui),
            "version": self.config.version
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config_dict, f, indent=2)
        
        print(f"💾 Configuration saved to: {self.config_file}")
    
    def update_audio_settings(self, **kwargs):
        """Update audio settings"""
        for key, value in kwargs.items():
            if hasattr(self.config.audio, key):
                setattr(self.config.audio, key, value)
            else:
                print(f"⚠️  Unknown audio setting: {key}")
    
    def update_device_settings(self, **kwargs):
        """Update device settings"""
        for key, value in kwargs.items():
            if hasattr(self.config.device, key):
                setattr(self.config.device, key, value)
            else:
                print(f"⚠️  Unknown device setting: {key}")
    
    def update_output_settings(self, **kwargs):
        """Update output settings"""
        for key, value in kwargs.items():
            if hasattr(self.config.output, key):
                setattr(self.config.output, key, value)
            else:
                print(f"⚠️  Unknown output setting: {key}")
    
    def update_ui_settings(self, **kwargs):
        """Update UI settings"""
        for key, value in kwargs.items():
            if hasattr(self.config.ui, key):
                setattr(self.config.ui, key, value)
            else:
                print(f"⚠️  Unknown UI setting: {key}")
    
    def get_device_preference(self) -> str:
        """
        Get preferred device based on configuration and availability
        
        Returns:
            str: Device to use
        """
        if self.config.device.preferred_device == "auto":
            import torch
            if torch.cuda.is_available():
                return "cuda"
            elif torch.backends.mps.is_available():
                return "mps"
            else:
                return "cpu"
        
        return self.config.device.preferred_device
    
    def get_quality_settings(self) -> Dict[str, Any]:
        """
        Get quality settings based on configuration
        
        Returns:
            Dict: Quality settings for generation
        """
        quality_map = {
            "low": {
                "max_audio_length_ms": 5000,
                "batch_size": 1,
                "memory_optimization": True
            },
            "medium": {
                "max_audio_length_ms": 8000,
                "batch_size": 1,
                "memory_optimization": True
            },
            "high": {
                "max_audio_length_ms": 15000,
                "batch_size": 1,
                "memory_optimization": False
            }
        }
        
        base_settings = quality_map.get(self.config.audio.quality, quality_map["medium"])
        
        # Override with user settings
        base_settings.update({
            "max_audio_length_ms": self.config.audio.max_audio_length_ms,
            "sample_rate": self.config.audio.sample_rate
        })
        
        return base_settings
    
    def show_current_config(self):
        """Display current configuration"""
        print("🔧 Current CSM Configuration")
        print("=" * 40)
        
        print("\n🎵 Audio Settings:")
        print(f"  Sample Rate: {self.config.audio.sample_rate} Hz")
        print(f"  Max Length: {self.config.audio.max_audio_length_ms} ms")
        print(f"  Quality: {self.config.audio.quality}")
        print(f"  Output Format: {self.config.audio.output_format}")
        print(f"  Watermark: {self.config.audio.use_watermark}")
        
        print("\n🖥️  Device Settings:")
        print(f"  Preferred Device: {self.config.device.preferred_device}")
        print(f"  Actual Device: {self.get_device_preference()}")
        print(f"  Batch Size: {self.config.device.batch_size}")
        print(f"  Memory Optimization: {self.config.device.memory_optimization}")
        print(f"  Model Compilation: {self.config.device.compile_model}")
        
        print("\n📁 Output Settings:")
        print(f"  Directory: {self.config.output.output_directory}")
        print(f"  Save Transcripts: {self.config.output.save_transcripts}")
        print(f"  Save Metadata: {self.config.output.save_metadata}")
        print(f"  Auto Cleanup: {self.config.output.auto_cleanup}")
        print(f"  Max Files: {self.config.output.max_output_files}")
        
        print("\n🎨 UI Settings:")
        print(f"  Show Progress: {self.config.ui.show_progress}")
        print(f"  Verbose Logging: {self.config.ui.verbose_logging}")
        print(f"  Confirm Actions: {self.config.ui.confirm_destructive_actions}")
        print(f"  Theme: {self.config.ui.theme}")
    
    def reset_to_defaults(self):
        """Reset configuration to defaults"""
        self.config = self._create_default_config()
        print("🔄 Configuration reset to defaults")
    
    def export_config(self, filename: str):
        """Export configuration to a file"""
        config_dict = {
            "audio": asdict(self.config.audio),
            "device": asdict(self.config.device),
            "output": asdict(self.config.output),
            "ui": asdict(self.config.ui),
            "version": self.config.version
        }
        
        with open(filename, 'w') as f:
            json.dump(config_dict, f, indent=2)
        
        print(f"📤 Configuration exported to: {filename}")
    
    def import_config(self, filename: str):
        """Import configuration from a file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.config = CSMConfig(
            audio=AudioSettings(**data.get("audio", {})),
            device=DeviceSettings(**data.get("device", {})),
            output=OutputSettings(**data.get("output", {})),
            ui=UISettings(**data.get("ui", {})),
            version=data.get("version", "1.0")
        )
        
        print(f"📥 Configuration imported from: {filename}")

# Global configuration manager instance
_config_manager = None

def get_config() -> ConfigManager:
    """Get global configuration manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager

def load_app_config() -> CSMConfig:
    """Load application configuration"""
    return get_config().config 