from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.types import Date
from db import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    password = Column(String, nullable=False)
    creado = Column(Date)

    def __init__(self, username, nombre, apellido, password):
        self.username = username
        self.nombre = nombre
        self.apellido = apellido
        self.password = password
    def __repr__(self):
        return f'Usuario({self.username}, {self.nombre}, {self.apellido}, {self.password})'
    def __str__(self):
        return self.username


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    nombreCategoria = Column(String, nullable=False)
    creado = Column(Date)

    def __init__(self, id_usuario, nombreCategoria):
        self.id_usuario = id_usuario
        self.nombreCategoria = nombreCategoria
    def __repr__(self):
        return f'Categoria({self.id_usuario}, {self.nombreCategoria})'
    def __str__(self):
        return self.nombreCategoria

class Imagen(Base):
    __tablename__ = "imagenes"

    id = Column(Integer, primary_key=True, index=True)
    id_categoria = Column(Integer, ForeignKey('categorias.id'))
    nombre = Column(String, nullable=False)
    ruta = Column(String, nullable=False)
    subido = Column(Date)

    def __init__(self, id_categoria, nombre, ruta):
        self.id_categoria = id_categoria
        self.nombre = nombre
        self.ruta = ruta
    def __repr__(self):
        return f'Imagen({self.id_categoria}, {self.nombre}, {self.ruta})'
    def __str__(self):
        return self.nombre

class Articulo(Base):
    __tablename__ = "articulos"

    id = Column(Integer, primary_key=True, index=True)
    id_categoria = Column(Integer, ForeignKey('categorias.id'))
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio = Column(Float, nullable=False)
    creado = Column(Date)

    def __init__(self, id_categoria, id_usuario, nombre, descripcion, cantidad, precio):
        self.id_categoria = id_categoria
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.precio = precio
    def __repr__(self):
        return f'Articulo({self.id_categoria}, {self.id_usuario}, {self.nombre}, {self.descripcion}, {self.cantidad}, {self.precio})'
    def __str__(self):
        return self.nombre

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    dni = Column(String, nullable=False)
    creado = Column(Date)

    def __init__(self, id_usuario, nombre, apellido, direccion, email, telefono, dni):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.direccion = direccion
        self.email = email
        self.telefono = telefono
        self.dni = dni
    def __repr__(self):
        return f'Cliente({self.id_usuario}, {self.nombre}, {self.apellido}, {self.direccion}, {self.email}, {self.telefono}, {self.dni})'
    def __str__(self):
        return self.apellido

class Operacion(Base):
    __tablename__ = "operaciones"

    id = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey('usuarios.id'))
    id_cliente = Column(Integer, ForeignKey('clientes.id'))
    id_articulo = Column(Integer, ForeignKey('articulos.id'))
    precio = Column(Float, nullable=False)
    creado = Column(Date)

    def __init__(self, id_usuario, id_cliente, id_articulo, precio):
        self.id_usuario = id_usuario
        self.id_cliente = id_cliente
        self.id_articulo = id_articulo
        self.precio = precio
    def __repr__(self):
        return f'Operacion({self.id_usuario}, {self.id_cliente}, {self.id_articulo}, {self.precio})'
    def __str__(self):
        return self.id_cliente