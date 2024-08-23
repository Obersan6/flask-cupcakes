from unittest import TestCase
from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}

class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    @classmethod
    def setUpClass(cls):
        """Set up test database and create tables."""
        with app.app_context():
            db.drop_all()
            db.create_all()

    def setUp(self):
        """Make demo data."""
        with app.app_context():
            Cupcake.query.delete()

            cupcake = Cupcake(**CUPCAKE_DATA)
            db.session.add(cupcake)
            db.session.commit()

            db.session.refresh(cupcake)  # Ensure the instance is attached to the session
            self.cupcake = cupcake

    def tearDown(self):
        """Clean up fouled transactions."""
        with app.app_context():
            db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2, follow_redirects=True)  # Follow redirects

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):
        with app.test_client() as client:
            # Update data for the cupcake
            updated_data = {
                "flavor": "UpdatedFlavor",
                "size": "UpdatedSize",
                "rating": 4.5,
                "image": "http://updated.com/cupcake.jpg"
            }
    
            # Perform the PATCH request to update the cupcake
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.patch(url, json=updated_data)
    
            # Check that the response status code is 200 OK
            self.assertEqual(resp.status_code, 200)
    
            # Check the response data
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "UpdatedFlavor",
                    "size": "UpdatedSize",
                    "rating": 4.5,
                    "image": "http://updated.com/cupcake.jpg"
                }
            })
    
            # Ensure the cupcake data is updated in the database
            updated_cupcake = Cupcake.query.get(self.cupcake.id)
            self.assertEqual(updated_cupcake.flavor, "UpdatedFlavor")
            self.assertEqual(updated_cupcake.size, "UpdatedSize")
            self.assertEqual(updated_cupcake.rating, 4.5)
            self.assertEqual(updated_cupcake.image, "http://updated.com/cupcake.jpg")
    
    def test_delete_cupcake(self):
        with app.test_client() as client:
            # Create a cupcake for testing
            new_cupcake = Cupcake(
                flavor="TestFlavor",
                size="TestSize",
                rating=5,
                image="http://example.com/test_cupcake.jpg"
            )
            db.session.add(new_cupcake)
            db.session.commit()

            # Store the ID of the newly created cupcake
            cupcake_id = new_cupcake.id

            # Perform the DELETE request
            url = f"/api/cupcakes/{cupcake_id}"
            resp = client.delete(url)

            # Check that the response status code is 200 OK
            self.assertEqual(resp.status_code, 200)

            # Check the response message
            data = resp.json
            self.assertEqual(data, {"message": "deleted"})

            # Ensure the cupcake is deleted from the database
            deleted_cupcake = Cupcake.query.get(cupcake_id)
            self.assertIsNone(deleted_cupcake)


