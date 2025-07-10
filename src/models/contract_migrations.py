from database.sqlite import Database

class ContractMigrations:

    def migrate():
        db = Database()
        db.execute("""
            CREATE TABLE IF NOT EXISTS contract (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                holder_id INTEGER NOT NULL,
                plan_id INTEGER NOT NULL,
                payment_day INTEGER NOT NULL,
                creation_date TEXT NOT NULL,
                installments_paid INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY(holder_id) REFERENCES holder(id) ON DELETE CASCADE,
                FOREIGN KEY(plan_id) REFERENCES plan(id) ON DELETE CASCADE
            )
        """, commit=True)
        db.close()
