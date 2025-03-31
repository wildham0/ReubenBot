import discord
from fileManager import *
from roleNames import *
from discord.utils import get
import datetime

def check_weekly_lead(context):
    member = context["member"]
    role = context["role"]
    if role == weeklies_lead_role and role in member.roles:
        return True
    else:
        return False

async def submit_weekly(context, weekly_data):
    guild = context["guild"]
    user = context["user"]
    spoilers_id = context["spoilers"]
    weekly_id = context["weekly"]
    spoilers_channel = await guild.fetch_channel(spoilers_id)

    role = get(guild.roles, name=weeklies_spoilers_role)
    for m in role.members:
        print(m.name)
        await m.remove_roles(role)

    all_results = read_results_file()
    if all_results is None:
        all_results = { }

    results = ""
    sorted_results = sorted(all_results,key=lambda x:all_results[x]["time"])
    for r in sorted_results:
        current = all_results[r]
        results += current["name"] + ": " + current["time"]

    empty_results = { }
    write_results_file(empty_results)

    weekly_channel = await guild.fetch_channel(weekly_id)
    current_weekly = read_weekly_file()

    if current_weekly is not None:
        try:
            weekly_message = await weekly_channel.fetch_message(current_weekly["message"])
        except discord.errors.NotFound:
            print(f'Couldn\'t find previous weekly message.')
        else:
            await weekly_message.edit(content="**This weekly has concluded.**\n\n" + weekly_message.content + "\n\n**Results:**\n" + results)
            print("Results added to previous weekly.")

    #start new weekly
    weekly_data["author"] = str(user.id)
    format_weekly_message = format_weekly(weekly_data)
    weekly_role = get(guild.roles, name=weeklies_racer_role)

    new_message = await weekly_channel.send(format_weekly_message + weekly_role.mention)
    weekly_data["message"] = new_message.id
    weekly_data["startdate"] = datetime.datetime.now().strftime("%Y-%m-%d")
    write_weekly_file(weekly_data)

    await spoilers_channel.send("The weekly has concluded.\n\n**Results:**\n" + results + "\n--------------------")
    pins = await spoilers_channel.pins()
    for message in pins:
        await message.unpin()

async def submit_result(context, time):
    guild = context["guild"]
    member = context["member"]
    spoilers_id = context["spoilers"]
    spoilers_channel = await guild.fetch_channel(spoilers_id)

    all_results = read_results_file()

    if all_results is None:
        all_results = { }

    if member.name in all_results.keys():
        return "You have already submitted results for this weekly."

    if time == "forfeit":
        result = { "name" : member.display_name, "time" : "forfeit" }
        all_results[member.name] = result
        write_results_file(all_results)
        result_message = await spoilers_channel.send(member.mention + " forfeited.")
        await result_message.pin()
        role = get(guild.roles, name=weeklies_spoilers_role)
        await member.add_roles(role)
        return "You forfeited the weekly."
    elif time == "spec":
        role = get(guild.roles, name=weeklies_spoilers_role)
        await member.add_roles(role)
        return "Spectating the weekly."
    else:
        time_element = time.split(":")
        if len(time_element) < 3:
            return "Your time wasn't correctly formated. Use HH:MM:SS format."
        time_element[0] = "00" + time_element[0]
        time_element[1] = "00" + time_element[1]
        time_element[2] = "00" + time_element[2]
        processed_time = time_element[0][-2:] + ":" + time_element[1][-2:] + ":" + time_element[2][-2:]
        result = {"name": member.name, "time": processed_time }
        all_results[member.name] = result
        write_results_file(all_results)
        result_message = await spoilers_channel.send(member.mention + " finished with a time of " + processed_time + ".")
        await result_message.pin()
        role = get(guild.roles, name=weeklies_spoilers_role)
        await member.add_roles(role)
        return "Your time was submitted successfully!"

def format_weekly(weekly_data):
    format_weekly_message = (weekly_data["description"] + "\nAuthor: <@" +  weekly_data["author"] + ">\nSeed: " +
                           weekly_data["seed"] + "\nHash: " + weekly_data["hash"] +
                           "\n\n" + "`/submit hh:mm:ss` to submit your time.\n`/forfeit` to forfeit.\n`/spectate` to spectate.\n\n" )
    return format_weekly_message
