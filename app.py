import models
import db
from helpers import login_required
from db import engine
from flask import Flask, flash, jsonify, redirect, render_template, request, url_for, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from models import Usuario, Categoria, Articulo, Imagen, Cliente, Operacion


models.Base.metadata.create_all(bind=engine)

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
@login_required
def index():
    
    resultUser = db.session.query(Usuario).filter(Usuario.id==session["user_id"])
    resultOper = db.session.query(Operacion).filter(Operacion.id_usuario==session["user_id"])

    return render_template("index.html", resultOper=resultOper, resultUser=resultUser)


@app.route("/registro", methods=["GET", "POST"])
def register():
    session.clear()

    hidden = True
    alert = "alert-danger"

    if request.method == "POST":
        
        if not request.form.get("username"):
            flash("Debe proporcionar nombre de usuario")
            return render_template('registro.html', hidden=hidden, alert=alert)
        elif not request.form.get("nombre"):
            flash("Debe proporcionar nombre")
            return render_template('registro.html', hidden=hidden, alert=alert)
        elif not request.form.get("apellido"):
            flash("Debe proporcionar apellido")
            return render_template('registro.html', hidden=hidden, alert=alert)
        elif not request.form.get("confirmacion"):
            flash("Debe confirmar contraseña")
            return render_template('registro.html', hidden=hidden, alert=alert)
        elif request.form.get("password") != request.form.get("confirmacion"):
            flash("Las contraseñas no coinciden")
            return render_template('registro.html', hidden=hidden, alert=alert)
        else:
            hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

            NewUser = Usuario(request.form.get("username"), request.form.get("nombre"), request.form.get("apellido"), hash)
            db.session.add(NewUser)
            db.session.commit()
            flash("Usuario creado correctamente")
            alert = "alert-successs"
            return redirect('/login')
    
    else:
        return render_template("registro.html", hidden=hidden)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    hidden = True
    alert = "alert-danger"

    if request.method == "POST":
        
        if not request.form.get("username"):
            flash("Debe proporcionar nombre de usuario")
            return render_template('login.html', hidden=hidden, alert=alert)
        elif not request.form.get("password"):
            flash("Debe proporcionar contraseña")
            return render_template('login.html', hidden=hidden, alert=alert)
        else:
            username = request.form.get("username")
    
            rows = db.session.query(Usuario).filter(Usuario.username==username)
            for r in rows:
                hash = r.password
                id = r.id

            if rows.count() != 1 or not check_password_hash(hash, request.form.get('password')):
                flash("Nombre de usuario y/o contraseña incorrectos")
                return render_template('login.html', hidden=hidden, alert=alert)
           
            session["user_id"] = id

            return redirect('/')
    
    else:
        return render_template("login.html", hidden=hidden)



@app.route("/perfil", methods=["GET", "POST"])
def perfil():

    id = session["user_id"]
    result = db.session.query(Usuario).get(id)

    if request.method == "POST":

        if request.form.get("upd_password") != request.form.get("upd_confirmacion"):
            flash("Las contraseñas no coinciden")
            return render_template("perfil.html", username=result.username, nombre=result.nombre, apellido=result.apellido)

        if request.form.get("upd_password") != '':
            hash = generate_password_hash(request.form.get("upd_password"), method='pbkdf2:sha256', salt_length=8)
            result.password = hash

        result.nombre = request.form.get("upd_nombre")
        result.apellido = request.form.get("upd_apellido")
        db.session.commit()
        return redirect('/perfil')
    
    else:
        return render_template("perfil.html", username=result.username, nombre=result.nombre, apellido=result.apellido)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/categorias", methods=["GET", "POST"])
@login_required
def categorias():
    alert = ''
    if request.method == "POST":

        result = db.session.query(Categoria).all()
        for i in result:
            if request.form.get("new_categoria").lower() == i.nombreCategoria.lower():
                flash("Esa categoria ya existe")
                alert = "alert-warning"
                return render_template("categorias.html", alert=alert)

        NuevaCateg = Categoria(session["user_id"], request.form.get("new_categoria"))
        db.session.add(NuevaCateg)
        db.session.commit()
        flash("Categoria creada")
        alert = "alert-success"
    return render_template("categorias.html", alert=alert)


