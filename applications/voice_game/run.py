"""Main runner for voice game application"""

import os
import torch
from .game import VoiceGame
from applications.shared_utils import download_default_prompts

def create_game_characters():
    """Create game characters for demonstration"""
    print("📥 Downloading default prompts...")
    prompts = download_default_prompts()
    
    # Define game characters with different roles
    characters = {
        0: ("Hero", prompts["conversational_a"]["text"], prompts["conversational_a"]["audio"]),
        1: ("Villain", prompts["conversational_b"]["text"], prompts["conversational_b"]["audio"]),
        2: ("Boss", prompts["conversational_a"]["text"], prompts["conversational_a"]["audio"]),
        3: ("Quest Giver", prompts["conversational_b"]["text"], prompts["conversational_b"]["audio"]),
        4: ("Shopkeeper", prompts["conversational_a"]["text"], prompts["conversational_a"]["audio"])
    }
    
    return characters

def demo_combat_scenarios():
    """Demonstrate combat dialogue generation"""
    print("\n⚔️ === Combat Scenarios Demo ===")
    
    # Create game characters
    characters = create_game_characters()
    
    # Determine device
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
        print("⚠️  CUDA not available, using CPU (will be slow)")
    
    # Create voice game
    game = VoiceGame(characters, device=device)
    game.initialize()
    
    # Generate combat scenarios
    scenarios = ["battle", "boss_fight"]
    
    os.makedirs("outputs", exist_ok=True)
    
    for scenario in scenarios:
        print(f"\n🎮 Generating '{scenario}' dialogue...")
        full_audio, segments = game.generate_combat_dialogue(scenario)
        
        filename = f"outputs/game_{scenario}_dialogue.wav"
        game.save_dialogue(full_audio, filename)
        
        print(f"✅ '{scenario}' saved to {filename}")
        print(f"📊 Generated {len(segments)} dialogue lines")
        
        # Clear history between scenarios
        game.clear_dialogue_history()

def demo_story_scenarios():
    """Demonstrate story dialogue generation"""
    print("\n📖 === Story Scenarios Demo ===")
    
    # Create game characters
    characters = create_game_characters()
    
    # Determine device
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
        print("⚠️  CUDA not available, using CPU (will be slow)")
    
    # Create voice game
    game = VoiceGame(characters, device=device)
    game.initialize()
    
    # Generate story scenarios
    scenarios = ["quest_start", "shop_interaction"]
    
    os.makedirs("outputs", exist_ok=True)
    
    for scenario in scenarios:
        print(f"\n📚 Generating '{scenario}' dialogue...")
        full_audio, segments = game.generate_story_dialogue(scenario)
        
        filename = f"outputs/game_{scenario}_dialogue.wav"
        game.save_dialogue(full_audio, filename)
        
        print(f"✅ '{scenario}' saved to {filename}")
        print(f"📊 Generated {len(segments)} dialogue lines")
        
        # Clear history between scenarios
        game.clear_dialogue_history()

def demo_custom_dialogue():
    """Demonstrate custom dialogue generation"""
    print("\n🎨 === Custom Dialogue Demo ===")
    
    # Create game characters
    characters = create_game_characters()
    
    # Determine device
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
        print("⚠️  CUDA not available, using CPU (will be slow)")
    
    # Create voice game
    game = VoiceGame(characters, device=device)
    game.initialize()
    
    # Custom dialogue script
    custom_script = [
        {"character_id": 3, "text": "Greetings, traveler. You look like you've seen many adventures."},
        {"character_id": 0, "text": "Indeed I have. I'm searching for the legendary Crystal of Power."},
        {"character_id": 3, "text": "Ah, that crystal... Many have sought it, but few have returned."},
        {"character_id": 0, "text": "I'm not like the others. I have the strength and courage needed."},
        {"character_id": 3, "text": "Very well. Head to the Ancient Ruins beyond the mountains."},
        {"character_id": 0, "text": "Thank you for the guidance. I won't forget your help."},
        {"character_id": 1, "text": "Did someone mention the Crystal of Power? How interesting..."},
        {"character_id": 0, "text": "Who are you? Why are you eavesdropping on our conversation?"},
        {"character_id": 1, "text": "I am the Shadow Lord, and that crystal belongs to me!"},
        {"character_id": 0, "text": "Never! I'll stop you from getting that power!"}
    ]
    
    print(f"\n🎭 Generating custom dialogue sequence...")
    full_audio, segments = game.generate_dialogue_sequence(custom_script)
    
    os.makedirs("outputs", exist_ok=True)
    filename = "outputs/game_custom_dialogue.wav"
    game.save_dialogue(full_audio, filename)
    
    print(f"✅ Custom dialogue saved to {filename}")
    print(f"📊 Generated {len(segments)} dialogue lines")
    
    # Show character info
    print(f"\n👥 Characters used:")
    char_info = game.get_character_info()
    for char_id, info in char_info.items():
        print(f"   {char_id}: {info['name']}")

