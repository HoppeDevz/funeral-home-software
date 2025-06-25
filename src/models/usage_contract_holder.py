from database.sqlite import Database

class UsageContractHolder:
    def __init__(self, id=None, holder_id=None, contract_id=None, usage_date=None):
        self.id = id
        self.holder_id = holder_id
        self.contract_id = contract_id
        self.usage_date = usage_date

    def create(self):
        db = Database()
        db.execute("""
            INSERT INTO usage_contract_holder (holder_id, contract_id, usage_date)
            VALUES (?, ?, ?)
        """, (self.holder_id, self.contract_id, self.usage_date), commit=True)
        self.id = db.cursor.lastrowid
        db.close()
        return self

    @staticmethod
    def list_by_contract(contract_id):
        db = Database()
        row = db.fetchone("""
            SELECT uch.*, h.name AS holder_name
            FROM usage_contract_holder uch
            JOIN holder h ON uch.holder_id = h.id
            WHERE uch.contract_id = ?
            ORDER BY uch.usage_date DESC
            LIMIT 1
        """, (contract_id,))
        db.close()
        
        if row is None:
            return None
        
        usage = UsageContractHolder(
            id=row["id"],
            holder_id=row["holder_id"],
            contract_id=row["contract_id"],
            usage_date=row["usage_date"]
        )
        usage.holder_name = row["holder_name"]
        return usage
