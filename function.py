import os
from dotenv import load_dotenv
from pip._vendor import requests
from mcstatus import JavaServer

load_dotenv()

server = JavaServer(os.environ.get("IP"))


def start_ec2():
    url = os.environ.get("LAMBDA_START_URL")

    if not is_server_running():
        res = requests.get(url)
        if res.status_code == 200:
            return ":white_check_mark: Server is starting, please wait."
        return res.text
    else:
        status = server.status()
        return f"ℹ The server is already running and has {status.players.online} player(s) online"


def is_server_running():
    try:
        server.ping()
        return True
    except (TimeoutError, ConnectionRefusedError):
        return False
