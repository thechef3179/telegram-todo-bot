import sqlite3
import logging
from p2dmd import escape

logger = logging.getLogger(__name__)
logging.basicConfig(filename="logs/todo-v1.log", level=logging.INFO)

# function to check if table is there
def test_database(database_name: str)->int:
    con = sqlite3.connect(database_name)
    logger.info("connected to the database...")
    print("connected to the database...")
    cur = con.cursor()
    tables = cur.execute("select * from sqlite_master").fetchall()
    logger.info(f"getting tables...")
    print(f"getting tables...")
    tasks_exists_ = False
    users_exists_ = False
    for table in tables:
        if table[1] == "tasks":
            tasks_exists_ = True
            logger.info("tasks table already exists...")
            print("tasks table already exists...")
        if table[1] == "users":
            users_exists_ = True
            logger.info("users table already exists...")
            print("users table already exists...")
    if not tasks_exists_:
        logger.info("creating the tasks table...")
        print("creating the tasks table...")
        cur.execute("create table tasks(id integer primary key, status integer not null, priority integer not null, name text not null, chat_id text not null)")
        logger.info("finished creating the tasks table...")
        print("finished creating the tasks table...")
    if not users_exists_:
        logger.info("creating the users table...")
        print("creating the users table...")
        cur.execute("create table users (id integer primary key not null, chat_id text not null unique)")
        logger.info("finished creating the users table...")
        print("finished creating the users table...")
    logger.info("finished running database check...")
    print("finished running database check...")
    con.commit()
    con.close()
    return 0

# create global functions that handle database tasks
# add a task
def add_user(database_name:str, chat_id: str)->int:
    logger.info("testing db for add_user...")
    print("testing db for add_user...")
    test_database(database_name)
    con = sqlite3.connect(database_name)
    logger.info("connected to db for add_user...")
    print("connected to db for add_user...")
    cur = con.cursor()
    users = cur.execute(f"select * from users where chat_id = '{chat_id}'").fetchall()
    if len(users) > 0:
        logger.info("user already exists...")
        print("user already exists...")
        return 1
    else:
        logger.info("inserting values for add_user...")
        print("inserting values for add_user...")
        cur.execute(f"insert into users (chat_id) values ('{chat_id}')")
        logger.info("inserted values for add_user...")
        print("inserted values for add_user...")
    con.commit()
    con.close()
    return 0

# add a task
def add_task(database_name:str, name: str, chat_id: str, priority: int = 2, status: int = 0)->int:
    logger.info("testing db for add_task...")
    print("testing db for add_task...")
    test_database(database_name)
    con = sqlite3.connect(database_name)
    logger.info("connected to db for add_task...")
    print("connected to db for add_task...")
    cur = con.cursor()
    logger.info("inserting values for add_task...")
    print("inserting values for add_task...")
    cur.execute(f"insert into tasks (status, priority, name, chat_id) values ({status}, {priority}, '{name}', '{chat_id}')")
    logger.info("inserted values for add_task...")
    print("inserted values for add_task...")
    con.commit()
    con.close()
    return 0

# delete a task
def clear_completed_tasks(database_name: str, chat_id: str)->int:
    logger.info("testing db for clear_completed_tasks...")
    print("testing db for clear_completed_tasks...")
    test_database(database_name)
    con = sqlite3.connect(database_name)
    logger.info("connected to db for clear_completed_tasks...")
    print("connected to db for clear_completed_tasks...")
    cur = con.cursor()
    logger.info("deleting values for clear_completed_tasks...")
    print("deleting values for clear_completed_tasks...")
    cur.execute(f"delete from tasks where status = 1 and chat_id = '{chat_id}'")
    logger.info("deleted values for clear_completed_tasks...")
    print("deleted values for clear_completed_tasks...")
    con.commit()
    con.close()
    return 0

# delete a task
def delete_task(database_name: str, id: int, chat_id: str)->int:
    test_database(database_name)
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    logger.info("deleting values for delete_task...")
    print("deleting values for delete_task...")
    cur.execute(f"delete from tasks where id = {id} and chat_id = '{chat_id}'")
    logger.info("deleted values for delete_task...")
    print("deleted values for delete_task...")
    con.commit()
    con.close()
    return 0

# delete a user
def delete_user(database_name: str, chat_id: str)->int:
    test_database(database_name)
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    logger.info("deleting values for delete_user...")
    print("deleting values for delete_user...")
    cur.execute(f"delete from users where chat_id = '{chat_id}'")
    logger.info("deleted values for delete_user...")
    print("deleted values for delete_user...")
    con.commit()
    con.close()
    return 0

# mark a task as completed
def finish_task(database_name:str, id: int, chat_id: str)->int:
    test_database(database_name)
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    logger.info("updating values for finish_task...")
    print("updating values for finish_task...")
    cur.execute(f"update tasks set status = 1 where id = {id} and chat_id = '{chat_id}'")
    logger.info("updated values for finish_task...")
    print("updated values for finish_task...")
    con.commit()
    con.close()
    return 0

# mark a task as completed
def unfinish_task(database_name:str, id: int, chat_id: str)->int:
    test_database(database_name)
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    logger.info("updating values for unfinish_task...")
    print("updating values for unfinish_task...")
    cur.execute(f"update tasks set status = 0 where id = {id} and chat_id = '{chat_id}'")
    logger.info("updated values for unfinish_task...")
    print("updated values for unfinish_task...")
    con.commit()
    con.close()
    return 0

# list all incomplete tasks
def show_tasks(database_name: str, chat_id: str)->list:
    test_database(database_name)
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    logger.info("selecting values for show_tasks...")
    print("selecting values for show_tasks...")
    tasks = cur.execute(f"select * from tasks where chat_id = '{chat_id}' order by status asc, priority asc, id asc").fetchall()
    logger.info("selected values for show_tasks...")
    print("selected values for show_tasks...")
    output = ""
    if len(tasks) > 0:
        output += "# Here are your incomplete tasks:\n"
        for task in tasks:
            if task[1] == 0:    
                output += f"- [ ] {task[3]} -- **{task[0]}(p{task[2]})**\n"
        output += "\n\n# Here are your completed tasks:\n"
        for task in tasks:
            if task[1] == 1:    
                output += f"- [x] {task[3]} -- **{task[0]}(p{task[2]})**\n"
    else:
        output = "# You have no tasks in the list!!!\n"
    result = escape(output)
    output_parts = result.split("\n@|@|@|@\n\n")
    con.commit()
    con.close()
    return output_parts

# list all incomplete tasks
def get_user_ids(database_name: str)->list:
    test_database(database_name)
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    logging.info("selecting values for get_user_ids...")
    users = cur.execute(f"select * from users").fetchall()
    logging.info("selected values for get_user_ids...")
    ids = []
    for user in users:
        ids.append(user[1])
    return ids

