"""Physical red/blue pages of the authors' compact 21-point construction."""
import ast,hashlib,json,sys
from itertools import combinations
from pathlib import Path

def require(t,m):
    if not t:raise ValueError(m)
def decode(raw):
    rows=ast.literal_eval(raw.decode().split('\n\nsearch_',1)[0])
    require(isinstance(rows,list) and len(rows)==21,'original21-point order')
    require(all(isinstance(r,list) and len(r)==21 for r in rows),'entire square matrix')
    require(all(type(x) is int and x in (0,1) for r in rows for x in r),'two exact colors')
    require(all(rows[i][i]==0 and all(rows[i][j]==rows[j][i] for j in range(21)) for i in range(21)),
            'original diagonal and symmetric colors')
    return rows
raw=Path(__file__).with_name('primary21.txt').read_bytes();rows=decode(raw)
require(len(raw)==1056 and hashlib.sha256(raw).hexdigest()=='3b648b66a5990d0b6ed945ce80d3f546e90f2b233f924775bb02ac2418558a55',
        'entire primary fixture bytes')
spines=[]
for i,j in combinations(range(21),2):
    color=rows[i][j];pages=[k for k in range(21) if k not in (i,j) and rows[i][k]==rows[j][k]==color]
    require(len(pages)<=(3 if color==0 else 6),'original physical book caps')
    spines.append([i,j,color,pages])
counts=[sum(s[2]==c for s in spines) for c in (0,1)]
maxima=[max(len(s[3]) for s in spines if s[2]==c) for c in (0,1)]
require(counts==[93,117] and maxima==[3,6],'useful primary baseline')
damages=[]
for name,change in [('drop-row',lambda x:x.pop()),('asymmetric-edge',lambda x:x[0].__setitem__(1,1-x[0][1])),
                    ('third-color',lambda x:x[0].__setitem__(1,2)),('wrong-diagonal',lambda x:x[0].__setitem__(0,1))]:
    candidate=[r[:] for r in rows];change(candidate)
    try:decode(str(candidate).encode())
    except ValueError:damages.append(name)
    else:raise ValueError('damaged primary encoding accepted')
out={'agent':'six-books-1','role':'researcher','complete':True,'prior_art_validation':True,
     'zero_is_red_B4':True,'fixture_bytes':len(raw),'fixture_sha256':hashlib.sha256(raw).hexdigest(),
     'all210_physical_spines':spines,'red_blue_edges':counts,'maximum_pages':maxima,'damages_rejected':damages}
record=(json.dumps(out,sort_keys=True,separators=(',',':'))+'\n').encode()
Path(sys.argv[1]).write_bytes(record)
print(json.dumps({'complete':True,'bytes':len(record),'sha256':hashlib.sha256(record).hexdigest()}))
