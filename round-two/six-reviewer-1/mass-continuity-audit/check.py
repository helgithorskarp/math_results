#!/usr/bin/env python3
"""Reconstruct and compare the ENTIRE typed exact fixture, normal or optimized."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import signal
signal.alarm(45)
root=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('independent_mass_core',root/'core.py')
core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');p.add_argument('--expected',type=Path,default=root/'expected.json');args=p.parse_args()
actual=core.record()
if args.write:
    if args.expected.exists(): raise ValueError('refuse to overwrite sealed fixture')
    args.expected.write_text(json.dumps(actual,indent=2,sort_keys=True)+'\n')
expected=json.loads(args.expected.read_text())
if not core.same(actual,expected): raise ValueError('entire typed expected record mismatch')
print(json.dumps({'status':'PASS','whole_record_sha256':hashlib.sha256(core.canonical(actual)).hexdigest(),'cases':len(actual['literal_original_matrix_cases']),'mathematical_damage_rejections':len(actual['mathematical_damage_rejections'])},sort_keys=True))
