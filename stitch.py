from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
import boto3 as aws


aws_region = 'us-east-2'
s3_bucket = 'manim-chunks'

aws_session = aws.Session()
s3_resource = aws_session.resource('s3', aws_region)
s3_object = s3_resource.Bucket(s3_bucket)

# a client for the s3 service
s3 = aws.client('s3')

# find  the 7 audio files and stick it in a list.
response = s3.list_objects_v2(
    Bucket=s3_bucket,
    Prefix='videos/',
    MaxKeys=10000)
dirs = [d['Key'] for d in response['Contents']]

clips = []

# download the final videos
for num in range(len(dirs)):
    media_dir = 'tmp/Video_{}.mp4'.format(num)
    s3_object.Object('videos/Video_{}.mp4'.format(num)).download_file(media_dir)

# build the final video with clips
for num in range(len(dirs)):
    media_dir = 'tmp/Video_{}.mp4'.format(num)
    clips.append(VideoFileClip(media_dir))
final_video = concatenate_videoclips(clips)
final_video.write_videofile("final_video.mp4")
s3.upload_file("final_video.mp4", s3_bucket, "final_video.mp4")
