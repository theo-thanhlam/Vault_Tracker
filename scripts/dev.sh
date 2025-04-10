#!/bin/bash

# Function to start FastAPI (Backend)
start_backend() {
  echo "Starting FastAPI (Backend)..."
  
  # Activate the virtual environment for FastAPI
  source backend/.venv/bin/activate

  # Start FastAPI using uvicorn, and run it in the background
  uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000 &
}

# Function to start Next.js (Frontend)
start_frontend() {
  echo "Starting Next.js (Frontend)..."
  cd frontend && npm run dev &
}

# Function to start Redis
start_redis() {
  echo "Starting Redis..."
  redis-server &
}

# Main function to run all services concurrently
start_services() {
  start_redis
  start_backend
  start_frontend
}

# Check if the script argument is 'stop' to kill all services
stop_services() {
  echo "Stopping all services..."
  # pkill uvicorn &
  # pkill node &
  # pkill redis-server
  
  fuser -k -n tcp 3000 &&
  fuser -k -n tcp 8000 &&
  fuser -k -n tcp 6379
}

# Main process handling
case "$1" in
  start)
    start_services
    ;;
  stop)
    stop_services
    ;;
  *)
    echo "Usage: $0 {start|stop}"
    exit 1
    ;;
esac
