import argparse
import json

def getArgParser():
    parser = argparse.ArgumentParser(description="Command Line Utility for Juno Parser")

    parser.add_argument("operation", choices=["add", "delete", "put", "get", "query", "count", "list"], help="Please provide operation", default=None)
    parser.add_argument("object", choices=["collection", "vector"], help="Please provide db object", default=None)
    parser.add_argument("--args", type=str, help="Arguments for given operation in JSON format", default=None)
    return parser
