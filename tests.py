import server
import unittest
from unittest import TestCase
from model import db, connect_to_db, EIS_data, State, Project_State
#import datetime
from server import app

class TestFlaskRoutes(unittest.TestCase):

  def setUp(self):
    
    self.client = app.test_client()

    app.config['TESTING'] = True

    # change EIS_data to the test database once it is created
    connect_to_db(app, "postgresql:///EIS_data")

    # db.create_all()
    # example_data()

  def tearDown(self):
    pass


  def test_index(self):

      result = self.client.get('/')
      self.assertEqual(result.status_code, 200)


if __name__ == '__main__':  #pragma: no cover
    
    #runs all cases
    unittest.main() 
