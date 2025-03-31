import typing

from discord.ext import tasks
from discord import app_commands

from streaming import *
from weeklies import *
from roles import *
from roleNames import *
from help import *

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

configs = read_config_file()
mqServer = configs["server"]
weeklyChannel = configs["weeklychannel"]
weeklySpoilers = configs["spoilerschannel"]
botkey = configs["botkey"]

# Change command_guild to specific server for testing.
#command_guild = discord.Object(id=mqServer) #
command_guild = None


weekly_data = {
    "author" : "none",
    "description" : "a new weekly",
    "hash" : "FFFFFFFF",
    "title" : "a weekly",
    "id" : 0,
    "seed" : "https://ffmqrando.net",
    "message" : 0,
    "startdate" : datetime.datetime.now().strftime("%Y-%m-%d")
}

streaming_list = []

async def get_message_context(message):
    user = await client.fetch_user(message.author.id)
    guild = client.get_guild(mqServer)
    member = await guild.fetch_member(user.id)
    server = mqServer
    if get(guild.roles, name=weeklies_lead_role) in member.roles:
        create_weeklies = True
    elif get(guild.roles, name=moderator_role) in member.roles:
        create_weeklies = True
    elif get(guild.roles, name="admin") in member.roles:
        create_weeklies = True
    else:
        create_weeklies = False

    context = {
        "user" : user,
        "guild" : guild,
        "member" : member,
        "createweeklies" : create_weeklies,
        #"role" : role,
        "server" : server,
        "weekly" : weeklyChannel,
        "spoilers" : weeklySpoilers
    }

    return context

async def get_interaction_context(interaction):
    user = await client.fetch_user(interaction.user.id)
    guild = client.get_guild(mqServer)
    member = await guild.fetch_member(user.id)
    server = mqServer
    if get(guild.roles, name=weeklies_lead_role) in member.roles:
        create_weeklies = True
    elif get(guild.roles, name=moderator_role) in member.roles:
        create_weeklies = True
    elif get(guild.roles, name="admin") in member.roles:
        create_weeklies = True
    else:
        create_weeklies = False

    context = {
        "user" : user,
        "guild" : guild,
        "member" : member,
        "createweeklies" : create_weeklies,
        #"role" : role,
        "server" : server,
        "weekly" : weeklyChannel,
        "spoilers" : weeklySpoilers
    }

    return context

# Role commands
@tree.command(
    name="addrole",
    description="Request a specific role. Use /listroles to get a list of assignable roles.",
    guild=command_guild,
)
async def add_role_command(interaction, *, role_requested: str):
    context = await get_interaction_context(interaction)
    message = await add_role(context, role_requested)
    return await interaction.response.send_message(message, ephemeral=True)

@tree.command(
    name="removerole",
    description="Remove a specific role. Use /listroles to get a list of assignable roles.",
    guild=command_guild,
)
async def remove_role_command(interaction, *, role_requested: str):
    context = await get_interaction_context(interaction)
    message = await remove_role(context, role_requested)
    return await interaction.response.send_message(message, ephemeral=True)

@tree.command(
    name="listroles",
    description="List roles that can be self-assigned.",
    guild=command_guild,
)
async def list_roles_command(interaction):
    return await interaction.response.send_message(print_roles(), ephemeral=True)

# Weeklies management commands
@tree.command(
    name="createweekly",
    description="Create weeklies races. Only available to weekly leads.",
    guild=command_guild,
)
async def create_weekly_command(interaction, seed: str, hash: str, description: str):
    context = await get_interaction_context(interaction)
    global weekly_data
    if context["createweeklies"]:
        weekly_data["hash"] = hash
        weekly_data["seed"] = seed
        weekly_data["description"] = description
        message = "This is a preview. Use /submitweekly to confirm and post this weekly.\n\n" + format_weekly(weekly_data)
    else:
        message = "You don't have permission to use this command."
    return await interaction.response.send_message(message, ephemeral=True)

@tree.command(
    name="submitweekly",
    description="Submit a configured weekly. Be sure you used /createweekly and previewed the result first.",
    guild=command_guild,
)
async def submit_weekly_command(interaction):
    context = await get_interaction_context(interaction)

    if context["createweeklies"]:
        await interaction.response.defer(ephemeral=True)
        global weekly_data
        await submit_weekly(context, weekly_data)
        message = "Weekly posted!"
        return await interaction.followup.send(message)
    else:
        message = "You don't have permission to use this command."
        return await interaction.response.send_message(message, ephemeral=True)

# Streaming commands
@tree.command(
    name="startstreaming",
    description="Join the Now streaming FFMQ list.",
    guild=command_guild,
)
async def start_streaming_command(interaction, hours: typing.Optional[int] = 2):
    context = await get_interaction_context(interaction)
    await start_streaming(context["member"])
    streaming_list.append({"user": context["member"], "timer": hours * 60 * 60})
    return await interaction.response.send_message("Now streaming", ephemeral=True)

@tree.command(
    name="stopstreaming",
    description="Remove yourself from Now streaming FFMQ list.",
    guild=command_guild,
)
async def stop_streaming_command(interaction):
    context = await get_interaction_context(interaction)
    await stop_streaming(context["member"])
    global streaming_list
    for s in streaming_list:
        if s["user"] == context["member"]:
            streaming_list.remove(s)
    return await interaction.response.send_message("Stream has ended.", ephemeral=True)

# Participating to weeklies commands
@tree.command(
    name="submit",
    description="Submit your time for the weekly. Format is HH:MM:SS",
    guild=command_guild,
)
async def submit_time_command(interaction, time: str):
    context = await get_interaction_context(interaction)
    if interaction.channel.id != context["weekly"]:
        message = "Wrong channel. Use in #weekly-seed."
    else:
        message = await submit_result(context, time)
    return await interaction.response.send_message(message, ephemeral=True)

@tree.command(
    name="forfeit",
    description="Forfeit the weekly.",
    guild=command_guild,
)
async def forfeit_command(interaction):
    context = await get_interaction_context(interaction)
    if interaction.channel.id != context["weekly"]:
        message = "Wrong channel. Use in #weekly-seed."
    else:
        message = await submit_result(context, "forfeit")
    return await interaction.response.send_message(message, ephemeral=True)

@tree.command(
    name="spectate",
    description="Spectate the weekly.",
    guild=command_guild,
)
async def spectate_command(interaction):
    context = await get_interaction_context(interaction)
    if interaction.channel.id != context["weekly"]:
        message = "Wrong channel. Use in #weekly-seed."
    else:
        message = await submit_result(context, "spec")
    return await interaction.response.send_message(message, ephemeral=True)

# Help command
@tree.command(
    name="help",
    description="Information about ReubenBot.",
    guild=command_guild,
)
async def help_command(interaction):
    return await interaction.response.send_message(print_help(), ephemeral=True)

# Loop for streaming
@tasks.loop(seconds=60)
async def streaming_loop():
    global streaming_list
    for s in streaming_list:
        s["timer"] = s["timer"] - 600
        if s["timer"] < 0:
            await stop_streaming(s["user"])
            streaming_list.remove(s)

# Startup client
@client.event
async def on_ready():
    global mqServer
    await tree.sync(guild=command_guild)
    streaming_loop.start()
    print(f'Logged on as {client.user}!')

# Run bot
client.run(botkey)



