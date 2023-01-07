import os

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


async def send_update(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text=f'Update for {context.job.data.get("username")}!'
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    data = {'username': update.effective_user.username}
    await update.message.reply_text(text='Updates will follow soon...')
    context.job_queue.run_repeating(send_update, 3, name='send_update', data=data, chat_id=chat_id)


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