def demo_interactive_dialogue():
    """Demonstrate interactive dialogue generation"""
    print("\n🎮 === Interactive Dialogue Demo ===")
    
    # Create game characters
    characters = create_game_characters()
    
    # Determine device
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
        print("⚠️  CUDA not available, using CPU (will be slow)")
    
    # Create voice game
    game = VoiceGame(characters, device=device)
    game.initialize()
    
    print("\n🎯 Interactive Dialogue Builder")
    print("Available characters:")
    char_info = game.get_character_info()
    for char_id, info in char_info.items():
        print(f"   {char_id}: {info['name']}")
    
    dialogue_script = []
    
    print("\nEnter dialogue lines (format: 'character_id: text' or 'quit' to finish):")
    print("Example: '0: Hello there, how are you today?'")
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'q', 'exit']:
                break
                
            if ':' not in user_input:
                print("❌ Please use format: 'character_id: text'")
                continue
                
            char_id_str, text = user_input.split(':', 1)
            char_id = int(char_id_str.strip())
            text = text.strip()
            
            if char_id not in char_info:
                print(f"❌ Character ID {char_id} not found")
                continue
                
            dialogue_script.append({"character_id": char_id, "text": text})
            print(f"✅ Added: {char_info[char_id]['name']} - '{text[:30]}...'")
            
        except ValueError:
            print("❌ Invalid character ID. Please use a number.")
        except KeyboardInterrupt:
            print("\n👋 Cancelled")
            return
    
    if not dialogue_script:
        print("No dialogue entered.")
        return
    
    # Generate the interactive dialogue
    print(f"\n🎭 Generating interactive dialogue ({len(dialogue_script)} lines)...")
    full_audio, segments = game.generate_dialogue_sequence(dialogue_script)
    
    os.makedirs("outputs", exist_ok=True)
    filename = "outputs/game_interactive_dialogue.wav"
    game.save_dialogue(full_audio, filename)
    
    print(f"✅ Interactive dialogue saved to {filename}")
    print(f"📊 Generated {len(segments)} dialogue lines")

def main():
    """Main function to run voice game demos"""
    print("🎮 CSM Voice Game Application")
    print("=" * 50)
    
    try:
        # Run demos
        demo_combat_scenarios()
        demo_story_scenarios()
        demo_custom_dialogue()
        
        # Optional interactive demo
        print("\n🤔 Run interactive dialogue builder? (y/n):", end=" ")
        if input().lower().startswith('y'):
            demo_interactive_dialogue()
        
        print("\n🎉 All voice game demos completed!")
        print("📁 Check the 'outputs/' directory for generated audio files:")
        print("   - game_battle_dialogue.wav")
        print("   - game_boss_fight_dialogue.wav")
        print("   - game_quest_start_dialogue.wav")
        print("   - game_shop_interaction_dialogue.wav")
        print("   - game_custom_dialogue.wav")
        
    except Exception as e:
        print(f"❌ Error during voice game demo: {e}")
        print("💡 Make sure you have:")
        print("   - Sufficient GPU memory (or patience for CPU)")
        print("   - Hugging Face access to CSM-1B and Llama-3.2-1B")
        print("   - Run 'huggingface-cli login' first")

if __name__ == "__main__":
    main() 