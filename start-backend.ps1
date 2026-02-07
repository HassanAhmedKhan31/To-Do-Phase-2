# Deactivate virtual environment if active
if (Get-Command 'deactivate' -ErrorAction SilentlyContinue) {
    deactivate
}

# Navigate to the backend directory
cd backend

# Create a new virtual environment if it doesn't exist
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

# Activate the virtual environment
. .\.venv\Scripts\Activate.ps1

# Ensure pip is installed
.\.venv\Scripts\python.exe -m ensurepip --upgrade

# Install the required packages
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

# Start the backend server
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
