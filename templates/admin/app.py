from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib
import os
from datetime import date

app = Flask(__name__)
app.secret_key = 'explorex_secret_key_2024'

DB = 'explorex.db'

# ─── DATABASE HELPER ─────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# ─── AUTH HELPERS ─────────────────────────────────────────────
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def is_logged_in():
    return 'user_id' in session

def is_admin():
    return session.get('role') == 'admin'

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_logged_in():
            flash('Please login first.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not is_admin():
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated

# ─── HOME ─────────────────────────────────────────────────────
@app.route('/')
def index():
    db = get_db()
    search   = request.args.get('search', '')
    category = request.args.get('category', '')
    budget   = request.args.get('budget', 0, type=int)

    query = "SELECT * FROM destinations WHERE 1=1"
    params = []
    if search:
        query += " AND place_name LIKE ?"
        params.append(f'%{search}%')
    if category:
        query += " AND category = ?"
        params.append(category)

    destinations = db.execute(query, params).fetchall()

    # Get min price for each destination
    dest_list = []
    for d in destinations:
        min_price = db.execute(
            "SELECT MIN(price) as min_p FROM packages WHERE destination_id=?", (d['id'],)
        ).fetchone()['min_p']
        pkg_count = db.execute(
            "SELECT COUNT(*) as c FROM packages WHERE destination_id=?", (d['id'],)
        ).fetchone()['c']
        if budget and min_price and min_price > budget:
            continue
        dest_list.append({**dict(d), 'min_price': min_price, 'pkg_count': pkg_count})

    categories = db.execute("SELECT DISTINCT category FROM destinations").fetchall()
    db.close()
    return render_template('index.html', destinations=dest_list,
                           categories=categories, search=search,
                           category=category, budget=budget)

# ─── PACKAGES ─────────────────────────────────────────────────
@app.route('/packages/<int:dest_id>')
def packages(dest_id):
    db = get_db()
    dest = db.execute("SELECT * FROM destinations WHERE id=?", (dest_id,)).fetchone()
    if not dest:
        return redirect(url_for('index'))
    pkgs = db.execute("SELECT * FROM packages WHERE destination_id=? ORDER BY price", (dest_id,)).fetchall()
    db.close()
    return render_template('packages.html', dest=dest, packages=pkgs)

# ─── BOOK ─────────────────────────────────────────────────────
@app.route('/book', methods=['POST'])
@login_required
def book():
    pkg_id     = request.form.get('package_id')
    book_date  = request.form.get('booking_date')
    num_people = int(request.form.get('number_of_people', 1))

    db = get_db()
    pkg = db.execute(
        "SELECT p.*, d.id dest_id FROM packages p JOIN destinations d ON p.destination_id=d.id WHERE p.id=?",
        (pkg_id,)
    ).fetchone()

    if not pkg:
        flash('Invalid package.', 'danger')
        return redirect(url_for('index'))

    total = pkg['price'] * num_people
    db.execute(
        "INSERT INTO bookings (user_id, package_id, booking_date, number_of_people, total_amount, status) VALUES (?,?,?,?,?,'Confirmed')",
        (session['user_id'], pkg_id, book_date, num_people, total)
    )
    db.commit()
    db.close()
    flash(f'🎉 Booking confirmed! Your trip to is booked. Total: ₹{total:,}', 'success')
    return redirect(url_for('bookings'))

# ─── MY BOOKINGS ──────────────────────────────────────────────
@app.route('/bookings')
@login_required
def bookings():
    db = get_db()
    my_bookings = db.execute(
        """SELECT b.*, p.package_name, p.duration_days, p.price as pkg_price,
                  d.place_name, d.image, d.category
           FROM bookings b
           JOIN packages p ON b.package_id=p.id
           JOIN destinations d ON p.destination_id=d.id
           WHERE b.user_id=?
           ORDER BY b.created_at DESC""",
        (session['user_id'],)
    ).fetchall()
    db.close()
    return render_template('bookings.html', bookings=my_bookings)

# ─── LOGIN ────────────────────────────────────────────────────
@app.route('/login', methods=['GET', 'POST'])
def login():
    if is_logged_in():
        return redirect(url_for('index'))
    if request.method == 'POST':
        email    = request.form.get('email')
        password = hash_password(request.form.get('password'))
        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE email=? AND password=?", (email, password)
        ).fetchone()
        db.close()
        if user:
            session['user_id'] = user['id']
            session['name']    = user['name']
            session['email']   = user['email']
            session['role']    = user['role']
            flash(f'Welcome back, {user["name"]}!', 'success')
            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')

