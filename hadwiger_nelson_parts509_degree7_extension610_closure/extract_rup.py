#!/usr/bin/env python3
"""Remove deletion lines from a trimmed proof only if all additions are RUP."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import rup


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--cnf',type=Path,required=True)
    ap.add_argument('--trimmed',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    variables,formula=rup.parse_dimacs(args.cnf.read_bytes())
    lines=[line for line in args.trimmed.read_text().splitlines() if not line.startswith('d')]
    proof=[rup.parse_clause(line,variables) for line in lines]
    additions=rup.check(formula,proof)
    data=('\n'.join(lines)+'\n').encode('ascii');args.out.write_bytes(data)
    print(json.dumps(dict(additions=additions,bytes=len(data),sha256=sha256(data).hexdigest()),indent=2))


if __name__=='__main__':main()
