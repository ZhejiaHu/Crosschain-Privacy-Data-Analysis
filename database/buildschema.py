import psycopg2


def connect_db():
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", port=5433)
    # Open a cursor to perform database operations
    cur = conn.cursor()
    return conn, cur


def create_relations_account_and_transaction(conn, cur):
    cur.execute("""
        CREATE TABLE "CrossChainPrivacy".Account 
        (
            Address varchar(42) PRIMARY KEY,
            Balance numeric(64, 32),
            IsContract bit
        )
        """)
    cur.execute("""
        CREATE TABLE "CrossChainPrivacy".Transaction
        (
            Hash varchar(66) PRIMARY KEY,
            Status bit,
            Time_stamp varchar(10),
            From_account varchar(42),
            To_account varchar(42),
            Net varchar(20),
            Block_num int,
            ETH numeric(64, 32),
            Gas numeric(64, 32)
        )
        """)
    cur.close()
    conn.commit()


if __name__ == "__main__":
    conn, cur = connect_db()
    create_relations_account_and_transaction(conn, cur)

