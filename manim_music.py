import os
from datetime import datetime
import pickle
import json

import soundfile as sf
import numpy as np
import boto3 as aws


# constants
tmp = "/manim_rtvf383_final/tmp"
audio_files = "/{}/audio".format(tmp)
window_multiplier = 4
frame_rate = 20

# AWS constants
s3_bucket = 'manim-chunks'
aws_region = 'us-east-2'
bucket_audio_files = 'audio/{}'


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

def download_audio_file_from_s3(s3_bucket_obj, s3_source_file, destination_dir):
    s3_bucket_obj.Object(s3_source_file).download_file(destination_dir)
    return sf.read('{}'.format(destination_dir))


# constructs the video frdeom audio asynchronously
def main():
    now = datetime.now()
    print(os.listdir())
    # # remove files before fs setup
    # os.system('rm -r debug')
    # os.system('rm -r tmp')

    # fs setup
    # try:
    #     os.mkdir('/manim_rtvf383_final/debug')
    # except FileExistsError:
    #     pass
    # try:
    #     os.mkdir(audio_files)
    # except FileExistsError:
    #     pass
    # try:
    #     os.mkdir(tmp)
    # except FileExistsError:
    #     pass

    # a client for the s3 service
    s3 = aws.client('s3')

    # find  the 7 audio files and stick it in a list.
    response = s3.list_objects_v2(
        Bucket=s3_bucket,
        Prefix='audio/',
        MaxKeys=7)
    dirs = [d['Key'] for d in response['Contents']]

    # the s3 bucket pointer
    aws_session = aws.Session()
    s3_resource = aws_session.resource('s3', aws_region)
    s3_bucket_ref = s3_resource.Bucket(s3_bucket)

    # load data as sample information kept in np.array
    kick_data, samplerate = download_audio_file_from_s3(s3_bucket_ref, '{}'.format(dirs[5]), '{}/{}'.format(tmp, dirs[5]))
    snare_data, _         = download_audio_file_from_s3(s3_bucket_ref, '{}'.format(dirs[6]), '{}/{}'.format(tmp, dirs[6]))
    tom_h_data, _         = download_audio_file_from_s3(s3_bucket_ref, '{}'.format(dirs[1]), '{}/{}'.format(tmp, dirs[1]))
    tom_m_data, _         = download_audio_file_from_s3(s3_bucket_ref, '{}'.format(dirs[4]), '{}/{}'.format(tmp, dirs[4]))
    tom_l_data, _         = download_audio_file_from_s3(s3_bucket_ref, '{}'.format(dirs[3]), '{}/{}'.format(tmp, dirs[3]))
    ohl_data, _           = download_audio_file_from_s3(s3_bucket_ref, '{}'.format(dirs[2]), '{}/{}'.format(tmp, dirs[2]))
    ohr_data, _           = download_audio_file_from_s3(s3_bucket_ref, '{}'.format(dirs[0]), '{}/{}'.format(tmp, dirs[0]))

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
    # info: (data.shape[0] - data.shape[0] % frame_rate) / frame_rate =appx= num_seconds

    # chunking for processes
    count = 0
    step_sz = int(frame_rate / 2)
    for start in range(0, data.shape[0], step_sz):
        # this makes sure that the animations are smooth
        if start + step_sz + 1 > kick_data.size:
            stop = kick_data.size
        else:
            stop = start + step_sz + 1

        # write chunk to file
        var_to_file((True if count == 0 else False, start, data[start:stop, :]), "{}/{}data.bin".format(tmp, count))

        # listening to virtual riot figuring shit out like a boss song_title='Dreaming'
        count += 1

    for source, dirs, files in os.walk(tmp):
        for filename in files:
            local_file = os.path.join(source, filename)
            s3.upload_file(local_file, s3_bucket, local_file)
    print("Runtime = {}".format(datetime.now() - now))


if __name__ == '__main__':
    main()
