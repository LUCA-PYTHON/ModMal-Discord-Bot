from datetime import datetime
import discord
from discord import app_commands
from discord.app_commands import Group
from discord.ext import commands


class autotag(commands.Cog):

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

    autotag = Group(name='autotag', description='description', guild_only=True)

    ############################################################################################

    @autotag.command(name="add", description="› Füge ein neuen Auto - Tag hinzu.")
    @app_commands.describe(tag="› Tag, es wird überprüft ob dieses Tag im Ticket Grund ist.",
                           auto_antwort="› Antwort, die der User bekommt wenn ein Tag erkannt wird.",
                           bild="› Bild, das an die Antwort angehängt wird im Embed.")
    async def add(self, interaction: discord.Interaction, tag: str, auto_antwort: str, bild: discord.Attachment = None):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:

                await cur.execute("SELECT rolleID FROM team WHERE guildID = (%s) AND level = (%s)",
                                  (interaction.guild.id, 1))
                db_daten1 = await cur.fetchall()
                for daten1 in db_daten1:
                    role = interaction.guild.get_role(int(daten1[0]))
                    if role in interaction.user.roles:

                        await cur.execute("SELECT tag, auto_antwort FROM autofaq WHERE guildID = (%s)",
                                          interaction.guild.id)
                        db_daten = await cur.fetchall()
                        anzahl = 0
                        if db_daten:
                            for daten in db_daten:
                                anzahl += 1
                                db_tag = daten[0]
                                if db_tag == tag:
                                    embed = discord.Embed(description=f"› Es gibt das Auto - Tag (`{tag}`) schon.",
                                                          color=discord.Colour.red(),
                                                          timestamp=datetime.now())
                                    embed.set_author(name="Fehlermeldung",
                                                     icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                                    await interaction.response.send_message(embed=embed, ephemeral=True)
                                    return

                        if anzahl >= 3:
                            embed = discord.Embed(description=f"› Du kannst maximal 3 Auto-Tags festlegen.",
                                                  color=discord.Colour.red(),
                                                  timestamp=datetime.now())
                            embed.set_author(name="Fehlermeldung",
                                             icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                            return

                        if bild is None:
                            bild_url = None

                        if bild is not None:
                            bild_url = bild.url

                        await cur.execute(
                            "INSERT INTO autofaq(guildID, tag, auto_antwort, bild_url) VALUES(%s, %s, %s, %s)",
                            (interaction.guild.id, tag, auto_antwort, bild_url))
                        embed = discord.Embed(description=f"*Tag*: {tag}\n"
                                                          f"*Antwort*: `{auto_antwort}`",
                                              color=0x4c69f8,
                                              timestamp=datetime.now())
                        embed.set_author(name="Auto-Tag hinzugefügt",
                                         icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                        embed.set_footer(text=f'Das Zeichen "$" wird zu einem "Enter"!!')
                        if bild is not None:
                            embed.set_image(url=bild.url)
                        await interaction.response.send_message(embed=embed)
                else:
                    error_embed = discord.Embed(description=f"› Dir fehlt eine Teamrolle der Stufe 1.",
                                                color=discord.Colour.red(),
                                                timestamp=datetime.now())
                    error_embed.set_author(name="Fehlermeldung",
                                           icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @autotag.command(name="delete", description="› Lösche ein Auto - Tag wieder aus der Datenbank.")
    @app_commands.describe(tag="› Tag, welches gelöscht werden soll.")
    async def delete(self, interaction: discord.Interaction, tag: str):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:

                await cur.execute("SELECT rolleID FROM team WHERE guildID = (%s) AND level = (%s)",
                                  (interaction.guild.id, 1))
                db_daten1 = await cur.fetchall()
                for daten1 in db_daten1:
                    role = interaction.guild.get_role(int(daten1[0]))
                    if role in interaction.user.roles:

                        await cur.execute("SELECT tag FROM autofaq WHERE guildID = (%s)", interaction.guild.id)
                        result = await cur.fetchone()
                        if result is None:
                            embed = discord.Embed(description=f"› Das Auto - Tag (`{tag}`) gibt es nicht.",
                                                  color=discord.Colour.red(),
                                                  timestamp=datetime.now())
                            embed.set_author(name="Fehlermeldung",
                                             icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                            return

                        if result:
                            await cur.execute("DELETE FROM autofaq WHERE tag = (%s)", tag)
                            embed = discord.Embed(description=f"Es wurde das Auto - Tag `{tag}` entfernt.",
                                                  color=0x4c69f8,
                                                  timestamp=datetime.now())
                            embed.set_author(name="Auto-Tag entfernt",
                                             icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                            embed.set_footer(text=f"Author ID: {interaction.user.id}")
                            await interaction.response.send_message(embed=embed)
                            return
                else:
                    error_embed = discord.Embed(description=f"› Dir fehlt eine Teamrolle der Stufe 1.",
                                                color=discord.Colour.red(),
                                                timestamp=datetime.now())
                    error_embed.set_author(name="Fehlermeldung",
                                           icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @autotag.command(name="show", description="› Zeigt dir alle Auto - Tags.")
    @app_commands.describe(tag="› Tag, welches dir angezeigt werden soll (Optional)")
    async def show(self, interaction: discord.Interaction, tag: str = None):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:

                await cur.execute(
                    "SELECT rolleID FROM team WHERE guildID = (%s) AND level = (%s) OR guildID = (%s) AND level = (%s)",
                    (interaction.guild.id, 2, interaction.guild.id, 1))
                db_daten1 = await cur.fetchall()
                for daten1 in db_daten1:
                    role = interaction.guild.get_role(int(daten1[0]))
                    if role in interaction.user.roles:

                        await cur.execute("SELECT tag, auto_antwort, bild_url FROM autofaq WHERE guildID = (%s)",
                                          interaction.guild.id)
                        result = await cur.fetchall()

                        if result == ():
                            embed = discord.Embed(description="› Es sind keine Autotags vorhanden.",
                                                  color=0x2325a0,
                                                  timestamp=datetime.now())
                            embed.set_author(name="Fehlermeldung",
                                             icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                            return

                        if result:
                            if not tag:
                                tags = ""
                                for eintrag in result:
                                    ausgabe_tag = eintrag[0]
                                    self.counter += 1
                                    tags += f'{self.counter}. {ausgabe_tag}\n'
                                embed = discord.Embed(description=tags,
                                                      color=0x4c69f8,
                                                      timestamp=datetime.now())
                                embed.set_author(name="Auto - Tags", icon_url=interaction.user.display_avatar.url)
                                embed.set_footer(text=f"Author ID: {interaction.user.id}")
                                await interaction.response.send_message(embed=embed)
                                self.counter = 0

                            if tag:
                                for eintrag in result:
                                    ausgabe_tag = eintrag[0]
                                    ausgabe_antwort = eintrag[1]
                                    if tag == ausgabe_tag:
                                        embed = discord.Embed(description=ausgabe_antwort,
                                                              color=0x2325a0,
                                                              timestamp=datetime.now())
                                        embed.set_author(name=f'Tag - "{ausgabe_tag}"',
                                                         icon_url=interaction.user.display_avatar.url)
                                        embed.set_footer(text=f'Das Zeichen "$" wird zu einem "Enter"!!')
                                        if eintrag[2] is not None:
                                            embed.set_image(url=eintrag[2])
                                        await interaction.response.send_message(embed=embed)
                                        return

                                else:
                                    error_embed = discord.Embed(
                                        description=f"› Das Auto - Tag (`{tag}`) gibt es nicht.",
                                        color=discord.Colour.red(),
                                        timestamp=datetime.now())
                                    error_embed.set_author(name="Fehlermeldung",
                                                           icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                                    await interaction.response.send_message(embed=error_embed, ephemeral=True)

                else:
                    error_embed = discord.Embed(description=f"› `❌` | Dir fehlt eine Rolle der Stufe 2.",
                                                color=discord.Colour.red(),
                                                timestamp=datetime.now())
                    error_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
                    await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @autotag.command(name="edit", description="› Editiere ein Auto - Tag.")
    @app_commands.describe(tag="› Tag, welches editiert werden soll.",
                           new_antwort="› Die neue Antwort, des angegebenen Tags.")
    async def edit(self, interaction: discord.Interaction, tag: str, new_antwort: str):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT rolleID FROM team WHERE guildID = (%s) AND level = (%s)",
                                  (interaction.guild.id, 1))
                db_daten = await cur.fetchall()
                for daten in db_daten:
                    role = interaction.guild.get_role(int(daten[0]))
                    if role in interaction.user.roles:
                        await cur.execute("SELECT tag, auto_antwort FROM autofaq WHERE guildID = (%s)",
                                          interaction.guild.id)
                        result = await cur.fetchall()

                        if result == ():
                            embed = discord.Embed(
                                description=f"› Auf diesem Server gibt es keine Autotags.",
                                color=discord.Colour.red(),
                                timestamp=datetime.now())
                            embed.set_author(name="Fehlermeldung",
                                             icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                            return

                        if result:
                            for eintrag in result:
                                eintrag_tag = eintrag[0]
                                eintrag_antwort = eintrag[1]

                                if eintrag_antwort == new_antwort and eintrag_tag == tag:
                                    embed = discord.Embed(
                                        description=f"› Du hast gar nichts an dem Auto-Tag verändert!",
                                        color=discord.Colour.red(),
                                        timestamp=datetime.now())
                                    embed.set_author(name="Fehlermeldung",
                                                     icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                                    await interaction.response.send_message(embed=embed, ephemeral=True)
                                    return

                                if eintrag_antwort != new_antwort and eintrag_tag == tag:
                                    await cur.execute(
                                        "UPDATE autofaq SET auto_antwort = (%s) WHERE tag = (%s) AND guildID = (%s)",
                                        (new_antwort, tag, interaction.guild.id))
                                    add_embed = discord.Embed(description=f"```{eintrag_antwort}```\n"
                                                                          f"**editiert zu:**\n\n"
                                                                          f"```{new_antwort}```",
                                                              color=0x4c69f8,
                                                              timestamp=datetime.now())
                                    add_embed.set_author(name="Auto-Tag editiert",
                                                         icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                                    add_embed.set_footer(text=f"Snippet Name: {tag}")
                                    await interaction.response.send_message(embed=add_embed)
                                    return

                            else:
                                embed = discord.Embed(
                                    description=f"› Das Autotag (`{tag}`) gibt es nicht.",
                                    color=discord.Colour.red(),
                                    timestamp=datetime.now())
                                embed.set_author(name="Fehlermeldung",
                                                 icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                                await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    error_embed = discord.Embed(
                        description=f"› Dir fehlt eine Teamrolle der Stufe 1.",
                        color=discord.Colour.red(),
                        timestamp=datetime.now())
                    error_embed.set_author(name="Fehlermeldung",
                                           icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @autotag.command(name="test", description="› Führe einen Probe für ein Auto - Tag durch")
    @app_commands.describe(tag="› Tag, welches du ausprobieren möchtest.")
    async def test(self, interaction: discord.Interaction, tag: str):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT rolleID FROM team WHERE guildID = (%s) AND level = (%s)",
                                  (interaction.guild.id, 1))
                db_daten = await cur.fetchall()
                for daten in db_daten:
                    role = interaction.guild.get_role(int(daten[0]))
                    if role in interaction.user.roles:
                        await cur.execute(
                            "SELECT auto_antwort, bild_url FROM autofaq WHERE guildID = (%s) AND tag = (%s)",
                            (interaction.guild.id, tag))
                        db_daten2 = await cur.fetchone()
                        if db_daten2 is not None:
                            msg = db_daten2[0].replace("$", "\n")
                            tag_embed = discord.Embed(description=msg,
                                                      color=0x0f76da,
                                                      timestamp=datetime.now())
                            tag_embed.set_author(name="Auto-Tag", icon_url=interaction.user.display_avatar.url)
                            tag_embed.set_footer(text="Das ist eine Automatische Nachricht!")
                            if db_daten2[1] is not None:
                                tag_embed.set_image(url=db_daten2[1])
                            await interaction.response.send_message(embed=tag_embed)
                            return

                        if db_daten2 is None:
                            error_embed = discord.Embed(
                                description=f"› Das Auto-Tag (`{tag}`) gibt es nicht.",
                                color=discord.Colour.red(),
                                timestamp=datetime.now())
                            error_embed.set_footer(text="/autotag add [tag] [auto_antwort]")
                            error_embed.set_author(name="Fehlermeldung",
                                                   icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                            await interaction.response.send_message(embed=error_embed, ephemeral=True)
                            return

                else:
                    error_embed = discord.Embed(
                        description=f"› Dir fehlt eine Teamrolle der Stufe 1.",
                        color=discord.Colour.red(),
                        timestamp=datetime.now())
                    error_embed.set_author(name="Fehlermeldung",
                                           icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await interaction.response.send_message(embed=error_embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(autotag(bot))
