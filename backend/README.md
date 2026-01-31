# Python FastAPI setup
sudo apt install python3.12-venv python3-pip -y

cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload

* If uvicorn is not found or get the error: error: externally-managed-environment:

Virtual environments are not portable - they have hardcoded paths. You need to recreate it:

  cd /home/../git/ai-pizza-fastapi-nextjs/backend
  rm -rf venv
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt

  Then uvicorn will work.