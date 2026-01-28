from datetime import datetime
import discord
from discord import app_commands
from discord.app_commands import Group, Choice
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


class team(commands.Cog):

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

    team = Group(name='team', description='description', guild_only=True)

    ############################################################################################

    @team.command(name="add", description="› Lege eine Teamrole und die Prorität fest. (Level: 1 - 3).")
    @app_commands.choices(level=[
        Choice(name="🏆 - Höhstes Level", value=1),
        Choice(name="🥈 - Mittleres Level", value=2),
        Choice(name="🥉 - Niedriges Level", value=3)
    ])
    @app_commands.describe(rolle='› Rolle, die als Teamrolle hizugefügt werden soll.',
                           level="› Priorität, welche die Teamrolle haben soll (1 (höhste) - 3 (niedriste)).")
    async def add(self, interaction: discord.Interaction, rolle: discord.Role, level: Choice[int]):
        if interaction.user.guild_permissions.administrator:

            role = interaction.guild.get_role(rolle.id)
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT rolleID FROM team WHERE guildID = (%s)", interaction.guild.id)
                    ausgabe1 = await cur.fetchall()
                    if ausgabe1:
                        for eintrag in ausgabe1:
                            ausgabe_rolle = eintrag[0]
                            if int(ausgabe_rolle) == role.id:
                                embed = discord.Embed(description=f"› Die Teamrolle ({rolle.mention}) gibt es schon.",
                                                      color=discord.Colour.red(),
                                                      timestamp=datetime.now())
                                embed.set_author(name="Fehlermeldung",
                                                 icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                                await interaction.response.send_message(embed=embed, ephemeral=True)
                                return

                    await cur.execute("SELECT level FROM team WHERE guildID = (%s)", interaction.guild.id)
                    db_daten = await cur.fetchall()
                    anzahl = 0
                    if db_daten:
                        for _ in db_daten:
                            anzahl += 1

                    if anzahl >= 5:
                        embed = discord.Embed(description=f"› Du kannst maximal 5 Teamrollen festlegen.",
                                              color=discord.Colour.red(),
                                              timestamp=datetime.now())
                        embed.set_author(name="Fehlermeldung",
                                         icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        return

                    await cur.execute("INSERT INTO team(guildID, rolleID, level) VALUES(%s, %s, %s)",
                                      (interaction.guild.id, rolle.id, level.value))
                    embed = discord.Embed(description=f"**Rolle**: {rolle.mention}\n"
                                                      f"**Level**: `{level.name} / {level.value}`",
                                          color=0x4c69f8,
                                          timestamp=datetime.now())
                    embed.set_author(name="Teamrolle hinzugefügt",
                                     icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                    embed.set_footer(text=f"Author ID: {interaction.user.id}")
                    await interaction.response.send_message(embed=embed)
                    await logging(interaction, "Teamrolle hinzugefügt", interaction.user.display_avatar.url,
                                  f"› Es wurde die Teamrolle {rolle.mention} hinzugefügt.\nLevel: `{level.name}`",
                                  0x4c69f8, f"Auhtor ID: {interaction.user.id}")

        else:
            await interaction.response.send_message(
                "› `❌` | Diesen Befehl muss ein Administrator des Servers ausführen!", ephemeral=True)

    @team.command(name="show", description="› Zeigt dir die Team Rollen an.")
    async def show(self, interaction: discord.Interaction):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT rolleID, level FROM team WHERE guildID = (%s)", interaction.guild.id)
                result = await cur.fetchall()

                if result == ():
                    embed = discord.Embed(description="› Es sind keine Teamrollen vorhanden.",
                                          color=0x2325a0,
                                          timestamp=datetime.now())
                    embed.set_author(name="Fehlermeldung",
                                     icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return

                if result:
                    teamrollen = ""
                    for eintrag in result:
                        ausgabe_rolle = eintrag[0]
                        ausgabe_lvl = eintrag[1]
                        self.counter += 1
                        rolle = interaction.guild.get_role(int(ausgabe_rolle))
                        if ausgabe_lvl == 1:
                            level = "🏆 - Höhstes Level"
                        if ausgabe_lvl == 2:
                            level = "🥈 - Mittleres Level"
                        if ausgabe_lvl == 3:
                            level = "🥉 - Niedriges Level"
                        teamrollen += f'{self.counter}. Rolle:{rolle.mention} \nLevel: `{level} / {ausgabe_lvl}`\n\n'
                    embed = discord.Embed(description=teamrollen,
                                          color=0x4c69f8,
                                          timestamp=datetime.now())
                    if interaction.guild.icon is not None:
                        embed.set_author(name="Teamrollen", icon_url=interaction.guild.icon.url)
                    if interaction.guild.icon is None:
                        embed.set_author(name="Teamrollen", icon_url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f"Author ID: {interaction.user.id}")
                    await interaction.response.send_message(embed=embed)
                    self.counter = 0

    @team.command(name="delete", description="› Entferne eine Teamrolle aus der Datenbank.")
    @app_commands.describe(rolle="› Rolle, die gelöscht werden soll.")
    async def delete(self, interaction: discord.Interaction, rolle: discord.Role):

        if interaction.user.guild_permissions.administrator:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    await cursor.execute("SELECT rolleID FROM team WHERE rolleID = (%s)", rolle.id)
                    result = await cursor.fetchone()
                    if result is None:
                        embed = discord.Embed(description=f"› Die Teamrolle (`{rolle.name}`) gibt es nicht.",
                                              color=discord.Colour.red(),
                                              timestamp=datetime.now())
                        embed.set_author(name="Fehlermeldung",
                                         icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                        await interaction.response.send_message(embed=embed, ephemeral=True)
                        return

                    if result:
                        await cursor.execute("DELETE FROM team WHERE rolleID = (%s)", rolle.id)
                        embed = discord.Embed(description=f"› Es wurde die Teamrolle {rolle.mention} entfernt.",
                                              color=0x4c69f8,
                                              timestamp=datetime.now())
                        embed.set_footer(text=f"Author ID: {interaction.user.id}")
                        embed.set_author(name="Teamrolle entfernt",
                                         icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                        await interaction.response.send_message(embed=embed)
                        await logging(interaction, "Teamrolle entfernt", interaction.user.display_avatar.url,
                                      f"› Die Teamrolle ({rolle.mention}) wurde entfernt.",
                                      discord.Colour.red(), f"Auhtor ID: {interaction.user.id}")
                        return

        else:
            await interaction.response.send_message(
                "› `❌` | Diesen Befehl muss ein Administrator des Servers ausführen!", ephemeral=True)

    @team.command(name="edit_level", description="› Editiere von einer Teamrolle die Priorität.")
    @app_commands.describe(rolle="› Rolle, bei der das Level editiert werden soll.",
                           level="› Priorität, welche die Teamrolle haben soll (1 (höhste) - 3 (niedriste)).")
    @app_commands.choices(level=[
        Choice(name="🏆 - Höhstes Level", value=1),
        Choice(name="🥈 - Mittleres Level", value=2),
        Choice(name="🥉 - Niedriges Level", value=3)
    ])
    async def edit_level(self, interaction: discord.Interaction, rolle: discord.Role, level: Choice[int]):

        if interaction.user.guild_permissions.administrator:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT level FROM team WHERE guildID = (%s) AND rolleID = (%s)",
                                      (interaction.guild.id, rolle.id))
                    result = await cur.fetchall()

                    if result == ():
                        embed = discord.Embed(description=f"› Die Teamrolle ({rolle.mention}) gibt es nicht.",
                                              color=discord.Colour.red(),
                                              timestamp=datetime.now())
                        embed.set_author(name="Fehlermeldung",
                                         icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                        await interaction.response.send_message(embed=embed, ephemeral=True)

                    if result:
                        for eintrag in result:
                            if level == eintrag[0]:
                                embed = discord.Embed(
                                    description=f"› Die Teamrolle ({rolle.mention}) hat schon dieses Level.",
                                    color=discord.Colour.red(),
                                    timestamp=datetime.now())
                                embed.set_author(name="Fehlermeldung",
                                                 icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                                await interaction.response.send_message(embed=embed, ephemeral=True)
                                return

                            if level != eintrag[0]:
                                await cur.execute(
                                    "UPDATE team SET level = (%s) WHERE rolleID = (%s) AND guildID = (%s)",
                                    (level.value, rolle.id, interaction.guild.id))
                                embed = discord.Embed(
                                    description=f"› {rolle.mention} wurde auf auf das Level {level} gesetzt.",
                                    color=0x4c69f8,
                                    timestamp=datetime.now())
                                embed.set_author(name="Teamrolle editiert",
                                                 icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                                embed.set_footer(text=f"Author ID: {interaction.user.id}")
                                await interaction.response.send_message(embed=embed, ephemeral=True)
                                await logging(interaction, "Teamrolle editiert", interaction.user.display_avatar.url,
                                              F"› Es wurde die Teamrolle ({rolle.mention}) editiert.\n"
                                              F"Altes Level: `{eintrag[0]}`\n"
                                              F"Neues Level: `{level.value}`",
                                              discord.Colour.orange(), f"Author ID: {interaction.user.id}")
                                return

                            return

        else:
            await interaction.response.send_message(
                "› `❌` | Diesen Befehl muss ein Administrator des Servers ausführen!", ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(team(bot))
