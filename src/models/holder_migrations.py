from database.sqlite import Database

class HolderMigrations:

    def migrate():
        db = Database()
        db.execute("""
            CREATE TABLE IF NOT EXISTS holder (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                birth_date TEXT NOT NULL,
                marital_status TEXT NOT NULL,
                cpf TEXT NOT NULL,
                rg TEXT NOT NULL,
                address TEXT NOT NULL,
                neighborhood TEXT NOT NULL,
                zipcode TEXT NOT NULL,
                city TEXT NOT NULL,
                phone TEXT
            )
        """, commit=True)
        db.close()
