"""Pinned exact host input; generated state always stays in an external directory."""
from pathlib import Path
from hashlib import sha256
import importlib.util,sys,json
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
PINS={
 'hadwiger_nelson_dense506_two_point_extension/geometry.py':'ce68ab6130082828fbd4e709586ae9dd53273c41e0cb4bfe3aad0278d08faddd',
 'hadwiger_nelson_dense506_two_point_extension/host_colors.txt':'010e6190aa14b6eadc285a6131d7b455bd5434f79ed9b4f69cdfb2848acddcb4',
 'hadwiger_nelson_dense506_two_point_extension_review1/independent_check.py':'9b7e9de99164784b1e7504800442bc1931ecdcaf5217cbae4382b026187e3b72'}
def module(name,path):
 path=ROOT/path
 if sha256(path.read_bytes()).hexdigest()!=PINS[str(path.relative_to(ROOT))]:raise ValueError('source pin')
 spec=importlib.util.spec_from_file_location(name,path);out=importlib.util.module_from_spec(spec);spec.loader.exec_module(out);return out
def producer():return module('primary_geometry','hadwiger_nelson_dense506_two_point_extension/geometry.py')
def reviewer():return module('review_geometry','hadwiger_nelson_dense506_two_point_extension_review1/independent_check.py')
def colors():
 path=ROOT/'hadwiger_nelson_dense506_two_point_extension/host_colors.txt'
 if sha256(path.read_bytes()).hexdigest()!=PINS[str(path.relative_to(ROOT))]:raise ValueError('colour pin')
 out=list(map(int,path.read_text().strip()))
 if len(out)!=506 or set(out)!={0,1,2,3}:raise ValueError('colour row')
 return out
def write(path,value):path.write_text(json.dumps(value,separators=(',',':'))+'\n')
def file_hash(path):return sha256(path.read_bytes()).hexdigest()
