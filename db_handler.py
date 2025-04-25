import sqlite3
import os
from datetime import datetime


DB_PATH = os.path.join("new_notes.db")

def initialize_db():
    conn = sqlite3.connect(DB_PATH)  # Connects to (or creates) the database file
    cursor = conn.cursor()  # Used to execute SQL commands

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            image_path TEXT,
            ocr_text TEXT,
            created_at TEXT
        )
    """)

    conn.commit()  # Saves the changes
    conn.close()   # Closes the connection

def add_note(title,image_path,ocr_text):
    conn=sqlite3.connect(DB_PATH)
    cursor=conn.cursor()
    cursor.execute("""
    INSERT INTO notes(title,image_path,ocr_text,created_at)
    VALUES (?,?,?,?)
    """,(title,image_path,ocr_text,datetime.now().isoformat()))


    conn.commit()


def get_all_notes():
    conn=sqlite3.connect(DB_PATH)
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
    notes=cursor.fetchall()
    conn.close()
    return notes