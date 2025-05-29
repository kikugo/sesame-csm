# CSM Applications

This directory contains practical applications built on top of the CSM (Conversational Speech Model).

## Available Applications

### 🎭 Character Chat
Create conversational AI characters with consistent voices.
- **Location**: `character_chat/`
- **Usage**: `python -m applications.character_chat.run`
- **Description**: Build AI characters that can have conversations while maintaining consistent voice identity

### 📚 Story Generator  
Generate audio narration for stories and books.
- **Location**: `story_generator/`
- **Usage**: `python -m applications.story_generator.run`
- **Description**: Convert written stories into engaging audio narration with natural speech

### 🎮 Voice Game
Create game dialogue with multiple characters.
- **Location**: `voice_game/`
- **Usage**: `python -m applications.voice_game.run`
- **Description**: Generate dynamic game dialogue with multiple distinct character voices

## Shared Utilities

Common functionality for all applications is in `shared_utils/`:
- **Audio processing**: Loading, saving, and manipulating audio
- **Prompt management**: Handling character voices and prompts
- **Conversation flow**: Managing multi-turn conversations

## Quick Start

```bash
# Make sure you're in the repository root
cd sesame-csm

# Install dependencies
pip install -r requirements.txt

# Set up environment
export NO_TORCH_COMPILE=1

# Login to Hugging Face (required for model access)
huggingface-cli login

# Run any application
python -m applications.character_chat.run
```

## Requirements

- Python 3.10+
- CUDA-compatible GPU (recommended)
- Hugging Face account with access to:
  - [Llama-3.2-1B](https://huggingface.co/meta-llama/Llama-3.2-1B)
  - [CSM-1B](https://huggingface.co/sesame/csm-1b)

## Output

All generated audio files are saved to the `outputs/` directory.

## Adding New Applications

To add a new application:

1. Create a new directory in `applications/`
2. Add your application code
3. Use the shared utilities from `shared_utils/`
4. Update this README with your application info

## Note

These applications require significant computational resources. A CUDA-compatible GPU with sufficient VRAM is highly recommended for reasonable performance. 