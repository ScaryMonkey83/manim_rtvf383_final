aws s3 rm s3://manim-chunks/ --recursive --exclude "*" --include "tmp/*"
source venv/bin/activate
python -m awslambdaric manim_music.py