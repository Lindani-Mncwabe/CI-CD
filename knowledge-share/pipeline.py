import os
import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Slack authentication 
slack_bot_token = os.getenv('SLACK_BOT_TOKEN') 
channel_id = os.getenv('SLACK_CHANNEL_KNOWLEDGE_SHARE') 
slack_client = WebClient(token=slack_bot_token)

def send_slack_reminder(days_until_share):
    knowledge_share_date = (datetime.date.today() + datetime.timedelta(days=days_until_share)).strftime("%A, %B %d")
    message = (
        f"📅 *Reminder: Data Team's Bi-Weekly Knowledge Share*\n\n"
        f"Coming up in *{days_until_share} days* on *{knowledge_share_date}*.\n\n"
        "Anyone sharing anything with the team?\n\n"
        "Please prepare any topics you'd like to discuss!"
    )

    try:
        response = slack_client.chat_postMessage(channel=channel_id, text=message)
        print("Reminder sent successfully:", response["message"]["text"])
    except SlackApiError as e:
        print(f"Error sending reminder: {e.response['error']}")

def is_reminder_day():
    today = datetime.date.today()
    print("Today's date:", today)

    # Set the known bi-weekly knowledge share date
    start_date = datetime.date(2025, 1, 15)  # starting on this upcoming knowledge share date
    print("Start date:", start_date)
    
    # Adjust logic for dates before the start date
    if today < start_date:
        next_knowledge_share = start_date
    else:
        # Calculate days and weeks since start to determine the next bi-weekly session
        days_since_start = (today - start_date).days
        weeks_since_start = days_since_start // 14
        next_knowledge_share = start_date + datetime.timedelta(weeks=(weeks_since_start + 1) * 2)
    
    print("Next knowledge share date:", next_knowledge_share)

    # Check if today is 2 days before the next knowledge share
    days_until_share = (next_knowledge_share - today).days
    print("Days until knowledge share:", days_until_share)
    
    if days_until_share == 2:
        send_slack_reminder(days_until_share)
    else:
        print("Today is not 2 days before the knowledge share. No reminder sent.")

if __name__ == "__main__":
    is_reminder_day()
