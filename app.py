import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cci-itam-2026'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres.yyosujggynmcbhfqgrwg:3srdUc8IFDiUkbJu@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Asset(db.Model):
    __tablename__ = 'asset_labels'
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100))
    qr_asset_code = db.Column(db.String(50), unique=True)
    date_encoded = db.Column(db.Date, default=date.today)
    control_number = db.Column(db.String(50))
    item_description = db.Column(db.Text)
    issued_to = db.Column(db.String(100))
    date_purchase = db.Column(db.Date)
    status = db.Column(db.String(20), default="Available")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Login Failed', 'danger')
    return render_template('login.html')


@app.route('/')
@login_required
def dashboard():
    stats = {'total': Asset.query.count(), 'avail': Asset.query.filter_by(status='Available').count()}
    return render_template('dashboard.html', stats=stats)


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        try:
            new_asset = Asset(
                company=request.form['company'],
                qr_asset_code=request.form['qr_code'].upper(),
                control_number=request.form.get('control_num'),
                item_description=request.form.get('description'),
                issued_to=request.form.get('issued_to'),
                date_purchase=datetime.strptime(request.form['purchase_date'], '%Y-%m-%d').date(),
                status='Available'
            )
            db.session.add(new_asset)
            db.session.commit()
            flash('Asset Registered Successfully!', 'success')
            return redirect(url_for('inventory'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'danger')

    return render_template('register.html', today=date.today().isoformat(), today_str=date.today().strftime('%m/%d/%Y'))


@app.route('/inventory')
@login_required
def inventory():
    assets = Asset.query.order_by(Asset.id.desc()).all()
    return render_template('inventory.html', assets=assets)


@app.route('/logout')
def logout():
    logout_user();
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)