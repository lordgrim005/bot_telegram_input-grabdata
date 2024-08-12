import logging
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Set up credentials and gspread client
creds = Credentials.from_service_account_file(
    r'D:\Python\bottelkom-432002-d2d58722fb82.json', 
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)
client = gspread.authorize(creds)

# Function to add data to Google Sheet
def add_data_to_sheet(data):
    sheet = client.open_by_key('1SRf9mizZC3H5k37cbrTJ5brCXexqFaiUSEQloYJmSng').worksheet('Sheet1')
    sheet.append_row(data)

# Function to get data from Google Sheet
def get_data_from_sheet(range_name):
    sheet = client.open_by_key('1SRf9mizZC3H5k37cbrTJ5brCXexqFaiUSEQloYJmSng').worksheet('Sheet1')
    data = sheet.get(range_name)
    return data

# Command handler to start the bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Send me a message and I will log it to the Google Sheet.')

# Command handler to get data from the sheet
async def get_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data_range = 'A1:D10'  # Specify the range you want to fetch data from
    data = get_data_from_sheet(data_range)
    formatted_data = "\n".join([", ".join(row) for row in data])
    await update.message.reply_text(f"Data from sheet:\n{formatted_data}")

# Message handler to handle incoming messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text
    user = update.message.from_user
    data = [user.id, user.username, user.first_name, message_text]
    add_data_to_sheet(data)
    await update.message.reply_text('Message logged!')

# Main function
def main():
    application = ApplicationBuilder().token('7168782157:AAGkP7JYoqIu1VCl6_-G6BPDJmt1csau8ck').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getdata", get_data))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()

if __name__ == '__main__':
    main()
