from src.logger import log
from openwakeword.model import Model as WakewordModel
from openwakeword.utils import download_models
import src.mic as mic

log.info("Download wakeword model if not present")
download_models(["alexa"])

log.info("Initalize WakewordModel")
wakewordModel = WakewordModel(["alexa"], vad_threshold=0.5)

def listen_for_wakeword(threshold: float=0.5) -> bool:
    prediction = wakewordModel.predict(mic.get_frame(), threshold={"alexa":0.5}, debounce_time=1)
    score = next(iter(prediction.values()))

    return score >= threshold
