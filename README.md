# Data Redundancy Removal System

A lightweight, scalable system designed to identify, classify, and prevent redundant data from entering a cloud database. 

## Features
- **Classification**: Distinguishes between exact `REDUNDANT` data and `FALSE_POSITIVE` (near-duplicate) data.
- **Validation Mechanism**: Checks new entries against existing records using SHA-256 hashing for exact matches and string similarity for fuzzy matches.
- **Prevention**: Rejects duplicate data before it hits the database.
- **Append-Only Unique**: Only verified, unique entries are appended to the database.

## Architecture
- `database.py`: Simulates the cloud database (using SQLite) with insert and fetch operations.
- `validator.py`: The core logic engine. Hashes data, checks for exact matches, and uses `difflib` to check for high-similarity false positives.
- `main.py`: The entry point demonstrating the system in action with mock data.

## How to Run
1. Ensure you have Python 3.x installed.
2. Clone/download the files.
3. Run the main script:
   ```bash
   python main.py