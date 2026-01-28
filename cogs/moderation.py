from datetime import datetime
import discord
from discord import app_commands
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

class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.block_counter = 0

    async def cog_unload(self) -> None:
        return await super().cog_unload()

    ############################################################################################

    #███╗   ███╗ ██████╗ ██████╗ ███████╗██████╗  █████╗ ████████╗██╗ ██████╗ ███╗   ██╗
    #████╗ ████║██╔═══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║
    #██╔████╔██║██║   ██║██║  ██║█████╗  ██████╔╝███████║   ██║   ██║██║   ██║██╔██╗ ██║
    #██║╚██╔╝██║██║   ██║██║  ██║██╔══╝  ██╔══██╗██╔══██║   ██║   ██║██║   ██║██║╚██╗██║
    #██║ ╚═╝ ██║╚██████╔╝██████╔╝███████╗██║  ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║
    #╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

    ############################################################################################

    @app_commands.command(name="block", description="› Blockiere einen User vom ModMail-System. [Support - Team]")
    @app_commands.guild_only()
    @app_commands.describe(user="› Nutzer, welcher von der ModMail blockiert werden soll.",
                           grund="› Grund, weshalb der Nutzer von der ModMail blockiert werden soll.")
    async def block(self, interaction: discord.Interaction, user: discord.Member, *, grund: str = "Kein Grund angeben"):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT rolleID FROM team WHERE guildID = (%s) AND level = (%s) OR guildID = (%s) AND level = (%s) OR guildID = (%s) AND level = (%s)", (interaction.guild.id, 3, interaction.guild.id, 2, interaction.guild.id, 1))
                db_daten = await cur.fetchall()
                for daten in db_daten:
                    role = interaction.guild.get_role(int(daten[0]))
                    if role in interaction.user.roles:

                        if user.bot:
                            error_embed = discord.Embed(
                                description=f"› Du kannst keine Bot blockieren.",
                                color=discord.Colour.red(),
                                timestamp=datetime.now())
                            error_embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                            await interaction.response.send_message(embed=error_embed, ephemeral=True)
                            return

                        if user.id == interaction.user.id:
                            error_embed = discord.Embed(
                                description=f"› Du kannst dich nicht selst blockieren.",
                                color=discord.Colour.red(),
                                timestamp=datetime.now())
                            error_embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                            await interaction.response.send_message(embed=error_embed, ephemeral=True)
                            return

                        if user.top_role >= interaction.user.top_role:
                            error_embed = discord.Embed(
                                description=f"› Der Nutzer besitzt einen höhere/gleich hohe Rolle wie du selbst.",
                                color=discord.Colour.red(),
                                timestamp=datetime.now())
                            error_embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                            await interaction.response.send_message(embed=error_embed, ephemeral=True)

                        await cur.execute("SELECT userID, grund FROM block WHERE guildID = (%s)", interaction.guild.id)
                        db_daten2 = await cur.fetchall()

                        for daten2 in db_daten2:
                            data_userID2 = daten2[0]
                            data_grund2 = daten2[1]
                            if data_userID2 == user.id:
                                embed = discord.Embed(colour=0x4c69f8,
                                                      description=f"{user.mention} ist bereits blockiert.\n"
                                                                  f"**Grund**: `{data_grund2}`",
                                                      timestamp=datetime.now())
                                embed.set_author(name="Fehlermeldung", icon_url=interaction.user.display_avatar.url)
                                embed.set_footer(text=f"Nutzer ID: {user.id}")
                                await interaction.response.send_message(embed=embed, ephemeral=True)
                                return

                        else:
                            embed = discord.Embed(colour=0x4c69f8,
                                                  description=(
                                                      f"`{user}` wurde blockiert von {interaction.user.mention}"),
                                                  timestamp=datetime.now())
                            embed.set_author(name="Erfolgreich blockiert", icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                            embed.set_footer(text=f"Grund: {grund}")
                            embedblacklist = discord.Embed(colour=discord.Colour.red(),
                                                           description=f"› `❌` | Du wurdest blockiert wegen `{grund}`!")
                            embedblacklist.set_footer(text=f"Auf {interaction.guild.name} blockiert!")
                            embedblacklist.set_author(name="Du bist gesperrt.", icon_url=user.display_avatar.url)
                            try:
                                await user.send(embed=embedblacklist)
                                await interaction.response.send_message(embed=embed)
                                await cur.execute("INSERT INTO block(guildID, userID, grund) VALUES(%s, %s, %s)", (interaction.guild.id, user.id, grund))
                                await logging(interaction, f"{user} wurd blockiert", interaction.user.display_avatar.url, f"Discord-Nutzer: {user.mention} (`{user.id}`)\n"
                                                                                                                          f"Moderator: {interaction.user}", 0x4c69f8, f"Author ID: {interaction.user.id}")

                            except:
                                await interaction.response.send_message(embed=embed)
                                await logging(interaction, f"{user} wurd blockiert", interaction.user.display_avatar.url, f"Discord-Nutzer: {user.mention} (`{user.id}`)\n"
                                                                                                                          f"Moderator: {interaction.user}", 0x4c69f8, f"{user} hat DM`s aus!")

                else:
                    error_embed = discord.Embed(
                        description=f"› `❌` | Dir fehlt eine Rolle der Stufe 3.",
                        color=discord.Colour.red(),
                        timestamp=datetime.now())
                    error_embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @app_commands.command(name="unblock", description="› Entblockiere einen User von der ModMail. [Support - Team]")
    @app_commands.guild_only()
    @app_commands.describe(user="› Nutzer ,welcher von der ModmAIl entblockiert werden soll.")
    async def unblock(self, interaction: discord.Interaction, user: discord.Member):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT rolleID FROM team WHERE guildID = (%s) AND level = (%s) OR guildID = (%s) AND level = (%s)", (interaction.guild.id, 2, interaction.guild.id, 1))
                db_daten = await cur.fetchall()
                for daten in db_daten:
                    role = interaction.guild.get_role(int(daten[0]))
                    if role in interaction.user.roles:

                        await cur.execute("SELECT userID, grund FROM block WHERE guildID = (%s)", interaction.guild.id)
                        db_daten2 = await cur.fetchall()
                        if db_daten2 == ():
                            error_embed = discord.Embed(
                                description=f"› Es gibt keine blockierten Nutzer",
                                color=discord.Colour.red(),
                                timestamp=datetime.now())
                            error_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
                            await interaction.response.send_message(embed=error_embed, ephemeral=True)

                        if db_daten2:
                            for daten2 in db_daten2:
                                daten2_user = daten2[0]
                                if daten2_user != user.id:
                                    error_embed = discord.Embed(
                                        description=f"› {user.mention} ist nicht blockiert.",
                                        color=discord.Colour.red(),
                                        timestamp=datetime.now())
                                    error_embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                                    await interaction.response.send_message(embed=error_embed, ephemeral=True)
                                    return

                                if daten2_user == user.id:
                                    embed = discord.Embed(
                                        description=f'Es wurde `{user}` entfernt von {interaction.user.mention}',
                                        color=0x4c69f8)
                                    embed.set_author(name="Erfolgreich entblockiert", icon_url="https://cdn.discordapp.com/emojis/1034554637845532692.webp?size=96&quality=lossless")
                                    embed.set_footer(text=f"Block-Grund: {daten2[1]}")
                                    await interaction.response.send_message(embed=embed)
                                    await cur.execute("DELETE FROM block WHERE userID = (%s)", user.id)
                                    await logging(interaction, f"{user} wurde entblockiert", interaction.user.display_avatar.url, f"Discord-Nutzer: {user.mention} (`{user.id}`)\n"
                                                                                                                                  f"Moderator: {interaction.user}", discord.Colour.red(), f"Author ID: {interaction.user.id}")


                else:
                    error_embed = discord.Embed(description=f"› `❌` | Dir fehlt eine Rolle der Stufe 2.",
                                                color=discord.Colour.red(),
                                                timestamp=datetime.now())
                    error_embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @app_commands.command(name="blocked", description="› Schau dir dir Blockierten User an. [Support - Team]")
    @app_commands.guild_only()
    async def blocked(self, interaction: discord.Interaction):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT rolleID FROM team WHERE guildID = (%s) AND level = (%s) OR guildID = (%s) AND level = (%s) OR guildID = (%s) AND level = (%s)",
                    (interaction.guild.id, 3, interaction.guild.id, 2, interaction.guild.id, 1))
                db_daten = await cur.fetchall()
                for daten in db_daten:
                    role = interaction.guild.get_role(int(daten[0]))
                    if role in interaction.user.roles:

                        member_block = ""
                        self.block_counter = 0
                        await cur.execute("SELECT userID, grund FROM block WHERE guildID = (%s)", interaction.guild.id)
                        db_daten2 = await cur.fetchall()
                        for daten2 in db_daten2:
                            daten2_user = daten2[0]
                            daten2_grund = daten2[1]
                            user = interaction.guild.get_member(daten2_user)
                            self.block_counter += 1
                            member_block += f"{self.block_counter}. " + user.mention + f" - {daten2_grund}\n"
                        if self.block_counter <= 0:
                            member_block = "Es ist niemand blockiert"
                        embed = discord.Embed(description=member_block,
                                              color=0x4c69f8,
                                              timestamp=datetime.now())
                        if interaction.guild.icon is not None:
                            embed.set_author(name="Blockiert", icon_url=interaction.guild.icon.url)
                        if interaction.guild.icon is None:
                            embed.set_author(name="Blockiert", icon_url=interaction.user.display_avatar.url)
                        await interaction.response.send_message(embed=embed)

                else:
                    error_embed = discord.Embed(description=f"› `❌` | Dir fehlt eine Rolle der Stufe 3.",
                                                color=discord.Colour.red(),
                                                timestamp=datetime.now())
                    error_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
                    await interaction.response.send_message(embed=error_embed, ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(moderation(bot))