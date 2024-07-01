import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time

# Function to generate email content
def generate_email_content(name, ac_no, otp):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

    # Format the email content in HTML with CSS styling
    email_content = f"""
<html>
  <head>
    <style>
      body {{
        font-family: Arial, sans-serif;
        line-height: 1.6;
      }}
      .container {{
        max-width: 600px;
        margin: 0 auto;
        padding: 20px;
        background-color: #f9f9f9;
        border-radius: 5px;
      }}
      .banner {{
        background-color: black;
        color: white;
        padding: 10px;
        text-align: center;
        border-radius: 10px;
      }}
      .title {{
        font-size: 50px;
        font-weight: bold;
        color: #333;
        margin-bottom: 5px;
      }}
      .footer {{
        background-color: black;
        color: white;
        padding: 10px;
        text-align: center;
        border-radius: 5px;
        font-size: 14px;
        margin-top: 20px;
      }}
      .timestamp {{
        font-size: 12px;
        font-weight: bold;
        color: #333;
        text-align: right;
      }}
    </style>
  </head>
  <body>
    <div class="container">
      <div class="banner">
        <p style="font-size: 24px;">Your One Time Password</p>
      </div>
      <p class="timestamp"><strong>Timestamp (IST):</strong> {timestamp}</p>

      <p>Dear {name},</p>

      <p>Please use the OTP given below to login into your bank account with ID {ac_no}.</p>

      <h1 class="title">{otp}</h1>
      
      <p class="footer">BankWithUs</p>
    </div>
  </body>
</html>
"""
    return email_content

def send_email(to, otp, name, ac_no):

    subject = "OTP from BankWithUs"
    message = generate_email_content(name, ac_no, otp)

    # Email configuration
    email_from = 'smartgurucool@gmail.com'
    email_to = to
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'smartgurucool@gmail.com'
    smtp_password = open('pwd.txt').read()

    try:
        # Set up the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Create message container
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = email_to
        msg['Subject'] = subject

        # Add message body
        msg.attach(MIMEText(message, 'html'))

        # Send the email
        server.sendmail(email_from, email_to, msg.as_string())
        print(f"At {time.strftime('%Y-%m-%d %H:%M:%S')}, email sent successfully!")

        # Quit the SMTP server
        server.quit()
    except Exception as e:
        print("At {time.strftime('%Y-%m-%d %H:%M:%S')}, failed to send email:", e)

# send_email("me@kmranrg.com",1234,"anurag",100)