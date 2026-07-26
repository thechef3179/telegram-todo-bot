# ToDo Bot V1 📝

A lightweight, efficient Telegram bot designed to help you manage your tasks, track progress, and stay organized—all within the Telegram interface.

## ✨ Features

- **Task Management:** Add, list, delete, and track task statuses.
- **Priority System:** Quick task entry with default priority settings.
- **State Persistence:** Remembers your tasks and user status via a local database.
- **Bulk Cleanup:** Easily clear out old or completed tasks to keep your list fresh.
- **Subscription Management:** Users can opt-out of notifications/follow lists at any time.

## 🚀 Commands

| Command | Description |
| :--- | :--- |
| `/start` | Initialize the bot and start a new session (also get added to bot's follow list). |
| `/list` | View all your current pending tasks. |
| `/add task -p<0-9>` | Add a new task (defaults to priority `p2`). |
| `/delete <id>` | Permanently remove a task by its unique ID (can delete multiple tasks separated by space). |
| `/finish <id>` | Mark a specific task as completed (can finish multiple tasks separated by space). |
| `/unfinish <id>` | Revert a completed task back to incomplete (can unfinish multiple tasks separated by space). |
| `/clear` | Wipe all completed tasks from your list. |
| `/removeme` | Remove yourself from the bot's follow/notification list. |

## 🛠️ Tech Stack

- **Language:** [Python](https://www.python.org/)
- **Library:** [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) (Asynchronous)
- **Database:** SQLite 

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- A Telegram Bot Token from [@BotFather](https://t.me/botfather)

### 1. Clone the repository
```bash
git clone https://github.com/thechef3179/telegram-todo-bot.git
cd telegram-todo-bot
```
