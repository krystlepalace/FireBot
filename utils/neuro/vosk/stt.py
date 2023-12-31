import os
from vosk import KaldiRecognizer, Model
import subprocess
import json
from config import CONFIG


class STT:
    def __init__(
            self, 
            modelpath=CONFIG.vosk_model_full_path, 
            samplerate=16000
            ):
        self.modelpath = modelpath
        self.samplerate = samplerate

        model = Model(self.modelpath)
        self.recognizer = KaldiRecognizer(model, self.samplerate)
        self.recognizer.SetWords(True)

    def audio_to_text(self, audiofile) -> str:
        if not os.path.exists(audiofile):
            raise Exception("Указан неправильный путь к файлу")

        with subprocess.Popen(
            [
                "ffmpeg", 
                "-loglevel", "quiet",
                "-i", audiofile,
                "-ar", str(self.samplerate),
                "-ac", "1",
                "-f", "s16le",
                "-",
            ],
            stdout=subprocess.PIPE,
        ) as process:
            while True:
                data = process.stdout.read(4000)
                if len(data) == 0:
                    break
                if self.recognizer.AcceptWaveform(data):
                    print(self.recognizer.Result())
                else:
                    print(self.recognizer.PartialResult())

        result_json = self.recognizer.FinalResult()
        result_dict = json.loads(result_json)

        return result_dict["text"]
