from database.sqlite import Database

class PlanMigrations:

    def migrate():
        db = Database()
        db.execute("""
            CREATE TABLE IF NOT EXISTS plan (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                monthly_price REAL NOT NULL,
                installment_count INTEGER NOT NULL
            )
        """, commit=True)
        db.close()
