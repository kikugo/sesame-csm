# CSM

**2025/05/20** - CSM is availabile natively in [Hugging Face Transformers](https://huggingface.co/docs/transformers/main/en/model_doc/csm) 🤗 as of version `4.52.1`, more info available [in our model repo](https://huggingface.co/sesame/csm-1b)

**2025/03/13** - We are releasing the 1B CSM variant. The checkpoint is [hosted on Hugging Face](https://huggingface.co/sesame/csm_1b).

---

CSM (Conversational Speech Model) is a speech generation model from [Sesame](https://www.sesame.com) that generates RVQ audio codes from text and audio inputs. The model architecture employs a [Llama](https://www.llama.com/) backbone and a smaller audio decoder that produces [Mimi](https://huggingface.co/kyutai/mimi) audio codes.

A fine-tuned variant of CSM powers the [interactive voice demo](https://www.sesame.com/voice) on the Sesame website.

## 🚀 Applications Framework

This repository now includes a comprehensive applications framework with ready-to-use CSM applications:

### 📋 Available Applications

| Application | Description | Features |
|-------------|-------------|----------|
| 🎭 **Character Chat** | Create AI characters with consistent voices | Multi-character conversations, personality persistence |
| 📚 **Story Generator** | Convert stories to audio narration | Chapter-based generation, multiple narrator styles |
| 🎮 **Voice Game** | Generate game dialogue | Combat scenarios, story interactions, custom dialogue |
| 🔧 **Configuration** | Manage application settings | Audio quality, device preferences, output options |
| 🧪 **Quick Test** | Test CSM functionality | Dependency checks, performance benchmarking |

### 🏁 Quick Start

```bash
# 1. Clone this repository
git clone https://github.com/your-username/sesame-csm.git
cd sesame-csm

# 2. Run setup (checks dependencies, creates directories)
python setup_applications.py

# 3. Login to Hugging Face (required for model access)
huggingface-cli login

# 4. Launch the applications
python launch_applications.py
```

### 💡 Usage Examples

```bash
# Interactive launcher (recommended)
python launch_applications.py

# Run specific applications directly
python -m applications.character_chat.run
python -m applications.story_generator.run
python -m applications.voice_game.run

# Test your setup
python -m applications.quick_test
```

## 📖 Original CSM Usage

### Quick start

Install the repository dependencies by running:

```bash
pip install -r requirements.txt
```

Set the `NO_TORCH_COMPILE` environment variable to disable torchcompile:

```bash
export NO_TORCH_COMPILE=1
```

Load the CSM-1B model and generate audio:

```python
from generator import load_csm_1b

# Load the model
generator = load_csm_1b()

# Generate audio from text
audio = generator.generate(
    text="Hello, this is a test of the CSM model.",
    speaker=0,
    context=[],
    max_audio_length_ms=10_000,
)

# Save the audio
import torchaudio
torchaudio.save("output.wav", audio.unsqueeze(0), generator.sample_rate)
```

### Detailed usage

CSM takes as input:
- `text`: the text to synthesize to speech.
- `speaker`: the speaker ID.
- `context`: a list of `Segment` objects representing the conversation context.
- `max_audio_length_ms`: the maximum duration of the generated audio, in milliseconds.

It returns a tensor representing the generated audio.

```python
from generator import load_csm_1b, Segment

# Load the model
generator = load_csm_1b()

# Create context segments (optional)
context = [
    Segment(
        text="Hello, how are you today?",
        speaker=0,
        audio=some_audio_tensor
    )
]

# Generate response
audio = generator.generate(
    text="I'm doing great, thank you for asking!",
    speaker=1,
    context=context,
    max_audio_length_ms=15_000,
)
```

#### Using prompt audios

You can use prompts that have been recorded as audio. CSM works best when using consistent prompts across a conversation. Here's an example:

```python
from generator import load_csm_1b, Segment
import torchaudio

# Load model
generator = load_csm_1b()

# Load prompt audio
prompt_audio, sample_rate = torchaudio.load("prompt.wav")
prompt_audio = prompt_audio.squeeze(0)

# Resample if necessary
if sample_rate != generator.sample_rate:
    prompt_audio = torchaudio.functional.resample(
        prompt_audio, 
        orig_freq=sample_rate, 
        new_freq=generator.sample_rate
    )

# Create prompt segment
prompt = Segment(
    text="Your prompt text here",
    speaker=0,
    audio=prompt_audio
)

# Generate with prompt context
audio = generator.generate(
    text="Response text to generate",
    speaker=0,
    context=[prompt],
    max_audio_length_ms=10_000,
)
```

### Environment variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NO_TORCH_COMPILE` | Disables torch.compile | `False` |
| `FORCE_CPU` | Forces CPU usage even if CUDA is available | `False` |

## 🔧 Requirements

- Python 3.10+
- PyTorch 2.0+
- CUDA-compatible GPU (recommended, 8GB+ VRAM)
- Hugging Face account with access to:
  - [Llama-3.2-1B](https://huggingface.co/meta-llama/Llama-3.2-1B)
  - [CSM-1B](https://huggingface.co/sesame/csm-1b)

## 📁 Project Structure

```
sesame-csm/
├── applications/           # Application framework
│   ├── character_chat/     # Character conversation app
│   ├── story_generator/    # Story narration app
│   ├── voice_game/         # Game dialogue app
│   ├── config/             # Configuration system
│   ├── shared_utils/       # Common utilities
│   └── README.md           # Applications documentation
├── launch_applications.py  # Main launcher
├── setup_applications.py   # Setup script
├── generator.py            # Core CSM generator
├── models.py               # Model definitions
├── watermarking.py         # Audio watermarking
└── outputs/                # Generated audio files
```

## 📄 License

This project is licensed under the same terms as the original CSM repository. See the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. Areas where contributions would be especially helpful:

- New application ideas
- Performance optimizations
- Additional prompt management features
- Documentation improvements

## 🐛 Troubleshooting

**Memory Issues**: Use the configuration system to reduce audio quality or switch to CPU mode.

**Model Download Issues**: Ensure you're logged into Hugging Face and have access to the required models.

**Slow Generation**: Check that you're using GPU acceleration and consider adjusting quality settings.

For more help, run the Quick Test application to diagnose common issues.
