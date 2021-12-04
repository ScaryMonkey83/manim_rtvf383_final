import os
from datetime import datetime
import pickle

import soundfile as sf
from moviepy.editor import VideoFileClip, concatenate_videoclips
import numpy as np


# constants
file = "audio"
tmp = "tmp"
n_cores = 48
window_multiplier = 6
frame_rate = 60
qual_flag = '-qh --fps={}'.format(60)


def var_to_file(var, path):
    with open(path, 'wb') as f:
        pickle.dump(var, f)

def file_to_var(path):
    with open(path, 'rb') as f:
        return pickle.load(f)

def window_rms(a, window_sz):
    if type(window_sz) is float:
        window_sz = int(window_sz)
    a2 = np.power(a, 2)
    window = np.ones(window_sz) / float(window_sz)
    return np.sqrt(np.convolve(a2, window, 'valid'))


# constructs the video from audio asynchronously
if __name__ == '__main__':
    now = datetime.now()

    # remove files before fs setup
    os.system('rm -r debug')
    os.system('rm -r tmp')

    # fs setup
    os.system('mkdir debug')
    os.system('mkdir {}'.format(tmp))
    os.system('mkdir {}/media'.format(tmp))
    dirs = os.listdir(file)
    f = []
    for d in dirs:
        if d[-3:] == 'aif':
            f.append(d)
    dirs = f

    # load data as sample information kept in np.array
    kick_data, samplerate = sf.read('audio/{}'.format(dirs[5]))
    snare_data, _         = sf.read('audio/{}'.format(dirs[6]))
    tom_h_data, _         = sf.read('audio/{}'.format(dirs[1]))
    tom_m_data, _         = sf.read('audio/{}'.format(dirs[4]))
    tom_l_data, _         = sf.read('audio/{}'.format(dirs[3]))
    ohl_data, _           = sf.read('audio/{}'.format(dirs[2]))
    ohr_data, _           = sf.read('audio/{}'.format(dirs[0]))

    # convert from samples to db using local root mean square convolution
    kick_data  = window_rms(kick_data, samplerate / (frame_rate * window_multiplier))
    snare_data = window_rms(snare_data, samplerate / (frame_rate * window_multiplier))
    tom_h_data = window_rms(tom_h_data, samplerate / (frame_rate * window_multiplier))
    tom_m_data = window_rms(tom_m_data, samplerate / (frame_rate * window_multiplier))
    tom_l_data = window_rms(tom_l_data, samplerate / (frame_rate * window_multiplier))
    ohl_data   = window_rms(ohl_data, samplerate / (frame_rate * window_multiplier))
    ohr_data   = window_rms(ohr_data, samplerate / (frame_rate * window_multiplier))

    # normalize and select numbers conducive to frame rate
    data = np.stack([kick_data[0::int(samplerate / frame_rate)] / kick_data.max(),
                     snare_data[0::int(samplerate / frame_rate)] / snare_data.max(),
                     tom_h_data[0::int(samplerate / frame_rate)] / tom_h_data.max(),
                     tom_m_data[0::int(samplerate / frame_rate)] / tom_m_data.max(),
                     tom_l_data[0::int(samplerate / frame_rate)] / tom_l_data.max(),
                     ohl_data[0::int(samplerate / frame_rate)] / ohl_data.max(),
                     ohr_data[0::int(samplerate / frame_rate)] / ohr_data.max()],
                    axis=1)

    ##############################################################################
    ## At this point the data is clean, idx'd by frame and needs to be chunked  ##
    ##      data: np.ndarray (n_samples / (samplerate / frame_rate), 7)         ##
    ##############################################################################

    # printing shape of data to confirm that the quantity at line 86 is appx num_seconds
    print(data.shape)
    print((data.shape[0] - data.shape[0] % frame_rate) / frame_rate)

    # chunking for processes
    count = 0
    with open('{}/parallel_script_list.txt'.format(tmp), 'w') as f:
        for start in range(0, data.shape[0], frame_rate):
            # this makes sure that the animations are smooth
            if start + frame_rate > kick_data.size:
                stop = kick_data.size
            else:
                stop = start + frame_rate

            # won't err due to os/python separation (will print on stderr)
            os.system('mkdir tmp/media/{}'.format(count))

            # write chunk to file
            var_to_file((start, data[start:stop, :]), "{}/{}data.bin".format(tmp, count))

            # listening to snarky puppy figuring shit out like a boss song_title='outlier'
            if count == 0:
                f.write('python -m manim {} --disable_caching --music_file={}/{}data.bin -first=true --media_dir={}/{}/{} main.py Video > ~/manim_rtvf383_final/debug/segment_{}.log 2> /dev/null\n'
                        .format(qual_flag, tmp, count, tmp, 'media', count, count))
            else:
                f.write('python -m manim {} --disable_caching --music_file={}/{}data.bin --media_dir={}/{}/{} main.py Video > ~/manim_rtvf383_final/debug/segment_{}.log 2> /dev/null\n'
                        .format(qual_flag, tmp, count, tmp, 'media', count, count))
            count += 1

    # render the video segments
    os.system('bash ~/manim_rtvf383_final/multiprocess.sh ~/manim_rtvf383_final/{}/parallel_script_list.txt {}'
              .format(tmp, n_cores))

    # stitch segments together
    clips = []
    for num in range(count):
        media_dir = 'tmp/media/{}/videos/main/1080p60.0/Video.mp4'.format(num)
        clips.append(VideoFileClip(media_dir))
    final_video = concatenate_videoclips(clips)
    final_video.write_videofile("final_video.mp4")
    print("Runtime = {}".format(datetime.now() - now))
