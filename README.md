# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows CMD
venv\Scripts\activate

# OR macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend server
uvicorn main:app --reload

# (In a new terminal tab — optional) Run frontend
npm run dev

# To exit virtual environment
deactivate
