#!/usr/bin/env python3
"""Extract only extra positive witnesses from the bounded pilot checkpoint."""
import argparse,json
from pathlib import Path


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--pilot',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    pilot=json.loads(args.pilot.read_text());assert pilot['status']=='completed'
    extra=[]
    for row in pilot['library']:
        for i,witness in enumerate(row['witnesses'][1:],1):
            origin='imported_point610' if row['kind']=='forced' and row['key'] in (44,56) and i==1 else 'new_pilot'
            extra.append(dict(kind=row['kind'],key=row['key'],index=i,witness=witness,origin=origin))
    args.out.write_text(json.dumps(extra,indent=2,sort_keys=True)+'\n')


if __name__=='__main__':main()
