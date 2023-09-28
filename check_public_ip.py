import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


GMAIL_EMAIL = 'your_email@gmail.com'
GMAIL_PASSWORD = 'your_app_password'


TO_EMAIL = 'recipient_email@example.com'

previous_ip = None

def send_email(new_ip):
    subject = 'IP Address Change Detected'
    message = f'Your public IP address has changed to {new_ip}'

    msg = MIMEMultipart()
    msg['From'] = GMAIL_EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(GMAIL_EMAIL, GMAIL_PASSWORD)
    server.sendmail(GMAIL_EMAIL, TO_EMAIL, msg.as_string())
    server.quit()


def get_public_ip():
    try:
        response = requests.get('https://api64.ipify.org?format=json')
        data = response.json()
        return data['ip']
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == '__main__':
    while True:
        current_ip = get_public_ip()
        
        if current_ip and current_ip != previous_ip:
            send_email(current_ip)
            previous_ip = current_ip
        
        import time
        time.sleep(3600)  
