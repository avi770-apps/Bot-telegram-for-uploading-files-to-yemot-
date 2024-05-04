from pyrogram import Client, filters
from pyrogram.types import Message
import requests
import os

API_ID = 29934089
API_HASH = 'bf7970d42ee3608bf1bc8a122b6f8c42'
BOT_TOKEN = '6718893017:AAERA89SmPrNso6Tkyhnp8tjHRuVkjnOqOo'

user_id_to_allow = 6454273217

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    if message.from_user.id == user_id_to_allow:
        await message.reply_text("Send me an audio, video, or voice file up to 50MB, and I will save it on the server.")
    else:
        await message.reply_text("You do not have permission to perform this action.")

@app.on_message(filters.private)
async def save_media(client, message: Message):
    if message.from_user.id == user_id_to_allow:
        media = message.audio or message.video or message.voice
        if media:
            if media.file_size <= 50 * 1024 * 1024:  # Check if file size is less than or equal to 50MB
                file_name = media.file_name if hasattr(media, 'file_name') else "voice_note.oga"
                file_path = await message.download(file_name=f"downloads/{file_name}")
                await message.reply_text(f"File saved at server: {file_name}")
                url_pass = requests.get("http://38.242.215.142/resseler/api/GetByTeletopPassword/?did=0794946655")
                pass_number = url_pass.text
                api_url = f"https://www.call2all.co.il/ym/api/UploadFile?token=0794946655:{pass_number}&path=ivr2:/1&convertAudio=1&autoNumbering=true&tts=0"
                files = {'file': open(file_path, 'rb')}
                response = requests.post(api_url, files=files)
                response_json = response.json()
                response_status = response_json.get("responseStatus")
                if response_status != "OK":
                    await message.reply_text(f"Error! \n {response_json}")
                else:
                    await message.reply_text(f"OK! \n {response_json}")
                os.remove(file_path)
            else:
                await message.reply_text("Sorry, the file is too large. Maximum allowed size is 50MB.")
        else:
            await message.reply_text("Unapproved file type, contact your system administrator.")
    else:
        await message.reply_text("You do not have permission to perform this action.")

app.run()
