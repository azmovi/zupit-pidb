#!/bin/sh
set -e  
poetry run uvicorn --host 0.0.0.0 --port 8000 zupit.app:app

