# stitch segments together
from datetime import datetime

from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip

count = 89
clips = []
for num in range(count):
    media_dir = 'tmp/media/{}/videos/main/480p60.0/Video.mp4'.format(num)
    clips.append(VideoFileClip(media_dir))
final_video = concatenate_videoclips(clips)
final_video.write_videofile("final_video.mp4")
# os.system('rm -r {}'.format(tmp))
print('done')