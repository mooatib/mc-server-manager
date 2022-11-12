import os
from dotenv import load_dotenv
from pip._vendor import requests
from mcstatus import JavaServer
from model import Response, ResponseType
from interactions import Embed, EmbedField

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


def status():
    server_state = is_server_running()
    title = (":no_entry:  Offline", ":white_check_mark:  Online")[server_state]
    color = (0xFF0000, 0x32CD32)[server_state]

    if server_state:
        return [
            Embed(
                title=title,
                color=color,
                fields=[
                    EmbedField(
                        name=":busts_in_silhouette:  Players :",
                        value=players_name(),
                        inline=False,
                    )
                ],
            )
        ]
    else:
        [
            Embed(
                title=title,
                color=color,
                fields=[],
            )
        ]


def is_server_running():
    try:
        server.ping()
        return True
    except (TimeoutError, ConnectionRefusedError):
        return False


def number_of_players():
    status = server.status()
    return status.players.online


def get_players():
    status = server.status()
    query = server.query()
    players = status.raw["players"]["sample"]
    print(players)
    print(query)
    return players


def players_name():
    players = get_players()
    return (
        str([user["name"] for user in players])
        .replace("'", "")
        .replace("[", "")
        .replace("]", "")
    )
