from discord.utils import get
from roleNames import *

async def stop_streaming(member):
    guild = member.guild
    role = get(guild.roles, name=streaming_role)
    await member.remove_roles(role)

async def start_streaming(member):
    guild = member.guild
    role = get(guild.roles, name=streaming_role)
    await member.add_roles(role)


