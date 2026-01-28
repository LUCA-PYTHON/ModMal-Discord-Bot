from datetime import datetime
import discord
from discord import app_commands
from discord.app_commands import Group
from discord.ext import commands


async def logging(interaction, embed_author: str, embed_icon_url: str, embed_description: str, embed_color,
                  embed_footer: str):
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


class snippets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.counter = 0

    async def cog_unload(self) -> None:
        return await super().cog_unload()

    ############################################################################################

    # ███████╗███╗   ██╗██╗██████╗ ██████╗ ███████╗████████╗███████╗
    # ██╔════╝████╗  ██║██║██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔════╝
    # ███████╗██╔██╗ ██║██║██████╔╝██████╔╝█████╗     ██║   ███████╗
    # ╚════██║██║╚██╗██║██║██╔═══╝ ██╔═══╝ ██╔══╝     ██║   ╚════██║
    # ███████║██║ ╚████║██║██║     ██║     ███████╗   ██║   ███████║
    # ╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝     ╚══════╝   ╚═╝   ╚══════╝

    ############################################################################################

    snippet = Group(name='snippet', description='description', guild_only=True)

    ############################################################################################

    @snippet.command(name="add", description="› Füge ein ModMail Snippet hinzu")
    @app_commands.describe(name="› Name, den der Snippet Befehl haben soll.",
                           description="Beschreibung, die der Snippet Befehl mit dem Name haben soll.")
    async def add(self, interaction: discord.Interaction, name: str, description: str):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT rolleID FROM team WHERE guildID = (%s) AND level = (%s)",
                                  (interaction.guild.id, 1))
                db_daten = await cur.fetchall()
                for daten in db_daten:
                    role = interaction.guild.get_role(int(daten[0]))
                    if role in interaction.user.roles:
                        if len(description) > 200:
                            embed = discord.Embed(
                                description=f"› Die Beschreibung darf nicht mehr als 200 Zeichen haben.",
                                color=discord.Colour.red(),
                                timestamp=datetime.now())
                            embed.set_author(name="Fehlermeldung",
                                             icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                            return
                        await cur.execute("SELECT guildID, name FROM snippets WHERE guildID = (%s)",
                                          interaction.guild.id)
                        ausgabe1 = await cur.fetchall()
                        if ausgabe1:
                            for eintrag in ausgabe1:
                                ausgabe_guild = eintrag[0]
                                ausgabe_name = eintrag[1]
                                if str(ausgabe_name) == str(name) and int(ausgabe_guild) == int(interaction.guild.id):
                                    embed = discord.Embed(description=f"› Das Snippet (`{name}`) gibt es schon.",
                                                          color=discord.Colour.red(),
                                                          timestamp=datetime.now())
                                    embed.set_author(name="Fehlermeldung",
                                                     icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                                    await interaction.response.send_message(embed=embed, ephemeral=True)
                                    return
                        await cur.execute("INSERT INTO snippets(guildID, name, description) VALUES(%s, %s, %s)",
                                          (interaction.guild.id, name, description))
                        snippet_addembed = discord.Embed(description=f"› {description}",
                                                         color=0x4c69f8,
                                                         timestamp=datetime.now())
                        snippet_addembed.set_author(name="Snippet hinzugefügt",
                                                    icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                        snippet_addembed.set_footer(text=f"Snippet Name: {name}")
                        await interaction.response.send_message(embed=snippet_addembed)
                        await logging(interaction, "Snippet hinzugefügt", interaction.user.display_avatar.url,
                                      f"› {description}", 0x4c69f8, f"Snippet Name: {name}")
                        return
                else:
                    error_embed = discord.Embed(
                        description=f"› Dir fehlt eine Teamrolle der Stufe 1.",
                        color=discord.Colour.red(),
                        timestamp=datetime.now())
                    error_embed.set_author(name="Fehlermeldung",
                                           icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @snippet.command(name="show", description="› Schau dir alle/einzelne ModMail Snippets an")
    @app_commands.describe(name="› Das Snippet mit diesem Namen wird dir angezeigt.")
    async def show(self, interaction: discord.Interaction, name: str = None):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT rolleID FROM team WHERE guildID = (%s) AND level = (%s) OR guildID = (%s) AND level = (%s) OR guildID = (%s) AND level = (%s)",
                    (interaction.guild.id, 3, interaction.guild.id, 2, interaction.guild.id, 1))
                db_daten = await cur.fetchall()
                for daten in db_daten:
                    role = interaction.guild.get_role(int(daten[0]))
                    if role in interaction.user.roles:
                        await cur.execute("SELECT name, description FROM snippets WHERE guildID = (%s)",
                                          interaction.guild.id)
                        result = await cur.fetchall()

                        if result == ():
                            embed = discord.Embed(description="› Es sind keine Snippet vorhanden.",
                                                  color=discord.Colour.red(),
                                                  timestamp=datetime.now())
                            embed.set_author(name="Fehlermeldung",
                                             icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                            return

                        if result:

                            if not name:
                                snippetnames = ""
                                for eintrag in result:
                                    name = eintrag[0]
                                    self.counter += 1
                                    snippetnames += f'{self.counter}. {name}\n'
                                embed = discord.Embed(description=snippetnames,
                                                      color=0x4c69f8,
                                                      timestamp=datetime.now())
                                embed.set_author(name="Snippets", icon_url=interaction.user.display_avatar.url)
                                await interaction.response.send_message(embed=embed)
                                self.counter = 0

                            if name:
                                for eintrag in result:
                                    eintrag_name = eintrag[0]
                                    eintrag_des = eintrag[1]
                                    if name == eintrag_name:
                                        embed = discord.Embed(description=f'{eintrag_des}',
                                                              color=0x4c69f8,
                                                              timestamp=datetime.now())
                                        embed.set_author(name=f'Snippet - "{eintrag_name}"',
                                                         icon_url=interaction.user.display_avatar.url)
                                        await interaction.response.send_message(embed=embed)
                                        return

                                embed = discord.Embed(description=f"› Das Snippet (`{name}`) gibt es nicht.",
                                                      color=discord.Colour.red(),
                                                      timestamp=datetime.now())
                                embed.set_author(name="Fehlermeldung",
                                                 icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                                await interaction.response.send_message(embed=embed, ephemeral=True)
                                return

                            await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    error_embed = discord.Embed(
                        description=f"› Dir fehlt eine Teamrolle der Stufe 3.",
                        color=discord.Colour.red(),
                        timestamp=datetime.now())
                    error_embed.set_author(name="Fehlermeldung",
                                           icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @snippet.command(name="delete", description="› Lösche ein ModMail Snippet aus der Datenbank")
    @app_commands.describe(name="› Name des Snippets, der gelöscht wird.")
    async def delete(self, interaction: discord.Interaction, name: str):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT rolleID FROM team WHERE guildID = (%s) AND level = (%s)",
                                  (interaction.guild.id, 1))
                db_daten = await cur.fetchall()
                for daten in db_daten:
                    role = interaction.guild.get_role(int(daten[0]))
                    if role in interaction.user.roles:
                        await cur.execute("SELECT name FROM snippets WHERE name = (%s)", name)
                        result = await cur.fetchone()
                        if result is None:
                            embed = discord.Embed(description=f"› Das Snippet (`{name}`) gibt es nicht.",
                                                  color=discord.Colour.red(),
                                                  timestamp=datetime.now())
                            embed.set_author(name="Fehlermeldung",
                                             icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                            return

                        if result:
                            await cur.execute("DELETE FROM snippets WHERE name = (%s)", name)
                            embed = discord.Embed(description=f"› Es wurde das Snippet `{name}` entfernt.",
                                                  color=0x4c69f8,
                                                  timestamp=datetime.now())
                            embed.set_author(name="Snippet entfernt",
                                             icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                            embed.set_footer(text=f"Author ID: {interaction.user.id}")
                            await interaction.response.send_message(embed=embed)
                            await logging(interaction, "Snippet entfernt", interaction.user.display_avatar.url,
                                          f"› Es wurde das Snippet `{name}` entfernt.", discord.Colour.red(),
                                          f"Author ID: {interaction.user.id}")
                            return
                else:
                    error_embed = discord.Embed(
                        description=f"› Dir fehlt eine Teamrolle der Stufe 1.",
                        color=discord.Colour.red(),
                        timestamp=datetime.now())
                    error_embed.set_author(name="Fehlermeldung",
                                           icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @snippet.command(name="edit", description="› Editiere ein ModMail Snippet")
    @app_commands.describe(name="› Das Snippet mit dieserm Namen wird editiert.",
                           new_des="› Die neue Beschreibung des Snippets.")
    async def edit(self, interaction: discord.Interaction, name: str, new_des: str):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT rolleID FROM team WHERE guildID = (%s) AND level = (%s)",
                                  (interaction.guild.id, 1))
                db_daten = await cur.fetchall()
                for daten in db_daten:
                    role = interaction.guild.get_role(int(daten[0]))
                    if role in interaction.user.roles:
                        await cur.execute("SELECT name, description FROM snippets WHERE guildID = (%s)",
                                          interaction.guild.id)
                        result = await cur.fetchall()

                        if result == ():
                            embed = discord.Embed(
                                description=f"› Dieser Server hat keine Teamollen festgelegt!",
                                color=discord.Colour.red(),
                                timestamp=datetime.now())
                            embed.set_author(name="Fehlermeldung",
                                             icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                            return

                        if result:
                            for eintrag in result:
                                eintrag_name = eintrag[0]
                                eintrag_des = eintrag[1]

                                if eintrag_des == new_des and eintrag_name == name:
                                    embed = discord.Embed(
                                        description=f"› Du hast garnichts an dem Snippet verändert!",
                                        color=discord.Colour.red(),
                                        timestamp=datetime.now())
                                    embed.set_author(name="Fehlermeldung",
                                                     icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                                    await interaction.response.send_message(embed=embed, ephemeral=True)
                                    return

                                if eintrag_des != new_des and eintrag_name == name:
                                    await cur.execute(
                                        "UPDATE snippets SET description = (%s) WHERE name = (%s) AND guildID = (%s)",
                                        (new_des, name, interaction.guild.id))
                                    snippet_addembed = discord.Embed(description=f"```{eintrag_des}```\n"
                                                                                 f"**editiert zu:**\n\n"
                                                                                 f"```{new_des}```",
                                                                     color=0x4c69f8,
                                                                     timestamp=datetime.now())
                                    snippet_addembed.set_author(name="Snippet editiert",
                                                                icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                                    snippet_addembed.set_footer(text=f"Snippet Name: {name}")
                                    await interaction.response.send_message(embed=snippet_addembed)
                                    await logging(interaction, "Snippet editiert", interaction.user.display_avatar.url,
                                                  f"› Es wurde das Snippet `{name}` editiert.\n\nAlte Beschreibung: `{eintrag_des}`\nNeue Beschreibung: `{new_des}`",
                                                  discord.Colour.orange(), f"Author ID: {interaction.user.id}")
                                    return

                            else:
                                embed = discord.Embed(description=f"› Das Snippet (`{name}`) gibt es nicht.",
                                                      color=discord.Colour.red(),
                                                      timestamp=datetime.now())
                                embed.set_author(name="Fehlermeldung",
                                                 icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                                await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    error_embed = discord.Embed(
                        description=f"› `❌` | Dir fehlt eine Teamrolle der Stufe 1.",
                        color=discord.Colour.red(),
                        timestamp=datetime.now())
                    error_embed.set_author(name="Fehlermeldung",
                                           icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await interaction.response.send_message(embed=error_embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(snippets(bot))
