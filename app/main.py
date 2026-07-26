import os
import json
import re
import sqlite3
import logging
from db_controller import ( show_tasks, 
                           add_task, 
                           add_user,
                           get_user_ids,
                           delete_task, 
                           delete_user, 
                           finish_task, 
                           unfinish_task,
                           clear_completed_tasks,
                           )
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ( Application, 
                          ApplicationBuilder, 
                          Updater,
                          CallbackQueryHandler,
                          CommandHandler, 
                          MessageHandler, 
                          ContextTypes, 
                          filters,
                          )

# logging
logger = logging.getLogger(__name__)

# access the token (global variable)
# load tokens
logger.info("accessing the tokens...")
print("accessing the tokens...")
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
# load database
logger.info("loading database...")
print("loading database...")
database_name = "assets/tasks.db"
con = sqlite3.connect(database_name)
con.close()


# list handler
async def list_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global database_name
    chat_id = str(update.effective_chat.id)
    logger.info(chat_id)
    message_parts = show_tasks(database_name, chat_id)
    for message in message_parts:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='MarkdownV2')

# list handler
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global database_name
    chat_id = str(update.effective_chat.id)
    already_exists = add_user(database_name, chat_id)
    if already_exists:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="User already exists!!!")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="User added and ready to start!!!")

# finish from list handler
async def clear_finished_task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global database_name
    keyboard = [
            [
                InlineKeyboardButton("Yes", callback_data="clear_yes"),
                InlineKeyboardButton("No", callback_data="clear_no"),
                ],
            ]
    button_markdown = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Are you sure?\nThis will delete all the completed tasks!!!", reply_markup=button_markdown)
    await list_tasks(update, context)

async def clear_confirmation_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    global database_name
    chat_id = str(update.effective_chat.id)
    query = update.callback_query
    await query.answer()
    if query.data == "clear_yes":
        clear_completed_tasks(database_name, chat_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="cleared finished tasks...")
    elif query.data == "clear_no":
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Cancelled clearing the tasks...")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="error clearing the tasks...")
    await list_tasks(update, context)

# finish from list handler
async def finish_task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global database_name
    chat_id = str(update.effective_chat.id)
    message = update.message.text
    message = message[message.find(" ")+1:]
    id_lists = re.findall("[0-9]+", message)
    for id_ in id_lists:
        finish_task(database_name, id_, chat_id)
    if len(id_lists)>1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="finished those tasks...")
    elif len(id_lists)==1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="finished that task...")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="that id doesn't exist...")
    await list_tasks(update, context)

# unfinish from list handler
async def unfinish_task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global database_name
    chat_id = str(update.effective_chat.id)
    message = update.message.text
    message = message[message.find(" ")+1:]
    id_lists = re.findall("[0-9]+", message)
    for id_ in id_lists:
        unfinish_task(database_name, id_, chat_id)
    if len(id_lists)>1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="unfinished those tasks...")
    elif len(id_lists)==1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="unfinished that task...")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="that id doesn't exist...")
    await list_tasks(update, context)

# delete from list handler
async def delete_task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global database_name
    chat_id = str(update.effective_chat.id)
    message = update.message.text
    message = message[message.find(" ")+1:]
    id_lists = re.findall("[0-9]+", message)
    for id_ in id_lists:
        delete_task(database_name, id_, chat_id)
    if len(id_lists)>1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="deleted those tasks...")
    elif len(id_lists)==1:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="deleted that task...")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="that id doesn't exist...")
    await list_tasks(update, context)

# delete from list handler
async def delete_user_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global database_name
    chat_id = str(update.effective_chat.id)
    delete_user(database_name, chat_id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="removed user from mailing list...\nBye...")

# add to list handler
async def add_task_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global database_name
    chat_id = str(update.effective_chat.id)
    message = update.message.text
    message = message[message.find(" ")+1:]
    priority_find = re.findall("-[pP][0-9]", message)
    priority = 2
    if len(priority_find) > 0:
        priority = int(priority_find[0][2:])
        message = message.replace(priority_find[0], "")
    add_task(database_name, name=message, priority=priority, chat_id=chat_id)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="added to your tasks...")
    await list_tasks(update, context)

# add default handler
async def handle_default(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="This is a todo bot...\nInvalid command or message passed...")

# post init function
async def init_post(application: Application):
    global database_name
    commands = [
            ("start", "Start the todo bot"),
            ("list", "List the current tasks"),
            ("add", "Add a task (default priority set to p2)"),
            ("delete", "Delete a task (pass the task ID)"),
            ("finish", "Mark a task as complete (pass the task ID)"),
            ("unfinish", "Mark a task as incomplete (pass the task ID)"),
            ("clear", "Clear all completed tasks"),
            ("removeme", "Remove user from follow list"),
            ]
    await application.bot.set_my_commands(commands)
    users = get_user_ids(database_name)
    for user in users:
        await application.bot.send_message(chat_id=int(user), text="ToDo V1 application has started!\n\nHello...")

async def stop_post(application: Application):
    logger.info("Stopping the application...\n\n")
    print("Stopping the application...\n\n")
    users = get_user_ids(database_name)
    for user in users:
        await application.bot.send_message(chat_id=int(user), text="ToDo V1 application is shutting down!\n\nBye...")


if __name__ == "__main__":

    # start logger
    logging.basicConfig(filename="logs/todo-v1.log", level=logging.INFO)

    # create the bot
    logger.info("building the application...")
    print("building the application...")
    application = ApplicationBuilder().token(bot_token).post_init(init_post).post_stop(stop_post).build()

    # # start handling commands
    application.add_handler(CommandHandler("start", callback=start_handler))
    application.add_handler(CommandHandler("list", callback=list_tasks))
    application.add_handler(CommandHandler("add", callback=add_task_handler))
    application.add_handler(CommandHandler("delete", callback=delete_task_handler))
    application.add_handler(CommandHandler("finish", callback=finish_task_handler))
    application.add_handler(CommandHandler("unfinish", callback=unfinish_task_handler))
    application.add_handler(CommandHandler("clear", callback=clear_finished_task_handler))
    application.add_handler(CommandHandler("removeme", callback=delete_user_handler))
    application.add_handler(CallbackQueryHandler(clear_confirmation_button, pattern="clear_[yn][eo][s]*"))

    # default handler
    application.add_handler(MessageHandler(filters=None, callback=handle_default))

    # start polling
    logger.info("Starting polling...")
    print("Starting polling...")
    application.run_polling()
