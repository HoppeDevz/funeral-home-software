from database.sqlite import Database

class HolderDependentsMigrations:

    def migrate():
        db = Database()
        db.execute("""
            CREATE TABLE IF NOT EXISTS dependent (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                holder_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                relation INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY(holder_id) REFERENCES holder(id) ON DELETE CASCADE
            )
        """, commit=True)
        db.close()
