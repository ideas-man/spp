#!/usr/bin/env python3

import os
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Simple Python Prompt")
    parser.add_argument("--expr", "-e", type=str, help="Prompt expression.")
    parser.add_argument("--timeit", "-t", action="store_true", help="Display the elapsed time of the command.")
    parser.add_argument("--status", "-s", action="store_true", help="Display the exit status of the command.")
    parser.add_argument("--raw", "-r", action="store_true", help="Raw output")
    return parser.parse_args()

def exec_timer():
    if os.environ.get("SECONDS") and os.environ.get("SECONDS_START"):
        elapsed = float(os.environ["SECONDS"]) - float(os.environ["SECONDS_START"])
        return f"[{elapsed:.2f}]"
    return ""

def get_status():
    status = os.environ.get("EXIT_STATUS", "0")
    if status == "0":
        return "✓"
    return f"✗{status}"

def get_expr():


def main():
    args = parse_args()
    
    if args.timeit:
        timer = exec_timer()
    else:
        timer = ""
    
    if args.status:
        status = get_status()
    else:
        status = ""
    
    if args.format == "detailed":
        print(f"Status: {status} | Time: {timer}\n>:", end="", flush=True)
    else:
        print(f"{status} {timer}\n>:", end="", flush=True)

if __name__ == "__main__":
    main()