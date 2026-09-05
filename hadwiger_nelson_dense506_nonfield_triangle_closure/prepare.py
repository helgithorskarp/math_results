#!/usr/bin/env python3
from pathlib import Path
import argparse,json
import common as C
p=argparse.ArgumentParser(description='Reconstruct every differently coloured host pair and midpoint.')
p.add_argument('--work',type=Path,required=True)
a=p.parse_args();a.work.mkdir(parents=True,exist_ok=False)
print(json.dumps(C.write_inputs(a.work),indent=2))
