"""Quick test module for CSM functionality"""

import os
import torch
from generator import load_csm_1b
from applications.shared_utils import download_default_prompts, save_audio

def test_device_compatibility():
    """Test device compatibility and performance"""
    print("🧪 Testing Device Compatibility")
    print("-" * 40)
    
    # Test CUDA
    if torch.cuda.is_available():
        print("✅ CUDA available")
        print(f"   GPU: {torch.cuda.get_device_name(0)}")
        print(f"   Memory: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f}GB")
        device = "cuda"
    elif torch.backends.mps.is_available():
        print("✅ Apple Metal (MPS) available")
        device = "mps"
    else:
        print("⚠️  Only CPU available (will be slow)")
        device = "cpu"
    
    return device

def test_dependencies():
    """Test required dependencies"""
    print("\n🔍 Testing Dependencies")
    print("-" * 40)
    
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
    except ImportError:
        print("❌ PyTorch not found")
        return False
    
    try:
        import torchaudio
        print(f"✅ TorchAudio: {torchaudio.__version__}")
    except ImportError:
        print("❌ TorchAudio not found")
        return False
    
    try:
        import transformers
        print(f"✅ Transformers: {transformers.__version__}")
    except ImportError:
        print("❌ Transformers not found")
        return False
    
    try:
        from huggingface_hub import hf_hub_download
        print("✅ Hugging Face Hub")
    except ImportError:
        print("❌ Hugging Face Hub not found")
        return False
    
    try:
        import moshi
        print("✅ Moshi")
    except ImportError:
        print("❌ Moshi not found")
        return False
    
    return True

def test_model_loading(device="cuda"):
    """Test CSM model loading"""
    print(f"\n🤖 Testing CSM Model Loading on {device}")
    print("-" * 40)
    
    try:
        print("📥 Loading CSM-1B model...")
        generator = load_csm_1b(device=device)
        print("✅ Model loaded successfully!")
        return generator
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        print("💡 Make sure you have:")
        print("   - Hugging Face access to CSM-1B")
        print("   - Run 'huggingface-cli login'")
        return None

def test_prompt_download():
    """Test prompt downloading"""
    print("\n📥 Testing Prompt Download")
    print("-" * 40)
    
    try:
        prompts = download_default_prompts()
        print("✅ Default prompts downloaded successfully!")
        print(f"   Available prompts: {list(prompts.keys())}")
        return prompts
    except Exception as e:
        print(f"❌ Prompt download failed: {e}")
        return None

def test_quick_generation(generator, prompts):
    """Test quick audio generation"""
    print("\n🎙️ Testing Quick Audio Generation")
    print("-" * 40)
    
    try:
        test_text = "Hello, this is a quick test of the CSM model."
        print(f"📝 Generating: '{test_text}'")
        
        audio = generator.generate(
            text=test_text,
            speaker=0,
            context=[],
            max_audio_length_ms=5000,  # Short test
        )
        
        # Save test audio
        os.makedirs("outputs", exist_ok=True)
        save_audio(audio, "outputs/quick_test.wav", generator.sample_rate)
        
        print("✅ Audio generation successful!")
        print(f"   Saved to: outputs/quick_test.wav")
        print(f"   Duration: ~{len(audio) / generator.sample_rate:.1f} seconds")
        
        return True
    except Exception as e:
        print(f"❌ Audio generation failed: {e}")
        return False

def run_performance_benchmark(generator):
    """Run a simple performance benchmark"""
    print("\n⚡ Running Performance Benchmark")
    print("-" * 40)
    
    import time
    
    try:
        test_texts = [
            "Quick test one.",
            "This is test number two.",
            "Final benchmark test."
        ]
        
        total_time = 0
        total_audio_length = 0
        
        for i, text in enumerate(test_texts, 1):
            print(f"   Test {i}/3: '{text}'")
            
            start_time = time.time()
            audio = generator.generate(
                text=text,
                speaker=0,
                context=[],
                max_audio_length_ms=3000,
            )
            end_time = time.time()
            
            generation_time = end_time - start_time
            audio_length = len(audio) / generator.sample_rate
            
            total_time += generation_time
            total_audio_length += audio_length
            
            print(f"     ⏱️ Generated in {generation_time:.1f}s")
        
        # Calculate performance metrics
        avg_time = total_time / len(test_texts)
        real_time_factor = total_audio_length / total_time
        
        print(f"\n📊 Benchmark Results:")
        print(f"   Average generation time: {avg_time:.1f}s")
        print(f"   Real-time factor: {real_time_factor:.1f}x")
        if real_time_factor >= 1.0:
            print("   ✅ Real-time or faster generation!")
        else:
            print("   ⚠️  Slower than real-time")
            
        return True
    except Exception as e:
        print(f"❌ Benchmark failed: {e}")
        return False

def main():
    """Main quick test function"""
    print("🧪 CSM Quick Test")
    print("=" * 50)
    
    # Test 1: Device compatibility
    device = test_device_compatibility()
    
    # Test 2: Dependencies
    if not test_dependencies():
        print("\n❌ Dependency test failed. Please install missing packages.")
        return
    
    # Test 3: Prompt download
    prompts = test_prompt_download()
    if not prompts:
        print("\n❌ Prompt download failed. Check your internet connection.")
        return
    
    # Test 4: Model loading
    generator = test_model_loading(device)
    if not generator:
        print("\n❌ Model loading failed. Check your Hugging Face access.")
        return
    
    # Test 5: Quick generation
    if not test_quick_generation(generator, prompts):
        print("\n❌ Audio generation failed.")
        return
    
    # Test 6: Performance benchmark
    print("\n🤔 Run performance benchmark? (y/n):", end=" ")
    if input().lower().startswith('y'):
        run_performance_benchmark(generator)
    
    print("\n🎉 All tests completed!")
    print("✅ CSM is working correctly on your system.")
    print("📁 Check outputs/quick_test.wav for the generated audio.")

if __name__ == "__main__":
    main() 