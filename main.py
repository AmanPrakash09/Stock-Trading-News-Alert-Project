import requests
from twilio.rest import Client
from datetime import datetime, timedelta

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
COMPANY_NAME_NEWS = "tesla"

api_key = "OL5A3LH0WA6OAKAQ"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": api_key,
}

response = requests.get("https://www.alphavantage.co/query", params=parameters)
response.raise_for_status()
data = response.json()

hour_5_to_22 = []
hour = 5
time_now = datetime.today()
if int(time_now.hour) < 5 or int(time_now.hour) > 20:
    today = datetime.today()
    today = today - timedelta(days=1)
    yesterday = today - timedelta(days=1)
    today_date = str(today.date())
    yesterday_date = str(yesterday.date())
else:
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    today_date = str(today.date())
    yesterday_date = str(yesterday.date())

percent_test = ((float(data["Time Series (Daily)"][today_date]["2. high"])
                 - float(data["Time Series (Daily)"][yesterday_date]["2. high"]))
                / float(data["Time Series (Daily)"][yesterday_date]["2. high"])) * 100

print(percent_test)

news_list = []

if percent_test > 0:
    text_message = f"{STOCK} 🔺{round(percent_test)}%\n"
else:
    text_message = f"{STOCK} 🔻{round(percent_test)}%\n"

news_api_key = "94d9597d02a346199eb57b6acc0ac9af"
news_parameters = {
    "q": COMPANY_NAME_NEWS,
    "from": today_date,
    "sortBy": "publishedAt",
    "apiKey": news_api_key,
    "language": "en",
}
news_response = requests.get("https://newsapi.org/v2/everything", params=news_parameters)
news_response.raise_for_status()
news_data = news_response.json()

for n in range(3):
    news_list.append(news_data["articles"][n])

index = 1
for item in news_list:
    headline = item["title"]
    brief = item["description"]
    text_message += f"Headline from News {index}: {headline}\nBriefing from News {index}: {brief}\n"
    index += 1

print(text_message)

account_sid = "AC10d8c2309f0aaa689b4647c1d03888ed"
auth_token = "a748b429f9ff61e051295b18bdbf21d7"

client = Client(account_sid, auth_token)
message = client.messages \
    .create(
    body=text_message,
    from_="+12562545697",
    to="+17787516483"
)

print(message.status)
