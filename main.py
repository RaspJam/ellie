from src.logger import log
from faster_whisper import WhisperModel
from src.wakeword import listen_for_wakeword
import mic
import numpy as np
import time
import sounddevice as sd

model_size = "base"

log.info("Initalize WhisperModel")
whisperModel = WhisperModel(
    model_size, device="cpu", compute_type="int8", cpu_threads=4
)

log.info("Yerp")
while True:
    if listen_for_wakeword():
        log.info("Wakeword Detected!")

        segments, _ = whisperModel.transcribe(mic.get_chunk())

        for segment in segments:
            print(f"[{segment.start:.2f}s - {segment.end:.2f}s]: {segment.text}")

        log.fatal("cuz why not")
        exit(0)
