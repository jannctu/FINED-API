import multiprocessing
import os

name = "Gunicorn config for FINED"
accesslog = "/media/commlab/TenTB/home/jan/LearnFastAPI/FINED-service/logs/gunicorn-access.log"
errorlog = "/media/commlab/TenTB/home/jan/LearnFastAPI/FINED-service/logs/gunicorn-error.log"
bind = "0.0.0.0:8000"

worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count () * 2 + 1
worker_connections = 1024
backlog = 2048
max_requests = 5120
timeout = 120
keepalive = 2
forwarded_allow_ips = '*'

debug = os.environ.get("debug", "false") == "true"
reload = debug
preload_app = False
daemon = False

# adding ssl support
#certfile = "/etc/letsencrypt/live/lab1.jankristanto.com/fullchain.pem"
#keyfile = "/etc/letsencrypt/live/lab1.jankristanto.com/privkey.pem"