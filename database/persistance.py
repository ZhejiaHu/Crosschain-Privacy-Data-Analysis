import psycopg2
from model.account import Account
from model.transaction import Transaction


conn, cur = None, None


def connect_db():
    global conn, cur
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", port=5433)
    # Open a cursor to perform database operations
    cur = conn.cursor()


def save_account(account: Account):
    global cur
    cur.execute(f"""
    INSERT INTO "CrossChainPrivacy".account (address, balance)
    VALUES ('{account.address}', {account.balance})
    """)


def save_transaction(txn: Transaction):
    global cur
    cur.execute(f"""
    INSERT INTO "CrossChainPrivacy".transaction (hash, status, time_stamp, from_account, to_account, net, block_num, eth, gas)
    VALUES ('{txn.txn_hash}', CAST({txn.status} AS BIT), '{txn.timestamp}', '{txn.from_account}', '{txn.to_account}', '{txn.net}', {txn.block_num}, {txn.value}, {txn.gas})
    """)


def close_db():
    global cur, conn
    cur.close()
    conn.commit()



