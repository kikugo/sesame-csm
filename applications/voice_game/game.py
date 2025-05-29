"""Voice game implementation for CSM"""

import torch
from typing import Dict, List, Tuple
from generator import load_csm_1b, Segment
from applications.shared_utils import load_prompt_audio, save_audio, concatenate_audio_segments

class VoiceGame:
    """
    Generate game dialogue with multiple characters using CSM
    """
    
    def __init__(self, character_prompts: Dict[int, Tuple[str, str, str]], device="cuda"):
        """
        Initialize the voice game
        
        Args:
            character_prompts (Dict): Dictionary mapping character_id to (name, text, audio_path)
            device (str): Device to load the model on
        """
        self.character_prompts = character_prompts
        self.device = device
        self.generator = None
        self.characters = {}
        self.dialogue_history = []
        
    def initialize(self):
        """Initialize the CSM model and character prompts"""
        print("🎮 Initializing Voice Game...")
        self.generator = load_csm_1b(device=self.device)
        self.characters = self._create_characters()
        print("✅ Voice Game ready!")
        
    def _create_characters(self):
        """Create character prompt segments"""
        characters = {}
        for char_id, (name, text, audio_path) in self.character_prompts.items():
            audio = load_prompt_audio(audio_path, self.generator.sample_rate)
            characters[char_id] = {
                "name": name,
                "prompt": Segment(
                    text=text,
                    speaker=char_id,
                    audio=audio
                )
            }
            print(f"   📝 Created character: {name} (ID: {char_id})")
        return characters
    
    def character_speak(self, character_id: int, text: str, context: List[Segment] = None):
        """
        Generate speech for a specific character
        
        Args:
            character_id (int): ID of the character
            text (str): Text for the character to say
            context (List[Segment]): Additional context segments
            
        Returns:
            Segment: Character's speech segment
        """
        if self.generator is None:
            raise RuntimeError("VoiceGame not initialized. Call initialize() first.")
            
        if character_id not in self.characters:
            raise ValueError(f"Character ID {character_id} not found")
        
        # Build context: character prompt + recent dialogue + additional context
        full_context = [self.characters[character_id]["prompt"]]
        
        # Add recent dialogue history (last 3 segments)
        if self.dialogue_history:
            full_context.extend(self.dialogue_history[-3:])
            
        if context:
            full_context.extend(context)
            
        # Generate audio
        audio = self.generator.generate(
            text=text,
            speaker=character_id,
            context=full_context,
            max_audio_length_ms=10_000,
        )
        
        # Create segment
        segment = Segment(
            text=text,
            speaker=character_id,
            audio=audio
        )
        
        # Add to dialogue history
        self.dialogue_history.append(segment)
        
        return segment
    
    def generate_dialogue_sequence(self, dialogue_script: List[Dict]):
        """
        Generate a complete dialogue sequence
        
        Args:
            dialogue_script (List[Dict]): List of dialogue entries with 'character_id' and 'text'
            
        Returns:
            Tuple[torch.Tensor, List[Segment]]: (full_audio, segments)
        """
        if self.generator is None:
            raise RuntimeError("VoiceGame not initialized. Call initialize() first.")
        
        print(f"🎭 Generating dialogue sequence ({len(dialogue_script)} lines)...")
        
        segments = []
        
        for i, line in enumerate(dialogue_script, 1):
            character_id = line["character_id"]
            text = line["text"]
            character_name = self.characters[character_id]["name"]
            
            print(f"  {i}/{len(dialogue_script)} - {character_name}: '{text[:50]}...'")
            
            segment = self.character_speak(character_id, text)
            segments.append(segment)
        
        # Combine all audio
        full_audio = concatenate_audio_segments(segments)
        return full_audio, segments
    
    def generate_combat_dialogue(self, scenario="battle"):
        """
        Generate combat-specific dialogue
        
        Args:
            scenario (str): Type of combat scenario
            
        Returns:
            Tuple[torch.Tensor, List[Segment]]: (full_audio, segments)
        """
        combat_scripts = {
            "battle": [
                {"character_id": 0, "text": "Ready your weapons! Here they come!"},
                {"character_id": 1, "text": "You'll never defeat us, heroes!"},
                {"character_id": 0, "text": "We'll see about that! Attack!"},
                {"character_id": 1, "text": "Take this! Dark magic strike!"},
                {"character_id": 0, "text": "Shield up! Counter with fire spell!"},
                {"character_id": 1, "text": "Impossible! How are you so strong?"},
                {"character_id": 0, "text": "Justice always prevails! Victory is ours!"}
            ],
            "boss_fight": [
                {"character_id": 2, "text": "So, you dare challenge me in my own domain?"},
                {"character_id": 0, "text": "We've come to stop your reign of terror!"},
                {"character_id": 2, "text": "Foolish mortals! Behold my true power!"},
                {"character_id": 0, "text": "Everyone, stay together! This is our final battle!"},
                {"character_id": 2, "text": "You cannot hope to defeat a god!"},
                {"character_id": 0, "text": "We fight for hope! For the future! We will not fall!"}
            ]
        }
        
        if scenario not in combat_scripts:
            raise ValueError(f"Unknown combat scenario: {scenario}")
        
        return self.generate_dialogue_sequence(combat_scripts[scenario])
    
    def generate_story_dialogue(self, scenario="quest_start"):
        """
        Generate story-specific dialogue
        
        Args:
            scenario (str): Type of story scenario
            
        Returns:
            Tuple[torch.Tensor, List[Segment]]: (full_audio, segments)
        """
        story_scripts = {
            "quest_start": [
                {"character_id": 3, "text": "Welcome, brave adventurers. I have a quest for you."},
                {"character_id": 0, "text": "We're ready to help. What do you need?"},
                {"character_id": 3, "text": "The ancient crystal has been stolen from our temple."},
                {"character_id": 0, "text": "That sounds serious. Where should we look?"},
                {"character_id": 3, "text": "The thieves fled toward the Dark Forest. Be careful, it's dangerous."},
                {"character_id": 0, "text": "Don't worry. We'll retrieve your crystal and bring justice."}
            ],
            "shop_interaction": [
                {"character_id": 4, "text": "Welcome to my shop! I have the finest weapons and potions."},
                {"character_id": 0, "text": "What do you have for a warrior preparing for battle?"},
                {"character_id": 4, "text": "Ah! This enchanted sword will serve you well against dark creatures."},
                {"character_id": 0, "text": "Perfect! How much for the sword and some healing potions?"},
                {"character_id": 4, "text": "For a hero like you, I'll give you a special price. Safe travels!"}
            ]
        }
        
        if scenario not in story_scripts:
            raise ValueError(f"Unknown story scenario: {scenario}")
        
        return self.generate_dialogue_sequence(story_scripts[scenario])
    
    def save_dialogue(self, audio_tensor: torch.Tensor, filename: str):
        """
        Save dialogue audio to file
        
        Args:
            audio_tensor (torch.Tensor): Audio tensor to save
            filename (str): Output filename
        """
        save_audio(audio_tensor, filename, self.generator.sample_rate)
    
    def get_character_info(self):
        """Get information about all characters"""
        info = {}
        for char_id, char_data in self.characters.items():
            info[char_id] = {
                "name": char_data["name"],
                "speaker_id": char_id
            }
        return info
    
    def clear_dialogue_history(self):
        """Clear the dialogue history"""
        self.dialogue_history = []
        print("🧹 Dialogue history cleared") 