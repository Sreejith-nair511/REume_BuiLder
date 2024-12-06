import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Add new columns
try:
    c.execute('ALTER TABLE resumes ADD COLUMN image_url TEXT')
except sqlite3.OperationalError:
    pass  # The column already exists

try:
    c.execute('ALTER TABLE resumes ADD COLUMN template TEXT')
except sqlite3.OperationalError:
    pass  # The column already exists

conn.commit()
conn.close()
