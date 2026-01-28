from datetime import datetime
import discord
from discord import app_commands
from discord.app_commands import Choice, Group
from discord.ext import commands

class settings(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_unload(self) -> None:
        return await super().cog_unload()

    ############################################################################################

    # ____       _   _   _
    # / ___|  ___| |_| |_(_)_ __   __ _ ___
    # \___ \ / _ \ __| __| | '_ \ / _` / __|
    # ___) |  __/ |_| |_| | | | | (_| \__ \
    # |____/ \___|\__|\__|_|_| |_|\__, |___/
    #                            |___/

    ############################################################################################

    setup = Group(name='setup', description='description', guild_only=True)

    ############################################################################################

    @setup.command(name="start", description="› Starte das ModMail Setup. [Nur Server-Owner]")
    @app_commands.describe(log_kanal="› Kanal, indem alle wichtigen Dinge gesichert werden.",
                           pingrolle="› Rolle, die beim öffnen eines ModMail Tickets gepint wird.",
                           modmail_kanal="› Kanal, indem die ModMail Tickets geöffnet werden.")
    async def start(self, interaction: discord.Interaction, log_kanal: discord.TextChannel, pingrolle: discord.Role, modmail_kanal: discord.TextChannel):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM setup WHERE guildID = (%s)", interaction.guild.id)
                db_daten = await cur.fetchone()
                if db_daten is None:
                    await cur.execute("INSERT INTO setup(guildID, log_kanal, pingrolle, modmail_kanal, stand) VALUES(%s, %s, %s, %s, %s)", (interaction.guild.id, log_kanal.id, pingrolle.id, modmail_kanal.id, "aktiv"))
                    embed = discord.Embed(description=f"› Alle wichtigen Daten wurden hinzugefügt.",
                                          color=0x4c69f8,
                                          timestamp=datetime.now())
                    embed.add_field(name="Log Kanal", value=log_kanal.mention)
                    embed.add_field(name="Pingrolle", value=pingrolle.mention)
                    embed.add_field(name="ModMail Kanal", value=modmail_kanal.mention)
                    embed.set_author(name="ModMail Daten hinzugefügt", icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                    embed.set_footer(text=f"Author ID: {interaction.user.id}")
                    await interaction.response.send_message(embed=embed)

                if db_daten is not None:
                    embed = discord.Embed(
                        description=f"› Für `{interaction.guild.name}` gibt es schon ModMail Daten.",
                        color=discord.Colour.red(),
                        timestamp=datetime.now())
                    embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await interaction.response.send_message(embed=embed, ephemeral=True)

        if interaction.user.id != interaction.guild.owner.id:
            await interaction.response.send_message("› `❌` | Nur der **Server Owner** kann disen Command ausführen", ephemeral=True)

    @setup.command(name="edit", description="Editiere das ModMail Setup. [Nur Server-Owner]")
    @app_commands.describe(log_kanal="› Kanal, indem alle wichtigen Dinge gesichert werden.",
                           pingrolle="› Rolle, die beim öffnen eines ModMail Tickets gepint wird.",
                           modmail_kanal="› Kanal, indem die ModMail Tickets geöffnet werden.")
    async def edit(self, interaction: discord.Interaction, log_kanal: discord.TextChannel, pingrolle: discord.Role, modmail_kanal: discord.TextChannel):

        if interaction.user.id == interaction.guild.owner.id:

            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT * FROM setup WHERE guildID = (%s)", interaction.guild.id)
                    db_daten = await cur.fetchone()
                    if db_daten is not None:
                        await cur.execute("UPDATE setup SET log_kanal = (%s), pingrolle = (%s), modmail_kanal = (%s) WHERE guildID = (%s)", (log_kanal.id, pingrolle.id, modmail_kanal.id, interaction.guild.id))

                        embed = discord.Embed(description=f"› ModMail daten für {interaction.guild.name} wurden editiert.",
                                              color=0x4c69f8,
                                              timestamp=datetime.now())
                        embed.add_field(name="Log Kanal", value=log_kanal.mention)
                        embed.add_field(name="Pingrolle", value=pingrolle.mention)
                        embed.add_field(name="ModMail Kanal", value=modmail_kanal.mention)
                        embed.set_author(name="ModMail daten editiert", icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                        embed.set_footer(text=f"Author ID: {interaction.user.id}")
                        await interaction.response.send_message(embed=embed)

                    if db_daten is None:
                        error_embed = discord.Embed(
                            description=f"› Für `{interaction.guild.name}` gibt es keine ModMail Daten.",
                            color=discord.Colour.red(),
                            timestamp=datetime.now())
                        error_embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                        error_embed.set_footer(text="/setup start [log_kanal] [pingrolle] [modmail_kanal]")
                        await interaction.response.send_message(embed=error_embed, ephemeral=True)

        if interaction.user.id != interaction.guild.owner.id:
            await interaction.response.send_message("› `❌` | Nur der **Server Owner** kann disen Command ausführen", ephemeral=True)

    @setup.command(name="delete", description="› Lösche das ModMail Setup. [Nur Server-Owner].")
    async def delete(self, interaction: discord.Interaction):
        if interaction.user.id == interaction.guild.owner.id:

            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT * FROM setup WHERE guildID = (%s)", interaction.guild.id)
                    db_daten = await cur.fetchone()
                    if db_daten is not None:
                        await cur.execute("DELETE FROM setup WHERE guildID = (%s)", interaction.guild.id)
                        embed = discord.Embed(
                            description=f"› ModMail - Daten für {interaction.guild.name} erfolgreich gelöscht.",
                            timestamp=datetime.now(),
                            color=0x4c69f8)
                        embed.set_author(name="ModMail Daten gelöscht", icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                        embed.set_footer(text=f"Author ID: {interaction.user.id}")
                        await interaction.response.send_message(embed=embed)

                if db_daten is None:
                    embed = discord.Embed(
                        description=f"› Für `{interaction.guild.name}` gibt es keine ModMail - Daten.",
                        color=discord.Colour.red(),
                        timestamp=datetime.now())
                    embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            await interaction.response.send_message("› `❌` | Nur der **Server Owner** kann disen Command ausführen", ephemeral=True)

    @setup.command(name="show", description="› Zeigt dir die Einstellungen für das Modmail-System.")
    async def show(self, interaction: discord.Interaction):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT rolleID FROM team WHERE guildID = (%s) AND level = (%s) OR guildID = (%s) AND level = (%s)", (interaction.guild.id, 2, interaction.guild.id, 1))
                db_daten = await cur.fetchall()
                for data in db_daten:
                    role = interaction.guild.get_role(int(data[0]))
                    if role in interaction.user.roles:
                        await cur.execute("SELECT log_kanal, pingrolle, modmail_kanal, stand FROM setup WHERE guildID = (%s)", interaction.guild.id)
                        db_daten = await cur.fetchall()
                        if db_daten:
                            for daten in db_daten:
                                log_kanal = interaction.guild.get_channel(int(daten[0]))
                                pingrolle = interaction.guild.get_role(int(daten[1]))
                                modmail_kanal = interaction.guild.get_channel(int(daten[2]))
                                log_stand = str(daten[3])
                                embed = discord.Embed(description=f"› Hier sind alle ModMail Daten für {interaction.guild.name}.",
                                                      color=0x4c69f8,
                                                      timestamp=datetime.now())
                                embed.add_field(name=f"Log Kanal ({log_stand})", value=log_kanal.mention)
                                embed.add_field(name="Pingrolle", value=pingrolle.mention)
                                embed.add_field(name="ModMail Kanal", value=modmail_kanal.mention)
                                embed.set_author(name="ModMail Daten", icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                                embed.set_footer(text=f"Author ID: {interaction.user.id}")
                                await interaction.response.send_message(embed=embed)

                        if not db_daten:
                            embed = discord.Embed(description=f"› Es gibt keine ModMail faten für diesen Server.",
                                                        color=discord.Colour.red(),
                                                        timestamp=datetime.now())
                            embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                            await interaction.response.send_message(embed=embed, ephemeral=True)



                else:
                    error_embed = discord.Embed(description=f"› Dir fehlt eine Teamrolle der Stufe 2.",
                                                color=discord.Colour.red(),
                                                timestamp=datetime.now())
                    error_embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @setup.command(name="log", description="› Aktiviere/Deeaktiviere das Log System.")
    @app_commands.choices(log=[
        Choice(name="Aktivieren", value="aktiv"),
        Choice(name="Deaktivieren", value="deaktiviert")
    ])
    async def log(self, interaction: discord.Interaction, log: Choice[str]):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM setup WHERE guildID = (%s)", interaction.guild.id)
                db_daten = await cur.fetchone()
                if db_daten is not None:
                    if log.value == "aktiv":
                        await cur.execute("UPDATE setup set stand = (%s) WHERE guildID = (%s)", (log.value, interaction.guild.id))
                        embed = discord.Embed(description=f"› Das Log System wurde aktiviert.",
                                              color=0x4c69f8,
                                              timestamp=datetime.now())
                        embed.set_author(name="Log System aktiviert", icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                        embed.set_footer(text=f"Author ID: {interaction.user.id}")
                        await interaction.response.send_message(embed=embed)

                    if log.value == "deaktiviert":
                        await cur.execute("UPDATE setup set stand = (%s) WHERE guildID = (%s)", (log.value, interaction.guild.id))
                        embed = discord.Embed(description=f"› Das Log System wurde deaktiviert.",
                                              color=0x4c69f8,
                                              timestamp=datetime.now())
                        embed.set_author(name="Log System aktiviert", icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                        embed.set_footer(text=f"Author ID: {interaction.user.id}")
                        await interaction.response.send_message(embed=embed)

                if db_daten is None:
                    embed = discord.Embed(description=f"› Du musst zuerst das ModMail Setup erledigen.",
                                          color=discord.Colour.red(),
                                          timestamp=datetime.now())
                    embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    embed.set_footer(text="/setup start [log_kanal] [pingrolle] [modmail_kanal]")
                    await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(settings(bot))