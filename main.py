import argparse
from process import DataWangler


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_dir", type=str, help="test directory")
    args = parser.parse_args()
    t = DataWangler(args.test_dir)
    t.process()
