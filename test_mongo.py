from database.mongodb import get_database

db = get_database()

if db is None:
    print("❌ MongoDB NOT connected")
else:
    print("✅ MongoDB CONNECTED")
    print("Database:", db.name)

    try:
        db.test.insert_one({"status": "connected"})
        print("✅ Write successful")
    except Exception as e:
        print("❌ Write failed:", e)