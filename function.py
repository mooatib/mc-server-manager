import os
from dotenv import load_dotenv
from pip._vendor import requests
from model import Response, ResponseType
from interactions import Embed, EmbedField, EmbedImageStruct

load_dotenv()

server_data = str()

scheduled = []


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


def parse_delay(delay):
    return sum(x * float(t) for x, t in zip([1, 60, 3600], reversed(delay.split(":"))))


def schedule(timer):
    print("Timer started")
    scheduled.append(timer)
    print("Added in scheduled list")


async def unscheduled(timer):
    timer.cancel()
    print("Timer canceled")
    scheduled.append(timer)
    print("removed from scheduled list")


def status():
    return embed_status_builder()


def is_server_running():
    update_server_data()
    return bool(server_data["online"])


def number_of_players():
    try:
        return server_data["players"]["online"]
    except Exception:
        return 0


def get_players():
    try:
        players = server_data["players"]["list"]
    except Exception:
        players = "No players"
    return players


def motd():
    try:
        return (
            str(server_data["motd"]["clean"])
            .replace("'", "")
            .replace("[", "")
            .replace("]", "")
        )
    except Exception:
        return ""


def players_name():
    players = get_players()
    return str(players).replace("'", "").replace("[", "").replace("]", "")


def player_ratio():
    try:
        ratio = str(server_data["players"]["max"])
        return "".join([str(server_data["players"]["online"]), "/", ratio])
    except Exception:
        return ""


def update_server_data():
    global server_data
    server_data = requests.get(
        "".join(["https://api.mcsrvstat.us/2/", os.environ.get("IP")])
    ).json()


def embed_status_builder():
    server_state = is_server_running()
    server_state_title = ("Offline", "Online")[server_state]
    color = (0xFF0000, 0x32CD32)[server_state]

    embed = Embed(
        title=os.environ.get("IP"),
        color=color,
        description=motd(),
        thumbnail=EmbedImageStruct(
            url="".join(["https://api.mcsrvstat.us/icon/", os.environ.get("IP")])
        ),
        fields=[
            EmbedField(name="Status", value=server_state_title, inline=True),
        ],
    )

    if server_state:
        embed.add_field(
            name="Player count",
            value=player_ratio(),
            inline=True,
        ),
        embed.add_field(
            name="Version",
            value=str(server_data["version"]),
            inline=True,
        )
        embed.add_field(
            name="Players",
            value=players_name(),
            inline=False,
        ),

    return embed
