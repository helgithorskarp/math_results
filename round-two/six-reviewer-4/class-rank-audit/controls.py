"""Meaningful exact input, full-cone, empty-row, kernel and singularity damages."""
import json,sys,copy
from pathlib import Path
from fractions import Fraction as F
from exact import need,canon,digest,ldlt,polynomial_psd
from produce import run as make
from check import run as check

def reject(call,label):
 try:call()
 except (ValueError,KeyError,ZeroDivisionError,IndexError):return label
 raise ValueError('damage accepted: '+label)

def run(w,record):
 # Full positive reconstruction is mandatory before any damaged record is used.
 check(w,record);need(make(w)==record,'whole positive producer reference')
 damages=[]
 def data(label,f):
  q=copy.deepcopy(w);f(q);damages.append(reject(lambda:make(q),label))
 def rec(label,f):
  q=copy.deepcopy(record);f(q);damages.append(reject(lambda:check(w,q),label))
 data('missing rational coordinate',lambda q:q['cases'][1]['values'].pop())
 data('float coordinate',lambda q:q['cases'][0]['values'].__setitem__(0,0.5))
 data('duplicate coordinate name',lambda q:q['cases'][1]['names'].__setitem__(-1,q['cases'][1]['names'][0]))
 data('negative actual deficit',lambda q:q['cases'][0]['values'].__setitem__(0,'-1'))
 data('negative physical floor',lambda q:q['cases'][1].__setitem__('floor','-1/1000'))
 data('false stronger lower/upper floor',lambda q:q['cases'][0].__setitem__('floor','10000'))
 rec('last completed table entry',lambda q:q['cases'][1]['table'][-1].__setitem__(-1,'1'))
 rec('actual empty loop',lambda q:q['cases'][1]['original'].__setitem__('empty_loop','0'))
 rec('last original empty-row value',lambda q:q['cases'][1]['original']['empty_rows'].__setitem__(-1,'0'))
 rec('omitted entire degree-zero cap',lambda q:q['cases'][0]['parts'].pop(0))
 rec('omitted highest-middle degree',lambda q:q['cases'][1]['parts'].pop())
 rec('last complete physical upper entry',lambda q:q['cases'][1]['parts'][-1]['upper'][-1].__setitem__(-1,'0'))
 rec('last full lower entry',lambda q:q['cases'][1]['parts'][-1]['lower'][-1].__setitem__(-1,'-1'))
 rec('highest-middle physical metric',lambda q:q['cases'][1]['parts'][-1]['g'].__setitem__(-1,2))
 rec('forced star kernel',lambda q:q['cases'][0]['parts'][0]['kernels'][0].__setitem__(0,'0'))
 rec('omitted saturated-pair kernel',lambda q:q['cases'][1]['parts'][0]['kernels'].pop())
 rec('wrong principal quotient positions',lambda q:q['cases'][1]['parts'][0]['keep'].pop())
 rec('last harmonic multiplicity',lambda q:q['cases'][1]['parts'][-1].__setitem__('multiplicity',0))
 rec('weighted original lower rank',lambda q:q['cases'][1].__setitem__('lower_rank',65503))
 rec('original spectral gap',lambda q:q['cases'][1].__setitem__('gap','1/1000'))
 rec('saturated original pair count',lambda q:q['cases'][0].__setitem__('q',65))
 matrices=[([[F(0),F(0)],[F(0),F(1)]],1),([[F(1),F(1)],[F(1),F(1)]],1),([[F(2),F(-1)],[F(-1),F(2)]],2)]
 for a,rank in matrices:need(ldlt(a)[0]==polynomial_psd(a)[0]==rank,'complete singular positive control')
 for label,a in [('zero diagonal cross',[[F(0),F(1)],[F(1),F(0)]]),('negative diagonal',[[F(-1),F(0)],[F(0),F(-2)]]),('asymmetric form',[[F(1),F(2)],[F(0),F(1)]])]:
  for name,alg in [('congruence',ldlt),('polynomial',polynomial_psd)]:damages.append(reject(lambda a=a,alg=alg:alg(a),name+' '+label))
 return dict(full_positive_passed=True,semantic_damages=damages,damage_count=len(damages),singular_positive_controls=3)
if __name__=='__main__':
 w=json.loads(Path(__file__).with_name('WITNESS.json').read_text());record=json.loads(Path(sys.argv[1]).read_text());v=run(w,record);Path(sys.argv[2]).write_bytes(canon(v));print(json.dumps(v))
