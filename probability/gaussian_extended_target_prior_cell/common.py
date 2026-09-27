"""Pinned accepted scalar/orbit/geometry dependencies; no certificate replay."""
from pathlib import Path
from hashlib import sha256
import importlib.util,json,sys
HERE=Path(__file__).resolve().parent
PINS=json.loads((HERE/'INPUTS.json').read_text())['files']
for name,digest in PINS.items():
 if sha256((HERE/name).read_bytes()).hexdigest()!=digest:raise ValueError('changed dependency: '+name)
BASE=HERE.parent/'gaussian_deep_flap_cell'
sys.path.insert(0,str(BASE))
import radial as r
import middle as m
from direct_hinge import exp_neg,gaussian_constant,quadrature_error
spec=importlib.util.spec_from_file_location('accepted_deep_flap_geometry',BASE/'verify.py')
geometry_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(geometry_module)
