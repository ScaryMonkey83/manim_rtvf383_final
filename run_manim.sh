cd ~/manim_rtvf383_final || exit
screen
source venv/bin/activate
python manim_muisc.py || exit
aws ec2 stop-instances --instance-ids $1