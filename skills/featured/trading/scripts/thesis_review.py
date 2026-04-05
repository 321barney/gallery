import argparse

def main():
    parser = argparse.ArgumentParser(description="Review and postmortem theses.")
    parser.add_argument("--state-dir", required=True)
    subparsers = parser.add_subparsers(dest="command")
    
    review_parser = subparsers.add_parser("review-due")
    review_parser.add_argument("--as-of")
    
    postmortem_parser = subparsers.add_parser("postmortem")
    postmortem_parser.add_argument("thesis_id")
    
    subparsers.add_parser("summary")
    
    args = parser.parse_args()
    
    if args.command == "review-due":
        print(f"Checking for theses due for review as of {args.as_of}")
    elif args.command == "postmortem":
        print(f"Generating postmortem for {args.thesis_id}")
    elif args.command == "summary":
        print("Generating thesis summary statistics...")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
