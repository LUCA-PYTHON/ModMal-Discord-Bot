from datetime import datetime
import discord
from discord import app_commands
from discord.app_commands import Group
from discord.ext import commands

async def logging(interaction, embed_author: str, embed_icon_url: str, embed_description: str, embed_color, embed_footer: str):
    embed = discord.Embed(description=embed_description,
                          color=embed_color,
                          timestamp=datetime.now())
    embed.set_author(name=embed_author, icon_url=embed_icon_url)
    embed.set_footer(text=embed_footer)

    async with interaction.client.pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT log_kanal, stand FROM setup WHERE guildID = (%s)", int(interaction.guild.id))
            db_daten = await cur.fetchone()
            if db_daten is not None:
                if str(db_daten[1]) == "aktiv":
                    channel = interaction.guild.get_channel(int(db_daten[0]))
                    try:
                        await channel.send(embed=embed)
                    except:
                        pass

class prefix(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_unload(self) -> None:
        return await super().cog_unload()

    ############################################################################################

    #██████╗ ██████╗ ███████╗███████╗██╗██╗  ██╗
    #██╔══██╗██╔══██╗██╔════╝██╔════╝██║╚██╗██╔╝
    #██████╔╝██████╔╝█████╗  █████╗  ██║ ╚███╔╝
    #██╔═══╝ ██╔══██╗██╔══╝  ██╔══╝  ██║ ██╔██╗
    #██║     ██║  ██║███████╗██║     ██║██╔╝ ██╗
    #╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝

    ############################################################################################

    prefix = Group(name="prefix", description="none", guild_only=True)

    ############################################################################################

    @prefix.command(name="set", description="› Lege ein Prefix für die Snippets fest")
    @app_commands.describe(prefix="› Preifx, welches für die Snippets Befehle benutzt werden soll.")
    async def set(self, interaction: discord.Interaction, prefix: str):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT prefix FROM prefixes WHERE guildID = (%s)", interaction.guild.id)
                db_daten = await cur.fetchall()
                if db_daten == ():
                    await cur.execute("INSERT INTO prefixes(guildID, prefix) VALUES(%s, %s)", (interaction.guild.id, prefix))
                    embed = discord.Embed(description=f"› Prefix: `{prefix}`\n",
                                          color=0x4c69f8,
                                          timestamp=datetime.now())
                    embed.set_author(name="Prefix verändert", icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                    embed.set_footer(text=f"Prefix für: {interaction.guild.name}")
                    await interaction.response.send_message(embed=embed)

                if db_daten:
                    await cur.execute("UPDATE prefixes SET prefix = (%s) WHERE guildID = (%s)", (prefix, interaction.guild.id))
                    embed = discord.Embed(description=f"Prefix: `{prefix}`\n",
                                          color=0x4c69f8,
                                          timestamp=datetime.now())
                    embed.set_author(name="Prefix verändert", icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                    embed.set_footer(text=f"Prefix für: {interaction.guild.name}")
                    await interaction.response.send_message(embed=embed)

                await logging(interaction, "Prefix verändert", interaction.user.display_avatar.url, f"Prefix wurde geändert zu: `{prefix}`", 0x4c69f8, F"Author ID: {interaction.user.id}")

    @prefix.command(name="delete", description="› Lösche das Prefix aus der Datenbank")
    async def delete(self, interaction: discord.Interaction):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT prefix FROM prefixes WHERE guildID = (%s)", interaction.guild.id)
                db_daten = await cur.fetchall()
                if db_daten:
                    await cur.execute("DELETE FROM prefixes WHERE guildID = (%s)", interaction.guild.id)
                    embed = discord.Embed(description=f"› Das Prefix wurde erfolgreich gelöscht.",
                                          color=0x4c69f8,
                                          timestamp=datetime.now())
                    embed.set_author(name="Prefix gelöscht", icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                    embed.set_footer(text=f"Author ID: {interaction.user.id}")
                    await interaction.response.send_message(embed=embed)
                    await logging(interaction, "Prefix gelöscht", interaction.user.display_avatar.url, f"Prefix wurde auf `!` zurückgesetzt.", 0x4c69f8, f"Author ID: {interaction.user.id}")

                if db_daten == ():
                    embed = discord.Embed(description=f"› Auf {interaction.guild.name} wurde noch kein Prefix festgelegt.",
                                          color=discord.Colour.red(),
                                          timestamp=datetime.now())
                    embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

    @prefix.command(name="show", description="› Zeigt dir das Snippet Prefix")
    async def show(self, interaction: discord.Interaction):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT prefix FROM prefixes WHERE guildID = (%s)", interaction.guild.id)
                db_daten = await cur.fetchall()
                if db_daten:
                    for daten in db_daten:
                        prefix = daten[0]

                if db_daten == ():
                    prefix = "!"

                embed = discord.Embed(description=f"› Prefix: `{prefix}`\n",
                                      color=0x4c69f8,
                                      timestamp=datetime.now())
                embed.set_author(name="Prefix anzeigen", icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                embed.set_footer(text=f"Prefix für: {interaction.guild.name}")
                await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(prefix(bot))