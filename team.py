from telethon import TelegramClient, events
import logging
import asyncio
import re

# Replace these with your credentials
api_id = '27232480'
api_hash = 'b00b2f81b37e64a7eca45f11570ed7ac'
bot_token = '7245992910:AAFjz_Klm6CWR2X2uORIydulKZ8a8WBqswg'
public_group_ids = [-1002243936664, -1001371184682, 6145463489, -1002208686405]
private_chat_id = -1002208686405

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
                await client.send_message(private_chat_id, message_text)
                logging.info(f"Message forwarded: {message_text}")
            except Exception as e:
                logging.error(f"An error occurred while forwarding the message: {e}")
        else:
            logging.info(f"Message did not pass filter: {message_text}")

    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
