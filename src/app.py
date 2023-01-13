import os, time

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from scrapers import MainScraper, ItemScraper

from utils import build_item_url, get_driver, get_queries_from_json, handle_captcha, get_new_item_ids_from_query


async def send_update(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.data.get('chat_id')
    await context.bot.send_message(chat_id=chat_id, text="Как дела?")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    queries = get_queries_from_json()
    driver = get_driver()
    chat_id = update.message.chat_id

    await context.bot.send_message(chat_id=chat_id, text='Отправляюсь на Yad2, начинаю мониторить.')

    try:
        for num, query in enumerate(queries):
            _ = get_new_item_ids_from_query(driver, query)
            city, _, rooms, price = query.values()
            msg = f'<u><b>Фильтр {num+1}</b></u>\nГород: {city}\nКол-во комнат: {rooms}\nЦена: {price}₪'
            await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode=ParseMode.HTML)

        driver.quit()
        context.job_queue.run_repeating(send_update, 10, name='send_update', chat_id=chat_id, data={'chat_id': chat_id})
    except Exception as e:
        await handle_captcha(update.message.chat_id, context, e)
        await start(update, context)


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = context.job_queue.get_jobs_by_name('send_update')
    for job in jobs:
        job.schedule_removal()
    await update.message.reply_text('Поиск приостановлен. Нажмите /start чтобы возобновить поиск.')


if __name__ == "__main__":
    app = ApplicationBuilder().token(os.environ.get('TELEGRAM_BOT_TOKEN')).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))
    app.run_polling()
