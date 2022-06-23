import os
import discord
from discord.ext import commands
my_secret = os.environ['Token']

Client = commands.Bot(command_prefix = '&')
Client.remove_command("help")

@Client.event
async def onready():
  print("Ready!")

@Client.command()
async def help(ctx):
  embed = discord.Embed(title = "**COMMANDS**", description = '`These are the commands you can use for now : `', colour=655359)
  embed.set_thumbnail(url="https://cdn141.picsart.com/338512637029211.png")

  embed.add_field(
    name = "&help",
    value = "To list all commands"
  )
  embed.add_field(
    name = "&clear",
    value = "To clear messages"
  )
  embed.add_field(
    name = "&kick",
    value = "To kick members"
  )
  embed.add_field(
    name = "&ban",
    value = "To ban members"
  )
  embed.add_field(
    name = "&mute",
    value = "To mute members"
    
  )
  embed.add_field(
    name = "&unmute",
    value = "To unmute members"
  )
  embed.add_field(
    name = "&poll",
    value = "To create polls"  
  )
  embed.add_field(
    name = "&snipe",
    value = "To see last deleted message"
  )

  await ctx.send(embed = embed)


@Client.command(aliases=['clear'])
async def purge(ctx, amount=5):
    if(not ctx.author.guild_permissions.manage_messages):
        await ctx.send('Cannot run command! Requires: ``Manage Messages``')
        return
    amount = amount+1
    if amount > 101:
        await ctx.send('I can\'t delete more than 100 messages at a time!')
    else: 
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'Sucessfully deleted {amount} messages!')

@Client.command(case_insensitive=True)
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} has been kicked from {ctx.guild}!')
 
@Client.command(case_insensitive=True)
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{mention.mention} has been banned from {ctx.guild}!')

@Client.command(case_insensitive=True)
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    if reason == None:
        await ctx.send('Please write a reason!')
        return
    guild = ctx.guild
    muteRole = discord.utils.get(guild.roles, name = "Muted")
 
    if not muteRole:
        await ctx.send("No Mute Role found! Creating one now...")
        muteRole = await guild.create_role(name = "Muted")
 
        for channel in guild.channels:
            await channel.set_permissions(muteRole, speak=False, send_messages=False, read_messages=True, read_message_history=True)
        await member.add_roles(muteRole, reason=reason)
        await ctx.send(f"{member.mention} has been muted in {ctx.guild} | Reason: {reason}")
        await member.send(f"You have been muted in {ctx.guild} | Reason: {reason}")
 
@Client.command(case_insensitive=True)
async def unmute(ctx, member: discord.Member, *, reason=None):
 
    guild = ctx.guild
    muteRole = discord.utils.get(guild.roles, name = "Muted")
 
    if not muteRole:
        await ctx.send("The Mute role can\'t be found! Please check if there is a mute role or if the user already has it!")
        return
    await member.remove_roles(muteRole, reason=reason)
    await ctx.send(f"{member.mention} has been unmuted in {ctx.guild}")
    await member.send(f"You have been unmuted in {ctx.guild}")

@Client.command()
async def poll(ctx, *, question=None):
    if question == None:
        await ctx.send("Please write a poll!")
 
    icon_url = ctx.author.avatar_url 
 
    pollEmbed = discord.Embed(title = "New Poll!", description = f"{question}")
 
    pollEmbed.set_footer(text = f"Poll given by {ctx.author}", icon_url = ctx.author.avatar_url)
 
    pollEmbed.timestamp = ctx.message.created_at 
 
    await ctx.message.delete()
 
    poll_msg = await ctx.send(embed = pollEmbed)
 
    await poll_msg.add_reaction("⬆️")
    await poll_msg.add_reaction("⬇️")

snipe_message_author = {}
snipe_message_content = {}
 
@Client.event
async def on_message_delete(message):
     snipe_message_author[message.channel.id] = message.author
     snipe_message_content[message.channel.id] = message.content
     await sleep(60)
     del snipe_message_author[message.channel.id]
     del snipe_message_content[message.channel.id]
 
@Client.command()
async def snipe(ctx):
    channel = ctx.channel 
    try:
        snipeEmbed = discord.Embed(title=f"Last deleted message in #{channel.name}", description = snipe_message_content[channel.id])
        snipeEmbed.set_footer(text=f"Deleted by {snipe_message_author[channel.id]}")
        await ctx.send(embed = snipeEmbed)
    except:
        await ctx.send(f"There are no deleted messages in #{channel.name}")

@Client.command(pass_context=True)
async def giverole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"hey {ctx.author.name}, {user.name} has been giving a role called: {role.name}")

@Client.command(pass_context=True)
async def arr(ctx):
  embed = discord.Embed(
  title = "Reaction Role",
  description = "Click this to get star command and og role"
  )
  msg = await ctx.send(embed=embed)
  await msg.add_reaction(":red_circle:")
  await msg.add_reaction(":orange_circle:")
  await msg.add_reaction(":yellow_circle:")

@Client.event
async def on_raw_reaction_add(payload):
  message_id = payload.message_id
  if message_id == 940938439426199585:
    member = payload.member
    guild = member.guild

    emoji = payload.emoji.name
    if payload.emoji.name == ':red_circle:':
      role = discord.utils.get(guild_roles, name='OG')
    elif payload.emoji.name == ':orange_circle:':
      role = discord.utils.get(guild_roles, name='Star Command')
    elif payload.emoji.name == ':yellow_circle:':
      role = discord.utils.get(guild_roles, name='Flame')
    await member.add_roles(role)
      
    if role is not None:
      member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
      if member is not None:
        await member.add_roles(role)
        print("done")
      else:
        print("Member not found")
    
    else:
      print("Role not found")

@Client.command(pass_context=True)
async def fuck(ctx):
    await ctx.send("yamante kudasai")

@Client.command(pass_context=True)
async def h(ctx):
    await ctx.send("pls help")
  
Client.run(os.getenv("Token"))
