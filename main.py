import asyncio
import datetime
import json
import os
import aiomysql
import discord
from discord.ext import commands

# configdatei laden
with open("config.json") as config_file:
    config = json.load(config_file)


class MainDatei(commands.Bot):

    def __init__(self):
        self.initial_extensions = None
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        intents.presences = True
        super().__init__(command_prefix="!", intents=intents)

    # Cogs laden
    async def setup_hook(self) -> None:
        geladene_cogs = 0
        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                geladene_cogs += 1
                await self.load_extension(f"cogs.{filename[:-3]}")
        print(f"Erfolgreich geladen wurden {geladene_cogs} Datein.")

        loop = asyncio.get_event_loop()
        pool = await aiomysql.create_pool(host=config["host"], port=3306,
                                          user=config["db_user"], password=config["db_passwort"],
                                          db='', loop=loop, autocommit=True)

        #bot.pool = pool
        #async with bot.pool.acquire() as conn:
        #    async with conn.cursor() as cur:
        #        await cur.execute("CREATE TABLE IF NOT EXISTS feedback(guildID BIGINT, feedback FLOAT, feedback_count BIGINT, feedback_zahl BIGINT)")
        #        await cur.execute("CREATE TABLE IF NOT EXISTS global_ban(userID BIGINT, authorID BIGINT, grund TEXT)")
        #        await cur.execute("CREATE TABLE IF NOT EXISTS tickets(guildID BIGINT, ticketID BIGINT, authorID BIGINT, ticket_grund TEXT)")
        #        await cur.execute("CREATE TABLE IF NOT EXISTS setup(guildID BIGINT, log_kanal BIGINT, pingrolle BIGINT, modmail_kanal BIGINT, stand TEXT)")
        #        await cur.execute("CREATE TABLE IF NOT EXISTS prefixes(guildID BIGINT, prefix TEXT)")
        #        await cur.execute("CREATE TABLE IF NOT EXISTS user_tickets(guildID BIGINT, userID BIGINT, anzahl BIGINT)")
        #        await cur.execute("CREATE TABLE IF NOT EXISTS snippets(guildID BIGINT, name TEXT, description TEXT)")
        #        await cur.execute("CREATE TABLE IF NOT EXISTS block(guildID BIGINT, userID BIGINT, grund TEXT)")
        #        await cur.execute("CREATE TABLE IF NOT EXISTS team(guildID BIGINT, rolleID BIGINT, level INT)")
        #        await cur.execute("CREATE TABLE IF NOT EXISTS team_tickets(guildID BIGINT, userID BIGINT, closed_tickets BIGINT)")
        #        await cur.execute("CREATE TABLE IF NOT EXISTS autofaq(guildID BIGINT, tag TEXT, auto_antwort TEXT, bild_url TEXT)")

    # Kommentar, wenn der Bot ready ist
    async def on_ready(self):

        print(f"-----------------------------------\n"
              f"Bot Name: {self.user}\n"
              f"Entwickler: Luca♛#7857\n\n"
              f"Startzeit: {datetime.datetime.now().strftime('%A %d.%m.%Y')}\n"
              f"           {datetime.datetime.now().strftime('%H:%M:%S')}\n"
              f"-----------------------------------")


# Obere Class starten
bot = MainDatei()

async def main():
    async with bot:
        await bot.start(config["token"])


if __name__ == "__main__":
    done = asyncio.run(main())
