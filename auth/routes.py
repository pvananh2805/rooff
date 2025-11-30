# auth/routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import db, User

# 👇 tạo blueprint
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        handle = request.form.get("handle")
        password = request.form.get("password")
        user = User.query.filter((User.handle == handle) | (User.email == handle)).first()
        if user and user.check_password(password):
            login_user(user)
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for("home"))
        else:
            flash("Sai tài khoản hoặc mật khẩu", "danger")
    return render_template("auth_login.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Đã đăng xuất", "info")
    return redirect(url_for("home"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        handle = request.form.get("handle")
        email = request.form.get("email")
        password = request.form.get("password")
        if User.query.filter_by(handle=handle).first():
            flash("Handle đã tồn tại", "danger")
        elif User.query.filter_by(email=email).first():
            flash("Email đã tồn tại", "danger")
        else:
            user = User(handle=handle, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Đăng ký thành công, hãy đăng nhập!", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth_register.html")
