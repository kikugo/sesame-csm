"""Main runner for character chat application"""

import os
import torch
from .character import Character
from applications.shared_utils import save_audio, concatenate_audio_segments, download_default_prompts

def create_sample_characters():
    """Create sample characters for demonstration"""
    print("📥 Downloading default prompts...")
    prompts = download_default_prompts()
    
    characters = [
        Character(
            name="TechBot",
            prompt_text=prompts["conversational_a"]["text"],
            prompt_audio_path=prompts["conversational_a"]["audio"],
            speaker_id=0,
            personality="Friendly tech enthusiast who loves explaining technology"
        ),
        Character(
            name="StoryTeller",
            prompt_text=prompts["conversational_b"]["text"], 
            prompt_audio_path=prompts["conversational_b"]["audio"],
            speaker_id=1,
            personality="Creative storyteller who weaves engaging narratives"
        )
    ]
    
    return characters

def demo_single_character():
    """Demonstrate a single character conversation"""
    print("\n🎭 === Single Character Demo ===")
    
    # Create and initialize character
    characters = create_sample_characters()
    techbot = characters[0]
    
    # Determine device
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
        print("⚠️  CUDA not available, using CPU (will be slow)")
    
    techbot.initialize(device=device)
    
    # Sample conversation
    conversation = [
        "What's your favorite technology?",
        "That's fascinating! Tell me more about artificial intelligence.",
        "How do you think AI will change the world in the next ten years?",
        "Thank you for that insightful explanation!"
    ]
    
    print(f"\n🎙️ {techbot.name} is having a conversation...")
    responses = []
    
    for i, text in enumerate(conversation, 1):
        print(f"  Generating response {i}/{len(conversation)}: '{text[:50]}...'")
        response = techbot.respond(text)
        responses.append(response)
    
    # Save individual responses
    os.makedirs("outputs", exist_ok=True)
    for i, response in enumerate(responses, 1):
        filename = f"outputs/techbot_response_{i}.wav"
        techbot.save_response(response, filename)
    
    # Save full conversation
    full_audio = concatenate_audio_segments(responses)
    save_audio(full_audio, "outputs/techbot_full_conversation.wav", techbot.generator.sample_rate)
    
    print(f"✅ {techbot.name} conversation complete!")
    print(f"📊 Character info: {techbot.get_info()}")

def demo_multi_character():
    """Demonstrate a multi-character conversation"""
    print("\n🎭 === Multi-Character Demo ===")
    
    # Create characters
    characters = create_sample_characters()
    
    # Determine device
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
        print("⚠️  CUDA not available, using CPU (will be slow)")
    
    # Initialize both characters
    for char in characters:
        char.initialize(device=device)
    
    # Multi-character dialogue
    dialogue = [
        (0, "Hi there! I'm TechBot. I love talking about technology. What's your name?"),
        (1, "Hello TechBot! I'm StoryTeller. I love creating and sharing stories. Nice to meet you!"),
        (0, "That's awesome! Do you ever incorporate technology into your stories?"),
        (1, "Absolutely! I love stories about AI, robots, and futuristic worlds. Technology sparks imagination!"),
        (0, "That's so cool! Maybe we could collaborate on a story about AI someday."),
        (1, "I'd love that! We could create an amazing tale about the future of artificial intelligence.")
    ]
    
    print(f"\n🎙️ Multi-character conversation between {characters[0].name} and {characters[1].name}...")
    all_responses = []
    
    for i, (speaker_id, text) in enumerate(dialogue, 1):
        character = characters[speaker_id]
        print(f"  {character.name} ({i}/{len(dialogue)}): '{text[:50]}...'")
        
        # Use conversation history as context
        response = character.respond(text, context=all_responses[-3:])  # Last 3 responses as context
        all_responses.append(response)
    
    # Save the full multi-character conversation
    os.makedirs("outputs", exist_ok=True)
    full_audio = concatenate_audio_segments(all_responses)
    save_audio(full_audio, "outputs/multi_character_conversation.wav", characters[0].generator.sample_rate)
    
    print("✅ Multi-character conversation complete!")
    for char in characters:
        print(f"📊 {char.name} info: {char.get_info()}")

def main():
    """Main function to run character chat demos"""
    print("🎭 CSM Character Chat Application")
    print("=" * 50)
    
    try:
        # Run single character demo
        demo_single_character()
        
        # Run multi-character demo  
        demo_multi_character()
        
        print("\n🎉 All demos completed successfully!")
        print("📁 Check the 'outputs/' directory for generated audio files.")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print("💡 Make sure you have:")
        print("   - Sufficient GPU memory (or patience for CPU)")
        print("   - Hugging Face access to CSM-1B and Llama-3.2-1B")
        print("   - Run 'huggingface-cli login' first")

if __name__ == "__main__":
    main() 