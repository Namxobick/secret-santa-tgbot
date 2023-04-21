import aiogram


async def set_default_command(dispatcher: aiogram.Dispatcher):
    await dispatcher.bot.set_my_commands([
        aiogram.types.BotCommand('start', 'Start'),
        aiogram.types.BotCommand('menu', 'Menu'),
        aiogram.types.BotCommand('create_lobby', 'Create new lobby'),
        aiogram.types.BotCommand('join_lobby', 'Join to lobby'),
        aiogram.types.BotCommand('my_lobbies', 'Find out your lobbies'),
        aiogram.types.BotCommand('help', 'Help'),
    ])
