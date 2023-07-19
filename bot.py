import discord

from os import getenv
from dotenv import load_dotenv
from database import orm


load_dotenv()
token = getenv("BOT_TOKEN")
bot = discord.Bot()

emotions = {}


@bot.event
async def on_ready():
    print(f'Bot is ready and logged in as {bot.user.name}')


@bot.slash_command(name="react", description="set emoji on user")
async def react(ctx: discord.ApplicationContext, emotion: str, username: discord.User):
    # Ищем пользователя по имени
    user = discord.utils.get(ctx.guild.members, name=username.name)
    if user is None:
        await ctx.send(f'Пользователь с именем "{username}" не найден.')
        return

    orm.add_user(username.id, username.name)
    orm.add_emoji(username.id, emotion)

    # Устанавливаем эмоцию для пользователя
    emotions[user.name] = emotion
    await ctx.respond(f'Установлена эмоция "{emotion}" для пользователя {user.mention}.')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Проверяем, есть ли у пользователя установленная эмоция
    if message.author.name in emotions:
        emotion = emotions[message.author.name]
        # Добавляем эмоцию к сообщению пользователя
        await message.add_reaction(emotion)
    await bot.process_application_commands(message)

bot.run(token)
