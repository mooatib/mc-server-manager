import os
from dotenv import load_dotenv
from pip._vendor import requests
from mcstatus import JavaServer
from model import Response, ResponseType

load_dotenv()

server = JavaServer(os.environ.get("IP"))


def start_ec2():
    url = os.environ.get("LAMBDA_START_URL")

    res = requests.get(url)
    if res.status_code == 200:
        return Response(
            ResponseType.OK, ":white_check_mark: Server is starting, please wait."
        )
    return Response(ResponseType.ERROR, res.text)


def stop_ec2():
    url = os.environ.get("LAMBDA_STOP_URL")

    res = requests.get(url)
    if res.status_code == 200:
        return Response(ResponseType.OK, ":white_check_mark: Server stopped.")
    return Response(ResponseType.ERROR, res.text)


def is_server_running():
    try:
        server.ping()
        return True
    except (TimeoutError, ConnectionRefusedError):
        return False


def number_of_players():
    status = server.status()
    return status.players.online
