import os
import asyncio
from telethon import TelegramClient, events
from dotenv import load_dotenv

load_dotenv()

# =====================================
# GLOBAL VARIABLES
# =====================================

message_ids = []
reply_messages = []
selected_message = 0

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
    keywords.update([word.strip()
                    for word in keywords_string.split(';') if word.strip()])

app = TelegramClient("my_account", os.getenv('API_ID'), os.getenv('API_HASH'))

# =====================================
# SERVICE METHODS
# =====================================


def format(message):
    return f'```\n{message}```'


async def try_send(chat, message, save):
    if not save:
        await app.send_read_acknowledge(chat)
    message = await app.send_message(chat, message)
    if save:
        message_ids.append(message.id)


async def send(chat, message, save=True):
    try:
        await try_send(chat, message, save)
    except:
        # From documentation: https://docs.telethon.dev/en/stable/concepts/entities.html
        # To “encounter” an ID, you would have to “find it” like you would in the normal app.
        # If the peer is in your dialogs, you would need to client.get_dialogs()
        try:
            await app.get_dialogs()
            await try_send(chat, message, save)
        except ValueError as e:
            print('\nValueError occurred while trying to get all dialogs and send the message\n', str(e), '\n')


async def reply(chat):
    global selected_message
    if len(reply_messages) == 0:
        return
    selected_message += 1
    selected_message = selected_message % len(reply_messages)
    message = reply_messages[selected_message]
    await asyncio.sleep(delay)
    await send(chat, message, save=False)


async def show_messages():
    if len(reply_messages) == 0:
        await send('me', format('No messages found.'))
        return
    for index, message in enumerate(reply_messages):
        await send('me', f'{format(f"Message {index + 1}:")}\n{message}')


async def add_message(text):
    text_arr = text.split('\n', maxsplit=1)
    if len(text_arr) > 1:
        reply_messages.append(text_arr[1])
        await send('me', format('Message added successfully'))


async def remove_message(text):
    text_arr = text.split(maxsplit=1)
    if len(text_arr) > 1:
        try:
            index = int(text_arr[1])
            if index > 0 and index <= len(reply_messages):
                del reply_messages[index - 1]
                await send('me', format(f'Message {index} was deleted'))
            else:
                await send('me', format('Invalid message index'))
        except ValueError:
            await send('me', format(f'"{text_arr[1]}" is not a valid number'))
    else:
        await send('me', format(f'Message index is missing'))


async def clear_messages():
    reply_messages.clear()
    await send('me', format('The message list was cleared'))


async def get_info():
    set_string = keywords if len(keywords) > 0 else '{}'
    message = format(f'Delay: {delay} seconds\nKeywords: {set_string}\nReply messages: {len(reply_messages)}')
    await send('me', message)


async def add_keywords(text):
    global keywords
    new_keywords = text.lower().split()[1::]
    keywords.update(new_keywords)
    await send('me', format(f'Words {new_keywords} was successfully added to your keywords'))


async def remove_keywords(text):
    global keywords
    new_keywords = text.lower().split()[1::]
    removed_keywords = []
    for word in new_keywords:
        if word in keywords:
            removed_keywords.append(word)
            keywords.remove(word)

    if len(removed_keywords) == 0:
        await send('me', format('The given words are not contained within your keywords'))
    else:
        await send('me', format(f'Words {removed_keywords} was successfully removed from your keywords'))


async def clear_keywords():
    keywords.clear()
    await send('me', format('Keyword list was cleared'))


async def update_delay(text):
    global delay
    text_arr = text.split(maxsplit=1)
    if len(text_arr) > 1:
        try:
            delay = int(text_arr[1])
            await send('me', format(f'Delay was updated to {delay} seconds'))
        except ValueError:
            await send('me', format(f'"{text_arr[1]}" is not a valid time argument'))
    else:
        await send('me', format('Delay (seconds) argument is missing'))


async def clear():
    await app.delete_messages('me', message_ids)
    message_ids.clear()


async def handle_unknown_command():
    await send('me', format('Unknow command'))


async def exit():
    await clear()
    await app.disconnect()

# =====================================
# EVENT HANDLERS
# =====================================


@app.on(events.NewMessage(from_users='me', func=lambda e: e.is_private))
async def handle_command_message(message):
    global test

    if hasattr(message.chat, 'is_self') and message.chat.is_self:
        if message.raw_text.startswith('/'):
            message_ids.append(message.id)
            command = message.raw_text.split(maxsplit=1)[0].lower()
            # print(f'{command} command was invoked')

            match command:
                case '/messages':
                    await show_messages()
                case '/m_add':
                    await add_message(message.text)
                case '/m_remove':
                    await remove_message(message.text)
                case '/m_clear':
                    await clear_messages()
                case '/info':
                    await get_info()
                case '/k_add':
                    await add_keywords(message.text)
                case '/k_remove':
                    await remove_keywords(message.text)
                case '/k_clear':
                    await clear_keywords()
                case '/delay':
                    await update_delay(message.text)
                case '/clear':
                    await clear()
                case '/exit':
                    await exit()
                case _:
                    await handle_unknown_command()


@app.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handle_private_message(message):
    if hasattr(message.chat, 'is_self') and message.chat.is_self:
        return

    message.raw_text = message.raw_text.lower()
    for word in keywords:
        if word in message.raw_text:
            await reply(message.chat_id)
            break


# =====================================
# MAIN
# =====================================

app.start()
print('Telegram auto-reply program is running...')
app.run_until_disconnected()
print('Program terminated')
