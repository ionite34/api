import os

from google.cloud import datastore

client = datastore.Client()

emulator_host = os.getenv("DATASTORE_EMULATOR_HOST")
print(f"{emulator_host=}")

base_url = client.base_url
print(f"{base_url=}")

key = client.key("users", "213")

# task = datastore.Entity(key)

# task.update({
#     'name': 'Bob',
#     'transaction_id': 1878,
#     'revenue': 135.55,
#     'paid': True
# })

# client.put(task)

# print(f"Saved {task.key.name}: {task['name']}")

# Get the entity

task = client.get(key)

print(task)
