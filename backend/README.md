# Python FastAPI setup
sudo apt install python3.12-venv python3-pip -y

cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload
