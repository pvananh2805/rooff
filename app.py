from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from models import db, User
from auth.routes import auth_bp
from problems.routes import problems_bp
from snippets.routes import snippets_bp
from user.routes import user_bp   # import ở đây
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login = LoginManager(app)
    login.login_view = 'auth.login'

    @login.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # đăng ký blueprint
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(problems_bp, url_prefix='/problems')
    app.register_blueprint(snippets_bp, url_prefix='/snippets')
    app.register_blueprint(user_bp, url_prefix='/user')   # 👈 đăng ký ở đây

    # inject current_user vào template
    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)

    # route trang chủ
    @app.route("/")
    def home():
        return render_template("index.html")

    with app.app_context():
        db.create_all()

        # tạo admin mặc định nếu chưa có
        if not User.query.filter_by(handle="admin").first():
            admin = User(handle="admin", email="admin@example.com", role="admin")
            admin.set_password("admin123")  # mật khẩu mặc định, nên đổi sau khi deploy
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin account created: admin / admin123")

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
