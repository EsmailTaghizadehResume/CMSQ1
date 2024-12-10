import os
import io
import qrcode
import zipfile
from .models import User
from shop    import app, db, bcrypt
from PIL     import Image, ImageDraw, ImageFont
from .forms  import RegistrationForm, LoginForm
from shop.products.models import Product, Brand, Category
from flask   import Flask, render_template, session, request, redirect, url_for, flash, send_file, make_response


@app.route("/admin")
def admin():
    if "email" not in session:
        flash(f"Please Log In", "danger")
        return redirect(url_for("login"))
    products = Product.query.all()
    return render_template("admin/index.html", title="Admin Page", products=products)

@app.route('/brands')
def brands():
    if "email" not in session:
        flash(f"Please Log In", "danger")
        return redirect(url_for("login"))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title="Brands Page", brands=brands)

@app.route('/categories')
def categories():
    if "email" not in session:
        flash(f"Please Log In", "danger")
        return redirect(url_for("login"))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/categories.html', title="Categories Page", categories=categories)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=hash_password,
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Welcome {form.name.data},Thank You for registering", "success")
        return redirect(url_for("login"))
    return render_template("admin/register.html", form=form, title="Register")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session["email"] = form.email.data
            flash(f"Welcome, {user.username}. You are now logged in.", "success")
            return redirect(url_for("admin"))

    return render_template("admin/login.html", form=form, title="Log In")



class QRCodeGenerator:
    def __init__(self, font_path="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"):
        self.font_path = font_path

    def create_qr_code(self, data, text):
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        
        # Prepare to draw on the image
        draw = ImageDraw.Draw(img)
        
        # Load a font
        try:
            font = ImageFont.truetype(self.font_path, 20)
        except IOError:
            font = ImageFont.load_default()
        
        # Position for text (upper left corner)
        text_position = (10, 10)
        
        # Add text to image
        draw.text(text_position, text, fill="black", font=font)
        
        return img

@app.route("/exportQRcode", methods=["GET"])
def exportQRcode():
    products = Product.query.all()
    data_text_pairs = []
    
    for i in products:
        data_text_pairs.append((url_for('product_details', id=i.id, _external=True), i.name))
        
    # Create QRCodeGenerator instance
    qr_code_generator = QRCodeGenerator()

    # Create a ZIP file in memory
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w') as zip_file:
        # Generate QR codes and save them in the ZIP file
        for data, text in data_text_pairs:
            img = qr_code_generator.create_qr_code(data, text)
            # Create a BytesIO object to hold the image
            img_buf = io.BytesIO()
            img.save(img_buf, format='PNG')
            img_buf.seek(0)  # Seek to the beginning before adding to ZIP
            zip_file.writestr(f"{text}.png", img_buf.getvalue())  # Save the QR code images with the product name

    buf.seek(0)  # Seek back to the start of the BytesIO buffer

    # Create a response with the ZIP file as an attachment
    response = make_response(send_file(buf, as_attachment=True, download_name='qr_codes.zip', mimetype='application/zip'))
    return response
    
