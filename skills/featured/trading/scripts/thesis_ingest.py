import argparse
import json
import os
import uuid
import datetime

def main():
    parser = argparse.ArgumentParser(description="Ingest screener output as a thesis")
    parser.add_argument("--source", required=True, help="Agent/source producing the candidate")
    parser.add_argument("--input", required=True, help="Input JSON signals file")
    parser.add_argument("--state-dir", required=True, help="State directory for theses")
    
    args = parser.parse_args()
    os.makedirs(args.state_dir, exist_ok=True)
    
    # Mock logic
    try:
        with open(args.input, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"mock": "No file found, creating dummy thesis"}
        
    thesis_id = "th_" + str(uuid.uuid4())[:8]
    output_file = os.path.join(args.state_dir, f"{thesis_id}.yaml")
    
    with open(output_file, "w") as f:
        f.write(f"thesis_id: {thesis_id}\n")
        f.write(f"source: {args.source}\n")
        f.write("status: IDEA\n")
        f.write(f"created_at: {datetime.datetime.now().isoformat()}\n")
        
    print(f"Successfully ingested thesis to {output_file}")

if __name__ == "__main__":
    main()
