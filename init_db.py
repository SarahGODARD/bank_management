import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="bank_db",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS accounts;')
cur.execute('CREATE TABLE accounts (id serial PRIMARY KEY,'
                                 'name varchar (150) NOT NULL,'
                                 'amount integer NOT NULL,'
                                 'history text[],'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

# Insert data into the table

cur.execute('INSERT INTO accounts (name, amount, history)'
            'VALUES (%s, %s, %s)',
            ('Arisha Barron',
             600,
             ['deposit : 600;'])
            )

conn.commit()
cur.close()
conn.close()