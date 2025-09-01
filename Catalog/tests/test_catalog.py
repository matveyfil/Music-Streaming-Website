import pytest
from catalog-app import app as flask_app  # Import the Flask app instance from catalog-app.py

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client

def test_list_songs_no_search(client):
    """Test the catalog listing without search query."""
    rv = client.get('/catalog')
    assert rv.status_code == 200
    assert b'Songs' in rv.data  # Check if the title 'Songs' is in the response

def test_list_songs_with_search(client, mocker):
    """Test the catalog listing with a search query."""
    mocker.patch('catalog-app.r.keys', return_value=['song:1', 'song:2'])
    mocker.patch('catalog-app.r.hgetall', side_effect=[
        {'title': 'Test Song 1', 'filename': 'test1.mp3', 'duration': '240'},
        {'title': 'Another Test Song', 'filename': 'test2.mp3', 'duration': '300'}
    ])
    rv = client.get('/catalog?search=test')
    assert rv.status_code == 200
    assert b'Test Song 1' in rv.data  # Check if the search result is in the response
    assert b'Another Test Song' not in rv.data  # Check if the search result is filtered

def test_song_details(client, mocker):
    """Test fetching details of a specific song."""
    mocker.patch('catalog-app.r.hgetall', return_value={
        'title': 'Test Song', 'author': 'Test Author', 'year': '2022', 'duration': '240', 'filename': 'test.mp3'
    })
    rv = client.get('/song/1')
    assert rv.status_code == 200
    assert b'Test Song' in rv.data  # Check if the song details are in the response

def test_song_not_found(client, mocker):
    """Test fetching details of a non-existent song."""
    mocker.patch('catalog-app.r.hgetall', return_value={})
    rv = client.get('/song/999')
    assert rv.status_code == 404  # Should return 404 for non-existent song
    assert b'Song not found' in rv.data  # Check
