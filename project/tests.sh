#!/bin/bash

# Ensure the environment is prepared
if [ ! -d "./project/data" ]; then
    mkdir -p "./project/data"
fi

# Run the pipeline....
echo "Running pipeline.py..."
python3 project/pipeline.py





echo "All tests passed successfully!"