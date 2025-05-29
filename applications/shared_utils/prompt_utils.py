"""Prompt utility functions for CSM applications"""

import os
from huggingface_hub import hf_hub_download
from generator import Segment
from .audio_utils import load_prompt_audio

def download_default_prompts():
    """
    Download default prompts from Hugging Face
    
    Returns:
        dict: Dictionary containing prompt text and audio paths
    """
    prompts = {}
    
    # Download conversational prompts
    prompts["conversational_a"] = {
        "text": (
            "like revising for an exam I'd have to try and like keep up the momentum because I'd "
            "start really early I'd be like okay I'm gonna start revising now and then like "
            "you're revising for ages and then I just like start losing steam I didn't do that "
            "for the exam we had recently to be fair that was a more of a last minute scenario "
            "but like yeah I'm trying to like yeah I noticed this yesterday that like Mondays I "
            "sort of start the day with this not like a panic but like a"
        ),
        "audio": hf_hub_download(
            repo_id="sesame/csm-1b",
            filename="prompts/conversational_a.wav"
        )
    }
    
    prompts["conversational_b"] = {
        "text": (
            "like a super Mario level. Like it's very like high detail. And like, once you get "
            "into the park, it just like, everything looks like a computer game and they have all "
            "these, like, you know, if, if there's like a, you know, like in a Mario game, they "
            "will have like a question block. And if you like, you know, punch it, a coin will "
            "come out. So like everyone, when they come into the park, they get like this little "
            "bracelet and then you can go punching question blocks around."
        ),
        "audio": hf_hub_download(
            repo_id="sesame/csm-1b",
            filename="prompts/conversational_b.wav"
        )
    }
    
    return prompts

def create_character_prompt(name, text, audio_path, speaker_id, sample_rate):
    """
    Create a character prompt segment
    
    Args:
        name (str): Character name
        text (str): Prompt text
        audio_path (str): Path to prompt audio file
        speaker_id (int): Speaker ID for the character
        sample_rate (int): Target sample rate
        
    Returns:
        Segment: Character prompt segment
    """
    audio = load_prompt_audio(audio_path, sample_rate)
    return Segment(
        text=text,
        speaker=speaker_id,
        audio=audio
    )

def create_custom_character_prompts():
    """
    Create custom character prompts for different types of characters
    
    Returns:
        dict: Dictionary of character prompt templates
    """
    character_templates = {
        "friendly_assistant": {
            "text": "Hello! I'm here to help you with whatever you need. I'm friendly, knowledgeable, and always ready to assist.",
            "personality": "Friendly, helpful, professional"
        },
        "wise_narrator": {
            "text": "Once upon a time, in a world filled with wonder and mystery, there lived stories waiting to be told.",
            "personality": "Wise, thoughtful, storytelling"
        },
        "energetic_gamer": {
            "text": "Alright! Let's do this! I'm pumped up and ready for action. This is going to be epic!",
            "personality": "Energetic, enthusiastic, gaming-focused"
        },
        "calm_teacher": {
            "text": "Today we're going to learn something fascinating. Let's take it step by step and explore together.",
            "personality": "Patient, educational, clear"
        },
        "mysterious_guide": {
            "text": "Follow me carefully. The path ahead is treacherous, but I know the way through these ancient halls.",
            "personality": "Mysterious, knowledgeable, cautious"
        }
    }
    
    return character_templates

def get_character_voice_mapping():
    """
    Get mapping of character types to appropriate voice prompts
    
    Returns:
        dict: Mapping of character types to voice prompts
    """
    return {
        "friendly_assistant": "conversational_a",
        "wise_narrator": "conversational_a", 
        "energetic_gamer": "conversational_b",
        "calm_teacher": "conversational_a",
        "mysterious_guide": "conversational_b"
    } 