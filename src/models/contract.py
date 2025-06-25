from database.sqlite import Database

class Contract:
    def __init__(self, id=None, holder_id=None, plan_id=None, payment_day=None, creation_date=None, installments_paid=0):
        self.id = id
        self.holder_id = holder_id
        self.plan_id = plan_id
        self.payment_day = payment_day
        self.creation_date = creation_date
        self.installments_paid = installments_paid

    def create(self):
        db = Database()
        db.execute("""
            INSERT INTO contract (holder_id, plan_id, payment_day, creation_date, installments_paid)
            VALUES (?, ?, ?, ?, ?)
        """, (self.holder_id, self.plan_id, self.payment_day, self.creation_date, self.installments_paid), commit=True)
        self.id = db.cursor.lastrowid
        db.close()
        return self

    @staticmethod
    def list_by_holder(holder_id):
        db = Database()
        rows = db.fetchall("""
            SELECT c.*, p.name AS plan_name, p.monthly_price, p.installment_count
            FROM contract c
            JOIN plan p ON c.plan_id = p.id
            WHERE c.holder_id = ?
            ORDER BY c.creation_date DESC
        """, (holder_id,))
        db.close()
        contracts = []
        for row in rows:
            contract = Contract(
                id=row["id"],
                holder_id=row["holder_id"],
                plan_id=row["plan_id"],
                payment_day=row["payment_day"],
                creation_date=row["creation_date"],
                installments_paid=row["installments_paid"]
            )
            contract.plan_name = row["plan_name"]
            contract.monthly_price = row["monthly_price"]
            contract.installment_count = row["installment_count"]
            contracts.append(contract)
        return contracts

    @staticmethod
    def get_by_id(contract_id):
        db = Database()
        row = db.fetchone("""
            SELECT c.*, p.name AS plan_name, p.monthly_price, p.installment_count
            FROM contract c
            JOIN plan p ON c.plan_id = p.id
            WHERE c.id = ?
        """, (contract_id,))
        db.close()
        if row:
            contract = Contract(
                id=row["id"],
                holder_id=row["holder_id"],
                plan_id=row["plan_id"],
                payment_day=row["payment_day"],
                creation_date=row["creation_date"],
                installments_paid=row["installments_paid"]
            )
            contract.plan_name = row["plan_name"]
            contract.monthly_price = row["monthly_price"]
            contract.installment_count = row["installment_count"]
            return contract
        return None

    def update(self):
        db = Database()
        db.execute("""
            UPDATE contract
            SET holder_id = ?, plan_id = ?, payment_day = ?, creation_date = ?, installments_paid = ?
            WHERE id = ?
        """, (self.holder_id, self.plan_id, self.payment_day, self.creation_date, self.installments_paid, self.id), commit=True)
        db.close()

    @staticmethod
    def delete(contract_id):
        db = Database()
        db.execute("DELETE FROM contract WHERE id = ?", (contract_id,), commit=True)
        db.close()
