from datetime import datetime
import discord
from discord.ext import commands


class events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_unload(self) -> None:
        return await super().cog_unload()

    ############################################################################################

    # ███████╗██╗   ██╗███████╗███╗   ██╗████████╗███████╗
    # ██╔════╝██║   ██║██╔════╝████╗  ██║╚══██╔══╝██╔════╝
    # █████╗  ██║   ██║█████╗  ██╔██╗ ██║   ██║   ███████╗
    # ██╔══╝  ╚██╗ ██╔╝██╔══╝  ██║╚██╗██║   ██║   ╚════██║
    # ███████╗ ╚████╔╝ ███████╗██║ ╚████║   ██║   ███████║
    # ╚══════╝  ╚═══╝  ╚══════╝╚═╝  ╚═══╝   ╚═╝   ╚══════╝

    ############################################################################################

    @commands.Cog.listener()  # <- Wenn eine Nachricht gelöscht wird, wird es in den DMs / Ticket auch gelöscht.
    async def on_message_delete(self, message):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:

                if message.is_system():
                    return

                if message.type == "MessageType.application_command":
                    return

                bilder = message.attachments
                if isinstance(message.channel, discord.DMChannel):
                    await cur.execute("SELECT ticketID FROM tickets WHERE authorID = (%s)", message.author.id)
                    db_daten = await cur.fetchone()
                    if db_daten is not None:
                        if len(message.embeds) < 1:
                            channel = self.bot.get_channel(int(db_daten[0]))
                            async for msg in channel.history(limit=10):
                                if len(msg.embeds) >= 1:
                                    if len(bilder) >= 1:
                                        attachments = message.attachments
                                        for attach in attachments:
                                            des_img = msg.embeds[0].image
                                            author_msg = msg.embeds[0].author
                                            nachrichten_author = message.author
                                            if attach.url == des_img.url:
                                                if str(author_msg.name) == str(nachrichten_author):
                                                    embed = discord.Embed(description=f'{message.content}',
                                                                          color=discord.Colour.red(),
                                                                          timestamp=datetime.now())
                                                    embed.set_author(name=f'Nachricht gelöscht',
                                                                     icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                                                    embed.set_footer(text=f"Author: {message.author}")
                                                    embed.set_image(url=des_img.url)
                                                    await msg.edit(embed=embed)

                                    if len(bilder) == 0:
                                        em_msg = message.content
                                        em_des = msg.embeds[0].description
                                        author_msg = msg.embeds[0].author
                                        nachrichten_author = message.author

                                        if em_des == em_msg:
                                            if str(author_msg.name) == str(nachrichten_author):
                                                embed = discord.Embed(description=f'{message.content}',
                                                                      color=discord.Colour.red(),
                                                                      timestamp=datetime.now())
                                                embed.set_author(name=f'Nachricht gelöscht',
                                                                 icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                                                embed.set_footer(text=f"Author: {message.author}")
                                                await msg.edit(embed=embed)

        if isinstance(message.channel, discord.Thread):
            if message.author.id == self.bot.user.id:
                member = message.guild.get_member(int(message.channel.name))
                async for msg in member.dm_channel.history(limit=10):

                    if len(msg.embeds) >= 1:
                        if len(bilder) >= 1:
                            message_img = message.embeds[0].image
                            des_img = msg.embeds[0].image
                            author_msg = msg.embeds[0].author
                            nachrichten_author = message.author
                            if message_img.url == des_img.url:
                                if str(author_msg.name) == str(nachrichten_author):
                                    embed = discord.Embed(description=f'{message.content}',
                                                          color=discord.Colour.red(),
                                                          timestamp=datetime.now())
                                    embed.set_author(name=f'Nachricht gelöscht',
                                                     icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                                    embed.set_footer(text=f"Author: {message.author}")
                                    await message.edit(embed=embed)
                                    await msg.delete()

                    if len(bilder) == 0:
                        des = message.embeds[0].description
                        des2 = msg.embeds[0].description
                        author = msg.embeds[0].author
                        author2 = message.embeds[0].author
                        if des == des2:
                            if author.name == author2.name:
                                embed = discord.Embed(description=f'{des2}',
                                                      color=discord.Colour.red(),
                                                      timestamp=datetime.now())
                                embed.set_author(name=f'Nachricht gelöscht',
                                                 icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                                embed.set_footer(text=f"Teammitglied: {author.name}")
                                await message.channel.send(embed=embed)
                                await msg.delete()

    @commands.Cog.listener()  # <- Wenn eine Nachricht editiert wird, wir es auch im Ticket editiert.
    async def on_message_edit(self, message, before):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:

                if isinstance(before.channel, discord.DMChannel):
                    if message.author.bot:
                        return
                    else:
                        await cur.execute("SELECT ticketID FROM tickets WHERE authorID = (%s)", message.author.id)
                        db_daten = await cur.fetchone()
                        if db_daten is not None:
                            channel = self.bot.get_channel(int(db_daten[0]))
                            async for msg in channel.history(limit=10):
                                if len(msg.embeds) >= 1:
                                    des = message.content
                                    des2 = msg.embeds[0].description
                                    author = msg.embeds[0].author
                                    author2 = f"{message.author}"
                                    if des == des2:
                                        if author.name == author2:
                                            edit_embed = discord.Embed(
                                                description=f"{message.content}\n\n**editiert zu:**\n\n{before.content}",
                                                color=discord.Colour.blue(),
                                                timestamp=message.created_at)
                                            edit_embed.set_footer(text=f"Nachrichten ID: {message.id}")
                                            edit_embed.set_author(name=f"{message.author}")
                                            await msg.edit(embed=edit_embed)
                                            member_embed = discord.Embed(description=f"Nachricht erfolgreich editiert.",
                                                                         color=0x4c69f8,
                                                                         )
                                            member_embed.set_footer(text=f"Nachrichten ID: {message.id}")
                                            await message.author.send(embed=member_embed)

    @commands.Cog.listener()  # <- Wenn ein Nutzer den Server verlässt und ein Ticket offen ist, wird das Team informiert.
    async def on_member_remove(self, member):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:

                try:
                    await cur.execute("SELECT ticketID, authorID FROM tickets WHERE authorID = (%s)", member.id)
                    db_daten = await cur.fetchone()
                    if db_daten is not None:
                        channel = self.bot.get_channel(int(db_daten[0]))
                        if int(db_daten[1]) == int(member.id):
                            embed = discord.Embed(description=f"{member} hat den Server verlassen.",
                                                  timestamp=datetime.now(),
                                                  color=discord.Colour.red())
                            await channel.send(embed=embed)
                except Exception as e:
                    print(e)

    @commands.Cog.listener()  # <- Wenn ein Nutzer den Server betritt und ein Ticket offen ist, wird das Team informiert
    async def on_member_join(self, member):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:

                try:
                    await cur.execute("SELECT ticketID, authorID FROM tickets WHERE authorID = (%s)", member.id)
                    db_daten = await cur.fetchone()
                    if db_daten is not None:
                        channel = self.bot.get_channel(int(db_daten[0]))
                        if int(db_daten[1]) == int(member.id):
                            embed = discord.Embed(description=f"{member} hat den Server betreten.",
                                                  timestamp=datetime.now(),
                                                  color=discord.Colour.green())
                            await channel.send(embed=embed)
                except Exception as e:
                    print(e)

    @commands.Cog.listener()  # <- Wenn eine Team-rolle gelöscht wurde, wird das Team informiert.
    async def on_guild_role_delete(self, role):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT rolleID FROM team WHERE guildID = (%s)", role.guild.id)
                db_daten = await cur.fetchall()
                if db_daten:
                    for daten in db_daten:
                        if int(daten[0]) == role.id:
                            await cur.execute("DELETE FROM team WHERE rolleID = (%s)", role.id)

                            await cur.execute("SELECT log_kanal FROM setup WHERE guildID = (%s)", role.guild.id)
                            db_daten = await cur.fetchone()
                            log_channel = role.guild.get_channel(int(db_daten[0]))
                            if db_daten is not None:
                                embed = discord.Embed(
                                    description=f"› Es wurde die Teamrolle (`{role.name}`) gelöscht.",
                                    color=discord.Colour.red(),
                                    timestamp=datetime.now())
                                embed.set_author(name="Teamrolle gelöscht",
                                                 icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                                await log_channel.send(embed=embed)

    @commands.Cog.listener()  # <- Wenn der ModMail Kanal gelöscht wurde, wird das Team informiert.
    async def on_guild_channel_delete(self, channel):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT log_kanal FROM setup WHERE guildID = (%s)", channel.guild.id)
                db_daten = await cur.fetchone()
                if db_daten is not None:
                    log_channel = channel.guild.get_channel(int(db_daten[0]))
                    embed = discord.Embed(
                        description=f"› Es wurde der ModMail Kanal (`{channel.name}`) gelöscht.\n",
                        color=discord.Colour.red())
                    embed.set_footer(text=f"Nutze /setup edit damit die ModMail funktioniert.")
                    embed.set_author(name="ModMail Kanal gelöscht",
                                     icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                    await log_channel.send(embed=embed)

    @commands.Cog.listener()  # <- Wenn Ticket Thread gelöscht wird, wird das Ticket aus der DB gelöscht und das Team wird informiert
    async def on_thread_delete(self, thread):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT authorID FROM tickets WHERE guildID = (%s) AND ticketID = (%s)",
                                  (thread.guild.id, thread.id))
                db_daten = await cur.fetchone()

                await cur.execute("SELECT log_kanal FROM setup WHERE guildID = (%s)", thread.guild.id)
                db_daten2 = await cur.fetchone()

                if db_daten is not None:
                    await cur.execute("DELETE FROM tickets WHERE  guildID = (%s) AND ticketID = (%s)",
                                      (thread.guild.id, thread.id))
                    if db_daten2 is not None:
                        log_channel = thread.guild.get_channel(db_daten2[0])
                        embed = discord.Embed(
                            description=f"› Es wurde das ModMail Ticket (`{thread}`) gelöscht.\n",
                            color=discord.Colour.red())
                        embed.set_footer(text=f"Ticket Nutzer: {thread.guild.get_member(db_daten[0])}")
                        embed.set_author(name="ModMail Ticket gelöscht",
                                         icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                        await log_channel.send(embed=embed)

                    else:
                        pass
                else:
                    pass

    @commands.Cog.listener()
    async def on_thread_update(self, before, after):
        if before.name != after.name:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT authorID FROM tickets WHERE guildID = (%s) AND ticketID = (%s)",
                                      (before.guild.id, before.id))
                    db_daten = await cur.fetchone()

                    await cur.execute("SELECT log_kanal FROM setup WHERE guildID = (%s)", before.guild.id)
                    db_daten2 = await cur.fetchone()

                    if db_daten is not None:
                        await cur.execute("DELETE FROM tickets WHERE guildID = (%s) AND ticketID = (%s)",
                                          (before.guild.id, before.id))
                        if db_daten2 is not None:
                            log_channel = before.guild.get_channel(db_daten2[0])
                            embed = discord.Embed(
                                description=f"› Es wurde das ModMail Ticket ({after.mention}) editiert.\n"
                                            f"> Deshalb wurde das Ticket aus der Datenbank gelöscht",
                                color=discord.Colour.red())
                            embed.set_footer(text=f"Ticket Nutzer: {before.guild.get_member(db_daten[0])}")
                            embed.set_author(name="ModMail Ticket editiert",
                                             icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                            await log_channel.send(embed=embed)
                            await after.edit(name=f"Closed ({before.guild.get_member(db_daten[0]).id})", archived=True,
                                             locked=True)

                        else:
                            pass
                    else:
                        pass

        if after.archived is True:
            async with self.bot.pool.acquire() as conn:
                async with conn.cursor() as cur:
                    await cur.execute("SELECT authorID FROM tickets WHERE guildID = (%s) AND ticketID = (%s)",
                                      (before.guild.id, before.id))
                    db_daten = await cur.fetchone()

                    await cur.execute("SELECT log_kanal FROM setup WHERE guildID = (%s)", before.guild.id)
                    db_daten2 = await cur.fetchone()

                    if db_daten is not None:
                        await cur.execute("DELETE FROM tickets WHERE guildID = (%s) AND ticketID = (%s)",
                                          (before.guild.id, before.id))
                        if db_daten2 is not None:
                            log_channel = before.guild.get_channel(db_daten2[0])
                            embed = discord.Embed(
                                description=f"› Es wurde das ModMail Ticket ({after.mention}) archiviert.\n"
                                            f"> Deshalb wurde das Ticket aus der Datenbank gelöscht",
                                color=discord.Colour.red())
                            embed.set_footer(text=f"Ticket Nutzer: {before.guild.get_member(db_daten[0])}")
                            embed.set_author(name="ModMail Ticket archiviert",
                                             icon_url="https://cdn.discordapp.com/emojis/1034902940017774662.webp?size=96&quality=lossless")
                            await log_channel.send(embed=embed)

                        else:
                            pass
                    else:
                        pass


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(events(bot))
