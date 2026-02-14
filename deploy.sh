#!/bin/bash
# =============================================================
# Deployment script for squarem.in on Ubuntu (AWS EC2)
# Run on the server: bash deploy.sh
# =============================================================
set -e

APP_DIR="/home/ubuntu/squarem"
VENV="$APP_DIR/venv"

echo "=== squarem.in Deployment ==="

cd "$APP_DIR"

# --- Virtual environment ---
if [ ! -d "$VENV" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV"
fi
source "$VENV/bin/activate"

# --- Dependencies ---
echo "Installing dependencies..."
pip install -r requirements.txt

# --- Database ---
echo "Running migrations..."
python manage.py migrate --noinput

# --- Static files ---
echo "Collecting static files..."
python manage.py collectstatic --noinput

# --- Log directory ---
mkdir -p "$APP_DIR/logs"

# --- Gunicorn systemd service ---
echo "Setting up Gunicorn service..."
sudo cp "$APP_DIR/deployment/gunicorn.service" /etc/systemd/system/gunicorn.service
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl restart gunicorn
echo "Gunicorn service started."

# --- Nginx ---
if [ ! -f /etc/nginx/sites-available/squarem ]; then
    echo "Setting up Nginx config..."
    sudo cp "$APP_DIR/deployment/nginx-squarem.conf" /etc/nginx/sites-available/squarem
    sudo ln -sf /etc/nginx/sites-available/squarem /etc/nginx/sites-enabled/
    sudo rm -f /etc/nginx/sites-enabled/default
fi
sudo nginx -t && sudo systemctl reload nginx
echo "Nginx reloaded."

echo ""
echo "=== Deployment Complete ==="
echo "Check status:"
echo "  sudo systemctl status gunicorn"
echo "  sudo systemctl status nginx"
echo "  sudo journalctl -u gunicorn -f"
