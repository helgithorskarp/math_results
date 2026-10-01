"""Identify the exact published prerequisite before importing its kernel."""
from pathlib import Path
import hashlib,importlib.util,json
HERE=Path(__file__).resolve().parent
def load():
    inputs=json.loads((HERE/'INPUTS.json').read_text())
    root=HERE.parents[2];directory=root/inputs['directory']
    for name,digest in inputs['required_files'].items():
        if hashlib.sha256((directory/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('published prerequisite source differs: '+name)
    spec=importlib.util.spec_from_file_location('tammes8929_intervals',directory/'intervals.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module
