"""Whole edge-free C reduction; exact checks corroborate the written proof."""
import json,time,hashlib,sys
from pathlib import Path
import c_force,frontier,literal as L

start=time.monotonic()
def require(t,m):
    if not t:raise ValueError(m)
def guard():
    if time.monotonic()-start>30:raise RuntimeError('30s guard: incomplete, no theorem')
def digest(x):return hashlib.sha256((json.dumps(x,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest()
rank=frontier.run(require,guard,digest)
forcing=c_force.run(require,guard,digest)
rank_records=[]
for e in forcing['T_excess_regimes']:
    red,d,q=L.build(0,(L.H,L.K,L.C),(L.P,L.S),e);a=L.allowances(red,d)
    q0max=6-q[8]+a[13,8]
    q1max=6-q[11]-q[12]
    q2max=6-q[9]+a[9,15]
    require((q0max,q1max,q2max)==(3,2,4),'edge-free final rank bounds')
    rank_records.append({'excess':e,'initial_ranks':q[13:16],'ordinary_maxima':[q0max,q1max,q2max],
                         'retained':q[13]<=q0max and q[14]<=q1max and q[15]<=q2max})
require([x['initial_ranks'] for x in rank_records if x['retained']]==[(3,2,3),(3,2,4)],'both and only derived terminal ranks')
guard()
out={'agent':'six-books-1','role':'researcher','complete':True,
     'status':'Exact corroboration of ordinary C-row/rank reduction without an edge bound; terminal exclusion is a separate component',
     'frontier':rank,'C_forcing':forcing,'rank_necessity_records':rank_records,
     'forced_rows_r0':[L.H,L.K,L.C],'forced_ordered_SY':[[L.P,L.S],[L.S,L.P]],
     'possible_terminal_T_Q_ranks':[[3,2,3],[3,2,4]]}
raw=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode()
Path(sys.argv[1]).write_bytes(raw)
print(json.dumps({'complete':True,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'seconds':time.monotonic()-start}))
