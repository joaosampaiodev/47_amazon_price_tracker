from email import header
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

item = {
    'name': 'Samsung Galaxy S22 Ultra',
    'price': 2000,
    'url': 'https://www.amazon.de/dp/B09QH3B75W?pd_rd_i=B09QH3B75W&pd_rd_w=yOFL0&pf_rd_p=fee39403-4f80-4998-8cd6-6f73927e90b2&pd_rd_wg=hhH8D&pf_rd_r=PQX24B8KV858GMA8DZ7Z&pd_rd_r=b9ce84bc-8646-4cc6-bc69-7773b8816498'
}

my_http_header = {
    'Accepted-Language': 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

response = requests.get(url=item['url'], headers=my_http_header)

load_dotenv()

email  = os.getenv('GMAIL_EMAIL')
password  = os.getenv('GMAIL_PASSWORD')


def send_email(item, low_price):
    msg = EmailMessage()

    msg['Subject'] = 'Amazon price notification'
    msg['From'] = email
    msg['To'] = "jpcs5917@hotmail.com"

    connection = smtplib.SMTP('smtp.gmail.com', 587)
    connection.starttls()
    connection.login(user=email, password=password)

    msg.set_content(f"The price for {item['name']} is {low_price}")
    connection.send_message(msg)
    print(f"Notification sent!")





with open('page.html','w', encoding='utf-8') as file:
    page = response.text
    file.write(page)

soup = BeautifulSoup(page, 'html.parser')

whole_tag = soup.find(name='span', class_='a-price-whole')
fraction_tag = soup.find(name='span', class_='a-price-fraction')

whole = int(whole_tag.getText().replace(',','').replace('.','')) 
fraction = int(fraction_tag.getText())*0.01

price = whole + fraction

if price < item['price']:
    send_email(item, price)