"""Verify pinned public inputs before importing their interval kernel."""
from pathlib import Path
import hashlib,importlib.util,json
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
inputs=json.loads((HERE/'INPUTS.json').read_text())
if inputs['format']!=1:raise ValueError('input manifest format')
for item in inputs['dependencies']:
    for name,digest in item['required_files'].items():
        if hashlib.sha256((ROOT/item['directory']/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('pinned prerequisite bytes differ: '+name)
path=ROOT/'round-two/six-tammes-2/negative-cross-reduction/intervals.py'
spec=importlib.util.spec_from_file_location('negative_extension_interval_kernel',path)
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
