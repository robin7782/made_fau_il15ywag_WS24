#!/bin/bash

# Ensure the environment is prepared
if [ ! -d "./project/data" ]; then
    mkdir -p "./project/data"
fi

# Run the pipeline
echo "Running pipeline.py..."
python3 project/pipeline.py

# Validate the database
DB_FILE="./project/data/maindatabase.db"
if [ -f "$DB_FILE" ]; then
    echo "Database file exists."
else
    echo "Database file is missing."
    exit 1
fi

# Validate the database tables
echo "Validating database tables..."
TABLES=$(sqlite3 "$DB_FILE" ".tables")
if [[ "$TABLES" == *"hause_expense_usa"* && "$TABLES" == *"income_usa"* ]]; then
    echo "All required tables exist in the database."
else
    echo "Required tables are missing from the database."
    exit 1
fi

echo "All tests passed successfully!"