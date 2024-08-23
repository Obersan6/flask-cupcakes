# seed.py
from app import app
from models import db, Cupcake

# Use the app context to interact with the database
with app.app_context():
    db.drop_all()  
    db.create_all()  

    # Seed data
    c1 = Cupcake(
        flavor="cherry",
        size="large",
        rating=5,
    )

    c2 = Cupcake(
        flavor="chocolate",
        size="small",
        rating=9,
        image="https://www.bakedbyrachel.com/wp-content/uploads/2018/01/chocolatecupcakesccfrosting1_bakedbyrachel.jpg"
    )

    db.session.add_all([c1, c2])
    db.session.commit()

