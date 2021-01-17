# Folder creation
mkdir -p data
mkdir -p logs
mkdir -p passworddb

# Create virtual environment
python3.7 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt