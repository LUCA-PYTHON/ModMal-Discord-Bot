import asyncio
from datetime import datetime
import discord
import psutil
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands

class Button_Fuehrung(discord.ui.View):
    def __init__(self, author_id):
        super().__init__()

        self.author_id = author_id

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji="<:DeadShotZurck:1037760360276574228>", custom_id="zurueck")
    async def zurueck(self, i: discord.Interaction, button: discord.ui.button):
        if self.author_id == i.user.id:
            async with i.client.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT prefix FROM prefixes WHERE guildID = (%s)", i.guild.id)
                    db_daten = await cur.fetchone()
                    if db_daten is not None:
                        prefix = db_daten[0]

                    if db_daten is None:
                        prefix = "!"

                    for item in self.children:
                        if item.custom_id == "counter":
                            button_counter = item.label.split("/5")
                            counter = int(button_counter[0]) - 1
                            item.label = f"{str(counter)}/5"

                            if int(counter) <= -1:
                                view = DropdownView(self.author_id)

                                embed = discord.Embed(description=f"Das hier ist das Hilfe Menü. Mit dem Dropdown "
                                                                  f"Menü unten kannst du die einzelnen Kategorien auswählen. Bei weiterne"
                                                                  f" Fragen trette einfach dem __[Support Server](https://discord.gg/wGFzPk45hr  \"Betrete den Support Server\")__ bei!\n\n"
                                                                  f"**Hilfe Menüs**\n\n"
                                                                  f"> <:DeadShotHelp:1037756726704881685> **Bot - Führung** - Eine Erklärung der wichtigsten Befehle\n"
                                                                  f"> \n"
                                                                  f"> <:DeadShotMod:914516537057116160>  **Team Befehle** - Eine Liste von allen Team Befehlen.\n"
                                                                  f"> \n"
                                                                  f"> <:DeadShotSettings:1034191404487954442> **Einstellungs Befehle** - Eine Aufzählung aller Einstellungs Befehlen.\n"
                                                                  f"> \n"
                                                                  f"> <:DeadShotInfos:1034196978013319228> **Informations Befehle** - Eine Auslistung aller Informations Befehlen.",
                                                      timestamp=datetime.now(),
                                                      color=0x3357ca)
                                embed.set_author(name=f"{i.message.author.name} Hilfe Menü", icon_url=i.message.author.avatar.url)
                                embed.set_footer(text=f"Author ID: {i.user.id}")
                                embed.set_image(url="https://cdn.discordapp.com/attachments/909501269759127602/1034464798349467738/Modmail-bot_Hilfe.jpg")
                                await i.response.edit_message(embed=embed, view=view)

                            if int(counter) == int(0):
                                embed = discord.Embed(
                                    description=f"Hier findest du die Führung durch den ModMail Bot. Es werden dir die wichtigsten Befehle erklärt.\n⠀",
                                    timestamp=datetime.now(),
                                    color=0x3357ca)
                                embed.set_author(name=f"{i.message.author.name} Team Befehle", icon_url=i.message.author.avatar.url)
                                embed.set_footer(text=f"Author ID: {i.user.id}")
                                embed.set_image(url="https://cdn.discordapp.com/attachments/909501269759127602/1034464798349467738/Modmail-bot_Hilfe.jpg")
                                embed.add_field(name="Syntax Erklärung:", value="<> = Feld ist Otional\n"
                                                                                "[] = Feld ist Plicht")
                                embed.add_field(name="Befehl Erklärung", value=f'Prefix: "/"\n'
                                                                               f'Snippet-Prefix: "{prefix}"\n')
                                await i.response.edit_message(embed=embed, view=self)

                            if int(counter) == int(1):
                                embed = discord.Embed(
                                    description=f"Damit die ModMail funktioniert benötigen wir wichtige ModMail Daten, wie zum Beispiel den ModMail Kanal oder die Pingrolle.\n\n"
                                                f"> › Nutze dazu einfach den Befehl:\n"
                                                f"> `setup start [log_kanal] [pingrolle] [modmail_kanal]`\n\n"
                                                f"> › Zum editieren des Setups nutz den Befehl:\n"
                                                f"> `setup edit [log_kanal] [pingrolle] [modmail_kanal]`\n\n"
                                                f"> › Und zum löschen der ModMail daten nutzt einfach:\n"
                                                f"> `setup delete`\n\n"
                                                f"> › Du kannst dir die ModMail daten jeder Zeit anschauen mit:\n"
                                                f"> `setup show`",
                                    timestamp=datetime.now(),
                                    color=0x3357ca)
                                embed.set_author(name=f"Einrichten der ModMail", icon_url=i.message.author.avatar.url)
                                embed.set_footer(text=f"Author ID: {i.user.id}")
                                embed.set_image(url="https://cdn.discordapp.com/attachments/909501269759127602/1034464798349467738/Modmail-bot_Hilfe.jpg")
                                await i.response.edit_message(embed=embed, view=self)

                            if int(counter) == int(2):
                                embed = discord.Embed(
                                    description=f"Damit du und dein Serverteam alles Problemlos nutzen könnt benötigt der Bot Teamrollen der Stufe 1 (hoch) - 3 (niedrig), damit man mit einer höheren Rolle mehr Befehle nutzen kann.\n\n"
                                                f"> › Zum hinzufügen einer Teamrolle nutzt du den Befehl:\n"
                                                f"> `team add [rolle] [level]`\n\n"
                                                f"> › Um eine Teamrolle zu editieren nutz:\n"
                                                f"> `team edit [rolle] [level]`\n\n"
                                                f"> › Und um eine Teamrolle zu löschen nutz den befehl:\n"
                                                f"> `team delete [rolle]`\n\n"
                                                f"> › Schau dir alle Teamrollen an mit:\n"
                                                f"> `team show` oder `serverinfo`",
                                    timestamp=datetime.now(),
                                    color=0x3357ca)
                                embed.set_author(name=f"Teamrollen einrichten", icon_url=i.message.author.avatar.url)
                                embed.set_footer(text=f"Author ID: {i.user.id}")
                                embed.set_image(url="https://cdn.discordapp.com/attachments/909501269759127602/1034464798349467738/Modmail-bot_Hilfe.jpg")
                                await i.response.edit_message(embed=embed, view=self)

                            if int(counter) == int(3):
                                embed = discord.Embed(
                                    description=f"Um den Ticket Support so schnell und einfach wie möglich zu machen, kannst du Snippet erstellen.\n\n"
                                                f"> › Zum erstellen eines Snippet nutzt:\n"
                                                f"> `snippet add [name] [description]`\n\n"
                                                f"> › Zum editieren von SNippets nutzt:\n"
                                                f"> `snippet edit [name] [new_des]`\n\n"
                                                f"> › Um ein Snippet zu löschen nutz einfach:\n"
                                                f"> `snippet delete [name]`\n\n"
                                                f"> › Schau dir deine Snippet jeder Zeit an mit:\n"
                                                f"> `snippet show <name>`",
                                    timestamp=datetime.now(),
                                    color=0x3357ca)
                                embed.set_author(name=f"Snippet-Befehle einrichten", icon_url=i.message.author.avatar.url)
                                embed.set_footer(text=f"Author ID: {i.user.id}")
                                embed.set_image(url="https://cdn.discordapp.com/attachments/909501269759127602/1034464798349467738/Modmail-bot_Hilfe.jpg")
                                await i.response.edit_message(embed=embed, view=self)

                            if int(counter) == int(4):
                                weiter = [x for x in self.children if x.custom_id == "weiter"][0]
                                weiter.disabled = False
                                embed = discord.Embed(
                                    description=f"Damit du deine das Prefix für deine Snippet jeder Zeit ändern kannst, gibt es folgende Befehle.\n\n"
                                                f"> › Zum ändern des Prefixes nutz den befehl:\n"
                                                f"> `prefix set [prefix]`\n\n"
                                                f"> › Zum zurücksetzen des Prefixes nutz einfach:\n"
                                                f"> `prefix delete`\n\n"
                                                f"> › Lass dir dein Prefix jeder Zeit anzeigen mit:\n"
                                                f"> `prefix show`",
                                    timestamp=datetime.now(),
                                    color=0x3357ca)
                                embed.set_author(name=f"Prefix ändern", icon_url=i.message.author.avatar.url)
                                embed.set_footer(text=f"Author ID: {i.user.id}")
                                embed.set_image(url="https://cdn.discordapp.com/attachments/909501269759127602/1034464798349467738/Modmail-bot_Hilfe.jpg")
                                await i.response.edit_message(embed=embed, view=self)

                            if int(counter) == int(5):
                                embed = discord.Embed(
                                    description=f"Um den ModMail Support moderieren zu können, kannst du Leute auch blockieren.\n\n"
                                                f"> › Zum blockieren eines Nutzer, nutze den Befehl:\n"
                                                f"> `block [user] <grund>`\n\n"
                                                f"> › Zum entblockieren eines Nutzers nutz:\n"
                                                f"> `unblock [user]`\n\n"
                                                f"> › Schau dir alle blockierten Nutzer an mit:\n"
                                                f"> `blocked`",
                                    timestamp=datetime.now(),
                                    color=0x3357ca)
                                embed.set_author(name=f"Nutzer blockieren", icon_url=i.message.author.avatar.url)
                                embed.set_footer(text=f"Author ID: {i.user.id}")
                                embed.set_image(url="https://cdn.discordapp.com/attachments/909501269759127602/1034464798349467738/Modmail-bot_Hilfe.jpg")
                                await i.response.edit_message(embed=embed, view=self)
        else:
            error_embed = discord.Embed(
                description=f"› Das ist nicht deine Nachricht.",
                color=discord.Colour.red(),
                timestamp=datetime.now())
            error_embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
            error_embed.set_footer(text="Nutze /help für mehr Hilfe")
            await i.response.send_message(embed=error_embed, ephemeral=True)

    @discord.ui.button(style=discord.ButtonStyle.grey, label="0/5", custom_id="counter", disabled=True)
    async def counter(self, i: discord.Interaction, button: discord.ui.button):
        pass

    @discord.ui.button(style=discord.ButtonStyle.gray, emoji="<:DeadShotweiter:1037791915422253128>", custom_id="weiter")
    async def weiter(self, i: discord.Interaction, button: discord.ui.button):
        if self.author_id == i.user.id:
            for item in self.children:
                if item.custom_id == "counter":
                    button_counter = item.label.split("/5")
                    counter = int(button_counter[0]) + 1
                    item.label = f"{str(counter)}/5"

                    if int(counter) == int(1):
                        embed = discord.Embed(
                            description=f"Damit die ModMail funktioniert benötigen wir wichtige ModMail Daten, wie zum Beispiel den ModMail Kanal oder die Pingrolle.\n\n"
                                        f"> › Nutze dazu einfach den Befehl:\n"
                                        f"> `setup start [log_kanal] [pingrolle] [modmail_kanal]`\n\n"
                                        f"> › Zum editieren des Setups nutz den Befehl:\n"
                                        f"> `setup edit [log_kanal] [pingrolle] [modmail_kanal]`\n\n"
                                        f"> › Und zum löschen der ModMail daten nutzt einfach:\n"
                                        f"> `setup delete`\n\n"
                                        f"> › Du kannst dir die ModMail Daten jeder Zeit anschauen mit:\n"
                                        f"> `setup show`",
                            timestamp=datetime.now(),
                            color=0x3357ca)
                        embed.set_author(name=f"Einrichten der ModMail", icon_url=i.message.author.avatar.url)
                        embed.set_footer(text=f"Author ID: {i.user.id}")
                        embed.set_image(url="https://cdn.discordapp.com/attachments/909501269759127602/1034464798349467738/Modmail-bot_Hilfe.jpg")
                        await i.response.edit_message(embed=embed, view=self)

                    if int(counter) == int(2):
                        embed = discord.Embed(
                            description=f"Damit du und dein Serverteam alles Problemlos nutzen könnt benötigt der Bot Teamrollen der Stufe 1 (hoch) - 3 (niedrig), damit man mit einer höheren Rolle mehr Befehle nutzen kann.\n\n"
                                        f"> › Zum hinzufügen einer Teamrolle nutzt du den Befehl:\n"
                                        f"> `team add [rolle] [level]`\n\n"
                                        f"> › Um eine Teamrolle zu editieren nutz:\n"
                                        f"> `team edit [rolle] [level]`\n\n"
                                        f"> › Und um eine Teamrolle zu löschen nutz den befehl:\n"
                                        f"> `team delete [rolle]`\n\n"
                                        f"> › Schau dir alle Teamrollen an mit:\n"
                                        f"> `team show` oder `serverinfo`",
                            timestamp=datetime.now(),
                            color=0x3357ca)
                        embed.set_author(name=f"Teamrollen einrichten", icon_url=i.message.author.avatar.url)
                        embed.set_footer(text=f"Author ID: {i.user.id}")
                        embed.set_image(url="https://cdn.discordapp.com/attachments/909501269759127602/1034464798349467738/Modmail-bot_Hilfe.jpg")
                        await i.response.edit_message(embed=embed, view=self)

                    if int(counter) == int(3):
                        embed = discord.Embed(
                            description=f"Um den Ticket Support so schnell und einfach wie möglich zu machen, kannst du Snippet erstellen.\n\n"
                                        f"> › Zum erstellen eines Snippet nutzt:\n"
                                        f"> `snippet add [name] [description]`\n\n"
                                        f"> › Zum editieren von SNippets nutzt:\n"
                                        f"> `snippet edit [name] [new_des]`\n\n"
                                        f"> › Um ein Snippet zu löschen nutz einfach:\n"
                                        f"> `snippet delete [name]`\n\n"
                                        f"> › Schau dir deine Snippet jeder Zeit an mit:\n"
                                        f"> `snippet show <name>`",
                            timestamp=datetime.now(),
                            color=0x3357ca)
                        embed.set_author(name=f"Snippet-Befehle einrichten", icon_url=i.message.author.avatar.url)
                        embed.set_footer(text=f"Author ID: {i.user.id}")
                        embed.set_image(url="https://cdn.discordapp.com/attachments/909501269759127602/1034464798349467738/Modmail-bot_Hilfe.jpg")
                        await i.response.edit_message(embed=embed, view=self)

                    if int(counter) == int(4):
                        embed = discord.Embed(
                            description=f"Damit du deine das Prefix für deine Snippet jeder Zeit ändern kannst, gibt es folgende Befehle.\n\n"
                                        f"> › Zum ändern des Prefixes nutz den befehl:\n"
                                        f"> `prefix set [prefix]`\n\n"
                                        f"> › Zum zurücksetzen des Prefixes nutz einfach:\n"
                                        f"> `prefix delete`\n\n"
                                        f"> › Lass dir dein Prefix jeder Zeit anzeigen mit:\n"
                                        f"> `prefix show`",
                            timestamp=datetime.now(),
                            color=0x3357ca)
                        embed.set_author(name=f"Prefix ändern", icon_url=i.message.author.avatar.url)
                        embed.set_footer(text=f"Author ID: {i.user.id}")
                        embed.set_image(url="https://cdn.discordapp.com/attachments/909501269759127602/1034464798349467738/Modmail-bot_Hilfe.jpg")
                        await i.response.edit_message(embed=embed, view=self)

                    if int(counter) == int(5):
                        button.disabled = True
                        embed = discord.Embed(
                            description=f"Um den ModMail Support moderieren zu können, kannst du Leute auch blockieren.\n\n"
                                        f"> › Zum blockieren eines Nutzer, nutze den Befehl:\n"
                                        f"> `block [user] <grund>`\n\n"
                                        f"> › Zum entblockieren eines Nutzers nutz:\n"
                                        f"> `unblock [user]`\n\n"
                                        f"> › Schau dir alle blockierten Nutzer an mit:\n"
                                        f"> `blocked`",
                            timestamp=datetime.now(),
                            color=0x3357ca)
                        embed.set_author(name=f"Nutzer blockieren", icon_url=i.message.author.avatar.url)
                        embed.set_footer(text=f"Author ID: {i.user.id}")
                        embed.set_image(url="https://cdn.discordapp.com/attachments/909501269759127602/1034464798349467738/Modmail-bot_Hilfe.jpg")
                        await i.response.edit_message(embed=embed, view=self)

        else:
            error_embed = discord.Embed(
                description=f"› Das ist nicht deine Nachricht.",
                color=discord.Colour.red(),
                timestamp=datetime.now())
            error_embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
            error_embed.set_footer(text="Nutze /help für mehr Hilfe")
            await i.response.send_message(embed=error_embed, ephemeral=True)

class Button(discord.ui.View):
    def __init__(self, author_id):
        super().__init__()

        self.author_id = author_id

        self.add_item(discord.ui.Button(label="Support Server", url="https://discord.gg/wGFzPk45hr"))
        self.add_item(discord.ui.Button(label="Invite mich", url=discord.utils.oauth_url(909496854734057514)))

    @discord.ui.button(style=discord.ButtonStyle.red, label="Haupseite", emoji="🏠", custom_id="button")
    async def callback(self, interaction: discord.Interaction, button: discord.ui.button()):
        if self.author_id == interaction.user.id:

            view = DropdownView(self.author_id)

            embed = discord.Embed(description=f"Das hier ist das Hilfe Menü. Mit dem Dropdown "
                                              f"Menü unten kannst du die einzelnen Kategorien auswählen. Bei weiterne"
                                              f" Fragen trette einfach dem __[Support Server](https://discord.gg/wGFzPk45hr)__ bei!\n\n"
                                              f"**Hilfe Menüs**\n\n"
                                              f"> <:DeadShotHelp:1037756726704881685> **Bot - Führung** - Eine Erklärung der wichtigsten Befehle\n"
                                              f"> \n"
                                              f"> <:DeadShotMod:914516537057116160>  **Team Befehle** - Eine Liste von allen Team Befehlen.\n"
                                              f"> \n"
                                              f"> <:DeadShotSettings:1034191404487954442> **Einstellungs Befehle** - Eine Aufzählung aller Einstellungs Befehlen.\n"
                                              f"> \n"
                                              f"> <:DeadShotInfos:1034196978013319228> **Informations Befehle** - Eine Auslistung aller Informations Befehlen.",
                                  timestamp=datetime.now(),
                                  color=0x3357ca)
            embed.set_author(name=f"{interaction.message.author.name} Hilfe Menü", icon_url=interaction.message.author.avatar.url)
            embed.set_footer(text=f"Author ID: {interaction.user.id}")
            embed.set_image(
                url="https://cdn.discordapp.com/attachments/909501269759127602/1034464798349467738/Modmail-bot_Hilfe.jpg")
            await interaction.response.edit_message(embed=embed, view=view)

        else:
            error_embed = discord.Embed(
                description=f"› Das ist nicht deine Nachricht.",
                color=discord.Colour.red(),
                timestamp=datetime.now())
            error_embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
            error_embed.set_footer(text="Nutze /help für mehr Hilfe")
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception, item: [str], /) -> None:
        await interaction.response.send_message(content=f"› `❌` | Unerwarteter Error: {error}/{item}")

class Dropdown(discord.ui.Select):
    def __init__(self, author_id):

        self.author_id = author_id

        options = [
            discord.SelectOption(label="Bot - Führung", emoji="<:DeadShotHelp:1037756726704881685>", value="führung"),
            discord.SelectOption(label="Team Befehle", emoji="<:DeadShotMod:914516537057116160>", value="1"),
            discord.SelectOption(label="Einstellungs Befehle", emoji="<:DeadShotSettings:1034191404487954442>", value="2"),
            discord.SelectOption(label="Informations Befehle", emoji="<:DeadShotInfos:1034196978013319228>", value="3"),
            discord.SelectOption(label="Löschen", emoji="<:DeadShotDelete:1034205579297702028>", value="4")
            ]

        super().__init__(
            placeholder="Triff eine Auswahl",
            min_values=1,
            max_values=1,
            options=options,
            disabled=False,
        )

    async def callback(self, interaction: discord.Interaction):
        if self.author_id == interaction.user.id:
            async with interaction.client.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT prefix FROM prefixes WHERE guildID = (%s)", interaction.guild.id)
                    db_daten = await cur.fetchone()
                    if db_daten is not None:
                        prefix = db_daten[0]

                    if db_daten is None:
                        prefix = "!"

                    if self.values[0] == "führung":

                        embed = discord.Embed(
                            description=f"Hier findest du die Führung durch den ModMail Bot. Es werden dir die wichtigsten Befehle erklärt.\n⠀",
                            timestamp=datetime.now(),
                            color=0x3357ca)
                        embed.set_author(name=f"{interaction.message.author.name} Team Befehle", icon_url=interaction.message.author.avatar.url)
                        embed.set_footer(text=f"Author ID: {interaction.user.id}")
                        embed.set_image(url="https://cdn.discordapp.com/attachments/909501269759127602/1034464798349467738/Modmail-bot_Hilfe.jpg")
                        embed.add_field(name="Syntax Erklärung:", value="<> = Feld ist Otional\n"
                                                                        "[] = Feld ist Plicht")
                        embed.add_field(name="Befehl Erklärung", value=f'Prefix: "/"\n'
                                                                       f'Snippet-Prefix: "{prefix}"\n')
                        view = Button_Fuehrung(self.author_id)
                        await interaction.response.edit_message(embed=embed, view=view)

                    if self.values[0] == "1":

                        embed = discord.Embed(description=f"Hier findest du alle Team Befehle die du auf Discord Nutzen kannst um das Serverteam einzustellen.\n",
                                              timestamp=datetime.now(),
                                              color=0x3357ca)
                        embed.add_field(name="Team Befehle",
                                        value=f"> `team add    ` Füge eine Teamrolle hinzu\n"
                                              f"> `team edit   ` Editiere eine Teamrolle\n"
                                              f"> `team delete ` Lösche eine Teamrolle\n"
                                              f"> `team show   ` Zeigt dir alle Teamrollen\n"
                                              f"⠀",
                                        inline=False)
                        embed.add_field(name="Moderation Befehle",
                                        value=f"> `block       ` Blockiere einen Nutzer von der ModMail\n"
                                              f"> `unblock     ` Entblockiere einen Nutzer von der ModMail\n"
                                              f"> `blocked     ` Zeigt dir alle blockierten Nutzer\n"
                                              f"> `close       ` Schließe ein ModMail Ticket",
                                        inline=False)
                        embed.set_author(name=f"{interaction.message.author.name} Team Befehle", icon_url=interaction.message.author.avatar.url)
                        embed.set_footer(text=f"Author ID: {interaction.user.id}")
                        embed.set_image(url="https://cdn.discordapp.com/attachments/909501269759127602/1034465689546801192/Modmail-bot_Hilfe_1.jpg")
                        await interaction.response.edit_message(embed=embed, view=Button(self.author_id))

                    if self.values[0] == "2":
                        embed = discord.Embed(
                            description=f"Hier findest du alle Einstellungs Befehle zum einstellen der ModMail auf deinem Server.\n",
                            timestamp=datetime.now(),
                            color=0x3357ca)
                        embed.add_field(name="Snippet Befehle",
                                        value=f"> `snippet add    ` Füge eine Snippet hinzu\n"
                                              f"> `snippet edit   ` Editiere eine Snippet\n"
                                              f"> `snippet delete ` Lösche eine Snippet\n"
                                              f"> `snippet show   ` Zeigt dir alle Snippets\n"
                                              f"⠀",
                                        inline=False)
                        embed.add_field(name="Settings Befehle",
                                        value=f"> `setup start    ` Starte das ModMail - Setup\n"
                                              f"> `setup edit     ` Editiere die ModMail Daten\n"
                                              f"> `setup delete   ` Lösche die ModMail Daten\n"
                                              f"⠀",
                                        inline=False)
                        embed.add_field(name="Autotag Befehle",
                                        value=f"> `autotag start  ` Füge ein Autotag hinzu\n"
                                              f"> `autotag edit   ` Editiere ein Autotag\n"
                                              f"> `autotag delete ` Lösche ein Autotag\n"
                                              f"> `autotag show   ` Zeigt dir alle Autotags\n"
                                              f"⠀",
                                        inline=False)
                        embed.add_field(name="Prefix Befehle",
                                        value=f"> `prefix set     ` Füge/Editiere das Prefix hinzu\n"
                                              f"> `prefix delete  ` Lösche das Prefix\n"
                                              f"> `prefix show    ` Zeigt dir das prefix an",
                                        inline=False)
                        embed.set_author(name=f"{interaction.message.author.name} Team Befehle",
                                         icon_url=interaction.message.author.avatar.url)
                        embed.set_footer(text=f"Author ID: {interaction.user.id}")
                        embed.set_image(url="https://cdn.discordapp.com/attachments/909501269759127602/1034465689894912100/Modmail-bot_Hilfe_2.jpg")
                        await interaction.response.edit_message(embed=embed, view=Button(self.author_id))

                    if self.values[0] == "3":
                        embed = discord.Embed(
                            description=f"Hier findest du alle Informations Befehle zum anschauen der Informationen über Server/User/Tickets.\n",
                            timestamp=datetime.now(),
                            color=0x3357ca)
                        embed.add_field(name="Info Befehle",
                                        value=f"> `ticket_info  ` Zeigt dir alle Infos über ein Ticket\n"
                                              f"> `teaminfo     ` Zeigt dir alle Infos über ein Teamler\n"
                                              f"> `serverinfo   ` Zeigt dir alle Infos über einen Server\n"
                                              f"> `about        ` Zeigt dir alle Infos über den Bot\n"
                                              f"> `bestenliste  ` Zeigt dir die Top 10 Nutzer/Server",
                                        inline=False)
                        embed.set_author(name=f"{interaction.message.author.name} Team Befehle",
                                         icon_url=interaction.message.author.avatar.url)
                        embed.set_footer(text=f"Author ID: {interaction.user.id}")
                        embed.set_image(url="https://cdn.discordapp.com/attachments/909501269759127602/1034465690129797230/Modmail-bot_Hilfe_3.jpg")
                        await interaction.response.edit_message(embed=embed, view=Button(self.author_id))

                    if self.values[0] == "4":
                        await asyncio.sleep(1)
                        await interaction.message.delete()

        else:
            error_embed = discord.Embed(
                description=f"› Das ist nicht deine Nachricht.",
                color=discord.Colour.red(),
                timestamp=datetime.now())
            error_embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
            error_embed.set_footer(text="Nutze /help für mehr Hilfe")
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

