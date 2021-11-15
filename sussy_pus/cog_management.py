import discord
from discord.ext import commands

class ManagementCog(commands.Cog):

  def __init__(self, bot: commands.Bot):
    self.bot = bot
    self.last_msg = None

  @commands.Cog.listener()
  async def on_message_delete(self, message: discord.Message):
    self.last_msg = message

  @commands.command(name="snipe")
  async def snipe(self, ctx):

    if not self.last_msg:
      await ctx.send("There is no message to snipe!")
      return
    
    author = self.last_msg.author
    content = self.last_msg.content

    embed = discord.Embed(title=f"", description=content).set_author(name=author.display_name, icon_url=author.avatar_url).set_footer(text=f"Message sniped from {author.display_name}")
    await ctx.send(embed=embed)



def setup(bot: commands.Bot):
  bot.add_cog(ManagementCog(bot))