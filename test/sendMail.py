import smtplib, ssl
from email.mime.text import MIMEText

# 以下にGmailの設定を書き込む --- (環境変数に入れてあります)
gmail_account = "Sweepstakescheck@gmail.com"
gmail_password = "clover0718"


def send_mail(mail_to,subject,message):#メール送信 (送信先、件名、メッセージ)

    # メールデータ(MIME)の作成 ---
    msg = MIMEText(message, "html")
    msg["Subject"] = subject
    msg["To"] = mail_to
    msg["From"] = gmail_account

    # Gmailに接続 ---
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465,
        context=ssl.create_default_context())
    server.login(gmail_account, gmail_password)
    server.send_message(msg) # メールの送信

if __name__ == '__main__':
    send_mail("kazuto.yuta@gmail.com","テスト","これはテストメールです")#ok
    print("ok")