@app.route("/articulos", methods=["GET", "POST"])
@login_required
def articulos():
    alert = ''
    if request.method == "POST":

        categSelect = db.session.query(Categoria).filter(Categoria.nombreCategoria==request.form.get("categoriaSelect"))
        for i in categSelect:
            idCategoria = i.id
            nomCateg = i.nombreCategoria
        result = db.session.query(Articulo).filter(Articulo.id_categoria==idCategoria)
        for i in result:
            if request.form.get("nombre_articulo").lower() == i.nombre.lower():
                flash("Ese articulo ya existe")
                alert = "alert-warning"
                categ = db.session.query(Categoria).all()
                return render_template("articulos.html", alert=alert)

        NuevoArtic = Articulo(idCategoria, session["user_id"], request.form.get("nombre_articulo"), request.form.get("descripcion"), request.form.get("cantidad"), request.form.get("precio"))
        db.session.add(NuevoArtic)
        db.session.commit()
        flash("Articulo creado")
        alert = "alert-success"
    categ = db.session.query(Categoria).all()
    return render_template("articulos.html", alert=alert, categ=categ)


@app.route("/clientes", methods=["GET", "POST"])
@login_required
def clientes():
    alert = "alert-warning"
    if request.method == "POST":

        result = db.session.query(Cliente).filter(Cliente.dni==request.form.get("dni_cliente"))
        for i in result:
            if request.form.get("dni_cliente") == i.dni:
                flash("Ese cliente ya existe")
                alert = "alert-warning"
                return render_template("clientes.html", alert=alert)

        NuevoCli = Cliente(session["user_id"], request.form.get("nombre_cliente"), request.form.get("apellido_cliente"), request.form.get("direccion_cliente"), request.form.get("email_cliente"), request.form.get("telefono_cliente"), request.form.get("dni_cliente"))
        db.session.add(NuevoCli)
        db.session.commit()
        flash("Cliente creado")
        alert = "alert-success"
    return render_template("clientes.html", alert=alert)


@app.route("/venta", methods=["GET", "POST"])
@login_required
def venta():
    alert = ''
    existCli = False
    result = db.session.query(Cliente).filter(Cliente.dni==request.form.get("dni_cliente"))
    categSelect = request.form.get("categoriaSelect")
    articSelect = request.form.get("articuloSelect")
    cantArtic = request.form.get("cantidad")

    if request.method == "POST":

        if cantArtic:
            resultArtic = db.session.query(Articulo).filter(Articulo.nombre==articSelect)
            NuevaOp = Operacion(session["user_id"], result[0].id, resultArtic[0].id, resultArtic[0].precio)
            db.session.add(NuevaOp)
            db.session.commit()
            flash("Venta creada")
            alert = "alert-success"
            return render_template("venta.html", alert=alert, result=result)
        categ = db.session.query(Categoria).all()
        idCategoria = 0

        if categSelect:
            existCli = True
            resultCategSelect = db.session.query(Categoria).filter(Categoria.nombreCategoria==categSelect)
            for i in resultCategSelect:
                    idCategoria = i.id
                    resultArtic = db.session.query(Articulo).filter(Articulo.id_categoria==idCategoria)
                    return render_template("venta.html", existCli=existCli, result=result, resultArtic=resultArtic)

        for i in result:
            if request.form.get("dni_cliente") == i.dni:
                existCli = True
                flash("Cliente ya existente")
                alert ="alert-success"
                return render_template("venta.html", existCli=existCli, result=result, alert=alert, categ=categ)

        flash("Cliente no encontrado")
        alert = "alert-warning"
        return redirect("/clientes")
    
    return render_template("venta.html", existCli=existCli, result=result)

