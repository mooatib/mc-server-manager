import function
from model import Response, ResponseType


async def stop_container():
    if function.is_server_running():
        nbr = function.number_of_players()
        if nbr:
            return Response(
                ResponseType.WARNING,
                f""":warning: {nbr} player(s) are actually playing. \r Do you really want to stop the server ?""",
            )
        else:
            return function.stop_container()
    else:
        return Response(ResponseType.IGNORE, "ℹ The server is already stopped.")


async def start_container():
    if not function.is_server_running():
        return function.start_container()
    else:
        return Response(
            ResponseType.IGNORE,
            f"ℹ The server is already running and has {function.number_of_players()} player(s) online",
        )


async def status():
    return function.status()
