from database.sqlite import Database

class Plan:
    def __init__(self, id=None, name=None, monthly_price=None, installment_count=None):
        self.id = id
        self.name = name
        self.monthly_price = monthly_price
        self.installment_count = installment_count

    def create(self):
        db = Database()
        db.execute("""
            INSERT INTO plan (name, monthly_price, installment_count) VALUES (?, ?, ?)
        """, (self.name, self.monthly_price, self.installment_count), commit=True)
        self.id = db.cursor.lastrowid
        db.close()
        return self

    @staticmethod
    def list_all():
        db = Database()
        rows = db.fetchall("SELECT * FROM plan ORDER BY name")
        db.close()
        plans = []
        for row in rows:
            plans.append(Plan(
                id=row["id"],
                name=row["name"],
                monthly_price=row["monthly_price"],
                installment_count=row["installment_count"]
            ))
        return plans

    @staticmethod
    def get_by_id(plan_id):
        db = Database()
        row = db.fetchone("SELECT * FROM plan WHERE id = ?", (plan_id,))
        db.close()
        if row:
            return Plan(
                id=row["id"],
                name=row["name"],
                monthly_price=row["monthly_price"],
                installment_count=row["installment_count"]
            )
        return None

    @staticmethod
    def search_by_name(plan_name):
        db = Database()
        rows = db.fetchall("SELECT * FROM plan WHERE NAME LIKE ? ORDER BY name", (f"%{plan_name}%",))
        db.close()
        plans = []
        for row in rows:
            plans.append(Plan(
                id=row["id"],
                name=row["name"],
                monthly_price=row["monthly_price"],
                installment_count=row["installment_count"]
            ))
        return plans

    def update(self):
        db = Database()
        db.execute("""
            UPDATE plan SET name = ?, monthly_price = ?, installment_count = ? WHERE id = ?
        """, (self.name, self.monthly_price, self.installment_count, self.id), commit=True)
        db.close()

    @staticmethod
    def delete(plan_id):
        db = Database()
        db.execute("DELETE FROM plan WHERE id = ?", (plan_id,), commit=True)
        db.close()
