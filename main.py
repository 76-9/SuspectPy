import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.members = True
client = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or('s!'), case_insensitive=True, help_command=None, intents=intents)

@client.event 
async def on_ready():
  print("I'm in")
  print(client.user)
  await client.change_presence(status=discord.Status.online, activity=discord.Game('#FearTheSuspect'))


## ^ Rich presence
@client.command(description="Mutes the specified user.")
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, *, reason=None):
  guild = ctx.guild
  mutedRole = discord.utils.get(guild.roles, name="Muted")

  if not mutedRole:
    mutedRole = await guild.create_role(name="Muted")

    for channel in guild.channels:
      await channel.set_permissions(mutedRole, speak=False, send_messages=False)
  await member.add_roles(mutedRole, reason=reason)
  await ctx.send(f"Muted {member.mention} for reason {reason}")
  await member.send(f"You were muted in Suspect for {reason}")

@client.command(description="Unmutes the specified user.")
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member):
  guild = ctx.guild
  mutedRole = discord.utils.get(guild.roles, name="Muted")

  await member.remove_roles(mutedRole)
  await ctx.send(f"Unmuted {member.mention} successfully.")
  await member.send(f"You were unmuted in Suspect.")
## ^ Mutes and unmutes user
@client.command()
async def ping(ctx):
  latency = round(client.latency * 1000, 1)
  await ctx.send(f"Pong! {latency}ms")
## ^ Shows bot latency
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
  await member.ban(reason=reason)
  await ctx.send(f"{member} got slammed by the ban hammer. #rekt")
  await member.send(f"You got banned in Suspect because {reason}")

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
  await member.kick(reason=reason)
  await ctx.send(f"{member} got kicked.")
  await member.send(f"You got kicked in Suspect because {reason}")

## Ban + kick command 
extensions = ['Cogs.keep_alive']

if __name__ == '__main__':
    for ext in extensions:
        client.load_extension(ext)
    
## Keeping bot alive



token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)

keep_alive()
token = os.environ.get("DISCORD_BOT_SECRET")
client.run(token)

## Token stuff
## Token is hidden, there is no way to find it 

#
