from database.sqlite import Database

class UsageContractDependent:
    def __init__(self, id=None, dependent_id=None, contract_id=None, usage_date=None):
        self.id = id
        self.dependent_id = dependent_id
        self.contract_id = contract_id
        self.usage_date = usage_date

    def create(self):
        db = Database()
        db.execute("""
            INSERT INTO usage_contract_dependent (dependent_id, contract_id, usage_date)
            VALUES (?, ?, ?)
        """, (self.dependent_id, self.contract_id, self.usage_date), commit=True)
        self.id = db.cursor.lastrowid
        db.close()
        return self

    @staticmethod
    def list_by_contract(contract_id):
        db = Database()
        row = db.fetchone("""
            SELECT ucd.*, d.name AS dependent_name
            FROM usage_contract_dependent ucd
            JOIN dependent d ON ucd.dependent_id = d.id
            WHERE ucd.contract_id = ?
            ORDER BY ucd.usage_date DESC
            LIMIT 1
        """, (contract_id,))
        db.close()
        
        if row is None:
            return None
        
        usage = UsageContractDependent(
            id=row["id"],
            dependent_id=row["dependent_id"],
            contract_id=row["contract_id"],
            usage_date=row["usage_date"]
        )
        usage.dependent_name = row["dependent_name"]
        return usage

