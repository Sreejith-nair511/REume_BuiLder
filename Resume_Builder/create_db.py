import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()
c.execute('''
          ALTER TABLE resumes
          ADD COLUMN image_url TEXT
          ''')
conn.commit()
conn.close()
