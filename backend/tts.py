import numpy as np
import soundfile
import torch
from espnet2.bin.tts_inference import Text2Speech
from espnet2.utils.types import str_or_none

class TTS:
    def __init__(self, model_name):
        self.model_name = model_name

    def speech(self, text, output_path):
        text2speech = Text2Speech.from_pretrained(
            model_tag=str_or_none(self.model_name),
            vocoder_tag=str_or_none('none'),
            device="cuda",
            # Only for Tacotron 2 & Transformer
            threshold=0.5,
            # Only for Tacotron 2
            minlenratio=0.0,
            maxlenratio=10.0,
            use_att_constraint=False,
            backward_window=1,
            forward_window=3,
            # Only for FastSpeech & FastSpeech2 & VITS
            speed_control_alpha=1.0,
            # Only for VITS
            noise_scale=0.333,
            noise_scale_dur=0.333,
        )

        with torch.no_grad():
            speech = text2speech(text)["wav"]

        soundfile.write(output_path, speech.cpu().numpy(), text2speech.fs, "PCM_16")
        return speech.cpu().numpy(), text2speech.fs

if __name__=="__main__":
    tts = TTS('espnet/kan-bayashi_jsut_full_band_vits_prosody')
    tts.speech("こんちゎぁす", "out.wav")