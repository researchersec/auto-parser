import os
import hashlib
import pandas as pd
from demoparser2 import DemoParser

def compute_file_hash(filename):
    """Compute the SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        # Read file in chunks of 4K
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def parse_demo_file():
    for file in os.listdir():
        if file.endswith(".dem"):
            parser = DemoParser(file)
            
            # Parse player_death event for players X and Y
            event_df = parser.parse_event("player_death", player=["X", "Y"], other=["total_rounds_played"])
            # Parse ticks for players X and Y
            ticks_df = parser.parse_ticks(["X", "Y"])

            # Compute hash of the .dem file
            file_hash = compute_file_hash(file)

            # Save event_df and ticks_df to JSON files in their respective folders
            os.makedirs('events', exist_ok=True)
            os.makedirs('ticks', exist_ok=True)
            event_df.to_json(f'events/{file_hash}.json')
            ticks_df.to_json(f'ticks/{file_hash}.json')

if __name__ == "__main__":
    parse_demo_file()
