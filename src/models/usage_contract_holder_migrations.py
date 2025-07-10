from database.sqlite import Database

class UsageContractHolderMigrations:

    def migrate():
        db = Database()
        db.execute("""
            CREATE TABLE IF NOT EXISTS usage_contract_holder (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                holder_id INTEGER NOT NULL,
                contract_id INTEGER NOT NULL,
                usage_date TEXT NOT NULL,
                FOREIGN KEY(holder_id) REFERENCES holder(id) ON DELETE CASCADE,
                FOREIGN KEY(contract_id) REFERENCES contract(id) ON DELETE CASCADE
            )
        """, commit=True)
        db.close()
