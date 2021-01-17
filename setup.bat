:: Folder creation
mkdir data
mkdir passworddb
mkdir logs

:: Create virtual environment
python -m venv venv

:: Activate virtual environment
call venv/Scripts/activate.bat

:: Install requirements
pip install -r requirements.txt

:: Deactivate virtualenv
call venv/Scripts/deactivate.bat