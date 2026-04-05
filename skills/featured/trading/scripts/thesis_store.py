import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Query and store theses.")
    parser.add_argument("--state-dir", required=True)
    subparsers = parser.add_subparsers(dest="command")
    
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--ticker")
    list_parser.add_argument("--status")

    args = parser.parse_args()
    
    if args.command == "list":
        print(f"Listing theses in {args.state_dir} for Ticker: {args.ticker}, Status: {args.status}")
        # In a real scenario, this would glob the directory and parse YAMLs
        print("Done.")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
