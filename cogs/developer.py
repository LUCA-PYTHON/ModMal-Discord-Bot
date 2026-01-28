from datetime import datetime
import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands, tasks
import logging

# Logger erstellen
logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="logs/discord.log", encoding="utf-8")
dt_fmt = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter("[{asctime}] [{levelname:<8}] {name}: {message}", dt_fmt, style="{")
handler.setFormatter(formatter)
logger.addHandler(handler)


# Status Loop
@tasks.loop(minutes=10)
async def status_task(lala):
    async with lala.pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM tickets")
            db_daten = await cur.fetchall()

            if int(len(db_daten)) == int(1):
                ticket_text = "Ticket"

            elif int(len(db_daten)) >= int(1) or int(len(db_daten)) == int(0):
                ticket_text = "Tickets"

            await lala.change_presence(
                activity=discord.Activity(type=discord.ActivityType.playing, name=f"mit {len(db_daten)} {ticket_text}"),
                status=discord.Status.online)


class developer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.counter = 0

    async def cog_unload(self) -> None:
        return await super().cog_unload()

    ############################################################################################

    # ████████╗███████╗ █████╗ ███╗   ███╗
    # ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
    #   ██║   █████╗  ███████║██╔████╔██║
    #   ██║   ██╔══╝  ██╔══██║██║╚██╔╝██║
    #   ██║   ███████╗██║  ██║██║ ╚═╝ ██║
    #   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝

    ############################################################################################

    @app_commands.command(name="reload", description="Starte einen Erweiterung des Bots neu. 🔃")
    @app_commands.guilds(discord.Object(id=865251517832626176))
    @app_commands.describe(datei="Wähle eine Cog-Datei aus!")
    @app_commands.choices(datei=[
        Choice(name="📝 - Autotag Tasks", value="autotag"),
        Choice(name="📆 - Event Tasks", value="events"),
        Choice(name="📚 - Info Tasks", value="info"),
        Choice(name="⚒ - Moderation Tasks", value="moderation"),
        Choice(name="📨 - ModMail Tasks", value="ModMail"),
        Choice(name="⚔️ - Prefix Tasks", value="prefix"),
        Choice(name="📊 - Setting Tasks", value="settings"),
        Choice(name="📑 - Snippet Tasks", value="snippets"),
        Choice(name="📡 - Team Tasks", value="team")
    ])
    async def reload(self, interaction: discord.Interaction, datei: Choice[str]):

        try:
            await self.bot.reload_extension(f"cogs.{datei.value}")
            logger.info(f"Reloaded '{datei.value}' | Ausgeführt von {interaction.user}")

        except:
            await self.bot.load_extension(f"cogs.{datei.value}")
            logger.info(f"Loaded '{datei.value}' | Ausgeführt von {interaction.user}")

        embed = discord.Embed(description=f"Die Datei `{datei.name}` wurde erfolgreich neu geladen.",
                              color=discord.Colour.dark_blue(),
                              timestamp=datetime.now()
                              )
        embed.set_footer(text=f"User ID: {interaction.user.id}")
        embed.set_author(name="🔃 - Datei neu geladen", icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, only_guild: bool = False):

        if not only_guild:
            synced = await ctx.bot.tree.sync()
            await ctx.reply(f"Ich hab `{len(synced)} Befehle` erfolgreich synchronisiert.", mention_author=False)

        else:
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
            await ctx.reply(f"Ich habe `{len(synced)} Befehle` erfolgreich auf {ctx.guild.name} synchronisiert.",
                            mention_author=False)

        status_task.start(self.bot)
        logger.info(f"Es wurden {len(synced)} Befehle synchronisiert. | Ausgeführt von {ctx.author}")

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def global_ban(self, ctx: commands.Context, user: discord.User, *, grund: str):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM global_ban WHERE userID = (%s)", user.id)
                db_daten = await cur.fetchone()
                if db_daten is None:
                    await cur.execute("INSERT INTO global_ban(userID, authorID, grund) VALUES(%s, %s, %s)",
                                      (user.id, ctx.author.id, grund))
                    await ctx.reply(
                        f"<:DeadShotHacken:1034554637845532692> {user.mention} wurde erfolgreich vom ModMail Support gesperrt.")

                if db_daten is not None:
                    await ctx.reply(f"<:DeadShotKreuz:1034902940017774662> {user.mention} ist bereits gesperrt!",
                                    mention_author=False)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def global_unban(self, ctx: commands.Context, user: discord.User):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM global_ban WHERE userID = (%s)", user.id)
                db_daten = await cur.fetchone()
                if db_daten is not None:
                    await cur.execute("DELETE FROM global_ban WHERE userID = (%s)", user.id)
                    await ctx.reply(
                        f"<:DeadShotHacken:1034554637845532692> {user.mention} wurde erfolgreich vom ModMail Support entsperrt.")

                if db_daten is None:
                    await ctx.reply(f"<:DeadShotKreuz:1034902940017774662> {user.mention} ist nicht gesperrt!",
                                    mention_author=False)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(developer(bot))
