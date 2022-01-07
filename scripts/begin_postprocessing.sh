source venv/bin/activate
python -m awslambdaric stitch.main
aws s3 rm s3://manim-chunks/ --recursive --exclude "*" --include "videos/*"