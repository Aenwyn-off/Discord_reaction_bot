import discord

from os import getenv
from dotenv import load_dotenv
from database import orm

load_dotenv()
token = getenv("BOT_TOKEN")
bot = discord.Bot()


@bot.event
async def on_ready():
    print(f'Bot is ready and logged in as {bot.user.name}')


@bot.slash_command(name="react", description="set emoji on user")
async def react(ctx: discord.ApplicationContext, emotion: str, username: discord.User):
    # Ищем пользователя по имени
    user = discord.utils.get(ctx.guild.members, name=username.name)
    if user is None:
        await ctx.respond(f'Пользователь с именем "{username.mention}" не найден.')
        return

    # Добавляем пользователя в БД
    orm.add_user(username.id, username.name)

    async def emote_validator(lst, value):
        counter = 0
        if not lst:
            orm.add_emoji(username.id, emotion)
            await ctx.respond(f'Установлена эмоция "{emotion}" для пользователя {user.mention}.')
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

    if orm.get_user(message.author.id) is None:
        return

    # Проверяем, есть ли у пользователя установленная эмоция
    if message.author.id == orm.get_user(message.author.id).dis_id:
        for emote in orm.get_emojis(message.author.id):
            await message.add_reaction(str(emote))
        # Добавляем эмоцию к сообщению пользователя
    await bot.process_application_commands(message)


@bot.slash_command(name="unreact", description="delete emoji from user")
async def unreact(ctx: discord.ApplicationContext, emotion: str, username: discord.User):
    # Ищем пользователя по имени
    user = discord.utils.get(ctx.guild.members, name=username.name)
    if user is None:
        await ctx.respond(f'Пользователь с именем "{username.mention}" не найден.')
        return

    # if username.id == orm.get_user(username.id).dis_id:
    #     orm.add_user(username.id, username.name)

    async def emote_validator(lst, value):
        counter = 0
        if not lst:
            await ctx.respond(f"Нечего удалять")
        else:
            for val in lst:
                if str(val) == value:
                    counter += 1
                    break
            if counter == 1:
                orm.delete_user_emoji(emotion)
                await ctx.respond(f'Эмоция "{emotion}" для пользователя {user.mention} удалена')
            else:
                await ctx.respond(f'Эмоция - "{emotion}" не установлена пользователю')

    await emote_validator(orm.get_emojis(username.id), emotion)


@bot.slash_command(name="unreactall", description="delete all emojis from user")
async def unreactall(ctx: discord.ApplicationContext, username: discord.User):
    # Ищем пользователя по имени
    user = discord.utils.get(ctx.guild.members, name=username.name)
    if user is None:
        await ctx.respond(f'Пользователь с именем "{username.mention}" не найден.')
        return

    orm.delete_all_emoji_from_user(username.id)
    await ctx.respond(f'Все эмоции с пользователя {username.mention} - удалены')


bot.run(token)