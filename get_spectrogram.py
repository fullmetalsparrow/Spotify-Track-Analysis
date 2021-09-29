# MODULES
import os # path, walk, makedirs
import sys # argv, executable
import subprocess # run


# GLOBALS
PATH = os.path.abspath('.') # path to current directory
MP3 = {} # format: { 'output_dir' : ['audio_filepaths'] }


# Recursively iterate through a single downloaded playlist for song titles (only MP3) to analyze
for dirpath, _, filenames in os.walk(PATH + '\\playlists\\' + sys.argv[1]):
    for f in filenames:
        if '.mp3' in f[-4:].lower():
            key = os.path.abspath(PATH + '\\spectrograms\\' + dirpath.split('\\')[-1]) # Gets playlist title for ease of folder navigation
            if not os.path.isdir(key):
                os.makedirs(key)
            if key in MP3:
                MP3[key].append(os.path.abspath(os.path.join(dirpath, f)))
            else:
                MP3[key] = []
                MP3[key].append(os.path.abspath(os.path.join(dirpath, f)))


# Serves as the main script controller for spectrogram_execute.py in order to run librosa commands one at a time to avoid memory leaks
def main():

    for key, val in MP3.items():
        for audio in val:

            # Local variables
            filename = audio.split('\\')[-1][:-4]
            spectro_path = key + '\\' + filename + '.png' # change file extension for spectrogram output
            json_path = spectro_path[:-4] + '.json' # change file extension for table output

            # If files exist for spectrogram and table outputs, do not overwrite
            if os.path.isfile(spectro_path) and os.path.isfile(json_path):
                continue

            # Ensures venv will remain active during subprocess calls and allows for output to the console
            subprocess.run([sys.executable, 'spectrogram_execute.py', audio, filename, spectro_path, json_path], shell = True)
            

if __name__ == '__main__':
    main()
