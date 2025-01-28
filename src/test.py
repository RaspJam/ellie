import sounddevice as sd
import numpy as np
import queue
import faster_whisper
import time

# Queue for audio data
audio_queue = queue.Queue()

# Silence detection settings
SILENCE_THRESHOLD = 0.01  # Adjust as needed
SILENCE_DURATION = 2  # Seconds of silence to consider speech ended

# Whisper model
model = faster_whisper.WhisperModel("base", device="cpu")  # Use "cuda" for GPU acceleration

def audio_callback(indata, frames, time, status):
    """
    Callback function to handle incoming audio data.
    """
    if status:
        print(f"Status: {status}")
    # Add audio data to the queue
    audio_queue.put(indata.copy())

def transcribe_audio(audio_data, sample_rate):
    """
    Transcribes the given audio data using Faster Whisper.
    """
    # Convert to a format Faster Whisper expects (float32 and mono)
    audio_data = np.mean(audio_data, axis=1) if audio_data.ndim > 1 else audio_data
    results, _ = model.transcribe(audio_data, beam_size=5, language="en")
    transcription = " ".join(segment["text"] for segment in results)
    return transcription

def main():
    """
    Main function to handle real-time transcription.
    """
    print("Listening... Speak into the microphone.")
    sample_rate = 16000  # Match Whisper's default sampling rate
    silence_start_time = None
    recorded_audio = []

    with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate):
        while True:
            try:
                # Check for new audio data
                while not audio_queue.empty():
                    data = audio_queue.get()
                    recorded_audio.append(data)

                    # Check if the input is silent
                    if np.max(np.abs(data)) < SILENCE_THRESHOLD:
                        if silence_start_time is None:
                            silence_start_time = time.time()
                        elif time.time() - silence_start_time > SILENCE_DURATION:
                            print("Silence detected. Transcribing...")
                            # Combine recorded audio and transcribe
                            audio_data = np.concatenate(recorded_audio, axis=0)
                            transcription = transcribe_audio(audio_data, sample_rate)
                            print(f"Transcription: {transcription}")
                            recorded_audio.clear()
                            silence_start_time = None  # Reset silence detection
                    else:
                        silence_start_time = None  # Reset silence detection on speech activity

            except KeyboardInterrupt:
                print("Exiting...")
                break

if __name__ == "__main__":
    main()
