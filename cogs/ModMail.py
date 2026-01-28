import math
import re
from datetime import datetime
from discord import ui, app_commands
import discord
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


async def send_sticker(message, channel: discord.Thread = None, member: discord.Member = None):
    stickers = message.stickers
    if channel is None and member is not None:
        for sticker in stickers:
            if ".json" in message.stickers[0].url:
                await message.reply(
                    "› `❌` | Dieser Sticker ist ungültig, bitte sende diesen nicht mehr.")
                return

            embed = discord.Embed(
                description=f"{message.content}" + "\n\n" + f"[{sticker.name}]({sticker.url})",
                color=0x53c53e,
                timestamp=datetime.now())
            embed.set_author(name=f"{message.author}",
                             icon_url=message.author.display_avatar.url)
            embed.set_image(url=sticker.url)
            embed.set_footer(text=f"{message.guild.name}-Ticket Team")
            await member.send(embed=embed)
            await message.channel.send(embed=embed)
            await message.delete()
    if channel is not None and member is None:
        for sticker in stickers:
            if ".json" in message.stickers[0].url:
                await message.reply(
                    "› `❌` | Dieser Sticker ist ungültig, bitte sende diesen nicht mehr.")
                return

            memberembed = discord.Embed(
                description=f"{message.content}" + "\n\n" + f"[{sticker.name}]({sticker.url})",
                color=0x0f76da,
                timestamp=message.created_at)
            memberembed.set_author(name=f'{message.author}',
                                   icon_url=message.author.display_avatar.url)
            memberembed.set_image(url=sticker.url)
            await channel.send(embed=memberembed)
            await message.add_reaction(f"<:DeadShotHacken:1034554637845532692>")
            return


async def send_image(message, channel: discord.Thread = None, member: discord.Member = None):
    attachments = message.attachments

    if channel is not None and member is None:
        for img in attachments:
            name = img.url.split("/")[-1]

            memberembed = discord.Embed(
                description=f"{message.content}\n\n"
                            f"[{name}]({img.url})",
                color=0x0f76da,
                timestamp=message.created_at)
            memberembed.set_author(name=f'{message.author}',
                                   icon_url=message.author.display_avatar.url)
            memberembed.set_image(url=img.url)
            await channel.send(embed=memberembed)
            await message.add_reaction(f"<:DeadShotHacken:1034554637845532692>")
            return

    if channel is None and member is not None:
        for img in attachments:
            name = img.url.split("/")[-1]

            embed = discord.Embed(
                description=f"{message.content}" + "\n\n" + f"[{name}]({img.url})",
                color=0x53c53e,
                timestamp=datetime.now())
            embed.set_author(name=f"{message.author}",
                             icon_url=message.author.display_avatar.url)
            embed.set_image(url=img.url)
            embed.set_footer(text=f"{message.guild.name}-Ticket Team")
            await member.send(embed=embed)
            await message.channel.send(embed=embed)
            await message.delete()


async def send_message(message, channel: discord.Thread = None, member: discord.Member = None):
    if channel is not None and member is None:
        memberembed = discord.Embed(description=f"{message.content}",
                                    color=0x0f76da,
                                    timestamp=message.created_at)
        memberembed.set_author(name=f'{message.author}',
                               icon_url=message.author.display_avatar.url)
        await channel.send(embed=memberembed)
        await message.add_reaction(f"<:DeadShotHacken:1034554637845532692>")

    if channel is None and member is not None:
        embed = discord.Embed(description=f"{message.content}",
                              color=0x53c53e,
                              timestamp=datetime.now())
        embed.set_author(name=f"{message.author}", icon_url=message.author.display_avatar.url)
        embed.set_footer(text=f"{message.guild.name}-Ticket Team")
        await member.send(embed=embed)
        await message.channel.send(embed=embed)
        await message.delete()
        return


async def invite_message(message: discord.Message, einladung, channel: discord.Thread, bot):
    try:
        invite = await bot.fetch_invite(str(einladung))
        invite_guild = invite.guild
        invite_member = invite.approximate_member_count
        invite_online = invite.approximate_presence_count

    except:
        invite_guild = "No Data"
        invite_member = "No Data"
        invite_online = "No Data"

    memberembed = discord.Embed(description=f"{message.content}\n\n",
                                color=0x0f76da,
                                timestamp=message.created_at)
    memberembed.set_author(name=f'{message.author}',
                           icon_url=message.author.display_avatar.url)
    memberembed.set_footer(text=f"Guild Name: {invite_guild}\nMember: {invite_member} | Online: {invite_online}")
    await channel.send(embed=memberembed)
    await message.add_reaction(f"<:DeadShotHacken:1034554637845532692>")

    return


############################################################################################

# ██╗███╗   ██╗████████╗███████╗██████╗  █████╗  ██████╗████████╗██╗ ██████╗ ███╗   ██╗███████╗
# ██║████╗  ██║╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝
# ██║██╔██╗ ██║   ██║   █████╗  ██████╔╝███████║██║        ██║   ██║██║   ██║██╔██╗ ██║███████╗
# ██║██║╚██╗██║   ██║   ██╔══╝  ██╔══██╗██╔══██║██║        ██║   ██║██║   ██║██║╚██╗██║╚════██║
# ██║██║ ╚████║   ██║   ███████╗██║  ██║██║  ██║╚██████╗   ██║   ██║╚██████╔╝██║ ╚████║███████║
# ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝

############################################################################################


