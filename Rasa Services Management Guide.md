Rasa Chatbot Services README
This README provides instructions for managing the systemd services for a Rasa-based chatbot: rasa-api.service, rasa-actions.service, and rasa-front.service. These services handle the Rasa HTTP API, custom actions, and a web front-end, respectively.
Overview

rasa-api.service: Runs the Rasa core server with HTTP API.
rasa-actions.service: Runs the Rasa Actions server for custom actions.
rasa-front.service: Runs a Sanic web server for static content or front-end.

All services:

Run as the adminadie user.
Use the virtual environment at /home/adminadie/chat/.venv.
Operate in /home/adminadie/chat (or /home/adminadie/chat/static for rasa-front.service).

Prerequisites

Virtual environment at /home/adminadie/chat/.venv with Rasa and dependencies installed.
Rasa models in /home/adminadie/chat/models for rasa-api.service.
run_server.py script in /home/adminadie/chat/static for rasa-front.service.
adminadie user has read/write/execute permissions for /home/adminadie/chat and /home/adminadie/chat/static.

Installation

Ensure the virtual environment is set up:python3 -m venv /home/adminadie/chat/.venv
. /home/adminadie/chat/.venv/bin/activate
pip install rasa


Place Rasa models in /home/adminadie/chat/models.
Ensure run_server.py exists in /home/adminadie/chat/static.
Verify service files exist in /etc/systemd/system/:
rasa-api.service
rasa-actions.service
rasa-front.service



Service Management
Replace <service> with rasa-api, rasa-actions, or rasa-front in the commands below.
Start a Service
sudo systemctl start <service>.service

Example:
sudo systemctl start rasa-api.service
sudo systemctl start rasa-actions.service
sudo systemctl start rasa-front.service

Stop a Service
sudo systemctl stop <service>.service

Example:
sudo systemctl stop rasa-api.service
sudo systemctl stop rasa-actions.service
sudo systemctl stop rasa-front.service

Restart a Service
sudo systemctl restart <service>.service

Example:
sudo systemctl restart rasa-api.service
sudo systemctl restart rasa-actions.service
sudo systemctl restart rasa-front.service

Check Service Status
sudo systemctl status <service>.service

Example:
sudo systemctl status rasa-api.service
sudo systemctl status rasa-actions.service
sudo systemctl status rasa-front.service

Displays service status, recent logs, and errors.
View Service Logs
View logs for the current boot:
sudo journalctl -u <service>.service -b

Example:
sudo journalctl -u rasa-api.service -b
sudo journalctl -u rasa-actions.service -b
sudo journalctl -u rasa-front.service -b

Real-time logs:
sudo journalctl -u <service>.service -f

Debug logs (for --debug enabled services):
sudo journalctl -u <service>.service --since "1 hour ago"

Edit Service Files
Edit a service file:
sudo nano /etc/systemd/system/<service>.service

Example:
sudo nano /etc/systemd/system/rasa-front.service
sudo nano /etc/systemd/system/rasa-api.service
sudo nano /etc/systemd/system/rasa-actions.service

After editing:

Save (Ctrl+O, Enter, Ctrl+X in nano).
Reload systemd:sudo systemctl daemon-reload


Restart the service:sudo systemctl restart <service>.service



Enable/Disable on Boot
Enable auto-start on boot:
sudo systemctl enable <service>.service

Disable auto-start:
sudo systemctl disable <service>.service

Service Details
rasa-api.service

File: /etc/systemd/system/rasa-api.service
Description: Rasa HTTP API server.
Command: . /home/adminadie/chat/.venv/bin/activate && rasa run -m models --enable-api --cors "*" --debug
Working Directory: /home/adminadie/chat
User: adminadie
Restart: Always, with 5-second delay.
Environment: PYTHONUNBUFFERED=1

rasa-actions.service

File: /etc/systemd/system/rasa-actions.service
Description: Rasa Actions server.
Command: . /home/adminadie/chat/.venv/bin/activate && rasa run actions --debug
Working Directory: /home/adminadie/chat
User: adminadie
Restart: Always, with 5-second delay.
Environment: PYTHONUNBUFFERED=1

rasa-front.service

File: /etc/systemd/system/rasa-front.service
Description: Sanic web server for static content/front-end.
Command: /home/adminadie/chat/.venv/bin/python run_server.py
Working Directory: /home/adminadie/chat/static
User: adminadie
Restart: Always, with 5-second delay.
Environment: PYTHONUNBUFFERED=1

Troubleshooting

Service Fails:

Check status: sudo systemctl status <service>.service
Check logs: sudo journalctl -u <service>.service -b
Common issues:
Missing virtual environment or dependencies.
Missing Rasa models in /home/adminadie/chat/models.
Incorrect run_server.py path.
Port conflicts (e.g., port 5005).




Port Conflicts:
sudo netstat -tulnp | grep 5005

Adjust ports in service configuration if needed.

Permissions:Ensure adminadie has permissions for /home/adminadie/chat and /home/adminadie/chat/static.

Debugging:Run commands manually:
. /home/adminadie/chat/.venv/bin/activate
rasa run -m models --enable-api --cors "*" --debug  # rasa-api
rasa run actions --debug  # rasa-actions
/home/adminadie/chat/.venv/bin/python /home/adminadie/chat/static/run_server.py  # rasa-front



Notes

Monitor logs regularly for errors, especially after updates.
Back up Rasa models and run_server.py before changes.
Ensure sufficient system resources for all services.
