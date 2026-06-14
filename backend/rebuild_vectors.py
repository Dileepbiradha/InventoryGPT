from app import create_app

print("STEP 1")

from services.chroma_service import (
    index_inventory
)

print("STEP 2")

app = create_app()

print("STEP 3")

with app.app_context():

    print("STEP 4")

    index_inventory()

    print("STEP 5")

print("Inventory vectors indexed.")