class Dropdown(discord.ui.Select):
    def __init__(self, guilds):
        options = []
        for guild in guilds:
            options.append(discord.SelectOption(label=guild.name, description=F"Server ID: {guild.id}", value=guild.id))

        options.append(discord.SelectOption(label="Löschen", description="Lösche das DropDown Menü", value="löschen"))

        super().__init__(
            placeholder="📌 Wähle einen Server aus!",
            min_values=1,
            max_values=1,
            options=options,
            disabled=False,
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "löschen":
            embed = discord.Embed(
                description=f"› Du hast die Anfrage abgebrochen.",
                color=discord.Colour.red(),
                timestamp=datetime.now())
            embed.set_author(name=f"{interaction.message.author.name}-Modmail")
            embed.set_footer(text=f"Von {interaction.user.name}")
            await interaction.response.edit_message(embed=embed, view=None)
            return

        guildID = self.values[0]

        async with interaction.client.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM setup WHERE guildID = (%s)", int(guildID))
                db_daten = await cur.fetchone()
                if db_daten is not None:
                    await cur.execute("SELECT userID FROM block WHERE guildID = (%s)", int(guildID))
                    db_daten2 = await cur.fetchall()
                    for daten2 in db_daten2:
                        daten2_user = daten2[0]
                        if daten2_user == interaction.user.id:
                            embed = discord.Embed(
                                description=f"› Du bist auf diesem Server blockiert!",
                                timestamp=datetime.now(),
                                color=discord.Colour.red())
                            embed.set_author(name="Fehlermeldung",
                                             icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                            embed.set_footer(text="Schreibe einem Ticket Moderator des Servers.")
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                            return

                    await interaction.response.send_modal(open_ticket_modal(guildID))
                    return

                if db_daten is None:
                    embed = discord.Embed(
                        description=f"› Der Server mit der ID (`{guildID}`) hat das ModMail Setup nicht erledigt.",
                        timestamp=datetime.now(),
                        color=discord.Colour.red())
                    embed.set_author(name="Fehlermeldung",
                                     icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    embed.set_footer(text="Wähle einfach einen neuen Server aus!")
                    await interaction.response.send_message(embed=embed, ephemeral=True)


class DropdownView(discord.ui.View):
    def __init__(self, guild_list):
        super().__init__()

        self.add_item(Dropdown(guild_list))


class open_ticket_modal(ui.Modal, title="› ModMail - Support"):
    def __init__(self, guildid):
        super().__init__()
        self.guildID = guildid
        self.grund = ui.TextInput(label="Was ist der GRUND für deine Support-Ticket ?", style=discord.TextStyle.long,
                                  placeholder="z.B. Allgemeine Frage", required=True)
        self.anmerkung = ui.TextInput(label='Hast du sonst noch irgendwelche ANMERKUNGEN ?',
                                      style=discord.TextStyle.long,
                                      placeholder="z.B. eine Erklärung zum Thema. Wenn nicht, einfach leer lassen!",
                                      required=False)

        self.add_item(self.grund)
        self.add_item(self.anmerkung)

    async def on_submit(self, interaction: discord.Interaction):
        view_close = Close_View()

        # ServerID rausbekommen
        counter = -1
        for data in interaction.user.mutual_guilds:
            counter += 1
            if int(data.id) == int(self.guildID):
                guild = interaction.user.mutual_guilds[counter]

                dmembed = discord.Embed(description=f'› `📡` | Dein Ticket wurde auf {guild.name} geöffnet.',
                                        color=0x53c53e)
                if guild.icon is not None:
                    dmembed.set_author(name="Ticket geöffnet", icon_url=guild.icon.url)
                if guild.icon is None:
                    dmembed.set_author(name="Ticket geöffnet", icon_url=interaction.user.display_avatar.url)
                dmembed.set_footer(text=f"Mit dem 🔒 kannst du dein Ticket schließen.")
                dmembed.add_field(name="Grund des Support-Tickets:", value=F"› *{self.grund}*")
                await interaction.response.edit_message(embed=dmembed, view=view_close)

                async with interaction.client.pool.acquire() as conn:
                    async with conn.cursor() as cur:
                        await cur.execute("SELECT pingrolle, modmail_kanal FROM setup WHERE guildID = (%s)", guild.id)
                        db_daten = await cur.fetchone()
                        if db_daten is not None:
                            channel = guild.get_channel(db_daten[1])
                            team_role = guild.get_role(db_daten[0])

                            member = guild.get_member(interaction.user.id)
                            role = ", ".join([r.mention for r in member.roles][:20])

                            await cur.execute("SELECT anzahl FROM user_tickets WHERE guildID = (%s) AND userID = (%s)",
                                              (guild.id, interaction.user.id))
                            db_daten2 = await cur.fetchall()
                            if db_daten2 == ():
                                await cur.execute(
                                    "INSERT INTO user_tickets(guildID, userID, anzahl) VALUES(%s, %s, %s)",
                                    (int(guild.id), int(interaction.user.id), 1))
                                tickets_2 = " Kein geöffnetes Ticket."
                            if db_daten2:
                                for daten2 in db_daten2:
                                    closed_ticket_db = daten2[0]
                                    closed_tickets = closed_ticket_db + 1
                                    await cur.execute(
                                        "UPDATE user_tickets SET anzahl = (%s) WHERE userID = (%s) AND guildID = (%s)",
                                        (int(closed_tickets), interaction.user.id, guild.id))
                                    tickets_2 = f"Mit {closed_ticket_db} geöffneten Tickets."
                            kanal_embed = discord.Embed(
                                description=f"Ersteller: {interaction.user.mention} (`{interaction.user.id}`)\n"
                                            f"Account erstellt vor: **{(discord.utils.utcnow() - interaction.user.created_at).days} Tagen**."
                                            f"{tickets_2}",
                                timestamp=datetime.now(),
                                color=discord.Colour.dark_blue())
                            kanal_embed.add_field(name="Grund:", value=self.grund, inline=False)
                            if self.anmerkung.value != "":
                                kanal_embed.add_field(name="Anmerkungen", value=self.anmerkung)
                            kanal_embed.add_field(name="Rollen:", value=role, inline=False)
                            kanal_embed.set_author(name="Neues Ticket erstellt",
                                                   icon_url=interaction.user.display_avatar.url)
                            first_msg = await channel.send(f"{team_role.mention}", embed=kanal_embed)
                            ticket_channel = await first_msg.create_thread(name=f"{interaction.user.id}",
                                                                           auto_archive_duration=1440, slowmode_delay=2)
                            await cur.execute("SELECT * FROM tickets WHERE guildID = (%s) AND authorID = (%s)",
                                              (guild.id, interaction.user.id))
                            db_daten3 = await cur.fetchone()
                            if db_daten3 is None:
                                await cur.execute(
                                    "INSERT INTO tickets(guildID, ticketID, authorID, ticket_grund) VALUES(%s, %s, %s, %s)",
                                    (guild.id, ticket_channel.id, interaction.user.id, self.grund))
                            async for msg in interaction.channel.history(limit=2):
                                if len(msg.embeds) < 1:
                                    memberembed2 = discord.Embed(description=f'{msg.content}', color=0x0f76da,
                                                                 timestamp=datetime.now())
                                    memberembed2.set_author(name=f'{interaction.user}',
                                                            icon_url=interaction.user.display_avatar.url)

                                    await cur.execute(
                                        "SELECT tag, auto_antwort, bild_url FROM autofaq WHERE guildID = (%s)",
                                        guild.id)
                                    autotag_daten_db = await cur.fetchall()
                                    if autotag_daten_db:
                                        for autotag_daten in autotag_daten_db:
                                            if autotag_daten[0] in self.grund.value.lower() or autotag_daten[0] in self.grund.value.upper():
                                                dm_msg = autotag_daten[1].replace("$", "\n")
                                                tag_embed = discord.Embed(description=dm_msg,
                                                                          color=0x53c53e,
                                                                          timestamp=datetime.now())
                                                tag_embed.set_author(name="Auto-Tag",
                                                                     icon_url=interaction.user.display_avatar.url)
                                                tag_embed.set_footer(text="Das ist eine Automatische Nachricht!")
                                                if autotag_daten[2] is not None:
                                                    tag_embed.set_image(url=autotag_daten[2])
                                                await interaction.channel.send(embed=tag_embed)
                                                await msg.add_reaction(f"<:DeadShotHacken:1034554637845532692>")
                                                await ticket_channel.send(embed=memberembed2)
                                                await ticket_channel.send(embed=tag_embed)
                                                return

                                    await ticket_channel.send(embed=memberembed2)
                                    await msg.add_reaction(f"<:DeadShotHacken:1034554637845532692>")
                                    return

                        if db_daten is None:
                            embed = discord.Embed(
                                description=f"› Der Server {guild.name} hat das ModMail Setup nicht erledigt!",
                                color=discord.Colour.red(),
                                timestamp=datetime.now())
                            embed.set_author(name="Fehlermeldung",
                                             icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            embed = discord.Embed(
                description=f"› Du teilst keinen Server mit mir!",
                color=discord.Colour.red(),
                timestamp=datetime.now())
            embed.set_author(name="Fehlermeldung",
                             icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
            await interaction.response.send_message(embed=embed, ephemeral=True)


class Close_View(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji="🔒", custom_id="Close")
    async def close_button(self, interaction: discord.Interaction, button: discord.Button):
        async with interaction.client.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT guildID, ticketID FROM tickets WHERE authorID = (%s)",
                                  int(interaction.user.id))
                db_daten = await cur.fetchone()
                if db_daten is not None:
                    counter = -1
                    for data in interaction.user.mutual_guilds:
                        counter += 1
                        if int(data.id) == int(db_daten[0]):
                            guild = interaction.user.mutual_guilds[counter]
                            channel = guild.get_channel_or_thread(int(db_daten[1]))
                            if channel:
                                abbruchen_embed = discord.Embed(
                                    description=f"› `❌` | Ich habe dein Ticket auf {guild.name} geschlossen.",
                                    color=discord.Colour.dark_gray(),
                                    timestamp=datetime.now())
                                abbruchen_embed.set_author(name="Geschlossen")
                                abbruchen_embed.set_footer(text=f"Viel Spaß noch auf {guild.name}")

                                embed = discord.Embed(color=discord.Colour.red(),
                                                      description=f"`🔒` Du hast das Ticket geschlossen.",
                                                      title="Ticket geschlossen")
                                embed.set_footer(text="Neues Ticket mit erneutem anschreiben!")

                                await interaction.response.edit_message(embed=embed, view=None)
                                await interaction.user.send(embed=abbruchen_embed)
                                await cur.execute("DELETE FROM tickets WHERE authorID = (%s)", int(interaction.user.id))
                                await channel.edit(name=f"Closed ({interaction.user.id})", archived=True, locked=True)

                    else:
                        embed = discord.Embed(
                            description=f"› Du teilst keinen Server mit mir!",
                            color=discord.Colour.red(),
                            timestamp=datetime.now())
                        embed.set_author(name="Fehlermeldung",
                                         icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                        await interaction.response.send_message(embed=embed, ephemeral=True)

                if db_daten is None:
                    embed = discord.Embed(
                        description=f"› Das Ticket wurde bereits geschlossen.",
                        color=discord.Colour.red(),
                        timestamp=datetime.now())
                    embed.set_author(name="Fehlermeldung",
                                     icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await interaction.response.send_message(embed=embed, ephemeral=True)


class feedback_buttons(discord.ui.View):
    def __init__(self, guild_id, guild_name, timeout):
        super().__init__(timeout=timeout)

        self.message = None
        self.guild_id = guild_id
        self.guild_name = guild_name

    @discord.ui.button(style=discord.ButtonStyle.green, label="5", emoji="⭐")
    async def fuenf_stern(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with interaction.client.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT feedback, feedback_count, feedback_zahl FROM feedback WHERE guildID = (%s)",
                                  int(self.guild_id))
                db_daten = await cur.fetchone()
                if db_daten is not None:
                    daten1 = db_daten[1] + 1
                    daten2 = db_daten[2] + 5
                    await cur.execute(
                        "UPDATE feedback SET feedback = (%s), feedback_count = (%s), feedback_zahl = (%s) WHERE guildID = (%s)",
                        (round(daten2 / daten1, 2), daten1, daten2, self.guild_id))
                    embed = discord.Embed(description=f'› `🔒` | Das Ticket wurde **geschlossen**!!\n\n'
                                                      f'> Feedback Durchschnitt: `{round(daten2 / daten1, 2)}`⭐\n'
                                                      f'> Dein Feedback: `{button.label}`⭐',
                                          color=discord.Colour.red(),
                                          timestamp=datetime.now())
                    embed.set_author(name="Ticket geschlossen", icon_url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f"{self.guild_name}")
                    await interaction.response.edit_message(embed=embed, view=None)

                if db_daten is None:
                    await cur.execute(
                        "INSERT INTO feedback(guildID, feedback, feedback_count, feedback_zahl) VALUES(%s, %s, %s, %s)",
                        (self.guild_id, 5, 1, 5))
                    embed = discord.Embed(description=f'› `🔒` | Das Ticket wurde **geschlossen**!!\n\n'
                                                      f'> Feedback Durchschnitt: `{button.label}⭐`\n'
                                                      f'> Dein Feedback: `{button.label}⭐`',
                                          color=discord.Colour.red(),
                                          timestamp=datetime.now())
                    embed.set_author(name="Ticket geschlossen", icon_url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f"{self.guild_name}")
                    await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(style=discord.ButtonStyle.green, label="4", emoji="⭐")
    async def vier_stern(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with interaction.client.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT feedback, feedback_count, feedback_zahl FROM feedback WHERE guildID = (%s)",
                                  int(self.guild_id))
                db_daten = await cur.fetchone()
                if db_daten is not None:
                    daten1 = db_daten[1] + 1
                    daten2 = db_daten[2] + 4
                    await cur.execute(
                        "UPDATE feedback SET feedback = (%s), feedback_count = (%s), feedback_zahl = (%s) WHERE guildID = (%s)",
                        (round(daten2 / daten1, 2), daten1, daten2, self.guild_id))
                    embed = discord.Embed(description=f'› `🔒` | Das Ticket wurde **geschlossen**!!\n\n'
                                                      f'> Feedback Durchschnitt: `{round(daten2 / daten1, 2)}⭐`\n'
                                                      f'> Dein Feedback: `{button.label}⭐`',
                                          color=discord.Colour.red(),
                                          timestamp=datetime.now())
                    embed.set_author(name="Ticket geschlossen", icon_url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f"{self.guild_name}")
                    await interaction.response.edit_message(embed=embed, view=None)

                if db_daten is None:
                    await cur.execute(
                        "INSERT INTO feedback(guildID, feedback, feedback_count, feedback_zahl) VALUES(%s, %s, %s, %s)",
                        (self.guild_id, 4, 1, 4))
                    embed = discord.Embed(description=f'› `🔒` | Das Ticket wurde **geschlossen**!!\n\n'
                                                      f'> Feedback Durchschnitt: `{button.label}`⭐\n'
                                                      f'> Dein Feedback: `{button.label}⭐`',
                                          color=discord.Colour.red(),
                                          timestamp=datetime.now())
                    embed.set_author(name="Ticket geschlossen", icon_url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f"{self.guild_name}")
                    await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(style=discord.ButtonStyle.secondary, label="3", emoji="⭐")
    async def drei_stern(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with interaction.client.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT feedback, feedback_count, feedback_zahl FROM feedback WHERE guildID = (%s)",
                                  int(self.guild_id))
                db_daten = await cur.fetchone()
                if db_daten is not None:
                    daten1 = db_daten[1] + 1
                    daten2 = db_daten[2] + 3
                    await cur.execute(
                        "UPDATE feedback SET feedback = (%s), feedback_count = (%s), feedback_zahl = (%s) WHERE guildID = (%s)",
                        (round(daten2 / daten1, 2), daten1, daten2, self.guild_id))
                    embed = discord.Embed(description=f'› `🔒` | Das Ticket wurde **geschlossen**!!\n\n'
                                                      f'> Feedback Durchschnitt: `{round(daten2 / daten1, 2)}⭐`\n'
                                                      f'> Dein Feedback: `{button.label}⭐`',
                                          color=discord.Colour.red(),
                                          timestamp=datetime.now())
                    embed.set_author(name="Ticket geschlossen", icon_url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f"{self.guild_name}")
                    await interaction.response.edit_message(embed=embed, view=None)

                if db_daten is None:
                    await cur.execute(
                        "INSERT INTO feedback(guildID, feedback, feedback_count, feedback_zahl) VALUES(%s, %s, %s, %s)",
                        (self.guild_id, 3, 1, 3))
                    embed = discord.Embed(description=f'› `🔒` | Das Ticket wurde **geschlossen**!!\n\n'
                                                      f'> Feedback Durchschnitt: `{button.label}⭐`\n'
                                                      f'> Dein Feedback: `{button.label}⭐`',
                                          color=discord.Colour.red(),
                                          timestamp=datetime.now())
                    embed.set_author(name="Ticket geschlossen", icon_url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f"{self.guild_name}")
                    await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(style=discord.ButtonStyle.danger, label="2", emoji="⭐")
    async def zwei_stern(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with interaction.client.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT feedback, feedback_count, feedback_zahl FROM feedback WHERE guildID = (%s)",
                                  int(self.guild_id))
                db_daten = await cur.fetchone()
                if db_daten is not None:
                    daten1 = db_daten[1] + 1
                    daten2 = db_daten[2] + 2
                    await cur.execute(
                        "UPDATE feedback SET feedback = (%s), feedback_count = (%s), feedback_zahl = (%s) WHERE guildID = (%s)",
                        (round(daten2 / daten1, 2), daten1, daten2, self.guild_id))
                    embed = discord.Embed(description=f'› `🔒` | Das Ticket wurde **geschlossen**!!\n\n'
                                                      f'> Feedback Durchschnitt: `{round(daten2 / daten1, 2)}⭐`\n'
                                                      f'> Dein Feedback: `{button.label}⭐`',
                                          color=discord.Colour.red(),
                                          timestamp=datetime.now())
                    embed.set_author(name="Ticket geschlossen", icon_url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f"{self.guild_name}")
                    await interaction.response.edit_message(embed=embed, view=None)

                if db_daten is None:
                    await cur.execute(
                        "INSERT INTO feedback(guildID, feedback, feedback_count, feedback_zahl) VALUES(%s, %s, %s, %s)",
                        (self.guild_id, 2, 1, 2))
                    embed = discord.Embed(description=f'› `🔒` | Das Ticket wurde **geschlossen**!!\n\n'
                                                      f'> Feedback Durchschnitt: `{button.label}⭐`\n'
                                                      f'> Dein Feedback: `{button.label}⭐`',
                                          color=discord.Colour.red(),
                                          timestamp=datetime.now())
                    embed.set_author(name="Ticket geschlossen", icon_url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f"{self.guild_name}")
                    await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(style=discord.ButtonStyle.danger, label="1", emoji="⭐")
    async def ein_stern(self, interaction: discord.Interaction, button: discord.ui.Button):
        async with interaction.client.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT feedback, feedback_count, feedback_zahl FROM feedback WHERE guildID = (%s)",
                                  int(self.guild_id))
                db_daten = await cur.fetchone()
                if db_daten is not None:
                    daten1 = db_daten[1] + 1
                    daten2 = db_daten[2] + 1
                    await cur.execute(
                        "UPDATE feedback SET feedback = (%s), feedback_count = (%s), feedback_zahl = (%s) WHERE guildID = (%s)",
                        (round(daten2 / daten1, 2), daten1, daten2, self.guild_id))
                    embed = discord.Embed(description=f'› `🔒` | Das Ticket wurde **geschlossen**!!\n\n'
                                                      f'> Feedback Durchschnitt: `{round(daten2 / daten1, 2)}⭐`\n'
                                                      f'> Dein Feedback: `{button.label}⭐`',
                                          color=discord.Colour.red(),
                                          timestamp=datetime.now())
                    embed.set_author(name="Ticket geschlossen", icon_url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f"{self.guild_name}")
                    await interaction.response.edit_message(embed=embed, view=None)

                if db_daten is None:
                    await cur.execute(
                        "INSERT INTO feedback(guildID, feedback, feedback_count, feedback_zahl) VALUES(%s, %s, %s, %s)",
                        (self.guild_id, 1, 1, 1))
                    embed = discord.Embed(description=f'› `🔒` | Das Ticket wurde **geschlossen**!!\n\n'
                                                      f'> Feedback Durchschnitt: `{button.label}⭐`\n'
                                                      f'> Dein Feedback: `{button.label}⭐`',
                                          color=discord.Colour.red(),
                                          timestamp=datetime.now())
                    embed.set_author(name="Ticket geschlossen", icon_url=interaction.user.display_avatar.url)
                    embed.set_footer(text=f"{self.guild_name}")
                    await interaction.response.edit_message(embed=embed, view=None)

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)


class ModMail(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 350, commands.BucketType.member)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 1.5, commands.BucketType.member)
        self.bot.add_view(Close_View())

    async def cog_unload(self) -> None:
        return await super().cog_unload()

    ############################################################################################

    # ███╗   ███╗ ██████╗ ██████╗ ███╗   ███╗ █████╗ ██╗██╗
    # ████╗ ████║██╔═══██╗██╔══██╗████╗ ████║██╔══██╗██║██║
    # ██╔████╔██║██║   ██║██║  ██║██╔████╔██║███████║██║██║
    # ██║╚██╔╝██║██║   ██║██║  ██║██║╚██╔╝██║██╔══██║██║██║
    # ██║ ╚═╝ ██║╚██████╔╝██████╔╝██║ ╚═╝ ██║██║  ██║██║███████╗
    # ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝

    ############################################################################################

    @commands.Cog.listener()
    async def on_message(self, message):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM global_ban WHERE userID = (%s)", message.author.id)
                ban_daten = await cur.fetchone()
                if ban_daten is not None:
                    return

                if message.is_system():
                    return

                if message.author.bot:
                    return

                bucket = self.cooldown.get_bucket(message)
                retry_after = bucket.update_rate_limit()
                if retry_after:
                    return

                # Direkt Nachricht
                if isinstance(message.channel, discord.DMChannel):
                    await cur.execute("SELECT guildID, ticketID FROM tickets WHERE authorID = (%s)",
                                      int(message.author.id))
                    ticket_daten = await cur.fetchone()
                    if ticket_daten is not None:
                        guild = self.bot.get_guild(int(ticket_daten[0]))
                        channel = self.bot.get_channel(int(ticket_daten[1]))
                        await cur.execute("SELECT userID FROM block WHERE guildID = (%s)", guild.id)
                        db_daten = await cur.fetchall()
                        for daten in db_daten:
                            daten_user = daten[0]
                            if daten_user == message.author.id:
                                return

                        stickers = message.stickers
                        attachments = message.attachments
                        # Bilder gesendet
                        if len(attachments) > 0 and len(stickers) > 0:
                            await message.reply("› `❌` | Du kannst nur Sticker oder Bilder senden.")
                            return

                        if len(attachments) > 0:
                            if len(attachments) > 2:
                                await message.reply("› `❌` | Ich kann nicht mehr als 2 Bilder auf einmal senden.")
                                return
                            if len(attachments) <= 5:
                                await send_image(message, channel, None)
                                return

                        # Sticker gesendet
                        if len(stickers) > 0:
                            await send_sticker(message, channel, None)
                            return

                        # Nachricht gesendet
                        else:
                            invite_regex = re.compile(
                                "(?:https?://)?discord(?:(?:app)?\.com/invite|\.gg)/?[a-zA-Z0-9]+/?")
                            result = invite_regex.findall(message.content)
                            if result:
                                counter = 0
                                for data in result:
                                    counter += 1
                                    if counter > 1:
                                        await message.add_reaction("<:DeadShotKreuz:1034902940017774662>")
                                        return

                                await invite_message(message, data, channel, self.bot)
                                return

                            await send_message(message, channel, None)
                            return

                    if ticket_daten is None:
                        bucket = self.cd_mapping.get_bucket(message)
                        retry_after = bucket.update_rate_limit()

                        # Zu schnell hintereinander geschrieben (COOLDOWN)
                        if retry_after:
                            seconds_in_day = 86400
                            seconds_in_hour = 3600
                            seconds_in_minute = 60
                            seconds = retry_after
                            days = seconds // seconds_in_day
                            seconds = seconds - (days * seconds_in_day)
                            hours = seconds // seconds_in_hour
                            seconds = seconds - (hours * seconds_in_hour)
                            minutes = seconds // seconds_in_minute
                            seconds = seconds - (minutes * seconds_in_minute)

                            # Sekunden Cooldown
                            if math.ceil(retry_after) <= 60:
                                seconds2 = round(seconds)
                                embed = discord.Embed(
                                    description=f"› `❌` | Du schreibst zu schnell, warte bitte `{seconds2} Sekunden`!",
                                    color=discord.Colour.red())
                                embed.set_author(name=f"Cooldown !!")
                                embed.set_footer(text=f"Wenn es ein Problem gibt schreib Luca♛#7857.")
                                await message.author.send(embed=embed)
                                return

                            # Minuten Cooldown
                            elif math.ceil(retry_after) <= 86400:
                                embed = discord.Embed(
                                    description=f"› `❌` | Du schreibst zu schnell, warte bitte `{minutes} Minuten`!",
                                    color=discord.Colour.red())
                                embed.set_author(name=f"Cooldown !!")
                                embed.set_footer(text=f"Wenn es ein Problem gibt schreib Luca♛#7857.")
                                await message.author.send(embed=embed)
                                return

                        # Nachricht geschrieben
                        else:
                            guild_list = message.author.mutual_guilds
                            view = DropdownView(guild_list)
                            verify_embed = discord.Embed(
                                description=f"› `💎` | Möchtest du ein ModMail - Ticket öffnen ?",
                                color=0x1aeed7,
                                timestamp=message.created_at)
                            verify_embed.set_author(name=f"{self.bot.user.name}-Modmail")
                            verify_embed.set_footer(text=f"Von {message.author.name}")
                            await message.channel.send(embed=verify_embed, view=view)
                    return

                # Team/Thread Nachricht
                if isinstance(message.channel, discord.Thread):
                    await cur.execute("SELECT guildID, authorID FROM tickets")
                    db_daten2 = await cur.fetchall()
                    for daten2 in db_daten2:
                        if int(daten2[1]) == int(message.channel.name):
                            guild = self.bot.get_guild(int(daten2[0]))
                            member = guild.get_member(int(daten2[1]))

                            # Snippets erstellen und verarbeiten
                            await cur.execute("SELECT guildID, name, description FROM snippets WHERE guildID = (%s)",
                                              guild.id)
                            result = await cur.fetchall()
                            if result:
                                for eintrag in result:
                                    guildid = eintrag[0]
                                    name = eintrag[1]
                                    snippetdes = eintrag[2]

                                    if guildid == message.guild.id:
                                        await cur.execute("SELECT prefix FROM prefixes WHERE guildID = (%s)", guild.id)
                                        db_daten3 = await cur.fetchone()
                                        if db_daten3 is not None:
                                            prefix = db_daten3[0]

                                        if db_daten3 is None:
                                            prefix = "!"

                                        if message.content == f"{prefix}{name}":
                                            snippet_embed = discord.Embed(description=snippetdes,
                                                                          color=0x53c53e,
                                                                          timestamp=datetime.utcnow())
                                            snippet_embed.set_author(name=message.author,
                                                                     icon_url=message.author.display_avatar.url)
                                            snippet_embed.set_footer(text=f"{message.guild.name}-Ticket Team")
                                            await member.send(embed=snippet_embed)
                                            await message.channel.send(embed=snippet_embed)
                                            await message.delete()
                                            return

                            await cur.execute("SELECT prefix FROM prefixes WHERE guildID = (%s)", guild.id)
                            prefix_daten_db = await cur.fetchone()
                            if prefix_daten_db is not None:
                                prefix = prefix_daten_db[0]

                            if prefix_daten_db is None:
                                prefix = "!"

                            if message.content.startswith(prefix):
                                return

                            stickers = message.stickers
                            attachments = message.attachments

                            # Bilder gesendet
                            if len(attachments) > 0 and len(stickers) > 0:
                                await message.reply("› `❌` | Du kannst nur Sticker oder Bilder senden.")
                                return

                            if len(attachments) > 0:
                                if len(attachments) > 2:
                                    await message.reply("› `❌` | Ich kann nicht mehr als 2 Bilder aufeinmal senden.")
                                    return

                                if len(attachments) <= 5 or len(stickers) > 0:
                                    await send_image(message, None, member)
                                    return

                            # Sticker gesendet
                            if len(stickers) > 0:
                                await send_sticker(message, None, member)
                                return

                            # Nachricht gesendet
                            else:
                                await send_message(message, None, member)
                                return

                    else:
                        return

    @app_commands.command(name="close", description="› Schließe das ModMail Ticket [Support - Team]")
    @app_commands.guild_only()
    async def close(self, interaction: discord.Interaction):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT rolleID FROM team WHERE guildID = (%s) AND level = (%s) OR guildID = (%s) AND level = (%s) OR guildID = (%s) AND level = (%s)",
                    (interaction.guild.id, 3, interaction.guild.id, 2, interaction.guild.id, 1))
                db_daten = await cur.fetchall()
                for daten in db_daten:
                    role = interaction.guild.get_role(int(daten[0]))
                    if role in interaction.user.roles:

                        await cur.execute("SELECT ticketID, authorID FROM tickets WHERE guildID = (%s)",
                                          interaction.guild.id)
                        db_daten2 = await cur.fetchall()
                        print(db_daten2)
                        if db_daten2:
                            for daten2 in db_daten2:
                                if int(daten2[0]) == interaction.channel.id:
                                    member = interaction.guild.get_member(daten2[1])

                                    dmembed = discord.Embed(
                                        description=f'› `🔒` | Das Ticket wurde **geschlossen**!!\n\n'
                                                    f'> Möchtest du noch ein Support-Feedback abgeben?\n'
                                                    f'> Klicke unten auf einen Button. (5 gut - 1 schlecht)',
                                        color=discord.Colour.red(),
                                        timestamp=datetime.now())
                                    dmembed.set_footer(text=f"{interaction.guild.name}")
                                    if interaction.guild.icon is not None:
                                        dmembed.set_author(name="Ticket geschlossen",
                                                           icon_url=interaction.guild.icon.url)
                                    if interaction.guild.icon is None:
                                        dmembed.set_author(name="Ticket geschlossen",
                                                           icon_url=interaction.user.display_avatar.url)
                                    await cur.execute(
                                        "SELECT closed_tickets FROM team_tickets WHERE guildID = (%s) AND userID = (%s)",
                                        (interaction.guild.id, interaction.user.id))
                                    db_daten3 = await cur.fetchall()
                                    if db_daten3 == ():
                                        await cur.execute(
                                            "INSERT INTO team_tickets(guildID, userID, closed_tickets) VALUES(%s, %s, %s)",
                                            (interaction.guild.id, interaction.user.id, 1))
                                    if db_daten3:
                                        for daten3 in db_daten3:
                                            closed_ticket_db = daten3[0]
                                            closed_tickets = closed_ticket_db + 1
                                            await cur.execute(
                                                "UPDATE team_tickets SET closed_tickets = (%s) WHERE userID = (%s) AND guildID = (%s)",
                                                (int(closed_tickets), interaction.user.id, interaction.guild.id))

                                        await interaction.response.send_message(
                                            "› <:DeadShotHacken:1034554637845532692> | Das Ticket wurde erfolgreich geschlossen.")
                                        await cur.execute(
                                            "DELETE FROM tickets WHERE authorID = (%s) AND guildID = (%s)",
                                            (member.id, interaction.guild.id))
                                        await interaction.channel.edit(name=f"Closed ({member.id})", archived=True,
                                                                       locked=True)
                                        await logging(interaction, f"Ticket geschlossen",
                                                      interaction.user.display_avatar.url,
                                                      f"› Das Ticket {interaction.channel.mention} wurde geschlossen",
                                                      discord.Colour.red(), f"Geschlossen von: {interaction.user}")

                                        try:
                                            view = feedback_buttons(interaction.guild.id, interaction.guild.name, 60)
                                            view.message = await member.send(embed=dmembed, view=view)
                                            return
                                        except:
                                            pass

                        elif db_daten2 == ():
                            embed = discord.Embed(description="› `❌` | Das ist kein ModMail Ticket.",
                                                  color=discord.Colour.red(),
                                                  timestamp=datetime.now())
                            embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
                            await interaction.response.send_message(embed=embed, ephemeral=True)
                            return


                else:
                    error_embed = discord.Embed(description=f"› `❌` | Dir fehlt eine Rolle der Stufe 3.",
                                                color=discord.Colour.red(),
                                                timestamp=datetime.now())
                    error_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
                    await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @app_commands.command(name="kontakt", description="› Kontaktiere als Teammitglied einen Nutzer. [Support - Team]")
    @app_commands.guild_only()
    async def kontakt(self, interaction: discord.Interaction, member: discord.Member):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT rolleID FROM team WHERE guildID = (%s) AND level = (%s)", (interaction.guild.id, 1))
                db_daten = await cur.fetchall()
                for daten in db_daten:
                    role = interaction.guild.get_role(int(daten[0]))
                    if role in interaction.user.roles:
                        await cur.execute("SELECT guildID, ticketID FROM tickets WHERE authorID = (%s)",
                                          int(member.id))
                        ticket_daten = await cur.fetchone()
                        if ticket_daten is not None:
                            await interaction.response.send_message("Bereits ein Ticket offen")
                            return
                        await cur.execute("SELECT pingrolle, modmail_kanal FROM setup WHERE guildID = (%s)", interaction.guild.id)
                        db_daten = await cur.fetchone()
                        if db_daten is not None:
                            channel = interaction.guild.get_channel(db_daten[1])
                            team_role = interaction.guild.get_role(db_daten[0])

                            member = interaction.guild.get_member(member.id)
                            role = ", ".join([r.mention for r in member.roles][:20])

                            await cur.execute("SELECT anzahl FROM user_tickets WHERE guildID = (%s) AND userID = (%s)", (interaction.guild.id, member.id))
                            db_daten2 = await cur.fetchall()
                            if db_daten2 == ():
                                await cur.execute("INSERT INTO user_tickets(guildID, userID, anzahl) VALUES(%s, %s, %s)", (int(interaction.guild.id), int(member.id), 1))
                                tickets_2 = " Kein geöffnetes Ticket."
                            if db_daten2:
                                for daten2 in db_daten2:
                                    closed_ticket_db = daten2[0]
                                    closed_tickets = closed_ticket_db + 1
                                    await cur.execute("UPDATE user_tickets SET anzahl = (%s) WHERE userID = (%s) AND guildID = (%s)", (int(closed_tickets), member.id, interaction.guild.id))
                                    tickets_2 = f"Mit {closed_ticket_db} geöffneten Tickets."
                            kanal_embed = discord.Embed(
                                description=f"Ersteller: {member.mention} (`{member.id}`)\n"
                                            f"Account erstellt vor: **{(discord.utils.utcnow() - interaction.user.created_at).days} Tagen**."
                                            f"{tickets_2}",
                                timestamp=datetime.now(),
                                color=discord.Colour.dark_blue())
                            kanal_embed.add_field(name="Rollen:", value=role, inline=False)
                            kanal_embed.set_author(name="Neues Ticket erstellt",
                                                   icon_url=member.display_avatar.url)
                            first_msg = await channel.send(f"{team_role.mention}", embed=kanal_embed)
                            ticket_channel = await first_msg.create_thread(name=f"{interaction.user.id}",
                                                                           auto_archive_duration=1440, slowmode_delay=2)
                            await cur.execute("SELECT * FROM tickets WHERE guildID = (%s) AND authorID = (%s)", (interaction.guild.id, member.id))
                            db_daten3 = await cur.fetchone()
                            if db_daten3 is None:
                                await cur.execute("INSERT INTO tickets(guildID, ticketID, authorID, ticket_grund) VALUES(%s, %s, %s, %s)", (interaction.guild.id, ticket_channel.id, member.id, None))

                            memberembed = discord.Embed(description=f"{interaction.user.mention} hat dich kontaktiert.",
                                                        title="Ticket geöffnet",
                                                        color=0x0f76da)
                            memberembed.set_author(name=interaction.user.name, icon_url=interaction.user.display_avatar)
                            memberembed.set_footer(text=f"Ticket geöffnet am {datetime.now().strftime('%d.%m.%Y')}")
                            await member.send(embed=memberembed)
                            await interaction.response.send_message(f"› <:DeadShotHacken:1034554637845532692> | Ticket wurde erfolgreich geöffnet. ({ticket_channel.mention})")
                            return

                    else:
                        error_embed = discord.Embed(description=f"› `❌` | Dir fehlt eine Rolle der Stufe 1.",
                                                    color=discord.Colour.red(),
                                                    timestamp=datetime.now())
                        error_embed.set_author(name=interaction.user, icon_url=interaction.user.display_avatar.url)
                        await interaction.response.send_message(embed=error_embed, ephemeral=True)



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ModMail(bot))
