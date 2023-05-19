import os
import asyncio
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

# =====================================
# GLOBAL VARIABLES
# =====================================

message_ids = []

reply_message = os.getenv('REPLY_MESSAGE')
if not reply_message:
    reply_message = ''

delay = os.getenv('DELAY')
if delay:
    try:
        delay = int(delay)
    except ValueError:
        print('Env variable "DELAY" is not a number')
        delay = 10
else:
    delay = 10

keywords = set()
keywords_string = os.getenv('KEYWORDS')
if keywords_string:
    keywords.update([word.strip() for word in keywords_string.split(';') if word.strip()])

app = TelegramClient("my_account", os.getenv('API_ID'), os.getenv('API_HASH'))

# =====================================
# SERVICE METHODS
# =====================================


async def send(chat, message, save=True):
    try:
        message = await app.send_message(chat, message)
        if save:
            message_ids.append(message.id)
    except ValueError as e:
        print("\033[91m{}\033[0m".format('\tAn error occurred while sending a messag\n'), str(e))


async def update_message(text):
    global reply_message
    text_arr = text.split('\n', maxsplit=1)
    if len(text_arr) > 1:
        reply_message = text_arr[1]
    else:
        reply_message = ''
    await send('me', f'```\nYour reply message was changed to:```\n{reply_message}')


async def get_info():
    set_string = keywords if len(keywords) > 0 else '{}'
    message = f'```\nDelay: {delay} seconds\nKeywords: {set_string}\nReply message:```\n{reply_message}'
    await send('me', message)


async def add_keywords(text):
    global keywords
    new_keywords = text.lower().split()[1::]
    keywords.update(new_keywords)
    await send('me', f'```\nWords {new_keywords} was successfully added to your keywords```')


async def remove_keywords(text):
    global keywords
    new_keywords = text.lower().split()[1::]
    removed_keywords = []
    for word in new_keywords:
        if word in keywords:
            removed_keywords.append(word)
            keywords.remove(word)

    response = ''
    if len(removed_keywords) == 0:
        response = '```\nThe given words are not contained within your keywords```'
    else:
        response = f'```\nWords {removed_keywords} was successfully removed from your keywords```'

    mess = await send('me', response)


async def update_delay(text):
    global delay
    text_arr = text.split(maxsplit=1)
    if len(text_arr) > 1:
        try:
            delay = int(text_arr[1])
            await send('me', f'```\nDelay was updated to {delay} seconds.```')
        except ValueError:
            await send('me', f'```\n"{text_arr[1]}" is not a valid time argument.```')
    else:
        mess = await send('me', f'```\nDelay (seconds) argument is missing.```')


async def clear():
    await app.delete_messages('me', message_ids)
    message_ids.clear()


async def handle_unknown_command():
    await send('me', '```\nUnknow command```')


async def exit():
    await clear()
    await app.disconnect()

# =====================================
# EVENT HANDLERS
# =====================================


@app.on(events.NewMessage(from_users='me', func=lambda e: e.is_private))
async def handle_command_message(message):
    if hasattr(message.chat, 'is_self') and message.chat.is_self:
        if message.raw_text.startswith('/'):
            message_ids.append(message.id)
            command = message.raw_text.split(maxsplit=1)[0].lower()
            print(f'{command} command was invoked')

            match command:
                case '/message':
                    await update_message(message.text)
                case '/info':
                    await get_info()
                case '/add':
                    await add_keywords(message.text)
                case '/remove':
                    await remove_keywords(message.text)
                case '/delay':
                    await update_delay(message.text)
                case '/clear':
                    await clear()
                case '/exit':
                    await exit()
                case _:
                    await handle_unknown_command()


# @app.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
@app.on(events.NewMessage(func=lambda e: e.is_private))
async def handle_private_message(message):
    if hasattr(message.chat, 'is_self') and message.chat.is_self:
        return

    message.raw_text = message.raw_text.lower()
    reply = False
    for word in keywords:
        if word in message.raw_text:
            if len(reply_message) > 0:
                reply = True
            break
    if reply:
        await asyncio.sleep(delay)
        await send(message.chat_id, reply_message, save=False)

# =====================================
# MAIN
# =====================================

app.start()
app.run_until_disconnected()
