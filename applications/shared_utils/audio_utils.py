"""Audio utility functions for CSM applications"""

import torch
import torchaudio
from generator import Segment

def load_prompt_audio(audio_path, target_sample_rate):
    """
    Load and resample audio for prompts
    
    Args:
        audio_path (str): Path to the audio file
        target_sample_rate (int): Target sample rate for resampling
        
    Returns:
        torch.Tensor: Audio tensor resampled to target rate
    """
    audio_tensor, sample_rate = torchaudio.load(audio_path)
    audio_tensor = audio_tensor.squeeze(0)
    # Resample is lazy so we can always call it
    audio_tensor = torchaudio.functional.resample(
        audio_tensor, orig_freq=sample_rate, new_freq=target_sample_rate
    )
    return audio_tensor

def save_audio(audio_tensor, filepath, sample_rate):
    """
    Save audio tensor to file
    
    Args:
        audio_tensor (torch.Tensor): Audio tensor to save
        filepath (str): Output file path
        sample_rate (int): Sample rate of the audio
    """
    torchaudio.save(filepath, audio_tensor.unsqueeze(0).cpu(), sample_rate)
    print(f"💾 Audio saved to: {filepath}")

def concatenate_audio_segments(segments):
    """
    Concatenate multiple audio segments
    
    Args:
        segments (List[Segment]): List of audio segments to concatenate
        
    Returns:
        torch.Tensor: Concatenated audio tensor
    """
    return torch.cat([seg.audio for seg in segments], dim=0)

def add_silence(duration_ms, sample_rate):
    """
    Create a silence tensor
    
    Args:
        duration_ms (float): Duration of silence in milliseconds
        sample_rate (int): Sample rate for the silence
        
    Returns:
        torch.Tensor: Silence tensor
    """
    num_samples = int(duration_ms * sample_rate / 1000)
    return torch.zeros(num_samples)

def concatenate_with_pauses(segments, pause_duration_ms=500):
    """
    Concatenate audio segments with pauses between them
    
    Args:
        segments (List[Segment]): List of audio segments
        pause_duration_ms (float): Duration of pause between segments
        
    Returns:
        torch.Tensor: Concatenated audio with pauses
    """
    if not segments:
        return torch.tensor([])
    
    # Assume all segments have the same sample rate
    sample_rate = 24000  # CSM default sample rate
    silence = add_silence(pause_duration_ms, sample_rate)
    
    result = segments[0].audio
    for segment in segments[1:]:
        result = torch.cat([result, silence, segment.audio], dim=0)
    
    return result 