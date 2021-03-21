# PORTAL DE VENTAS - E-COMMERCE

> E-commerce that allows registering different users, creating categories, articles and generating sales with details of operations per user stored in a database.

## General info

Final proyect of CS50

## Technologies

* Flask
* Bootstrap
* Javascript

## Code Examples

Show examples of usage:
`@app.route("/clientes", methods=["GET", "POST"])
@login_required
def clientes():
    alert = "alert-warning"
    if request.method == "POST":

        result = db.session.query(Cliente).filter(Cliente.dni==request.form.get("dni_cliente"))
        for i in result:
            if request.form.get("dni_cliente") == i.dni:
                flash("Ese cliente ya existe")
                alert = "alert-warning"
                return render_template("clientes.html", alert=alert)`

## Features

List of features ready and TODOs for future development

* Create users, categories and articles
* Lookup clients for DNI number
* Record operations and display them by user

To-do list:

* Stock verified
* Generate sales order and send it to email customer

## Status

Project is: _finished_

## Inspiration

credits CS50, inspired in Finance proyect

## Contact

Created by Emiliano Modula (emilianomodula@gmail.com)
