"""Main runner for story generator application"""

import os
import torch
from .story import StoryGenerator
from applications.shared_utils import download_default_prompts

def get_sample_stories():
    """Get sample stories for demonstration"""
    stories = {
        "short_tale": """
In a small town nestled between rolling hills, there lived a young inventor named Maya. She spent her days tinkering with gadgets and dreaming of creating something that would change the world.

One day, while working in her workshop, she discovered an unusual crystal that seemed to glow with an inner light. As she held it in her hand, she felt a strange warmth spreading through her fingers.

Little did she know, this crystal would lead her on an adventure beyond her wildest dreams, and change not just her life, but the entire town's future.
        """.strip(),
        
        "sci_fi_opening": """
The year was 2157, and humanity had finally learned to speak with the stars. Dr. Elena Vasquez stood before the massive communication array, her heart racing as the first signals from the Andromeda galaxy crackled through the speakers.

"Command, we're receiving something," she whispered into her headset. The patterns were unlike anything they had encountered before—not random cosmic noise, but something deliberate, something intelligent.

As the translation algorithms worked their magic, a message began to form on her screen: "We have been waiting for you to find us. Welcome to the galactic community, young species. We have much to teach you, and much to learn from you."

Elena's hands trembled as she realized she was witnessing the most significant moment in human history. First contact had finally happened, and nothing would ever be the same.
        """.strip(),
        
        "fantasy_adventure": """
The ancient map crackled as Sir Aldric unfolded it in the dim candlelight of the tavern. The parchment was older than the kingdom itself, marked with symbols that spoke of forgotten treasures and dangerous guardians.

"The Dragon's Crown," he murmured, tracing the path marked in faded ink. "Legend says it grants the power to unite all the fractured kingdoms under one peaceful rule."

His companion, the clever mage Lyra, leaned closer. "The path leads through the Whispering Woods, across the Chasm of Echoes, and into the heart of Mount Shadowpeak. Many have tried this journey, Aldric. None have returned."

But Sir Aldric's resolve was unshakeable. In a world torn apart by endless wars, the Dragon's Crown represented hope—a chance to bring lasting peace to all the lands. He folded the map carefully and stood up.

"Then we'll be the first to succeed," he declared. "The realm's future depends on it."
        """.strip()
    }
    
    return stories

def demo_short_story():
    """Demonstrate generating audio for a short story"""
    print("\n📚 === Short Story Demo ===")
    
    # Get default prompts and stories
    prompts = download_default_prompts()
    stories = get_sample_stories()
    
    # Determine device
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
        print("⚠️  CUDA not available, using CPU (will be slow)")
    
    # Create story generator
    generator = StoryGenerator(
        narrator_prompt_text=prompts["conversational_a"]["text"],
        narrator_prompt_audio_path=prompts["conversational_a"]["audio"],
        device=device
    )
    
    generator.initialize()
    
    # Generate audio for the short tale
    story_text = stories["short_tale"]
    print(f"📖 Generating audio for story ({len(story_text)} characters)...")
    
    full_audio, segments = generator.generate_story_audio(story_text, chunk_method="paragraph")
    
    # Save the story audio
    os.makedirs("outputs", exist_ok=True)
    generator.save_story_audio(full_audio, "outputs/maya_inventor_story.wav")
    
    print(f"✅ Story audio generated!")
    print(f"📊 Generated {len(segments)} audio segments")
    print(f"⏱️  Total audio length: ~{len(full_audio) / 24000:.1f} seconds")

def demo_multiple_stories():
    """Demonstrate generating audio for multiple different stories"""
    print("\n📚 === Multiple Stories Demo ===")
    
    # Get default prompts and stories
    prompts = download_default_prompts()
    stories = get_sample_stories()
    
    # Determine device
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
        print("⚠️  CUDA not available, using CPU (will be slow)")
    
    # Create story generator
    generator = StoryGenerator(
        narrator_prompt_text=prompts["conversational_b"]["text"],  # Different voice
        narrator_prompt_audio_path=prompts["conversational_b"]["audio"],
        device=device
    )
    
    generator.initialize()
    
    # Generate audio for each story
    story_files = {
        "sci_fi_opening": "outputs/sci_fi_first_contact.wav",
        "fantasy_adventure": "outputs/fantasy_dragon_crown.wav"
    }
    
    os.makedirs("outputs", exist_ok=True)
    
    for story_name, output_file in story_files.items():
        print(f"\n📖 Generating '{story_name}'...")
        story_text = stories[story_name]
        
        full_audio, segments = generator.generate_story_audio(
            story_text, 
            chunk_method="sentence",  # Different chunking method
            max_chunk_length=12000
        )
        
        generator.save_story_audio(full_audio, output_file)
        print(f"✅ '{story_name}' saved to {output_file}")
        print(f"📊 Generated {len(segments)} segments")

def demo_chapter_generation():
    """Demonstrate generating audio for story chapters"""
    print("\n📚 === Chapter Generation Demo ===")
    
    # Sample chapters for a longer story
    chapters = [
        """Chapter 1: The Discovery

Dr. Sarah Chen had always believed that the universe held secrets beyond human imagination. As the lead xenolinguist at the Mars Research Station, she spent her days analyzing signals from deep space, searching for patterns that might indicate intelligent life.

On a cold Tuesday morning, everything changed. The signal wasn't like the others—it was clearly artificial, clearly intentional. As Sarah stared at the data streaming across her monitors, she realized that humanity was about to make first contact.""",

        """Chapter 2: The Message

The translation took three days. Working around the clock with her team, Sarah slowly decoded the alien message. What they found was both terrifying and beautiful: a warning and an invitation.

"Your species shows promise," the message read, "but you stand at a crossroads. Choose wisely, young ones, for the path you select will determine not just your future, but the future of this entire galaxy."

Sarah knew that everything had changed. The universe was no longer empty and silent."""
    ]
    
    # Get default prompts
    prompts = download_default_prompts()
    
    # Determine device
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
        print("⚠️  CUDA not available, using CPU (will be slow)")
    
    # Create story generator
    generator = StoryGenerator(
        narrator_prompt_text=prompts["conversational_a"]["text"],
        narrator_prompt_audio_path=prompts["conversational_a"]["audio"],
        device=device
    )
    
    generator.initialize()
    
    # Generate chapters
    print(f"📖 Generating {len(chapters)} chapters...")
    results = generator.generate_chapter_audio(chapters, output_prefix="contact_story_chapter")
    
    print(f"✅ All chapters generated!")
    print(f"📁 Check outputs/ for chapter_*.wav files")

def main():
    """Main function to run story generator demos"""
    print("📚 CSM Story Generator Application")
    print("=" * 50)
    
    try:
        # Download prompts first
        print("📥 Downloading default prompts...")
        download_default_prompts()
        
        # Run demos
        demo_short_story()
        demo_multiple_stories()
        demo_chapter_generation()
        
        print("\n🎉 All story generation demos completed!")
        print("📁 Check the 'outputs/' directory for generated audio files:")
        print("   - maya_inventor_story.wav")
        print("   - sci_fi_first_contact.wav") 
        print("   - fantasy_dragon_crown.wav")
        print("   - contact_story_chapter_*.wav")
        
    except Exception as e:
        print(f"❌ Error during story generation: {e}")
        print("💡 Make sure you have:")
        print("   - Sufficient GPU memory (or patience for CPU)")
        print("   - Hugging Face access to CSM-1B and Llama-3.2-1B")
        print("   - Run 'huggingface-cli login' first")

if __name__ == "__main__":
    main() 