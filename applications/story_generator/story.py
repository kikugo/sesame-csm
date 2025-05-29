"""Story generator implementation for CSM"""

import torch
from generator import load_csm_1b, Segment
from applications.shared_utils import load_prompt_audio, save_audio, concatenate_audio_segments

class StoryGenerator:
    """
    Generate audio narration for stories using CSM
    """
    
    def __init__(self, narrator_prompt_text, narrator_prompt_audio_path, device="cuda"):
        """
        Initialize the story generator
        
        Args:
            narrator_prompt_text (str): Text for the narrator prompt
            narrator_prompt_audio_path (str): Path to narrator prompt audio
            device (str): Device to load the model on
        """
        self.narrator_prompt_text = narrator_prompt_text
        self.narrator_prompt_audio_path = narrator_prompt_audio_path
        self.device = device
        self.generator = None
        self.narrator_prompt = None
        
    def initialize(self):
        """Initialize the CSM model and narrator prompt"""
        print("📚 Initializing Story Generator...")
        self.generator = load_csm_1b(device=self.device)
        self.narrator_prompt = self._create_narrator_prompt()
        print("✅ Story Generator ready!")
        
    def _create_narrator_prompt(self):
        """Create the narrator prompt segment"""
        audio = load_prompt_audio(self.narrator_prompt_audio_path, self.generator.sample_rate)
        return Segment(
            text=self.narrator_prompt_text,
            speaker=0,  # Narrator is always speaker 0
            audio=audio
        )
    
    def generate_story_audio(self, story_text, chunk_method="paragraph", max_chunk_length=15000):
        """
        Generate audio for a story
        
        Args:
            story_text (str): The story text to narrate
            chunk_method (str): How to split the story ("paragraph", "sentence", "length")
            max_chunk_length (int): Maximum audio length per chunk in ms
            
        Returns:
            tuple: (full_audio_tensor, list_of_segments)
        """
        if self.generator is None:
            raise RuntimeError("StoryGenerator not initialized. Call initialize() first.")
        
        # Split story into chunks
        chunks = self._split_story(story_text, chunk_method)
        
        print(f"📖 Generating audio for {len(chunks)} story chunks...")
        
        # Generate audio for each chunk
        audio_segments = []
        context = [self.narrator_prompt]
        
        for i, chunk in enumerate(chunks, 1):
            print(f"  Generating chunk {i}/{len(chunks)}: '{chunk[:50]}...'")
            
            audio = self.generator.generate(
                text=chunk,
                speaker=0,
                context=context + audio_segments[-2:],  # Keep last 2 segments as context
                max_audio_length_ms=max_chunk_length,
            )
            
            segment = Segment(
                text=chunk,
                speaker=0,
                audio=audio
            )
            audio_segments.append(segment)
        
        # Combine all audio
        full_audio = concatenate_audio_segments(audio_segments)
        return full_audio, audio_segments
    
    def _split_story(self, story_text, method="paragraph"):
        """
        Split story into chunks for processing
        
        Args:
            story_text (str): The story text
            method (str): Splitting method
            
        Returns:
            list: List of text chunks
        """
        if method == "paragraph":
            # Split by paragraphs (double newlines)
            chunks = [p.strip() for p in story_text.split("\n\n") if p.strip()]
        elif method == "sentence":
            # Split by sentences
            import re
            sentences = re.split(r'[.!?]+', story_text)
            chunks = [s.strip() + "." for s in sentences if s.strip()]
        elif method == "length":
            # Split by character length (approximately)
            max_chars = 200  # Rough character limit per chunk
            words = story_text.split()
            chunks = []
            current_chunk = []
            current_length = 0
            
            for word in words:
                if current_length + len(word) > max_chars and current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = [word]
                    current_length = len(word)
                else:
                    current_chunk.append(word)
                    current_length += len(word) + 1  # +1 for space
            
            if current_chunk:
                chunks.append(" ".join(current_chunk))
        else:
            # Default: treat as single chunk
            chunks = [story_text]
        
        return chunks
    
    def save_story_audio(self, audio_tensor, filename):
        """
        Save story audio to file
        
        Args:
            audio_tensor (torch.Tensor): Audio tensor to save
            filename (str): Output filename
        """
        save_audio(audio_tensor, filename, self.generator.sample_rate)
    
    def generate_chapter_audio(self, chapters, output_prefix="chapter"):
        """
        Generate audio for multiple chapters
        
        Args:
            chapters (list): List of chapter texts
            output_prefix (str): Prefix for output files
            
        Returns:
            list: List of (audio_tensor, segments) for each chapter
        """
        results = []
        
        for i, chapter in enumerate(chapters, 1):
            print(f"\n📖 Processing Chapter {i}/{len(chapters)}...")
            audio, segments = self.generate_story_audio(chapter)
            
            # Save chapter audio
            filename = f"outputs/{output_prefix}_{i:02d}.wav"
            self.save_story_audio(audio, filename)
            
            results.append((audio, segments))
        
        return results 