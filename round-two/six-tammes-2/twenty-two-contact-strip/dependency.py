"""Pinned executable interval kernel and identified mathematical premise."""
from pathlib import Path
import hashlib,importlib.util,json
HERE=Path(__file__).resolve().parent
data=json.loads((HERE/'INPUTS.json').read_text())['dependencies'][0]
directory=HERE.parents[2]/data['directory']
for file,digest in data['required_files'].items():
    if hashlib.sha256((directory/file).read_bytes()).hexdigest()!=digest:
        raise ValueError('pinned prerequisite hash mismatch: '+file)
spec=importlib.util.spec_from_file_location('g22_pinned_enclosures',directory/'enclosures.py')
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
