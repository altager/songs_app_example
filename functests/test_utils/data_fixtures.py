import pytest

__all__ = [
    'create_document'
]


@pytest.fixture
def create_document(db):
    def _create_document(data: dict):
        return str(db.songs.insert_one(data).inserted_id)

    return _create_document
