from discord.utils import get
from roleNames import *

async def add_role(context, argument):
    member = context["member"]
    guild = context["guild"]
    role = argument
    if role in valid_roles:
        role_data = get(guild.roles, name=role)
        await member.add_roles(role_data)
        message = f"Role {role_data.name} added!"
        print(f'Added role {role_data.name} to {member.name}.')
    else:
        message = f"{argument} isn't a valid role. Type '/help roles' for a list of valid roles."
        print(f'Invalid role for {member.name}.')

    return message

async def remove_role(context, argument):
    member = context["member"]
    guild = context["guild"]
    role = argument
    if role in valid_roles:
        role_data = get(guild.roles, name=role)
        await member.remove_roles(role_data)
        message = f"Role {role_data.name} removed."
        print(f'Removed role {role_data.name} from {member.name}.')
    else:
        message = f"{argument} isn't a valid role. Type '/help roles' for a list of valid roles."
        print(f'Invalid role for {member.name}.')

    return message