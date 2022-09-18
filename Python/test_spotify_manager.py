import pytest

def test_spotify_manager():
    sp = SpotifyManager.__init__()
    assert type(sp).__name__ == "SpotifyManager"