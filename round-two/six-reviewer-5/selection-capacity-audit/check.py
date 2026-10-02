"""Independent frozen mathematical record, not a 71-code enumeration."""
import argparse
import json
from pathlib import Path
from literal import physical_rows, primary_partitions, canonical, require
from capacity import tables, scalar_controls


def compute():
    return {'agent':'six-reviewer-5','role':'independent mathematical reviewer',
            'physical_rows':physical_rows(),'general_primary_counts':primary_partitions(Path(__file__).with_name('primary69.txt')),
            'unified_capacity_controls':scalar_controls(),'projected_necessary_inventories':tables()}


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--check',type=Path)
    args = parser.parse_args(); result = compute()
    if args.check: require(canonical(result) == canonical(json.loads(args.check.read_text())), 'entire frozen independent record')
    print(canonical(result))


if __name__ == '__main__': main()
