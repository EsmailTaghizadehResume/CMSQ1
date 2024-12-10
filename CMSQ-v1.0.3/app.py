# app.py
from shop import app, db

# Ensure that this block runs only if the script is executed directly,
# and not when imported.
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=8080)
