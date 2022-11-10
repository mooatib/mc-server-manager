import os
import interactions
import function
import service
from model import Response, ResponseType

token = os.environ.get("CLIENT_ID")
guild = os.environ.get("GUILD_ID")

proceed_button = interactions.Button(
    style=interactions.ButtonStyle.DANGER, label="Proceed", custom_id="proceed"
)

abort_button = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY, label="Abort", custom_id="abort"
)

proceed_abort_row = interactions.ActionRow.new(proceed_button, abort_button)

bot = interactions.Client(token)


@bot.command(
    name="start",
    description="Start EC2 instance",
    scope=guild,
)
async def start(ctx):
    res = function.start_ec2()
    await ctx.send(res, ephemeral=True)


@bot.command(
    name="stop",
    description="Stop EC2 instance",
    scope=guild,
)
async def stop(ctx):
    await ctx.defer(ephemeral=True)
    res = await service.stop_ec2()
    if res.type == ResponseType.WARNING:
        await ctx.send(res.msg, components=proceed_abort_row)
    elif res.type == ResponseType.OK:
        await proceed(ctx)
    else:
        await ctx.send(res.msg)


@bot.component("proceed")
async def proceed(ctx):
    res = function.stop_ec2()
    await ctx.send(res.msg, ephemeral=True)


@bot.component("abort")
async def abort(ctx):
    res = Response(ResponseType.OK, ":wastebasket: Operation aborted succesfully.")
    await ctx.send(res.msg, ephemeral=True)


bot.start()
