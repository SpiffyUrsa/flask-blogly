from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        # TODO: Assuming this deletes all users from table
        User.query.delete() 

        user = User(first_name="TestUser", last_name="1")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback() 
        # TODO: What happens after an error occurs and tearDown runs? Does setUp run again?
        ## This and setUp() wrap around every test function

    def test_index(self):
        with app.test_client() as client:
            resp = client.get("/")

            self.assertEqual(resp.status_code, 302) #redirect
            # CODEREVIEW: response.headers is a dict that includes location. check location address 
            ## did you redirct & to where?
    def test_users_listing(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser', html)
    
    def test_show_new_user_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Create a user', html) # CODEREVIEW <a> tags, can break with additional attr

    def test_handle_new_user(self):
        """ Checks for rediect after adding new user""" 
        with app.test_client() as client:
            d = {"first-name": "TestUser2", "last-name": "cat", "image-url": ""}
            # CODEREVIEW: test failed, potential for edge cases
            resp = client.post("/users/new", data=d, follow_redirects=False)

            self.assertEqual(resp.status_code, 302)
            # CODEREVIEW
            
    def test_handle_new_user_in_database(self):
        """ Checks if new user added to database""" 
        with app.test_client() as client:
            d = {"first-name": "TestUser2", "last-name": "cat"}
            resp = client.post("/users/new", data=d, follow_redirects=True)
        

            ## TODO: check for user name
            # CODE REVIEW look for user name in listing page
            self.assertEqual(resp.status_code, 200)


