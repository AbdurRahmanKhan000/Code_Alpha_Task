from database import CloudDatabase
from validator import DataValidator

def main():
    # Initialize our simulated Cloud Database and Validator
    print("--- Initializing Data Redundancy Removal System ---")
    db = CloudDatabase()
    validator = DataValidator(db)

    # Test data payloads
    test_data = [
        "User_101 | John Doe | johndoe@email.com | Active",   # 1. Unique
        "User_102 | Jane Smith | janesmith@email.com | Active", # 2. Unique
        "User_101 | John Doe | johndoe@email.com | Active",   # 3. Redundant (Exact match of #1)
        "User_101 | John Doe | johndoe@email.com | Inactive", # 4. False Positive (High similarity to #1, but status changed)
        "User_103 | Bob Johnson | bobj@email.com | Active"    # 5. Unique
    ]

    print("\n--- Processing Incoming Data Stream ---")
    for i, data in enumerate(test_data, 1):
        print(f"\nIncoming Record {i}: {data}")
        
        status, message = validator.validate_and_classify(data)
        
        if status == "UNIQUE":
            print(f"✅ [{status}] {message}")
        elif status == "REDUNDANT":
            print(f"🛑 [{status}] {message}")
        elif status == "FALSE_POSITIVE":
            print(f"⚠️ [{status}] {message}")
        else:
            print(f"❌ [{status}] {message}")

    print("\n--- Final Database State ---")
    all_records = db.get_all_records()
    print(f"Total unique records in database: {len(all_records)}")
    for record in all_records:
        print(f"- {record['content']}")

if __name__ == "__main__":
    main()