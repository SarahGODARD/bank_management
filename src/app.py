import os
import psycopg2
from flask import Flask, render_template, request, url_for, redirect
from flask import jsonify

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='bank_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn

@app.route('/deposit', methods=['PUT'])
def deposit():
    name = request.form['name']
    deposit = request.form['deposit']
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT amount FROM accounts WHERE name = %s',
                (name,))
    prev_amount = cur.fetchall()
    print(prev_amount[0][0])
    amount = prev_amount[0][0]+int(deposit)
    cur.execute('UPDATE accounts SET amount = %s WHERE name = %s',
                (amount, name))
                #(str(name), str(int(deposit)+int(prev_amount)) ))
    conn.commit()
    cur.close()
    conn.close()
    return "lol" 

@app.route('/create_account', methods=['POST'])
def create():
    try:
        name = request.form['name']
        amount = request.form['amount']
        history = ["Create account", "Deposit : " + request.amount]
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('INSERT INTO accounts (name, amount, history)'
                    'VALUES (%s, %s, %s)',
                    (name, amount, history))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return str(e)
    return "lol"

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM accounts;')
    accounts = cur.fetchall()
    cur.close()
    conn.close()
    #return render_template('index.html', accounts=accounts)
    return jsonify(accounts)