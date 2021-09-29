# MODULES
import sys # argv
import librosa # load, get_duration, stft, amplitude_to_db, times_like, fft_frequencies
import librosa.display # specshow
import numpy as np # abs, max 
import pandas as pd # DataFrame, to_json
import matplotlib.pyplot as plt # subplots, savefig


def main():

    # Sample MP3 files at 44100 Hz and transform to dB-normalized Short-Time Fourier Transform for spectrogram output
    print('\nWorking on file: ' + sys.argv[2])
    y, sr = librosa.load(sys.argv[1], sr = 44100)
    if librosa.get_duration(y = y, sr = sr) >= 600.00:
        print('File: ' + sys.argv[2] + ' is too large. Exiting process...\n')
        sys.exit(0) # do not process files larger than 10 minutes in length
    D = librosa.stft(y, n_fft = 512, hop_length = 512)
    S_db = librosa.amplitude_to_db(np.abs(D), ref = np.max)
    print('Fourier transform completed successfully on: ' + sys.argv[2])

    # Capture dB level output for (n_fft / 2) + 1 frequency ranges over the song duration into .json for post-processing
    seconds = librosa.times_like(S_db, sr = 44100)
    freqs = librosa.fft_frequencies(sr = 44100, n_fft = 512)
    df = pd.DataFrame(S_db, index = freqs, columns = seconds)
    df.to_json(path_or_buf = sys.argv[4]) # format { 'time_index(s)' : { 'freq' : 'dB_level' } }
    print('Spectrum analysis JSON successfully created for: ' + sys.argv[2])

    # Capture spectrogram output into .png for visual inspection
    fig, ax = plt.subplots()
    img = librosa.display.specshow(S_db, x_axis = 'time', y_axis = 'linear', ax = ax)
    ax.set(title = sys.argv[2])
    fig.colorbar(img, ax = ax, format = '%+2.f dB')
    plt.savefig(sys.argv[3])
    print('Spectrogram PNG successfully created for: ' + sys.argv[2] + '\n\n')
    plt.close('all') # ensure memory leaks do not occur from open figures

if __name__ == '__main__':
    main()
