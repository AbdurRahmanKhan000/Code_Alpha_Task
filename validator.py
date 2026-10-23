import hashlib
from difflib import SequenceMatcher

class DataValidator:
    def __init__(self, database, similarity_threshold=0.85):
        self.db = database
        self.similarity_threshold = similarity_threshold

    def _generate_hash(self, data):
        """Generate a unique SHA-256 hash for exact matches."""
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def _check_similarity(self, str1, str2):
        """Calculate similarity ratio between two strings."""
        return SequenceMatcher(None, str1, str2).ratio()

    def validate_and_classify(self, new_data):
        """
        Validates new data against the database.
        Returns a tuple: (Status, Message)
        """
        new_hash = self._generate_hash(new_data)
        existing_records = self.db.get_all_records()

        for record in existing_records:
            # 1. Exact Match Check (Redundant)
            if record["hash"] == new_hash:
                return "REDUNDANT", "Exact duplicate found. Rejected."

            # 2. Similarity Check (False Positive)
            similarity = self._check_similarity(record["content"], new_data)
            if similarity >= self.similarity_threshold:
                return "FALSE_POSITIVE", f"High similarity ({similarity:.2f}) found. Requires manual review. Rejected."

        # 3. Unique Data -> Append to Database
        success = self.db.insert_record(new_data)
        if success:
            return "UNIQUE", "Data verified and added to the cloud database."
        else:
            return "ERROR", "Database insertion failed."