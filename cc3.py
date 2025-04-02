import uvicorn
import psycopg
import os
from psycopg.rows import dict_row
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request

PORT=8352

# Load environment variables from .env file
load_dotenv()
DB_URL = os.getenv("DB_URL")

# Connect to the PostgreSQL database
conn = psycopg.connect(
    DB_URL,
    autocommit=True,
    row_factory=dict_row
)

@app.get("/temp")
def temp():
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM hotel_rooms")
        rows = cur.fetchall()
    return rows

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

# rum nummer, pris, hur många personer
rooms = [
    {"room_number": 101, "price": 1200, "capacity": 2},
    {"room_number": 102, "price": 1500, "capacity": 3},
    {"room_number": 103, "price": 1000, "capacity": 1},
    {"room_number": 104, "price": 2000, "capacity": 4},
]

@app.get("/rooms")
def getRooms(request: Request):
    return rooms

# uvicorn cc3:app --host 0.0.0.0 --port 8352 --reload

# http//vm4430.kaj.pouta.csc.fi:8352/rooms