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
    INSERT INTO "CrossChainPrivacy".account (address, balance, iscontract, chain_id)
    VALUES ('{account.address}', {account.balance}, CAST({1 if account.is_contract else 0} AS BIT), {account.chain_id})
    """)


def save_transaction(txn: Transaction):
    global cur
    cur.execute(f"""
    INSERT INTO "CrossChainPrivacy".transaction (hash, status, time_stamp, from_account, to_account, block_num, eth, gas, chain_id)
    VALUES ('{txn.txn_hash}', CAST({txn.status} AS BIT), '{txn.timestamp}', '{txn.from_account}', '{txn.to_account}', {txn.block_num}, {txn.value}, {txn.gas}, {txn.chain_id})
    """)


def close_db():
    global cur, conn
    cur.close()
    conn.commit()



