"""Flask app for Cupcakes"""

from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_debugtoolbar import DebugToolbarExtension 
from models import db, connect_db, Cupcake

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Caccolino5@localhost/cupcake'
app.config['SECRET_KEY'] = 'abcd1234'
app.config['DEBUG_TB_INTERCEPT_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

debug = DebugToolbarExtension(app)

connect_db(app)

# Static route

# Homepage 
@app.route('/')
def homepage():
   """
   This should return an HTML page that is entirely static (the route should just render the template, without providing any information on cupcakes in the database). 
   
   Simply show an empty list of the cupcakes and a form where new cupcakes can be added. 
   """
   cupcakes = Cupcake.query.all()
   return render_template('index.html', cupcakes=cupcakes)

# API Routes

# Get all cupcakes
@app.route('/api/cupcakes')
def list_cupcakes():
    """Get all cupcakes data and respond with JSON."""

    # Loop over the cupcakes 
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]

    # jsonify 'all_cupcakes'
    return jsonify(cupcakes=all_cupcakes)

# Get a cupcake
@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """
    Get data from a specific cupcake and respond with JSON.
    If a cupcake can't be found it should raise a 404.
    """

    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

# Create a cupcake
@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    """
    Create a cupcake with: flavor, size, rating, image.
    Respond with JSON.
    """

    # Make new instance of Cupcake
    data = request.json
    new_cupcake = Cupcake(
        flavor=request.json['flavor'],
        size=request.json['size'],
        rating=request.json['rating'],
        image=request.json['image']        
        )
    db.session.add(new_cupcake)
    db.session.commit()

    return jsonify(cupcake = new_cupcake.serialize()), 201

# Update a cupcake
@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """
    Update the details of an existing cupcake specified by the cupcake ID.

    This route handles PATCH requests to update the attributes of a cupcake.
    It retrieves the cupcake with the given ID from the database, updates: flavor, size, rating, and image fields based on the JSON data provided in the request body. 
    
    If any field is not provided in the request, its current value is preserved. 
    
    After updating the cupcake, the changes are committed to the database.

    Returns:
        JSON response containing the updated cupcake data with the following 
        structure:
        {
            "cupcake": {
                "id": <cupcake_id>,
                "flavor": <flavor>,
                "size": <size>,
                "rating": <rating>,
                "image": <image_url>
            }
        }
    """

    # Retrieve the corresponding cupcake by id
    cupcake = Cupcake.query.get_or_404(id)
    
    # Update the cupcake fields with the data from the request
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    
    # Commit the changes to the database
    db.session.commit()

    # Return the updated cupcake as JSON
    return jsonify(cupcake=cupcake.serialize())

# Delete a cupcake
@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    """"
    This should raise a 404 if the cupcake cannot be found.
    
    Delete cupcake with the id passed in the URL. Respond with JSON like:
      {message: "Deleted"}.
    """
    
    # Retrieve the corresponding cupcake by id
    cupcake = Cupcake.query.get_or_404(id)
    # Delete the cupcake
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message='deleted')



