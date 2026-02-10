import sounddevice as sd
import numpy as np
import tempfile
from scipy.io.wavfile import write
from google.cloud import speech


def record_audio(seconds=4, rate=16000):
    print(f"Recording for {seconds} seconds...")

    # Record audio (mono, int16)
    audio = sd.rec(
        int(seconds * rate),
        samplerate=rate,
        channels=1,
        dtype="int16"
    )
    sd.wait()  # Wait until recording is finished

    # Save to temporary WAV file
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(tmp.name, rate, audio)

    return tmp.name


def speech_to_text_google(wav_path):
    # Instantiates a client (same pattern as TextToSpeechClient)
    client = speech.SpeechClient()

    # Load audio file
    with open(wav_path, "rb") as f:
        audio_content = f.read()

    # Audio input object (equivalent to SynthesisInput)
    recognition_audio = speech.RecognitionAudio(
        content=audio_content
    )

    # Recognition configuration (equivalent to VoiceSelectionParams / AudioConfig)
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-us",
        enable_automatic_punctuation=True,
    )

    # Perform the speech-to-text request
    response = client.recognize(
        config=recognition_config,
        audio=recognition_audio,
    )

    if not response.results:
        return None

    return response.results[0].alternatives[0].transcript
