from pyrogram.types import InlineKeyboardButton


class Data:
    generate_single_button = [InlineKeyboardButton("بدء استخراج الجلسة", callback_data="generate")]

    home_buttons = [
        generate_single_button,
        [InlineKeyboardButton(text="الرجوع", callback_data="home")]
    ]

    generate_button = [generate_single_button]

    buttons = [
        generate_single_button,
        [InlineKeyboardButton("لمعلمة عمل البوت او صيانته", url="https://t.me/Privapact")],
        [
            InlineKeyboardButton("كيفية عمل البوت", callback_data="help"),
            InlineKeyboardButton("عن البوت", callback_data="about")
        ],
        [InlineKeyboardButton("يوتات اخرى رائعة", url="https://t.me/PrivaPact")],
    ]

    START = """
مرحبًا {}

مرحبًا بك في {}

يمكنك استخدامي لإنشاء جلسة سلسلة Pyrogram (حتى الإصدار 2) وجلسة سلسلة Telethon. استخدم الأزرار أدناه لمعرفة المزيد!

بواسطة @Privapact
    """

    HELP = """
 **الاوامر المتوفرة** 

/about - عن البوت
/help - رسالة المساعدة
/start - بدء البوت
/generate - صنع ترمكس
/cancel - الغاء العملية
/restart - اعادة بدئ العملية
"""

    ABOUT = """
**عن البوت** 

بوت تليجرام لإنشاء جلسة  Pyrogram وجلسة  Telethon 

المكتبة : Pyrogram

اللغة: Python

المطور: @Privapact
    """
