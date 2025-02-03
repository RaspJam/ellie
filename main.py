from src.logger import log
from faster_whisper import WhisperModel
from src.wakeword import listen_for_wakeword
import src.mic as mic
import numpy as np
import time
import spacy
from src.coin import Coin, BANK

model_size = "small"

log.info("Initalize WhisperModel")
whisperModel = WhisperModel(
    model_size, device="cpu", compute_type="int8", cpu_threads=4
)

log.info("Load COINS model")
nlp = spacy.load('COINS')

log.info("Yerp")
while True:
    if listen_for_wakeword():
        log.info("Wakeword Detected!")

        segments, _ = whisperModel.transcribe(mic.get_chunk())
        seg = list(segments)[0]

        log.debug(seg.text)
        doc = nlp(seg.text)

        coin = Coin()
        for ent in doc.ents:
            setattr(coin, ent.label_[0].lower(), ent.text.lower())

        log.debug(coin)

        BANK.data[coin.c][coin.o]()

        log.fatal("cuz why not")
        exit(0)