class DropdownView(discord.ui.View):
    def __init__(self, author_id):
        super().__init__()
        self.add_item(Dropdown(author_id))


class info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.block_counter = 0

    async def cog_unload(self) -> None:
        return await super().cog_unload()

    ############################################################################################

    #██╗███╗   ██╗███████╗ ██████╗ ██████╗ ███╗   ███╗ █████╗ ████████╗██╗ ██████╗ ███╗   ██╗███████╗███╗   ██╗
    #██║████╗  ██║██╔════╝██╔═══██╗██╔══██╗████╗ ████║██╔══██╗╚══██╔══╝██║██╔═══██╗████╗  ██║██╔════╝████╗  ██║
    #██║██╔██╗ ██║█████╗  ██║   ██║██████╔╝██╔████╔██║███████║   ██║   ██║██║   ██║██╔██╗ ██║█████╗  ██╔██╗ ██║
    #██║██║╚██╗██║██╔══╝  ██║   ██║██╔══██╗██║╚██╔╝██║██╔══██║   ██║   ██║██║   ██║██║╚██╗██║██╔══╝  ██║╚██╗██║
    #██║██║ ╚████║██║     ╚██████╔╝██║  ██║██║ ╚═╝ ██║██║  ██║   ██║   ██║╚██████╔╝██║ ╚████║███████╗██║ ╚████║
    #╚═╝╚═╝  ╚═══╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═══╝

    ############################################################################################

    @app_commands.command(name="ticketinfo", description="› Zeigt dir wichtige Informationen zu einem Ticket.")
    @app_commands.guild_only()
    @app_commands.describe(ticket="› Ticket, überwelches dir Informationen angezeigt werden.")
    async def ticket_info(self, interaction: discord.Interaction, ticket: discord.Thread):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT rolleID FROM team WHERE guildID = (%s) AND level = (%s) OR guildID = (%s) AND level = (%s) OR guildID = (%s) AND level = (%s)", (interaction.guild.id, 3, interaction.guild.id, 2, interaction.guild.id, 1))
                db_daten = await cur.fetchall()
                for daten in db_daten:
                    role = interaction.guild.get_role(int(daten[0]))
                    if role in interaction.user.roles:

                        try:
                            ersteller = interaction.guild.get_member(int(ticket.name))

                        except:
                            error_embed = discord.Embed(
                                description=f"› Das ist kein/ein geschlossenes ModMail Ticket.",
                                color=discord.Colour.red(),
                                timestamp=datetime.now())
                            error_embed.set_author(name="Fehlermeldung",
                                                   icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                            await interaction.response.send_message(embed=error_embed, ephemeral=True)
                            return

                        await cur.execute("SELECT ticket_grund FROM tickets WHERE guildID = (%s) AND authorID = (%s)", (interaction.guild.id, ersteller.id))
                        grund_daten = await cur.fetchone()
                        if grund_daten is not None:
                            ticket_grund = grund_daten[0]

                        await cur.execute("SELECT anzahl FROM user_tickets WHERE guildID = (%s) AND userID = (%s)", (interaction.guild.id, ersteller.id))
                        db_daten2 = await cur.fetchall()
                        if db_daten2 == ():
                            ticket_count = 0
                        for daten2 in db_daten2:
                            daten_anzahl = daten2[0]
                            ticket_count = daten_anzahl

                        msg_count = 0
                        async for msg in ticket.history(limit=None):
                            msg_count += 1

                        embed = discord.Embed(description=f"Alle *Informationen* zu {ticket.mention}",
                                              timestamp=datetime.now(),
                                              color=0x4c69f8)
                        embed.add_field(name="Ticket ID", value=f"`{ticket.id}`", inline=False)
                        embed.add_field(name="Ticket Grund", value=ticket_grund, inline=False)
                        embed.add_field(name="Ticket Ersteller", value=ersteller.mention, inline=False)
                        embed.add_field(name="Geöffnete Tickets", value=ticket_count, inline=False)
                        embed.add_field(name="Nachrichten", value=msg_count, inline=False)
                        embed.add_field(name=f"Erstelldatum", value=ticket.created_at.strftime('%d.%m.%Y'))
                        embed.set_footer(text=f"AuthorID: {interaction.user.id}")
                        embed.set_author(name="Ticket - Informationen", icon_url=interaction.user.display_avatar.url)
                        await interaction.response.send_message(embed=embed)
                        return

                else:
                    error_embed = discord.Embed(
                        description=f"› Dir fehlt eine Teamrolle der Stufe 3.",
                        color=discord.Colour.red(),
                        timestamp=datetime.now())
                    error_embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await interaction.response.send_message(embed=error_embed, ephemeral=True)

    @app_commands.command(name="teaminfo", description="› Zeigt dir Informationen über ein Teammitglied.")
    @app_commands.guild_only()
    @app_commands.describe(user="› Nutzer, über den ModMail Informationen angezeigt werden.")
    async def teaminfo(self, interaction: discord.Interaction, user: discord.Member = None):
        if user == None:
            user = interaction.user

        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT rolleID, level FROM team WHERE guildID = (%s)", interaction.guild.id)
                db_daten = await cur.fetchall()

                for daten2 in db_daten:
                    role = interaction.guild.get_role(int(daten2[0]))
                    if role in user.roles:

                        team_rollen = ""
                        for daten3 in db_daten:
                            role = interaction.guild.get_role(int(daten3[0]))
                            db_lvl = daten3[1]
                            if role in user.roles:
                                team_rollen += f"{role.mention} (*Level*: {db_lvl}),\n"

                        team_rl = team_rollen

                        timestamp = str(datetime.timestamp(user.joined_at)).split(".")
                        timestamp1 = timestamp[0]

                        await cur.execute("SELECT closed_tickets FROM team_tickets WHERE guildID = (%s) AND userID = (%s)", (interaction.guild.id, user.id))
                        db_daten = await cur.fetchall()
                        if db_daten == ():
                            db_ticket = "Keine Tickets geschlossen"

                        if db_daten:
                            for daten in db_daten:
                                db_ticket = daten[0]

                        embed = discord.Embed(description=f"Informationen für {user.mention}",
                                              timestamp=datetime.now(),
                                              color=0x4c69f8)
                        embed.set_author(name="Team Informationen", icon_url=user.display_avatar.url)
                        embed.set_footer(text=f"Author ID: {interaction.user.id}")
                        embed.add_field(name="Member seit:", value=f"<t:{timestamp1}:D>", inline=False)
                        embed.add_field(name="Geschlossene Tickets", value=db_ticket)
                        embed.add_field(name="Team Rollen", value=team_rl[:-2], inline=False)
                        await interaction.response.send_message(embed=embed)

                else:
                    embed = discord.Embed(
                        description=f"› {user.mention} hat keine Teamrolle/Teamrollen.",
                        color=discord.Colour.red(),
                        timestamp=datetime.now())
                    embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="serverinfo", description="› Zeigt dir Informationen über diesen Server.")
    @app_commands.guild_only()
    async def serverinfo(self, interaction: discord.Interaction):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT stand FROM setup WHERE guildID = (%s)", interaction.guild.id)
                db_daten = await cur.fetchone()
                if db_daten is not None:

                    await cur.execute("SELECT closed_tickets, userID FROM team_tickets WHERE guildID = (%s) ORDER BY closed_tickets DESC", interaction.guild.id)
                    db_daten2 = await cur.fetchone()
                    if db_daten2 is not None:
                        team_anzahl = f"{interaction.guild.get_member(db_daten2[1]).mention} Ticket: `{db_daten2[0]}`"

                    if db_daten2 is None:
                        team_anzahl = "Keine Daten vorhanden"

                    timestamp = str(datetime.timestamp(interaction.guild.created_at)).split(".")
                    timestamp1 = timestamp[0]

                    await cur.execute("SELECT rolleID, level FROM team WHERE guildID = (%s)", interaction.guild.id)
                    db_daten3 = await cur.fetchall()

                    if db_daten3:
                        rollen_anzahl = 0
                        team_rollen = ""
                        for daten3 in db_daten3:
                            rollen = interaction.guild.get_role(int(daten3[0]))
                            db_lvl = daten3[1]
                            rollen_anzahl += 1
                            team_rollen += f"{rollen.mention} (*Level*: {db_lvl}),\n"

                    if db_daten3 == ():
                        rollen_anzahl = 0
                        team_rollen = "Keine Daten vorhanden"

                    await cur.execute("SELECT prefix FROM prefixes WHERE guildID = (%s)", interaction.guild.id)
                    db_daten4 = await cur.fetchone()
                    if db_daten4 is not None:
                        prefix = db_daten4[0]

                    if db_daten4 is None:
                        prefix = "!"

                    await cur.execute("SELECT feedback FROM feedback WHERE guildID = (%s)", interaction.guild.id)
                    db_daten5 = await cur.fetchone()
                    if db_daten5 is not None:
                        feedback = f"{db_daten5[0]} ⭐"

                    if db_daten5 is None:
                        feedback = "Keine Daten vorhanden"

                    embed = discord.Embed(description=f"Informationen zu {interaction.guild.name}",
                                          timestamp=datetime.now(),
                                          color=0x4c69f8)
                    embed.set_footer(text=f"Author ID: {interaction.user.id}")
                    embed.set_author(name="Serverinformationen", icon_url=interaction.user.display_avatar.url)
                    if interaction.guild.icon is not None:
                        embed.set_thumbnail(url=interaction.guild.icon.url)
                    embed.add_field(name="Server Ersteller", value=f"{interaction.guild.owner.mention} (`{interaction.guild.owner.id}`)")
                    embed.add_field(name="Log Kanal", value=str(db_daten[0]), inline=False)
                    embed.add_field(name="Erstellt am", value=f"<t:{timestamp1}:D>", inline=False)
                    embed.add_field(name="Snippet-Prefix", value=f"Prefix: `{prefix}`", inline=False)
                    embed.add_field(name="Feedback", value=f"{feedback}", inline=False)
                    embed.add_field(name="Aktivstes Teammitglied", value=team_anzahl, inline=False)
                    embed.add_field(name=f"Teamrollen ({int(rollen_anzahl)} / 5)", value=team_rollen[:-2])
                    await interaction.response.send_message(embed=embed)

                if db_daten is None:
                    embed = discord.Embed(description=f"› {interaction.guild.name} hat das ModMail Setup nicht erledigt.",
                                          color=discord.Colour.red(),
                                          timestamp=datetime.now())
                    embed.set_author(name="Fehlermeldung", icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="about", description="› Zeigt dir Informationen zum Bot.")
    @app_commands.guild_only()
    async def about(self, interaction: discord.Interaction):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT closed_tickets FROM team_tickets")
                db_daten = await cur.fetchall()
                global_tickets = 0
                for daten in db_daten:
                    global_tickets += daten[0]

                timestamp = str(datetime.timestamp(self.bot.user.created_at)).split(".")
                timestamp1 = timestamp[0]

                entwickler = await self.bot.fetch_user(714361420409733171)

                embed = discord.Embed(description=f"Informationen über {self.bot.user.mention}",
                                      timestamp=datetime.now(),
                                      color=0x4c69f8)
                embed.set_author(name="Bot Informationen", icon_url=self.bot.user.avatar.url)
                embed.set_footer(text=f"Author ID: {interaction.user.id}")
                embed.add_field(name="Bot Entwickler", value=entwickler, inline=False)
                embed.add_field(name="Alle Server", value=len(self.bot.guilds), inline=False)
                embed.add_field(name="Globale Nutzer", value=len(self.bot.users), inline=False)
                embed.add_field(name="CPU Useage", value=f"{psutil.cpu_percent()}%")
                embed.add_field(name="Erstellt am", value=f"<t:{timestamp1}:D>", inline=False)
                embed.add_field(name="Globale Tickets", value=global_tickets, inline=False)
                await interaction.response.send_message(embed=embed)

    @app_commands.command(name="bestenliste", description="› Zeigt dir die Top 10 Server/Nutzer an.")
    @app_commands.guild_only()
    @app_commands.describe(kategorie="› Wähle eine Kategorie aus!")
    @app_commands.choices(kategorie=[
        Choice(name="Geschlossene Tickets", value="s_tickets"),
        Choice(name="Geöffnete Tickets", value="m_tickets")
    ])
    async def bestenliste(self, interaction: discord.Interaction, kategorie: Choice[str]):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:

                if kategorie.value == "s_tickets":
                    await cur.execute(f"SELECT userID, closed_tickets FROM team_tickets WHERE guildID = (%s) ORDER BY closed_tickets DESC", interaction.guild.id)
                    lb = await cur.fetchall()
                    data = ""
                    i = 0
                    for daten in lb:
                        i += 1
                        user = await self.bot.fetch_user(int(daten[0]))
                        data += f"{i}. {user.mention}  __Tickets__: `{daten[1]}`\n"


                if kategorie.value == "m_tickets":
                    await cur.execute(f"SELECT userID, anzahl FROM user_tickets WHERE guildID = (%s) ORDER BY anzahl DESC", interaction.guild.id)
                    lb = await cur.fetchall()
                    data = ""
                    i = 0
                    for daten in lb:
                        i += 1
                        user = await self.bot.fetch_user(int(daten[0]))
                        data += f"{i}. {user.mention}  __Tickets__: `{daten[1]}`\n"

                embed = discord.Embed(description=data,
                                      timestamp=datetime.now(),
                                      color=0x4c69f8)
                embed.set_author(name=f"{kategorie.name} Bestenliste", icon_url=interaction.user.display_avatar.url)
                embed.set_footer(text=f"Author ID: {interaction.user.id}")
                await interaction.response.send_message(embed=embed)

    @app_commands.command(name="help", description="› Schau dir das Hilfe Menü an.")
    @app_commands.guild_only()
    async def help(self, interaction: discord.Interaction):

        view = DropdownView(interaction.user.id)

        embed = discord.Embed(description=f"Das hier ist das Hilfe Menü. Mit dem Dropdown "
                                          f"Menü unten kannst du die einzelnen Kategorien auswählen. Bei weiterne"
                                          f" Fragen trette einfach dem __[Support Server](https://discord.gg/wGFzPk45hr \"Betrete den Support Server\")__ bei!\n\n"
                                          f"**Hilfe Menüs**\n\n"
                                          f"> <:DeadShotHelp:1037756726704881685> **Bot - Führung** - Eine Erklärung der wichtigsten Befehle\n"
                                          f"> \n"
                                          f"> <:DeadShotMod:914516537057116160>  **Team Befehle** - Eine Liste von allen Team Befehlen.\n"
                                          f"> \n"
                                          f"> <:DeadShotSettings:1034191404487954442> **Einstellungs Befehle** - Eine Aufzählung aller Einstellungs Befehlen.\n"
                                          f"> \n"
                                          f"> <:DeadShotInfos:1034196978013319228> **Informations Befehle** - Eine Auslistung aller Informations Befehlen.",
                              timestamp=datetime.now(),
                              color=0x3357ca)
        embed.set_author(name=f"{self.bot.user.name} Hilfe Menü", icon_url=self.bot.user.avatar.url)
        embed.set_footer(text=f"Author ID: {interaction.user.id}")
        embed.set_image(url="https://cdn.discordapp.com/attachments/909501269759127602/1034464798349467738/Modmail-bot_Hilfe.jpg")
        await interaction.response.send_message(embed=embed, view=view)
        view.message = await interaction.original_response()

    @app_commands.command(name="userinfo", description="Informationen zu Usern")
    @app_commands.guild_only()
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * FROM global_ban WHERE userID = (%s)", user.id)
                db_daten = await cur.fetchone()
                if db_daten:
                    print(db_daten)
                    await interaction.response.send_message(f"{user.mention} ist gebannt.\n"
                                                            f"Gebannt von: {await self.bot.fetch_user(db_daten[1])}\n"
                                                            f"Grund: {db_daten[2]}")

                if db_daten is None:
                    await interaction.response.send_message("Nicht gebannt.")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(info(bot))
