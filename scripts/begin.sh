source venv/bin/activate
python -m manim -qh --fps=60 --disable_caching main.py Video # > "debug/segment_$AWS_BATCH_JOB_ID.log" 2> /dev/null
aws s3 cp "debug/segment_$AWS_BATCH_JOB_ID.log" "s3://manim-chunks/debug/segment_$AWS_BATCH_JOB_ID.log"
aws s3 cp "media/videos/main/1080p60.0/Video.mp4" "s3://manim-chunks/videos/Video_$AWS_BATCH_JOB_ID.mp4"