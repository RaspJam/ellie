from src.logger import log
import numpy as np
import pyaudio

# Parameters for audio input
RATE = 16000  # 16 kHz sample rate
CHANNELS = 1  # Mono audio
FORMAT = pyaudio.paInt16  # 16-bit PCM audio
FRAME_DURATION_MS = 80  # Frame duration in milliseconds
CHUNK = int(RATE * FRAME_DURATION_MS / 1000)  # Number of samples per frame
INDEX = 0 # TODO: set this to first device in list

log.info("Initalize PyAudio")
audio = pyaudio.PyAudio()

log.info("----------------------record device list---------------------")
info = audio.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount', 0)
for i in range(0, int(numdevices)):
    if (int(audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels', 0))) > 0:
        log.info(f"Input Device id {i} - {audio.get_device_info_by_host_api_device_index(0, i).get('name')}")
log.info("-------------------------------------------------------------")

log.debug(f"Open audio stream on index {INDEX}")
mic_stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index = INDEX, frames_per_buffer=CHUNK)

def get_raw_frame(num_frames: int = CHUNK) -> bytes:
    # NOTE: Allowing overflow means that data is going to get lost.
    #       This makes sense as get_frame is an optional call.
    #       However important data may be lost during this time...
    return mic_stream.read(CHUNK, exception_on_overflow=False)

def get_frame(num_frames: int = CHUNK) -> np.ndarray:
    raw_frame = get_raw_frame(num_frames)
    frame = np.frombuffer(raw_frame, dtype=np.int16)
    return frame

def get_chunk(length: int=5) -> np.ndarray:
    frames = []

    for _ in range(0, int(RATE / CHUNK * length)):
        data = mic_stream.read(CHUNK)
        frames.append(data)

    # TODO: lets not normailze to the range [-1, 1] inside this function...
    return np.frombuffer(b''.join(frames), dtype=np.int16) / 32768.0
