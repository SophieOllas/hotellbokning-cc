import uvicorn
import psycopg
import os
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import date

PORT=8352

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=PORT,
        ssl_keyfile="/etc/letsencrypt/privkey.pem",
        ssl_certfile="/etc/letsencrypt/fullchain.pem",
    )
# Load environment variables from .env file
load_dotenv()
DB_URL = os.getenv("DB_URL")

# Connect to the PostgreSQL database
conn = psycopg.connect(
    DB_URL,
    autocommit=True,
    row_factory=dict_row
)

class Booking(BaseModel):
    guest_id: int
    room_id: int
    datefrom: date
    dateto: date

@app.post("/bookings")
def create_booking(booking: Booking):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO hotel_bookings(
            guest_id,
            room_id,
            datefrom,
            dateto
        ) VALUES (
            %s, 
            %s,
            %s,
            %s
            )
            RETURNING id
        """, [
            booking.guest_id, 
            booking.room_id, 
            booking.datefrom, 
            booking.dateto
            ])
        new_id = cur.fetchone()['id']

    return {"msg": "Booking created successfully", "id": new_id}

@app.get("/temp/{}")
def temp():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hotel_rooms")
        rows = cur.fetchall()
    return rows


#@app.get("/if/{user_input}")
#def if_test(user_input: str):
 #   message = None
  #  if user_input == "hello" or user_input == "hi":
   #     message = user_input + " yourself!"
    #    elif user_input == "goodbye" and 1 > 0:
     #       message = "goodbye yourself!"
      #      else:
       #         message = f"I don't understand {user_input}" # f string
                # jämför js `I dont understand ${user_input}`;
    #return {"msg": message}

@app.get("/rooms")
def getRooms():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hotel_rooms ORDER BY room_number")
        rooms = cur.fetchall()
        return rooms

@app.get("/rooms/{id}")
def getOneRoom(id: int):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hotel_rooms WHERE id = %s", [id])    
        room = cur.fetchone()
        if not room:
            return {"error": "Room not found"}
        return room

# uvicorn cc3:app --host 0.0.0.0 --port 8352 --reload

# http//vm4430.kaj.pouta.csc.fi:8352/rooms