# ─── REGISTER ─────────────────────────────────────────────────
@app.route('/register', methods=['GET', 'POST'])
def register():
    if is_logged_in():
        return redirect(url_for('index'))
    if request.method == 'POST':
        name     = request.form.get('name')
        email    = request.form.get('email')
        password = hash_password(request.form.get('password'))
        confirm  = request.form.get('confirm_password')

        if request.form.get('password') != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        db = get_db()
        exists = db.execute("SELECT id FROM users WHERE email=?", (email,)).fetchone()
        if exists:
            flash('Email already registered. Please login.', 'danger')
            db.close()
            return render_template('register.html')

        db.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?,?,?,'user')",
            (name, email, password)
        )
        db.commit()
        db.close()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# ─── LOGOUT ───────────────────────────────────────────────────
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

# ─── ADMIN DASHBOARD ──────────────────────────────────────────
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    db = get_db()
    stats = {
        'destinations': db.execute("SELECT COUNT(*) c FROM destinations").fetchone()['c'],
        'packages':     db.execute("SELECT COUNT(*) c FROM packages").fetchone()['c'],
        'bookings':     db.execute("SELECT COUNT(*) c FROM bookings").fetchone()['c'],
        'users':        db.execute("SELECT COUNT(*) c FROM users WHERE role='user'").fetchone()['c'],
        'revenue':      db.execute("SELECT COALESCE(SUM(total_amount),0) s FROM bookings WHERE status='Confirmed'").fetchone()['s'],
    }
    top_dest = db.execute(
        """SELECT d.place_name, COUNT(b.id) cnt FROM bookings b
           JOIN packages p ON b.package_id=p.id
           JOIN destinations d ON p.destination_id=d.id
           GROUP BY d.id ORDER BY cnt DESC LIMIT 1"""
    ).fetchone()
    recent = db.execute(
        """SELECT b.*, u.name user_name, p.package_name, d.place_name
           FROM bookings b
           JOIN users u ON b.user_id=u.id
           JOIN packages p ON b.package_id=p.id
           JOIN destinations d ON p.destination_id=d.id
           ORDER BY b.created_at DESC LIMIT 8"""
    ).fetchall()
    db.close()
    return render_template('admin/dashboard.html', stats=stats, top_dest=top_dest, recent=recent)

