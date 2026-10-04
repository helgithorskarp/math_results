"""Verify the new packet and unchanged credited original source before imports."""
from pathlib import Path
import hashlib, importlib.util, sys
BASE = Path(__file__).resolve().parent
ROOT = BASE
import bundle
NEW_SOURCE = bundle.check_bundle(BASE)
PARENT = BASE/'credited/uniform-zero-cap-cutoff'
PIN = 'b783ede83b894ba80936d6d11ad25a7be2c437602234e23aa95ebc3d4c454cb5'
if hashlib.sha256((PARENT/'SHA256SUMS').read_bytes()).hexdigest() != PIN:
    raise ValueError('changed credited 9980 manifest')
spec = importlib.util.spec_from_file_location('credited_sourcecheck', PARENT/'sourcecheck.py')
gate = importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
SOURCE = gate.check_bundle(PARENT)
sys.path.insert(0, str(PARENT))
import cap, coefficient, recovery, portable_frame, portable_fields, portable_zero, ipoly
r, require = cap.r, cap.require
