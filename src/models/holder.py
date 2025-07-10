from database.sqlite import Database

class Holder:
    
    def __init__(self, id=None, name=None, birth_date=None, marital_status=None, cpf=None, rg=None,
                 address=None, neighborhood=None, zipcode=None, city=None, phone=None):
        self.id = id
        self.name = name
        self.birth_date = birth_date
        self.marital_status = marital_status
        self.cpf = cpf
        self.rg = rg
        self.address = address
        self.neighborhood = neighborhood
        self.zipcode = zipcode
        self.city = city
        self.phone = phone

    def create(self):
        db = Database()
        db.execute("""
            INSERT INTO holder (
                name, birth_date, marital_status, cpf, rg,
                address, neighborhood, zipcode, city, phone
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            self.name, self.birth_date, self.marital_status, self.cpf, self.rg,
            self.address, self.neighborhood, self.zipcode, self.city, self.phone
        ), commit=True)
        # Fetch last inserted id
        self.id = db.cursor.lastrowid
        db.close()
        return self

    @staticmethod
    def get_by_id(holder_id):
        db = Database()
        row = db.fetchone("SELECT * FROM holder WHERE id = ?", (holder_id,))
        db.close()
        if row:
            return Holder(
                id=row["id"],
                name=row["name"],
                birth_date=row["birth_date"],
                marital_status=row["marital_status"],
                cpf=row["cpf"],
                rg=row["rg"],
                address=row["address"],
                neighborhood=row["neighborhood"],
                zipcode=row["zipcode"],
                city=row["city"],
                phone=row["phone"]
            )
        return None

    @staticmethod
    def search_by_name(name_query):
        db = Database()
        rows = db.fetchall("SELECT * FROM holder WHERE name LIKE ?", (f"%{name_query}%",))
        db.close()
        holders = []
        for row in rows:
            holders.append(Holder(
                id=row["id"],
                name=row["name"],
                birth_date=row["birth_date"],
                marital_status=row["marital_status"],
                cpf=row["cpf"],
                rg=row["rg"],
                address=row["address"],
                neighborhood=row["neighborhood"],
                zipcode=row["zipcode"],
                city=row["city"],
                phone=row["phone"]
            ))
        return holders

    def update(self):
        db = Database()
        db.execute("""
            UPDATE holder SET
                name = ?,
                birth_date = ?,
                marital_status = ?,
                cpf = ?,
                rg = ?,
                address = ?,
                neighborhood = ?,
                zipcode = ?,
                city = ?,
                phone = ?
            WHERE id = ?
        """, (
            self.name, self.birth_date, self.marital_status, self.cpf, self.rg,
            self.address, self.neighborhood, self.zipcode, self.city, self.phone,
            self.id
        ), commit=True)
        db.close()

    def delete(self):
        db = Database()
        db.execute("DELETE FROM holder WHERE id = ?", (self.id,), commit=True)
        db.close()
