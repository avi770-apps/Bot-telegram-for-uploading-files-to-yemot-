
from pyrogram.types import Message
import requests
import os

API_ID = 1239876 #API_ID שקיבלתם באתר 
API_HASH = 'abc777vshdjndb' #API_HASH שקיבלתם באתר
BOT_TOKEN = '123:aaa' #טוקן של הבוט


app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start_command(client, message: Message):
    await message.reply_text("Send me an audio, video, or voice file up to 50MB, and I will save it on the server.")

@app.on_message(filters.private)
async def save_media(client, message: Message):
    media = message.audio or message.video or message.voice
    if media:
        if media.file_size <= 50 * 1024 * 1024:  # Check if file size is less than or equal to 50MB
            file_name = media.file_name if hasattr(media, 'file_name') else "voice_note.oga"
            file_path = await message.download(file_name=f"downloads/{file_name}")
            await message.reply_text(f"File saved at server: {file_name}")
            number_sys = "039660770" #מספר מערכת
            pass_number = "123456" # סיסמת ניהול למערכת
            path = "ivr2:/1/1" #נתיב להעלאת הקובץ
            convertAudio = "1" # אם להמיר את הקובץ ל wav - 1 או 0
            autoNumbering = "true" #אם לעלות כמספר קובץ חדש או לפי שם הקובץ
            tts = "0" #אם הקובץ הוא קובץ tts או לא : 1 או 0
            api_url = f"https://www.call2all.co.il/ym/api/UploadFile?token={number_sys}:{pass_number}&path={path}&convertAudio={convertAudio}&autoNumbering={autoNumbering}&tts={tts}"
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

app.run()
