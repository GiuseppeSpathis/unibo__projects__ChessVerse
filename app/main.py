import eel
import mysql.connector
import requests
from screeninfo import get_monitors
import random
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_NAME = os.getenv("DATABASE_NAME")

def get_full_screen_size():
    monitors = get_monitors()
    screen_width = max(m.width for m in monitors)
    screen_height = max(m.height for m in monitors)
    return screen_width, screen_height

screen_width, screen_height = get_full_screen_size()

conn = mysql.connector.connect(
    host=DATABASE_HOST,
    user=DATABASE_USER,
    password=DATABASE_PASSWORD,
    database=DATABASE_NAME
)

cursor = conn.cursor()

eel.init('web')

def is_nickname_in_database(nickname):
   cursor.execute("SELECT * FROM Guest WHERE Username=%s", (nickname,))
   result = cursor.fetchone()
   
   if(result is not None):
     return True
   
   return False

def generate_random_nickname():
    while True:
        random_number = random.randint(1, 1000000000)
        nickname = f'Guest-{random_number}'

        
        if not is_nickname_in_database(nickname):
            return nickname


guest_nickname = generate_random_nickname()
 
@eel.expose
def add_guest():
   insert_query = "INSERT INTO Guest (Username) VALUES (%s)"
   cursor.execute(insert_query, (guest_nickname,))
   conn.commit()

@eel.expose
def get_guest_name():
    print(guest_nickname)
    return guest_nickname


   


eel.start('login/login.html', size=(screen_width, screen_height))

cursor.close()
conn.close()