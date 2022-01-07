import json
import os
from datetime import datetime
from os import system

from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
import boto3 as aws
from botocore.exceptions import ClientError

# if __name__ == '__main__':
#     dirs = os.listdir('test_vids')
#     clips = []
#
#     for num in range(len(dirs)):
#         media_dir = 'test_vids/Video_{}.mp4'.format(num)
#         try:
#             clips.append(VideoFileClip(media_dir))
#         except OSError:
#             continue
#     final_video = concatenate_videoclips(clips)
#     final_video.write_videofile("final_video.mp4")

if __name__ == '__main__':
    now = datetime.now()

    aws_region = 'us-east-2'
    s3_bucket = 'manim-chunks'

    aws_session = aws.Session()
    s3_resource = aws_session.resource('s3', aws_region)
    s3_object = s3_resource.Bucket(s3_bucket)

    # a client for the s3 service
    s3 = aws.client('s3')

    # find the video files and stick 'em in a list.
    response = s3.list_objects_v2(
        Bucket=s3_bucket,
        Prefix='videos/',
        MaxKeys=10000)
    dirs = [d['Key'] for d in response['Contents']]

    clips = []

    # download the final videos
    for num in range(len(dirs)):
        media_dir = 'test_vids/Video_{}.mp4'.format(num)
        try:
            s3_object.Object('videos/Video_{}.mp4'.format(num)).download_file(media_dir)
        except ClientError as e:
            continue

    # build the final video with clips
    for num in range(len(dirs)):
        media_dir = 'test_vids/Video_{}.mp4'.format(num)
        try:
            clips.append(VideoFileClip(media_dir))
        except OSError:
            continue

    final_video = concatenate_videoclips(clips)
    final_video.write_videofile("final_video.mp4")