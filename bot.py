import os
from interactions import (
    Button,
    ButtonStyle,
    ActionRow,
    Client,
    PresenceActivity,
    ClientPresence,
    Embed,
    EmbedField,
)
import function
import service
from model import Response, ResponseType

token = os.environ.get("CLIENT_ID")
guild_id = os.environ.get("GUILD_ID")

presence_activity = PresenceActivity(name="Minecraft", type=1)
up_presence = ClientPresence(activities=[presence_activity], status="online", afk=False)
down_presence = ClientPresence(status="idle", afk=True)

proceed_button = Button(style=ButtonStyle.DANGER, label="Proceed", custom_id="proceed")
abort_button = Button(style=ButtonStyle.PRIMARY, label="Abort", custom_id="abort")
proceed_abort_row = ActionRow.new(proceed_button, abort_button)

bot = Client(token, scope=guild_id, presence=down_presence)

###COMMANDS###
@bot.command(
    name="start",
    description="Start Minecraft docker container",
)
async def start(ctx):
    await ctx.defer(ephemeral=True)
    res = await service.start_container()
    await ctx.send(res.msg)
    await bot.change_presence(up_presence)


@bot.command(
    name="stop",
    description="Stop Minecraft docker container",
)
async def stop(ctx):
    await ctx.defer(ephemeral=True)
    res = await service.stop_container()
    if res.type == ResponseType.WARNING:
        await ctx.send(res.msg, components=proceed_abort_row)
    elif res.type == ResponseType.OK:
        await proceed(ctx)
    else:
        await ctx.send(res.msg)


@bot.command(
    name="status",
    description="Get information about the server, such as the list of connected players",
)
async def status(ctx):
    await ctx.defer(ephemeral=False)
    status_embeds = await service.status()
    await ctx.send(embeds=status_embeds)


###COMPONENTS###
@bot.component("proceed")
async def proceed(ctx):
    res = function.stop_container()
    await ctx.send(res.msg, ephemeral=True)
    await bot.change_presence(down_presence)


@bot.component("abort")
async def abort(ctx):
    res = Response(ResponseType.OK, ":wastebasket: Operation aborted succesfully.")
    await ctx.send(res.msg, ephemeral=True)


###EVENTS###
@bot.event
async def on_ready():
    await change_presense()


async def change_presense():
    if function.is_server_running():
        await bot.change_presence(up_presence)
    else:
        await bot.change_presence(down_presence)


bot.start()
