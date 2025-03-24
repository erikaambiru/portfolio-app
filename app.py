from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')

# メール設定
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_APP_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        # 入力検証
        if not all([name, email, message]):
            return jsonify({'error': '全ての項目を入力してください'}), 400

        # メール本文の作成
        body = f"""
        新しいお問い合わせがありました：
        
        名前: {name}
        メールアドレス: {email}
        
        メッセージ:
        {message}
        """

        # メールの送信
        msg = Message(
            subject=f'ポートフォリオサイトからのお問い合わせ: {name}様より',
            recipients=[app.config['MAIL_USERNAME']],
            body=body
        )
        mail.send(msg)

        # 自動返信メールの送信
        auto_reply = Message(
            subject='お問い合わせありがとうございます',
            recipients=[email],
            body=f"""
            {name}様
            
            お問い合わせありがとうございます。
            内容を確認次第、折り返しご連絡させていただきます。
            
            以下、お問い合わせ内容です：
            
            {message}
            """
        )
        mail.send(auto_reply)

        return jsonify({'message': 'メッセージを送信しました'}), 200

    except Exception as e:
        return jsonify({'error': 'メッセージの送信に失敗しました'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
