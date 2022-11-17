import function
from model import Response, ResponseType


async def stop_ec2(ignore_warning: bool):
    if function.is_server_running():
        nbr = function.number_of_players()
        if nbr and not ignore_warning:
            return Response(
                ResponseType.WARNING,
                f""":warning: {nbr} player(s) are actually playing. \r Do you really want to stop the server ?""",
            )
        else:
            return function.stop_ec2()
    else:
        return Response(ResponseType.IGNORE, "ℹ The server is already stopped.")


async def start_ec2():
    if not function.is_server_running():
        return function.start_ec2()
    else:
        return Response(
            ResponseType.IGNORE,
            f"ℹ The server is already running and has {function.number_of_players()} player(s) online",
        )


async def status():
    return function.status()


def schedule(timer):
    return function.schedule(timer)
