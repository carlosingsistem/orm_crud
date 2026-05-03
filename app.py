from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuracion de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///orm.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Instanciamos SQLALchemy
db = SQLAlchemy(app)

# Creacion de la tabla Product con las columnas id, name, price y stock (valor por defecto 0)
class Product(db.Model):
    __tablename__ = "product"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

        
    def __repr__(self):
        return f"Name: {self.name}\tPrice: {self.price}\tStock: {self.stock}"

# Funcion para inicializar la base de datos, pues se crea la tabla Product
def init_database():
    with app.app_context():
        db.create_all()
        print("✨ Base de datos y tabla product creados exitosamente!")

# Funcion para insertar un producto 
def insert_product():
    with app.app_context():
        name = input("Nombre del producto: ").strip()
        price = input("Precio: ").strip()
        stock = input("Stock (Enter para valor por defecto 0): ").strip()

        # Si se ingresa todos los campos
        if name and price and stock:
            # Cramos un objeto Product
            product = Product(name=name, price=float(price), stock=int(stock))
            # Lo añadimos a la session
            db.session.add(product)
            # Guardamos en la BD
            db.session.commit()
            print("✍️ Producto Insertado Exitosamente!")
            return
        # Si no se ingresa el stock toma el valor por defecto antes definido (0)
        product = Product(name=name, price=float(price))
        # Lo añadimos a la session
        db.session.add(product)
        # Guardamos en la BD
        db.session.commit()
        print("✨ Producto insertado con valor por defecto (0) exitosamente!")

# Funcion para listar los productos de la base de datos, tambien filtrados por stock y id      
def query_products():
    with app.app_context():
        # Todos los productos
        products = Product.query.all()
        c = 1
        print("\t\t TODOS LOS PRODUCTOS")
        for pro in products:
            print("----------------------------------------------")
            print(f"\t\tProducto N°{c}")
            print(pro)
            print("----------------------------------------------")
            c += 1
        # Productos que tengan stock 0
        products_filter = Product.query.filter(Product.stock == 0).all()
        c = 1
        print("\tTODOS LOS PRODUCTOS CON STOCK 0")
        for pro in products_filter:
            print("----------------------------------------------")
            print(f"\t\tProducto N°{c}")
            print(pro)
            print("----------------------------------------------")
            c += 1
        print("\t\t PRODUCTO POR ID")
        # Buscar por id y mostrar el producto
        product = Product.query.filter_by(id=2).first()
        if product:
            print("----------------------------------------------")
            print(product)
            print("----------------------------------------------")
        else:
            print("📢 Producto No Encontrado!")

# Funcion para actualizar un producto existente, buscando por id
def update_product():
    with app.app_context():
        # Buscamos por ID
        id = int(input("ID: "))
        product = Product.query.filter_by(id=id).first()
        # Si el producto existe entonces hacemos la actualizacion
        if product:
            name = input("Nombre del producto: ").strip()
            price = input("Precio: ").strip()
            stock = input("Stock (Enter para valor por defecto 0): ").strip()
            # Si se ingresa todos los campos
            if name and price and stock:
                # Modificamos los atributos
                product.name = name
                product.price = float(price)
                product.stock = int(stock)
                
                db.session.commit()
                print("✍️ Producto Actualizado Exitosamente!")
                return
            # En caso de que no se ingrese el stock entonces toma el valor por defecto (0)
            product.name = name
            product.price = float(price)
            # Guardamos los cambios en la BD
            db.session.commit()
            print("✍️ Producto Actualizado Exitosamente!")
            
        else:
            print("📢 Producto No Encontrado!")

# Funcion para eliminar un producto existente de la base de datos
def delete_product():
    with app.app_context():
        # Buscamos por ID
        id = int(input("ID: "))
        product = Product.query.filter_by(id=id).first()
        # Eliminamos el producto si existe
        if product:
            # Marcar para eliminar
            db.session.delete(product)
            # Guardamos los cambios en la BD
            db.session.commit()
            print("✍️ Producto Eliminado Exitosamente!")
        else:
            print("📢 Producto No Encontrado!")
            
if __name__ == "__main__":
    init_database()
    while True:
        print("""\n
        ==================== BIENVENIDO A PRODAPP ===================
        1. Insertar un producto
        2. Mostrar todos los productos, producto con stock 0 y por id
        3. Actualizar un Producto
        4. Eliminar un producto
        5. Exit
        =============================================================
        """)
        op = int(input("Por favor selecciona una opcion: "))
        if op == 1:
            insert_product()
        elif op == 2:
            query_products()
        elif op == 3:
            update_product()
        elif op == 4:
            delete_product()
        elif op == 5:
            break
        else:
            print("Opcion invalida! Intenta de nuevo..")