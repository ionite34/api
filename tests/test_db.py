import os
from typing import Final

import pytest
from google.cloud import datastore

UID: Final[str] = "7a52facf-4ab4-4552-8724-248eadfb9cfc"


@pytest.fixture(scope="session")
def ds_client():
    """Get a datastore client"""
    db = datastore.Client()
    print(db.base_url)
    print(os.environ.get("DATASTORE_EMULATOR_HOST"))
    return db


def test_get(ds_client):
    """Test getting an entity"""
    key = ds_client.key(UID, "1")
    task = ds_client.get(key)
    assert task is None

    # Set the entity
    task = ds_client.entity(key)
    task.update({"name": "Bob"})
    ds_client.put(task)

    # Get the entity again
    task = ds_client.get(key)
    assert task == {"name": "Bob"}
