import discord
from discord import app_commands
from discord.ext import commands
from typing import Optional

GUILDS = [discord.Object(id) for id in (...,)] #서버 ID를 넣어주세요.

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=".",
            intents=discord.Intents.all()
        )

    async def setup_hook(self):
        for guild in GUILDS:
            await self.tree.sync(guild=guild)

    async def on_ready(self):
        print(f"{self.user.name}으로 로그인")

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game("봇 테스트")
        )


bot = Bot()


@bot.command(name="안녕", aliases=["반가워"])
async def send_hello(ctx: commands.Context):
    await ctx.send("안녕하세요!")


# @bot.command(name="테스트")
# async def args_test(ctx: commands.Context, arg1: str, arg2: str, arg3: str): # 인자값을 정해진 만큼 받고 싶을 때
#     await ctx.send(f"첫번째 값: {arg1}\n두번째 값: {arg2}\n세번째 값: {arg3}")

# @bot.command(name="테스트")
# async def args_test(ctx: commands.Context, *args: str): # 인자값을 여러개 받고 싶을 때
#     await ctx.send(f"{', '.join(args)}\n총합 {len(args)}개")

@bot.command(name="테스트")
async def args_test(ctx: commands.Context, *, args: str):  # 인자값을 하나의 문자열로 받고 싶을 때
    await ctx.send(f"입력된 내용: {args}")


# @bot.command(name="기본값")
# async def default_value(ctx: commands.Context, arg1: str = None):
#     await ctx.send(f"arg의 값: {arg1}")

@bot.command(name="기본값")
async def default_value(ctx: commands.Context, arg1: Optional[str] = None):
    await ctx.send(f"arg의 값: {arg1}")


@bot.command(name="타입")
async def type_annotation(ctx: commands.Context, arg1: str, arg2: int, arg3: float):
    await ctx.send(f"arg1의 타입: {type(arg1)}\narg2의 타입: {type(arg2)}\narg3의 타입: {type(arg3)}")


@bot.command(name="예외")
async def exception(ctx: commands.Context, arg: int):
    await ctx.send(f"arg1의 타입: {type(arg)}, 값: {arg}")

# @exception.error
# async def exception_error(ctx: commands.Context, error):
#     await ctx.send(f"예외가 발생하였습니다.\n```{error}```")

@exception.error
async def exception_error(ctx: commands.Context, error):
    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("값을 입력해 주세요.")

    elif isinstance(error, commands.errors.BadArgument):
        await ctx.send("숫자만 입력해 주세요.")

    else:
        await ctx.send(f"예외가 발생하였습니다.\n```{error}```")


@bot.tree.command(
    name="안녕",
    description="봇이 인사를 합니다.",
    guilds=GUILDS
)
async def app_send_hello(interaction: discord.Interaction):
    await interaction.response.send_message("안녕하세요!")


@bot.tree.command(
    name="매개변수",
    description="매개변수 테스트 명령어 입니다.",
    guilds=GUILDS
)
@app_commands.rename(
    arg1="arg1",
    arg2="인수2",
    arg3="인수3"
)
@app_commands.describe(
    arg1="문자열을 입력해 주세요.",
    arg2="정수를 입력해 주세요.",
    arg3="논리값을 입력해 주세요."
)
async def app_args_test(interaction: discord.Interaction, arg1: str, arg2: int, arg3: Optional[bool] = None):
    await interaction.response.send_message(f"arg1: {arg1}\narg2: {arg2}\narg3: {arg3}")


@bot.tree.command(
    name="예외",
    description="예외를 발생시킵니다.",
    guilds=GUILDS
)
async def app_exception(interaction: discord.Interaction):
    raise Exception("예외발생!")

@app_exception.error
async def app_exception_error(interaction: discord.Interaction, error):
    await interaction.response.send_message(f"에러가 발생하였습니다.\n```{error}```")


with open("./token.txt", "r") as fr:
    bot.run(fr.read())
