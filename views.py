from flask import abort, request, session, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from markdown import markdown
from datetime import datetime
from uuid import uuid4
from os import path

from models import *


@app.before_request
def clear_trailing():
    """
    Remove trailing slashes from URL paths before processing.

    If a URL path ends with a '/', this function redirects to the same URL without the trailing '/'.

    Returns:
        redirect: A redirect to the URL without the trailing slash.
    """

    rp = request.path
    if rp != "/" and rp.endswith("/"):
        return redirect(rp[:-1])


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Handle user registration and account creation.

    Returns:
        render_template: Renders the register.html template with relevant data.
    """

    logout()

    msg = ""
    if (
        request.method == "POST"
        and "id" in request.form
        and "password" in request.form
        and "confirm-password" in request.form
        and "name" in request.form
        and "phone" in request.form
        and "email" in request.form
        and "address" in request.form
    ):
        id = request.form["id"]
        password = request.form["password"]
        confirm_password = request.form["confirm-password"]
        name = request.form["name"]
        phone = request.form["phone"]
        email = request.form["email"]
        address = request.form["address"]

        user = User.query.filter_by(id=id).first()

        if user:
            msg = "User already registered with that ID."
        elif len(id) != 14 or not id.isdigit():
            msg = "Incorrect ID entered."
        elif len(password) < 6 or len(password) > 28:
            msg = "Your password needs to be between 6 and 28 letters long."
        elif confirm_password != password:
            msg = "Your passwords don't match! Try typing them again."
        elif (
            not id
            or not password
            or not confirm_password
            or not name
            or not phone
            or not email
            or not address
        ):
            msg = "It looks like you forgot to fill out a few fields."
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(
                id=id,
                password=hashed_password,
                name=name,
                phone=phone,
                email=email,
                address=address,
                is_admin=0,
            )

            db.session.add(new_user)
            db.session.commit()
            user = User.query.filter_by(id=id).first()
            session["loggedin"] = True
            session["id"] = user.id
            session["is_admin"] = user.is_admin
            msg = "Your account has been successfully created."

            return redirect(url_for("index"))
    elif request.method == "POST":
        msg = "Please make sure you filled out the form before you continue."

    return render_template("register.html", msg=msg)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login and session creation.

    Returns:
        render_template: Renders the login.html template with relevant data.
    """

    logout()

    msg = ""
    if request.method == "POST" and "id" in request.form and "password" in request.form:
        id = request.form["id"]
        password = request.form["password"]

        user = User.query.filter_by(id=id).first()
        if not user:
            msg = "Account not found!"
        elif not id or not password:
            msg = "Please fill out the form."
        elif user:
            if check_password_hash(user.password, password):
                session["loggedin"] = True
                session["id"] = user.id
                session["is_admin"] = user.is_admin
                msg = "You're logged in successfully."

                return redirect(url_for("index"))
            else:
                msg = "Wrong password! Try again?"

    elif request.method == "POST":
        msg = "Please make sure you filled out the form before you continue."

    return render_template("login.html", msg=msg)


@app.route("/logout")
def logout():
    """
    Log out the current user and clear their session.

    Returns:
        redirect: Redirects to the index page after logging out.
    """

    session.pop("loggedin", None)
    session.pop("id", None)
    session.pop("is_admin", None)
    return redirect(url_for("index"))


@app.route("/account")
def account():
    user = User.query.filter_by(id=session["id"]).first()
    return render_template("account.html", user=user)


@app.route("/departments")
def departments():
    departments = Department.query.all()
    return render_template(
        "list.html",
        list_title="Departments",
        list_description="You may select a department to access further details or view its services.",
        path="department",
        items=departments,
    )


@app.route("/departments/<id>")
def department(id):
    department = Department.query.filter_by(id=id).first()
    if not department:
        abort(404)
    all_services_url = url_for("department_services", id=department.id)
    return render_template(
        "listing.html",
        type="department",
        item=department,
        all_services_url=all_services_url,
    )


