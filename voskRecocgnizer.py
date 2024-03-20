from pydub import AudioSegment
import os
import sys
import time
import wave
import json
from vosk import Model, KaldiRecognizer, SetLogLevel
from syllable3 import generate
# install with `pip install vosk`

SetLogLevel(0)


def recongize_vosk(audio_filename, model_path='voskASRmodel') -> None:
    '''
    Recognize audio from 'audio_filename' with vosk model.

    Parameters:
        audio_filename (str): name of the audio file to recognize
        model_path (str): Path to vosk model. Default is 'model'.

    Returns:
        recognition result
    '''

    print(f"Reading your file '{audio_filename}'...")
    wf = wave.open(audio_filename, "rb")
    print(f"'{audio_filename}' file was successfully read")

    # check if audio if mono wav
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit()

    print(f"Reading your vosk model '{model_path}'...")
    model = Model(model_path)
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)
    print(f"'{model_path}' model was successfully read")

    print('Start converting to text. It may take some time...')
    start_time = time.time()

    results = []
    # recognize speech using vosk model
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)

    part_result = json.loads(rec.FinalResult())
    results.append(part_result)

    return results

def main():

    # Load the audio file
    audio_file = "New Recording 340.mp3"
    #convert mp3 to wav
    audio = AudioSegment.from_mp3(audio_file)
    audio.export("recording.wav", format="wav")
    temp = 'recording.wav'

    results = recongize_vosk(temp)

    text = ''
    for r in results:
        text += r['text'] + ' '
    print(text)

if __name__ == "__main__":
    main()