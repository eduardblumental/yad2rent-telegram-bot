import os, time

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from scrapers import MainScraper, ItemScraper

from utils import build_main_url, build_item_url, get_driver, get_queries_from_json


async def send_update(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text=f'Update for {context.job.data.get("username")}!'
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    queries = get_queries_from_json()
    driver = get_driver()

    for query in queries:
        driver.get(build_main_url(query.get('city_code'), query.get('rooms'), query.get('price')))
        time.sleep(2)

        try:
            _ = MainScraper(page_source=driver.page_source)
        except Exception as e:
            context.bot.send_message(chat_id=update.message.chat_id, text=f'CAPTCHA on the way. {e}')

    driver.quit()

    await update.message.reply_text(text='Updates will follow soon...')
    context.job_queue.run_repeating(send_update, 600, name='send_update', chat_id=update.message.chat_id)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = context.job_queue.get_jobs_by_name('send_update')
    for job in jobs:
        job.schedule_removal()
    await update.message.reply_text('Updates are stopped. Press /start to continue receiving updates.')


if __name__ == "__main__":
    app = ApplicationBuilder().token(os.environ.get('TELEGRAM_BOT_TOKEN')).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()
