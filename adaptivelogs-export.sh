#!/bin/bash

# Usage: ./adaptivelogs-export.sh <lookup_file> [<environment_name>]
if [ "$#" -lt 1 ] || [ "$#" -gt 2 ]; then
  echo "Usage: $0 <lookup_file> [<environment_name>]"
  exit 1
fi

LOOKUP_FILE=$1

# Check if the lookup file exists
if [ ! -f "$LOOKUP_FILE" ]; then
  echo "Error: Lookup file '$LOOKUP_FILE' not found."
  exit 1
fi

# Function to process a single environment
process_environment() {
  local ENV_NAME=$1
  local LOGS_URL="$2/adaptive-logs/recommendations"
  local USER_ID=$3
  local TOKEN=$4
  

  echo "Processing environment: $ENV_NAME"
  echo "LOGS_URL: $LOGS_URL"

  # Perform the API request
  curl -u "$USER_ID:$TOKEN" -X GET "$LOGS_URL" > "${ENV_NAME}_recs.json"

  # Process the JSON response
  python3 prettify-json.py "${ENV_NAME}_recs.json"
  python3 parse-json-recs-to-csv.py "${ENV_NAME}_recs.json"
}

if [ "$#" -eq 2 ]; then
  ENV_NAME=$2

  # Extract the user ID and token for the given environment
  CREDENTIALS=$(grep "^$ENV_NAME," "$LOOKUP_FILE")
  if [ -z "$CREDENTIALS" ]; then
    echo "Error: Environment '$ENV_NAME' not found in lookup file."
    exit 1
  fi

  LOGS_URL=$(echo "$CREDENTIALS" | cut -d',' -f2)
  USER_ID=$(echo "$CREDENTIALS" | cut -d',' -f3)
  TOKEN=$(echo "$CREDENTIALS" | cut -d',' -f4)

  echo "LOGS_URL: $LOGS_URL"

  # Process the specified environment
  process_environment "$ENV_NAME" "$LOGS_URL" "$USER_ID" "$TOKEN"
else
  # Process all environments in the lookup file
  while IFS=',' read -r ENV_NAME LOGS_URL USER_ID TOKEN; do
    echo "in while loop,LOGS_URL: $LOGS_URL"
    process_environment "$ENV_NAME" "$LOGS_URL" "$USER_ID" "$TOKEN"
  done < "$LOOKUP_FILE"
fi