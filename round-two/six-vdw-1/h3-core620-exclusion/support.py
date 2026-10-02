"""Pin the previously published independent definitions before loading helpers."""
import hashlib
import importlib.util
import json
from pathlib import Path

PUBLIC=Path(__file__).resolve().parent.parent/'h3-orbit16-exclusion620'
PINS_SHA='100c117c166bd00e1d78b1815744c6c334289cf50542a17b25ef82186c100381'
PREMISE={'height':9576,'artifact_ref':'bafkreig4gyqfrxg7brwukbp7jbrfbj2bkzv6sctzy2ba6lgbt55qkbykme',
         'source_commit':'99b8f2cf222afd483784a41cdfbb94221158acae','source_pins_sha256':PINS_SHA}
REPS=[8,10,12,20,34,72]


def require(ok,message):
    if not ok:raise ValueError(message)


def load(name):
    require(hashlib.sha256((PUBLIC/'SOURCE_PINS.json').read_bytes()).hexdigest()==PINS_SHA,'pinned premise source inventory')
    pins=json.loads((PUBLIC/'SOURCE_PINS.json').read_text())
    for file,digest in pins.items():require(hashlib.sha256((PUBLIC/file).read_bytes()).hexdigest()==digest,'changed published helper '+file)
    spec=importlib.util.spec_from_file_location('proved_h3_'+name,PUBLIC/(name+'.py'))
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