# ─── ADMIN DESTINATIONS ───────────────────────────────────────
@app.route('/admin/destinations', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_destinations():
    db = get_db()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            db.execute(
                "INSERT INTO destinations (place_name, description, image, category) VALUES (?,?,?,?)",
                (request.form['place_name'], request.form['description'],
                 request.form['image'], request.form['category'])
            )
            db.commit()
            flash('Destination added!', 'success')
        elif action == 'edit':
            db.execute(
                "UPDATE destinations SET place_name=?, description=?, image=?, category=? WHERE id=?",
                (request.form['place_name'], request.form['description'],
                 request.form['image'], request.form['category'], request.form['id'])
            )
            db.commit()
            flash('Destination updated!', 'success')
        elif action == 'delete':
            db.execute("DELETE FROM destinations WHERE id=?", (request.form['id'],))
            db.commit()
            flash('Destination deleted.', 'success')
        db.close()
        return redirect(url_for('admin_destinations'))

    destinations = db.execute("SELECT * FROM destinations ORDER BY place_name").fetchall()
    dest_list = []
    for d in destinations:
        pkg_count = db.execute("SELECT COUNT(*) c FROM packages WHERE destination_id=?", (d['id'],)).fetchone()['c']
        dest_list.append({**dict(d), 'pkg_count': pkg_count})
    db.close()
    return render_template('admin/destinations.html', destinations=dest_list)

# ─── ADMIN PACKAGES ───────────────────────────────────────────
@app.route('/admin/packages', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_packages():
    db = get_db()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            db.execute(
                "INSERT INTO packages (destination_id, package_name, price, duration_days, details, includes) VALUES (?,?,?,?,?,?)",
                (request.form['destination_id'], request.form['package_name'],
                 request.form['price'], request.form['duration_days'],
                 request.form['details'], request.form['includes'])
            )
            db.commit()
            flash('Package added!', 'success')
        elif action == 'edit':
            db.execute(
                "UPDATE packages SET package_name=?, price=?, duration_days=?, details=?, includes=? WHERE id=?",
                (request.form['package_name'], request.form['price'],
                 request.form['duration_days'], request.form['details'],
                 request.form['includes'], request.form['id'])
            )
            db.commit()
            flash('Package updated!', 'success')
        elif action == 'delete':
            db.execute("DELETE FROM packages WHERE id=?", (request.form['id'],))
            db.commit()
            flash('Package deleted.', 'success')
        db.close()
        return redirect(url_for('admin_packages'))

    filter_dest = request.args.get('dest', 0, type=int)
    if filter_dest:
        packages = db.execute(
            "SELECT p.*, d.place_name FROM packages p JOIN destinations d ON p.destination_id=d.id WHERE p.destination_id=? ORDER BY p.price",
            (filter_dest,)
        ).fetchall()
    else:
        packages = db.execute(
            "SELECT p.*, d.place_name FROM packages p JOIN destinations d ON p.destination_id=d.id ORDER BY d.place_name, p.price"
        ).fetchall()
    destinations = db.execute("SELECT * FROM destinations ORDER BY place_name").fetchall()
    db.close()
    return render_template('admin/packages.html', packages=packages, destinations=destinations, filter_dest=filter_dest)

# ─── ADMIN BOOKINGS ───────────────────────────────────────────
@app.route('/admin/bookings', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_bookings():
    db = get_db()
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'status':
            db.execute("UPDATE bookings SET status=? WHERE id=?",
                      (request.form['status'], request.form['booking_id']))
            db.commit()
            flash('Booking status updated!', 'success')
        elif action == 'delete':
            db.execute("DELETE FROM bookings WHERE id=?", (request.form['booking_id'],))
            db.commit()
            flash('Booking deleted.', 'success')
        db.close()
        return redirect(url_for('admin_bookings'))

    filter_status = request.args.get('status', '')
    query = """SELECT b.*, u.name user_name, u.email user_email,
                      p.package_name, p.duration_days, d.place_name
               FROM bookings b
               JOIN users u ON b.user_id=u.id
               JOIN packages p ON b.package_id=p.id
               JOIN destinations d ON p.destination_id=d.id
               WHERE 1=1"""
    params = []
    if filter_status:
        query += " AND b.status=?"
        params.append(filter_status)
    query += " ORDER BY b.created_at DESC"
    bookings = db.execute(query, params).fetchall()
    revenue  = db.execute("SELECT COALESCE(SUM(total_amount),0) s FROM bookings WHERE status='Confirmed'").fetchone()['s']
    db.close()
    return render_template('admin/bookings.html', bookings=bookings,
                           revenue=revenue, filter_status=filter_status)

# ─── ADMIN USERS ──────────────────────────────────────────────
@app.route('/admin/users', methods=['GET','POST'])
@login_required
@admin_required
def admin_users():
    db = get_db()
    if request.method == 'POST':
        uid = request.form.get('user_id')
        if int(uid) != session['user_id']:
            db.execute("DELETE FROM users WHERE id=? AND role='user'", (uid,))
            db.commit()
            flash('User deleted.', 'success')
        else:
            flash('Cannot delete your own account.', 'danger')
        db.close()
        return redirect(url_for('admin_users'))

    users = db.execute(
        """SELECT u.*, COUNT(b.id) booking_count, COALESCE(SUM(b.total_amount),0) total_spent
           FROM users u LEFT JOIN bookings b ON u.id=b.user_id
           GROUP BY u.id ORDER BY u.created_at DESC"""
    ).fetchall()
    db.close()
    return render_template('admin/users.html', users=users)

# ─── RUN ──────────────────────────────────────────────────────
if __name__ == '__main__':
    app.run(debug=True)
