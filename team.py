from telethon import TelegramClient, events
import logging
import asyncio
import re

# Replace these with your credentials
api_id = 'hsjdhjs'
api_hash = 'djsahdjshjdha'
bot_token = 'sjdhjsdhjashj'
public_group_ids = [-1002243936664, -1001371184682, 6145463489]
private_chat_id = -4269781975

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define your filter
def message_passes_filter(message_text):
    # Check for presence of specific keywords or phrases
    keywords = ['Oct', 'Nov', 'Dec', 'Available']
    pattern = re.compile('|'.join(keywords), re.IGNORECASE)
    return bool(pattern.search(message_text))

async def main():
    client = TelegramClient('bot_session', api_id, api_hash)
    await client.start(bot_token=bot_token)

    @client.on(events.NewMessage(chats=public_group_ids))
    async def handler(event):
        message = event.message
        message_text = message.text or ""

        if message.media:
            # If the message has media (like images), forward it directly
            try:
                await client.forward_messages(private_chat_id, message)
                logging.info(f"Media forwarded: {message.media}")
            except Exception as e:
                logging.error(f"An error occurred while forwarding the media: {e}")
        elif message_passes_filter(message_text):
            # If it's a text message and passes the filter
            try:
                await client.send_message(private_chat_id, f"Forwarded Message from Group:\n{message_text}")
                logging.info(f"Message forwarded: {message_text}")
            except Exception as e:
                logging.error(f"An error occurred while forwarding the message: {e}")
        else:
            logging.info(f"Message did not pass filter: {message_text}")

    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
