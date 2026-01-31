#!/bin/bash
# Deployment script for AWS EC2
# Run this on your EC2 instance after pulling the code

echo "=== Invoice App Deployment ==="

# Create virtual environment (if not exists)
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create admin users if needed (run once)
# python reset_now.py

echo "=== Deployment Complete ==="
echo ""
echo "Start with gunicorn:"
echo "  source venv/bin/activate"
echo "  gunicorn invoice.wsgi:application --bind 0.0.0.0:8000"
echo ""
echo "Or run in background with nohup:"
echo "  nohup gunicorn invoice.wsgi:application --bind 0.0.0.0:8000 &"
