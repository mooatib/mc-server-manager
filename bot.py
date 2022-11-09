import os
import interactions
from function import start_ec2

token = os.environ.get("CLIENT_ID")
guild = os.environ.get("GUILD_ID")

bot = interactions.Client(token)


@bot.command(
    name="start",
    description="Start EC2 instance",
    scope=guild,
)
async def start(ctx):
    res = start_ec2()
    await ctx.send(res, ephemeral=True)


bot.start()
