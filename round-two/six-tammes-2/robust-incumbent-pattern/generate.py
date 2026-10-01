"""Regenerate the rational model table from the graph, without reading it."""
from pathlib import Path
import argparse
import json
import check
from models import Models

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--prerequisite-root',type=Path,default=check.ROOT)
    args=p.parse_args()
    config=json.loads((check.HERE/'certificate.json').read_text())
    check.validate_config(config)
    base,core=check.load_prerequisites(args.prerequisite_root.resolve(),config)
    print(json.dumps(Models(base,core).manifest(),sort_keys=True,indent=2))
