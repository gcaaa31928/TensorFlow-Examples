import fnmatch
import os
from random import shuffle

import librosa


def find_files(directory, pattern='*.wav'):
    '''Recursively finds all files matching the pattern.'''
    files = []
    for root, dirnames, filenames in os.walk(directory):
        for filename in fnmatch.filter(filenames, pattern):
            files.append(os.path.join(root, filename))
    return files


def load_generic_audio(directory, sample_rate):
    files = find_files(directory)
    audios = []
    for filename in files:
        audio, _ = librosa.load(filename, sr=sample_rate, mono=True)
        audios.append(audio)
    return audios


class AudioReader:
    def __init__(self,
                 sample_rate=16000,
                 sample_size=4000,
                 vocal_audio_directory='./vocal',
                 non_vocal_audio_directory='./non_vocal'):
        self.sample_rate = sample_rate
        self.sample_size = sample_size
        self.audios = self.read_dir(vocal_audio_directory, self.sample_rate, is_vocal=True)
        self.audios.extend(self.read_dir(non_vocal_audio_directory, self.sample_rate))
        shuffle(self.audios)
        print(len(self.audios))
        self.current_audio_index = 0

    def next_audio_sample(self):
        audio, label = self.audios[self.current_audio_index]
        self.current_audio_index += 1
        return audio, label

    def read_dir(self, dir, sample_rate, is_vocal=False):
        audio_files = []
        label = 1 if is_vocal else 0
        for audio in load_generic_audio(dir, sample_rate):
            audio_files.append((audio, label))
        return audio_files
