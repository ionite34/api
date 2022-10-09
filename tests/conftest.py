import os
import subprocess
import time
from contextlib import suppress
from queue import Empty, Queue
from subprocess import Popen

import pytest
from fastapi.testclient import TestClient
from google.cloud import datastore

from api.server import app

emulator = Queue()


def pytest_configure(config):
    # Start the emulator
    p = Popen(
        [
            "gcloud",
            "beta",
            "emulators",
            "datastore",
            "start",
        ]
    )
    # Wait for the emulator to start
    time.sleep(1)
    if p.poll() is not None:
        pytest.fail("Failed to start emulator")
    emulator.put(p)

    # Set env vars
    envs: bytes = subprocess.check_output(
        "gcloud beta emulators datastore env-init", shell=True
    )
    env_dict = parse_envs(envs.decode())
    print(f"Starting emulator with envs: {env_dict}")
    os.environ.update(env_dict)

    ensure_emulator()


def parse_envs(envs: str) -> dict:
    env_lines = envs.replace("export ", "").split("\n")
    parsed = [line.split("=") for line in env_lines if line]
    env_dict = {k: v.replace("::1", "[::1]") for k, v in parsed}
    return env_dict


def pytest_unconfigure(config):
    """Delete the test settings file"""
    with suppress(Empty):
        p = emulator.get_nowait()
        p.terminate()


def ensure_emulator():
    """Ensures we can in emulator environment"""
    emulator_host = os.getenv("DATASTORE_EMULATOR_HOST")
    if not emulator_host:
        pytest.fail("Not in emulated env")

    client = datastore.Client()
    url = client.base_url
    assert "google" not in url


@pytest.fixture
def api_client() -> TestClient:
    """
    Return an API test client that can interact with a temporary database
    """
    return TestClient(app)
