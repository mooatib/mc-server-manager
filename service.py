import function
from model import Response, ResponseType


async def stop_ec2():
    if function.is_server_running():
        nbr = function.number_of_players()
        if nbr:
            return Response(
                ResponseType.WARNING,
                f""":warning: {nbr} player(s) are actually playing. \r Do you really want to stop the server ?""",
            )
        else:
            res = function.stop_ec2()
            if res.status_code == 200:
                return Response(ResponseType.OK, ":white_check_mark: Server stopped.")
            else:
                return Response(ResponseType.ERROR, "An error occurred..")
    else:
        return Response(ResponseType.IGNORE, "ℹ The server is already stopped.")
