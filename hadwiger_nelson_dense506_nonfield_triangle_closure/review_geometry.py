"""Independent eight-basis host reconstruction used only by audit entry points."""
from pathlib import Path
from hashlib import sha256
import importlib.util,sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent.parent
p=ROOT/'hadwiger_nelson_dense506_two_point_extension_review1/independent_check.py'
if sha256(p.read_bytes()).hexdigest()!='9b7e9de99164784b1e7504800442bc1931ecdcaf5217cbae4382b026187e3b72':raise ValueError('review arithmetic pin')
s=importlib.util.spec_from_file_location('independent_ring',p);R=importlib.util.module_from_spec(s);s.loader.exec_module(R)
def host():
 source=ROOT/'hadwiger_nelson_nonmono159_214_lowden2'
 return R.build_host(R.read_source(source/'points159.tsv',159),R.read_source(source/'points214.tsv',214),-1)
def colors():
 raw=(ROOT/'hadwiger_nelson_dense506_two_point_extension/host_colors.txt').read_bytes()
 R.require(sha256(raw).hexdigest()=='010e6190aa14b6eadc285a6131d7b455bd5434f79ed9b4f69cdfb2848acddcb4','colour source pin')
 return list(map(int,raw.decode().strip()))
