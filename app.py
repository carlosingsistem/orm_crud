from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///orm.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = "product"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

        
    def __repr__(self):
        return f"Name: {self.name}\tPrice: {self.price}\tStock: {self.stock}"

def init_database():
    with app.app_context():
        db.create_all()
        print("✨ Database, product table created successfuly!")
        
def insert_product():
    with app.app_context():
        name = input("Nombre del producto: ").strip()
        price = input("Precio: ").strip()
        stock = input("Stock (Enter para valor por defecto 0): ").strip()


        if name and price and stock:
            product = Product(name=name, price=float(price), stock=int(stock))
            db.session.add(product)
            db.session.commit()
            print("✍️ Producto Insertado Exitosamente!")
                    
        product = Product(name=name, price=float(price))
        print("✨ Producto insertado con valor por defecto (0) exitosamente!")
        
def query_products():
    with app.app_context():
        # Todos los productos
        products = Product.query.all()
        c = 1
        for pro in products:
            print("----------------------------------------------")
            print(f"\t\tProducto N°{c}")
            print(pro)
            print("----------------------------------------------")
            c += 1
        # Productos que tengan stock 0
        products_filter = Product.query.filter(Product.stock == 0).all()
        # Buscar por id
        product = Product.query.filter_by(id=2).first()
        if product:
            print("----------------------------------------------")
            print("Product: ", product)
            print("----------------------------------------------")
        else:
            print("📢 Producto No Encontrado!")

def update_product():
    with app.app_context():
        id = int(input("ID: "))
        product = Product.query.filter_by(id=id).first()
        if product:
            name = input("Nombre del producto: ").strip()
            price = input("Precio: ").strip()
            stock = input("Stock (Enter para valor por defecto 0): ").strip()
            if name and price and stock:
                product.name = name
                product.price = float(price)
                product.stock = int(stock)
                
                db.session.commit()
                print("✍️ Producto Actualizado Exitosamente!")

            product.name = name
            product.price = float(price)
            
            db.session.commit()
            print("✍️ Producto Actualizado Exitosamente!")
            
        else:
            print("📢 Producto No Encontrado!")

def delete_product():
    with app.app_context():
        
        id = int(input("ID: "))
        product = Product.query.filter_by(id=id).first()
        
        if product:
            db.session.delete(product)
            print("✍️ Producto Eliminado Exitosamente!")
        else:
            print("📢 Producto No Encontrado!")
            
if __name__ == "__main__":
    init_database()
    insert_product()
    query_products()
    update_product()
    delete_product()