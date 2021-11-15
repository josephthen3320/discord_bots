from discord.ext import commands
import discord
import time
from datetime import datetime

colour = {"red":0xff0000, "yellow":0xffff00, "blue":0x0000ff, "black":0x000000, "purple":0x8a2be2, "green":0x00ff00}

class BasicCMD(commands.Cog):
  """Basic bot commands."""

  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.command(name="help")
  async def h(self, ctx: commands.Context):
    """Displays help for the bot."""

    desc = "Pus Nyangami is a useless bot that annoys the hell out of you."
    cmdlist_general = "`!help` displays this message"
    cmdlist_tod = "`!truth` shows a Truth prompt\n`!dare` shows a Dare prompt\n`!tod` if you can't decide"
    cmdlist_random = "`!quote` gives you a quote from Pus\n`!facts` gives you a random cat fact\n`!r [x]d[y]` roll `x` dies of `y` sides."

    embed = discord.Embed(title="", description=desc, color=0x00ff00, timestamp=datetime.utcnow())

    embed.set_author(name="Pus Nyangami", icon_url="https://raw.githubusercontent.com/josephthen3320/discord_bots/main/images/icons/pus_s3_13_hi.png")

    embed.add_field(name="Commands", value=cmdlist_general, inline=False)
    embed.add_field(name="Truth or Dare", value=cmdlist_tod)
    embed.add_field(name="Random Stuff", value=cmdlist_random)
    embed.add_field(name="-----", value="[Invite me to your server!](https://discord.com/api/oauth2/authorize?client_id=905377397363314708&permissions=534119967856&scope=bot)", inline=False)
    embed.set_footer(text="Nyandafuru~!")

    await ctx.send(embed=embed)

  @commands.command(name="set-status")
  async def setstatus(self, ctx: commands.Context, *, text: str):
    """Set the Pus' status."""
    embed = discord.Embed(
      title="Pus status updated!",
      description=f"Status changed to `{text}`"
    )


    await self.bot.change_presence(activity=discord.Game(name=text))
    await ctx.send(embed=embed)

  @commands.command(name="ping")
  async def ping(self, ctx: commands.Context):
    """Get Pus' latency."""
    start_time = time.time()
    message = await ctx.send(embed=discord.Embed(title="Testing Pus Ping..."))
    end_time = time.time()

    duration = round((end_time - start_time) * 1000)
    desc = f"{round(self.bot.latency * 1000)}ms\nAPI: {duration}ms"

    embed = discord.Embed(
      title="Pong!",
      description=desc
    )

    await message.edit(embed=embed)

  @commands.command(name="f_announce")
  async def f_announce(self, ctx, *args):
    if "-t" in args:
      title_idx = args.index("-t") + 1
      title = args[title_idx]
    else:
      tmpmsg = await ctx.send("Please input a title")
      time.sleep(2)
      await tmpmsg.delete()
      return

    if "-c" in args:
      content_idx = args.index("-c") + 1
      content = args[content_idx]
    else:
      content = ""

    if "-col" in args:
      color_idx = args.index("-col") + 1
      color = args[color_idx]
      if color in colour:
        rgb = colour[color]
      else:
        await ctx.send("Colour not recognised. Try again.")
        return
    else:
      rgb = 0xC0C0C0

    embed = discord.Embed(title=title, description=content, timestamp=datetime.utcnow(), color=rgb)

    if "-f1" in args:
      f1_idx    = args.index("-f1")
      f1_name   = args[f1_idx + 1]
      f1_value  = args[f1_idx + 2]
      embed.add_field(name=f1_name, value=f1_value)

      if "-f2" in args:
        f2_idx    = args.index("-f2")
        f2_name   = args[f2_idx + 1]
        f2_value  = args[f2_idx + 2]
        embed.add_field(name=f2_name, value=f2_value)

    if "-a" in args:
      author_idx = args.index("-a") + 1
      author = args[author_idx]
      embed.set_author(name=author)

    if "-i" in args:
      icon_idx = args.index("-i") + 1
      icon = args[icon_idx]
      embed.set_thumbnail(url=icon)

    if "-img" in args:
      img_idx = args.index("-img") + 1
      img = args[img_idx]
      embed.set_image(url=img)
    
    if "-url" in args:
      url_idx = args.index("-url") + 1
      url = f"[Learn more]({args[url_idx]})"
      embed.add_field(name = "-----", value=url, inline=False)
      
    embed.set_footer(text="Nyandafuru~!")

    await ctx.message.delete()
    await ctx.send(embed=embed)


def setup(bot: commands.Bot):
  bot.add_cog(BasicCMD(bot))