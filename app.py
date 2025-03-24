from flask import Flask, render_template, request, jsonify
from flask_mail import Mail, Message
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
from dotenv import load_dotenv
import re
import html
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')

# レート制限の設定
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["5 per minute", "100 per day"]
)

# メール設定
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_APP_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_USERNAME')

mail = Mail(app)

def validate_email(email):
    """メールアドレスのバリデーション"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def sanitize_input(text):
    """入力値のサニタイズ"""
    return html.escape(text.strip())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
@limiter.limit("5 per minute")  # レート制限
def send_message():
    try:
        data = request.get_json()
        
        # 必須フィールドの確認
        required_fields = ['name', 'email', 'message']
        if not all(field in data for field in required_fields):
            return jsonify({'error': '全ての項目を入力してください'}), 400
        
        # 入力値の取得とサニタイズ
        name = sanitize_input(data['name'])
        email = sanitize_input(data['email'])
        message = sanitize_input(data['message'])
        
        # 入力値の長さチェック
        if len(name) > 100:
            return jsonify({'error': '名前は100文字以内で入力してください'}), 400
        if len(email) > 256:
            return jsonify({'error': 'メールアドレスは256文字以内で入力してください'}), 400
        if len(message) > 1000:
            return jsonify({'error': 'メッセージは1000文字以内で入力してください'}), 400
            
        # メールアドレスのバリデーション
        if not validate_email(email):
            return jsonify({'error': '有効なメールアドレスを入力してください'}), 400

        # メール本文の作成
        body = f"""
        新しいお問い合わせがありました：
        
        名前: {name}
        メールアドレス: {email}
        送信日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
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
            
            ※このメールは自動送信されています。
            """
        )
        mail.send(auto_reply)

        return jsonify({'message': 'メッセージを送信しました'}), 200

    except Exception as e:
        app.logger.error(f'Error sending message: {str(e)}')
        return jsonify({'error': 'メッセージの送信に失敗しました'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
