#!/usr/bin/env python3
from pathlib import Path
import argparse
import hashlib
import json
import time
from model import build,raw


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out');args=ap.parse_args();start=time.monotonic()
    data=build();blob=raw(data)
    if args.out:Path(args.out).write_bytes(blob)
    print(json.dumps({'status':'PASS','vertices':data['patch_vertices'],'edges':data['patch_edges'],
      'chromatic_number':data['chromatic_number'],'phase_solutions':data['phase_solutions'],
      'common_plane_unit_neighbour':data['common_plane_unit_neighbour'],
      'interface_stronger_than_base':data['interface_stronger_than_base'],
      'certificate_sha256':hashlib.sha256(blob).hexdigest(),'seconds':time.monotonic()-start},sort_keys=True))


if __name__=='__main__':main()
