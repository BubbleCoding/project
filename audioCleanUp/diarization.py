from pyannote.audio import Pipeline
from pyannote.audio.pipelines.utils.hook import ProgressHook
import torch
import warnings
warnings.filterwarnings("ignore", message="The MPEG_LAYER_III subtype is unknown to TorchAudio.*")

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1")
pipeline.to(torch.device("cuda"))
with ProgressHook() as hook:
    diarization = pipeline("../audio/FedeNickWav.wav", num_speakers=4, hook=hook)

print(diarization)