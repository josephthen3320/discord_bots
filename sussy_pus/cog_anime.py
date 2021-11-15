# cog_anime.py
import discord
from discord.ext import commands
import time
import asyncio
from NyaaPy.nyaa import Nyaa
from jikanpy import Jikan
from hentai import Hentai, Format

jikan = Jikan()
nyaa = Nyaa()

explicit_ratings = ["Rx", "R+"]

def search_anime(mal_id):
  result = jikan.anime(mal_id)
  return result


class AnimeCog(commands.Cog):

    def __init__(self, bot: commands.Bot):
      self.bot = bot

    @commands.command(name="nyaa")
    async def nyaa(self, ctx, *args):
      author = ctx.message.author
      tmpmsg = await ctx.send("Fetching information from Nyaa.si")
      await ctx.message.delete()

      if len(args) < 1:
        await ctx.send(f"{author.mention} please try again. Usage: `?nyaa [title]`")
        return
      elif len(args) >= 1:
        search_term = " ".join(args)
        search_term = str(search_term)
      
      print(search_term)
      results = nyaa.search()

      titles = []
      
      for i in range(len(results)):
        titles.append(results[i]['name'])

      print(titles)

      

      

    # Fetch anime information
    @commands.command(name="anmrecc")
    @commands.cooldown(rate=1, per=4)
    async def anmrecc(self, ctx, *args):
      author = ctx.message.author
      tmpmsg = await ctx.send("Fetching information from MAL...")
      await ctx.message.delete()
      isVisible = False

      print(f"> MAL Search Requested by {author}")

      # print(args)
      print(">   Check: Arguments")
      if len(args) < 1:   # check if any arguments passed
        print(">   Error: args LESS THAN 1")
        await ctx.send(f"{author.mention} please try again. Usage: `+anmrecc [-v] [title]`")
        return
      elif len(args) > 1:   # if there is more than one argument, 
        arg1 = args[0]      # check if 1st argument == -v   to toggle
                            # visibility of R-rated anime thumbnails
        if arg1 == "-v":
          print(">   Toggle: isVisible=true")
          isVisible = True
          # print(f"isVisible = {isVisible}")
          search_term = " ".join(args[1:])
        else:
          print(">   Toggle: isVisible=false")
          isVisible = False
          search_term = " ".join(args)
        # print(search_term)
      else:
        print(">   Notice: No argument set")
        search_term = " ".join(args)

      print(">   Check passed")
      print(f">   Request: term=\"{search_term}\", isVisible={isVisible}")
      
      print(">   Wait: Fetching MAL ID")
      results   = jikan.search('anime', search_term, page=1)['results']
      mal_id = results[0]['mal_id']
      print(">   Fetch complete\n>   Wait: Fetching Anime Data")
      result    = jikan.anime(mal_id)
      print(">   Fetch complete")

      await tmpmsg.delete()

      # fetch result into variable
      title     = result['title']
      title_jp  = result['title_japanese']
      image     = result['image_url']
      rating    = result['rating']
      episodes  = result['episodes']
      anitype   = result['type']
      mal_url   = result['url']
      genre     = []
      [genre.append(i['name']) for i in result['genres']]
      genre_content = "; ".join(genre)

      # Synopsis processing
      if result['synopsis'] != None:
        synopsis = result['synopsis'][0:500] + f"... [Read more]({mal_url})"
      else:
        synopsis = f"[Read more]({mal_url})"

      msgcolour = 0x00fff0

      # R-rating processing
      if rating[0:2] in explicit_ratings:
        msgcolour = 0xff0000
        if not isVisible:
          image = ""

        embed = discord.Embed(title="This anime is rated R!", colour=msgcolour).set_author(name="Content Warning", icon_url="https://github.com/josephthen3320/discord_bots/blob/main/images/icons/pus_s3_15.png?raw=true")
        await ctx.send(embed=embed)
        notification = await ctx.send("1 second protocol...")
        time.sleep(1)
        await notification.delete()

      # Process final message
      embed = discord.Embed(title=title, description="", color=msgcolour)
      embed.set_image(url=image)
      embed.set_footer(text=f"Requested by {author.display_name}")
      embed.set_author(name=f"{author.display_name}", icon_url=author.avatar_url)
      embed.add_field(name="Original Title",  value=title_jp,       inline=True)
      embed.add_field(name="Type",            value=anitype,        inline=True)
      embed.add_field(name="Episodes",        value=episodes,       inline=True)
      embed.add_field(name="Genre",           value=genre_content,  inline=True)
      embed.add_field(name="Synopsis",        value=synopsis,       inline=False)

      await ctx.send(embed=embed)   # send message
        
    @anmrecc.error
    async def anmrecc_error(self, ctx, error):
      if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(title="Cooldown alert", description=f"Try again in {round(error.retry_after)} seconds.", delete_after=5)
        await ctx.send(embed=embed)

    # anmsearch: Anime Search in MAL
    @commands.command(name="anmsearch")
    async def anmsearch(self, ctx, *args):
      author = ctx.message.author
      if len(args) < 1:
        await ctx.send(f"{author.mention}, what do you want me to search for?\nUsage: `+anmsearch [query]`")
        return

      if "-v" in args:
        isVisible = True
        search_term = list(args)
        search_term.remove("-v")
      else:
        isVisible = False
        search_term = list(args)

      query = " ".join(search_term)
      print(query)

      tmp = await ctx.send("Searching MAL database...")
      results = jikan.search('anime', query, page=1)['results']
      await tmp.delete()
      print(f"Results count: {len(results)}")

      titles = []
      ids = []
      for i in range(5):
        tmp1 = results[i]['title']
        tmp2 = results[i]['mal_id']
        print(f"{tmp1} ({tmp2})")
        titles.append(tmp1)
        ids.append(tmp2)     

      tmp = []
      for i in range(5):
        tmp.append(f"[{i+1}] {titles[i]}")

      for i in range(5):
        content = "\n".join(tmp)

      embed = discord.Embed(title="Anime Search Results", description=content)
      await ctx.send(embed=embed)

      message = await ctx.send("Please input a number 1-5")
      # check = lambda m: m.author == ctx.author and m.channel == ctx.channel
      try:
        selection = await self.bot.wait_for("message", timeout=10)
      except asyncio.TimeoutError:
        message = await message.edit(content="No response in 10 seconds, cancelling...")
        time.sleep(3)
        await message.delete()
        return

      response = int(selection.content)

      if response in [1,2,3,4,5]:
        id = ids[response-1]
        result    = jikan.anime(id)
      else:
        await message.edit("Error: Input out of range (1-5).\nSearch cancelled.")
        return

      # fetch result into variable
      title     = result['title']
      title_jp  = result['title_japanese']
      image     = result['image_url']
      rating    = result['rating']
      episodes  = result['episodes']
      anitype   = result['type']
      mal_url   = result['url']
      genre     = []
      [genre.append(i['name']) for i in result['genres']]
      genre_content = "; ".join(genre)

      # Synopsis processing
      if result['synopsis'] != None:
        synopsis = result['synopsis'][0:500] + f"... [Read more]({mal_url})"
      else:
        synopsis = f"[Read more]({mal_url})"

      msgcolour = 0x00fff0

      # R-rating processing
      if rating[0:2] in explicit_ratings:
        msgcolour = 0xff0000
        
        if not isVisible:
          image = ""

        embed = discord.Embed(title="This anime is rated R!", colour=msgcolour).set_author(name="Content Warning", icon_url="https://github.com/josephthen3320/discord_bots/blob/main/images/icons/pus_s3_15.png?raw=true")
        await ctx.send(embed=embed)
        notification = await ctx.send("1 second protocol...")
        time.sleep(1)
        await notification.delete()

      # Process final message
      embed = discord.Embed(title=title, description="", color=msgcolour)
      embed.set_image(url=image)
      embed.set_footer(text=f"Requested by {author.display_name}")
      embed.set_author(name=f"{author.display_name}", icon_url=author.avatar_url)
      embed.add_field(name="Original Title",  value=title_jp,       inline=True)
      embed.add_field(name="Type",            value=anitype,        inline=True)
      embed.add_field(name="Episodes",        value=episodes,       inline=True)
      embed.add_field(name="Genre",           value=genre_content,  inline=True)
      embed.add_field(name="Synopsis",        value=synopsis,       inline=False)

      await ctx.send(embed=embed)   # send message

    @commands.command(name='mngsearch')
    async def mngsearch(self, ctx, *args):
      author = ctx.message.author
      if len(args) < 1:
        await ctx.send(f"{author.mention}, what do you want me to search for?\nUsage: `+mngsearch [query]`")
        return

      if "-v" in args:
        isVisible = True
        search_term = list(args)
        search_term.remove("-v")
      else:
        isVisible = False
        search_term = list(args)

      query = " ".join(search_term)
      print(query)

      tmp = await ctx.send("Searching MAL database...")
      results = jikan.search('manga', query, page=1)['results']
      await tmp.delete()
      print(f"Results count: {len(results)}")

      titles = []
      ids = []
      for i in range(5):
        tmp1 = results[i]['title']
        tmp2 = results[i]['mal_id']
        print(f"{tmp1} ({tmp2})")
        titles.append(tmp1)
        ids.append(tmp2)     

      tmp = []
      for i in range(5):
        tmp.append(f"[{i+1}] {titles[i]}")

      for i in range(5):
        content = "\n".join(tmp)

      embed = discord.Embed(title="Manga Search Results", description=content)
      search_result = await ctx.send(embed=embed)

      message = await ctx.send("Please input a number 1-5")
      # check = lambda m: m.author == ctx.author and m.channel == ctx.channel
      try:
        selection = await self.bot.wait_for("message", timeout=10)
      except asyncio.TimeoutError:
        message = await message.edit(content="No response in 10 seconds, cancelling...")
        time.sleep(3)
        await message.delete()
        return

      response = int(selection.content)

      if response in [1,2,3,4,5]:
        id = ids[response-1]
        result    = jikan.manga(id)
      else:
        await message.edit("Error: Input out of range (1-5).\nSearch cancelled.")
        return

      print(result)

      # fetch result into variable
      title     = result['title']
      title_jp  = result['title_japanese']
      image     = result['image_url']
      # rating    = result['rating']
      # episodes  = result['episodes']
      anitype   = result['type']
      mal_url   = result['url']
      genre     = []
      [genre.append(i['name']) for i in result['genres']]
      genre_content = "; ".join(genre)

      # Synopsis processing
      if result['synopsis'] != None:
        synopsis = result['synopsis'][0:500] + f"... [Read more]({mal_url})"
      else:
        synopsis = f"[Read more]({mal_url})"

      msgcolour = 0x00fff0

      # R-rating processing
      # if rating[0:2] in explicit_ratings:
      #   msgcolour = 0xff0000
        
      #   if not isVisible:
      #     image = ""

        # embed = discord.Embed(title="This anime is rated R!", colour=msgcolour).set_author(name="Content Warning", icon_url="https://github.com/josephthen3320/discord_bots/blob/main/images/icons/pus_s3_15.png?raw=true")
        # await ctx.send(embed=embed)
        # notification = await ctx.send("1 second protocol...")
        # time.sleep(1)
        # await notification.delete()

      # Process final message
      embed = discord.Embed(title=title, description="", color=msgcolour)
      embed.set_image(url=image)
      embed.set_footer(text=f"Requested by {author.display_name}")
      embed.set_author(name=f"{author.display_name}", icon_url=author.avatar_url)
      embed.add_field(name="Original Title",  value=title_jp,       inline=True)
      embed.add_field(name="Type",            value=anitype,        inline=True)
      # embed.add_field(name="Episodes",        value=episodes,       inline=True)
      embed.add_field(name="Genre",           value=genre_content,  inline=True)
      embed.add_field(name="Synopsis",        value=synopsis,       inline=False)

      await ctx.send(embed=embed)   # send message
      await search_result.delete()
      await message.delete()
      await selection.delete()
      



def setup(bot: commands.Bot):
  bot.add_cog(AnimeCog(bot))