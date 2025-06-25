from database.sqlite import Database

class UsageContractDependentMigrations:

    def migrate():
        db = Database()
        db.execute("""
            CREATE TABLE IF NOT EXISTS usage_contract_dependent (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dependent_id INTEGER NOT NULL,
                contract_id INTEGER NOT NULL,
                usage_date TEXT NOT NULL,
                FOREIGN KEY(dependent_id) REFERENCES dependent(id),
                FOREIGN KEY(contract_id) REFERENCES contract(id)
            )
        """, commit=True)
        db.close()
