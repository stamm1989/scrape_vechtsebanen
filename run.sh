filename=$(date +"%d-%m-%Y_%H%M%S_logs.txt")
. venv/bin/activate
python main.py > logs/${filename} 2>&1