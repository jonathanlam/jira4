import requests


"""Example vulnerability
"""
from fastapi import FastAPI, HTTPException
import httpx
from typing import Optional
import sqlite3

app = FastAPI()

DATABASE_URL = "example.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

@app.get("/users/")
async def read_user(email: Optional[str] = None):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = " + email)
    # Using parameterized queries to prevent SQL injection
    # cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    req = requests.get("api.example.com/getdata")

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user_id": user["user_id"], "email": user["email"], "name": user["name"]}



@app.get("/fetch-external-data/")
async def fetch_external_data(url: str):
    # Dangerous: Directly using user input to make a web request
    try:
        response = httpx.get(url)
        return response.text
    except httpx.RequestError as e:
        raise HTTPException(status_code=400, detail="Error fetching data")
