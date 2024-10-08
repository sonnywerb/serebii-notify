import json
import smtplib
import os
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from serebii_scraper import sv_news, tera_raids, event_distributions

def printJson(jsonToPrint):
    json_data = json.dumps(jsonToPrint, ensure_ascii=False, indent=4)
    print(json_data)

def format_content():
    content = "==========POKEMON SV NEWS==========\n"
    if sv_news:
        for news in sv_news:
            content += json.dumps(news, indent=4, ensure_ascii=False) + "\n\n"
    else:
        content += "No new updates! Stay tuned.\n\n"
    
    content += "=========ACTIVE TERA RAIDS=========\n"
    for raids in tera_raids:
        content += json.dumps(raids, indent=4, ensure_ascii=False) + "\n\n"
    
    content += "========ACTIVE EVENT DISTRIBUTIONS========\n"
    for event in event_distributions:
        content += json.dumps(event, indent=4, ensure_ascii=False) + "\n\n"
    
    return content

now = datetime.now();
current_date = now.strftime('%m/%d/%y')

load_dotenv()

# email details
sender_email = os.getenv("SENDER_EMAIL")
app_password = os.getenv("APP_PASSWORD")
mailing_list = os.getenv("MAILING_LIST").split(",")
subject = str(current_date) + " Pokémon Scarlet & Violet Updates"
body = format_content()

# create email message
message = MIMEMultipart()
message['From'] = sender_email
message['To'] = ", ".join(mailing_list)
message['Subject'] = subject
# attach the email body
message.attach(MIMEText(body, 'plain'))

# send email
try:
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, mailing_list, message.as_string())
        print("email sent!")
except Exception as e:
    print(f"Failed to send email: {e}")

