"""Character implementation for conversational AI"""

from dataclasses import dataclass
from typing import List, Optional
import torch
from generator import load_csm_1b, Segment
from applications.shared_utils import load_prompt_audio, save_audio

@dataclass
class Character:
    """
    A conversational AI character with consistent voice and personality
    """
    name: str
    prompt_text: str
    prompt_audio_path: str
    speaker_id: int
    personality: Optional[str] = None
    
    def __post_init__(self):
        """Initialize the character after creation"""
        self.generator = None
        self.prompt = None
        self._conversation_history = []
        
    def initialize(self, device="cuda"):
        """
        Initialize the CSM model and character prompt
        
        Args:
            device (str): Device to load the model on
        """
        print(f"🤖 Initializing character '{self.name}'...")
        self.generator = load_csm_1b(device=device)
        self.prompt = self._create_prompt()
        print(f"✅ Character '{self.name}' ready!")
        
    def _create_prompt(self):
        """Create the character's voice prompt segment"""
        audio = load_prompt_audio(self.prompt_audio_path, self.generator.sample_rate)
        return Segment(
            text=self.prompt_text,
            speaker=self.speaker_id,
            audio=audio
        )
    
    def respond(self, text: str, context: Optional[List[Segment]] = None, use_history=True):
        """
        Generate a response from the character
        
        Args:
            text (str): Text for the character to say
            context (List[Segment], optional): Additional context segments
            use_history (bool): Whether to use conversation history
            
        Returns:
            Segment: Character's response as an audio segment
        """
        if self.generator is None:
            raise RuntimeError("Character not initialized. Call initialize() first.")
            
        # Build context from prompt, history, and additional context
        full_context = [self.prompt]
        
        if use_history:
            full_context.extend(self._conversation_history)
            
        if context:
            full_context.extend(context)
            
        # Generate audio response
        audio = self.generator.generate(
            text=text,
            speaker=self.speaker_id,
            context=full_context,
            max_audio_length_ms=10_000,
        )
        
        # Create response segment
        response = Segment(
            text=text,
            speaker=self.speaker_id,
            audio=audio
        )
        
        # Add to history
        self._conversation_history.append(response)
        
        return response
    
    def save_response(self, response: Segment, filename: str):
        """
        Save a response to an audio file
        
        Args:
            response (Segment): Response segment to save
            filename (str): Output filename
        """
        save_audio(response.audio, filename, self.generator.sample_rate)
        
    def get_conversation_history(self):
        """Get the character's conversation history"""
        return self._conversation_history.copy()
        
    def clear_history(self):
        """Clear the character's conversation history"""
        self._conversation_history = []
        
    def get_info(self):
        """Get character information"""
        return {
            "name": self.name,
            "speaker_id": self.speaker_id,
            "personality": self.personality,
            "conversation_length": len(self._conversation_history)
        } 