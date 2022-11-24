import os
import unittest

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.schema import Candidate

load_dotenv()

engine = create_engine(
    os.environ.get('DATABASE_URI'), connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)


class VoterTestCase(unittest.TestCase):
    def test_get_candidate(self):
        response = client.get('/candidates/1')

        self.assertEqual(response.json(),
            {'id': 1, 'name': 'นายก ทำไรทำสวน', 'pictureUrl': 'https://pbs.twimg.com/media/B85PR4tCEAAB3lA.jpg\r\n',
             'area_id': 1, 'party_id': 2})

    def test_get_candidates(self):
        response = client.get('/candidates')

        self.assertEqual(response.status_code, 200)

    def test_get_candidates_by_area(self):
        response = client.get('/candidates/area/1')

        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