@app.route("/departments/<id>/services")
def department_services(id):
    department = Department.query.filter_by(id=id).first()
    if not department:
        abort(404)
    services = Service.query.filter_by(department_id=id).all()
    return render_template(
        "list.html",
        list_title=f"{department.title} Services",
        list_description="You may select a service to access additional details or place an order.",
        path="service",
        items=services,
    )


@app.route("/services")
def services():
    services = Service.query.all()
    return render_template(
        "list.html",
        list_title="Services",
        list_description="You may select a service to access additional details or place an order.",
        item_type="all_services",
        path="service",
        items=services,
        Department=Department,
    )


@app.route("/services/<id>")
def service(id):
    service = Service.query.filter_by(id=id).first()
    if not service:
        abort(404)
    readme = markdown(service.readme)
    return render_template(
        "listing.html",
        type="service",
        item=service,
        Department=Department,
        readme=readme,
    )


@app.route("/new_order", methods=["GET", "POST"])
def new_order():
    if "loggedin" not in session:
        return url_for("login")
    services = Service.query.all()
    recommend = request.args.get("recommend")
    msg = ""

    if request.method == "POST" and "service" in request.form:
        service = request.form["service"]
        details = request.form["details"] if "details" in request.form else None

        files = request.files.getlist("file")
        file_paths = []
        if not all(file.filename == '' for file in files):
            for file in files:
                filename = str(uuid4()) + "_" + secure_filename(file.filename)
                file.save(path.join(app.config["UPLOAD_DIRECTORY"], filename))
                file_paths.append(filename)

        new_order = Order(
            details=details,
            start_date=datetime.now(),
            service_id=int(service),
            user_id=session["id"],
            file_paths=",".join(file_paths) if file_paths else None,
        )
        db.session.add(new_order)
        db.session.commit()
        msg = "Order was created successfully."

    elif request.method == "POST":
        msg = "Please make sure you filled out the form before you continue."

    return render_template(
        "new_order.html",
        services=services,
        recommend=recommend,
        int=int,
        msg=msg,
    )


@app.route("/new", methods=["GET", "POST"])
def new():
    if "loggedin" not in session or session["is_admin"] == False:
        abort(401)
    departments = Department.query.all()
    recommend = request.args.get("recommend")
    msg = ""

    if (
        request.method == "POST"
        and "title" in request.form
        and "description" in request.form
        and "type" in request.form
        and "associated" in request.form
    ):
        title = request.form["title"]
        description = request.form["description"]
        readme = request.form["readme"] if "readme" in request.form else None
        type_of = request.form["type"]
        associated_with = (
            request.form["associated"] if request.form["associated"] != "none" else None
        )

        existing = (
            Department.query.filter_by(title=title).first()
            or Service.query.filter_by(title=title).first()
        )
        if existing:
            msg = f"A Service or Department already exists with the same name."
        elif type_of == "Department":
            new = Department(
                title=title,
                description=description,
                readme=readme,
            )
            db.session.add(new)
            db.session.commit()
            msg = "Department was created successfully."
        elif type_of == "Service":
            department = Department.query.filter_by(id=associated_with).first()
            if department:
                new = Service(
                    title=title,
                    description=description,
                    readme=readme,
                    department_id=department.id,
                )
            else:
                new = Service(
                    title=title,
                    description=description,
                    readme=readme,
                )

            db.session.add(new)
            db.session.commit()
            msg = "Service was created successfully."

    elif request.method == "POST":
        msg = "Please make sure you filled out the form before you continue."

    return render_template(
        "new.html", departments=departments, recommend=recommend, msg=msg
    )


@app.errorhandler(404)
def page_not_found(e):
    """
    Handle a 404 Page Not Found error.

    Args:
        e: The error object.

    Returns:
        render_template: Renders the 404.html template for a 404 error.
    """

    return render_template("404.html"), 404


@app.errorhandler(401)
def unauthorized(e):
    """
    Handle an unauthorized (401) error.

    Args:
        e: The error object.

    Returns:
        redirect: Redirects to the index page for an unauthorized user.
    """

    return redirect(url_for("index"))
