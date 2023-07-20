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

    # Добавляем пользователя и эмоцию в БД
    if username.id == orm.get_user(username.id).id:
        orm.add_user(username.id, username.name)

    async def emote_validator(lst, value):
        counter = 0
        if not lst:
            orm.add_emoji(username.id, emotion)
        else:
            for val in lst:
                if str(val) == value:
                    counter += 1
            if counter != 1:
                orm.add_emoji(username.id, emotion)
                await ctx.respond(f'Установлена эмоция "{emotion}" для пользователя {user.mention}.')
            else:
                await ctx.respond(f'Эмоция "{emotion}" уже установлена')

    await emote_validator(orm.get_emojis(username.id), emotion)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Проверяем, есть ли у пользователя установленная эмоция
    if message.author.id == orm.get_user(message.author.id).dis_id:
        for emote in orm.get_emojis(message.author.id):
            await message.add_reaction(str(emote))
        # Добавляем эмоцию к сообщению пользователя
    await bot.process_application_commands(message)


bot.run(token)
