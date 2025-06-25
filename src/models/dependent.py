from database.sqlite import Database

class Dependent:
    def __init__(self, id=None, holder_id=None, name=None):
        self.id = id
        self.holder_id = holder_id
        self.name = name

    def create(self):
        db = Database()
        db.execute("""
            INSERT INTO dependent (holder_id, name) VALUES (?, ?)
        """, (self.holder_id, self.name), commit=True)
        self.id = db.cursor.lastrowid
        db.close()
        return self

    @staticmethod
    def list_by_holder(holder_id):
        db = Database()
        rows = db.fetchall("SELECT * FROM dependent WHERE holder_id = ?", (holder_id,))
        db.close()
        dependents = []
        for row in rows:
            dependents.append(Dependent(
                id=row["id"],
                holder_id=row["holder_id"],
                name=row["name"]
            ))
        return dependents

    @staticmethod
    def get_by_id(dependent_id):
        db = Database()
        row = db.fetchone("SELECT * FROM dependent WHERE id = ?", (dependent_id,))
        db.close()
        if row:
            return Dependent(
                id=row["id"],
                holder_id=row["holder_id"],
                name=row["name"]
            )
        return None

    @staticmethod
    def update(dependent):
        db = Database()
        db.execute("""
            UPDATE dependent SET name = ?, holder_id = ? WHERE id = ?
        """, (dependent.name, dependent.holder_id, dependent.id), commit=True)
        db.close()

    @staticmethod
    def delete(dependent_id):
        db = Database()
        db.execute("DELETE FROM dependent WHERE id = ?", (dependent_id,), commit=True)
        db.close()
