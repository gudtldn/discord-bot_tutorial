import discord
from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=".",
            intents=discord.Intents.all()
        )

    async def on_ready(self):
        print(f"{self.user.name}으로 로그인")
        
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game("봇 테스트")
        )
    
bot = Bot()

with open("./token.txt", "r") as fr:
    bot.run(fr.read())