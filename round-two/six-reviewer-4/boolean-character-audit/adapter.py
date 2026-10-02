"""Late data-only decoder; never imports author executables or trusts their census."""
import csv,hashlib,io,json
from geometry import canonical,need
EXPECTED='e7ecddbc9d917d193dafe60472e7a2fe16c8d30ac27beddd3c72e79e85045e28'
def decode(raw):
    need(len(raw)==155886 and hashlib.sha256(raw).hexdigest()==EXPECTED,'entire pinned regenerated native CSV bytes')
    rows=list(csv.reader(io.StringIO(raw.decode('ascii'))))
    header=['index','roots','t','truth']+[z for j in range(1,10)for z in('a'+str(j),'step'+str(j))]
    need(len(rows)==2177 and rows[0]==header,'complete native22-field CSV schema')
    neutral=[]
    for i,row in enumerate(rows[1:]):
        need(len(row)==22,'complete nine witness pairs')
        values=[int(z)for z in row];need(all(str(v)==s for v,s in zip(values,row)),'canonical whole integer encoding')
        index,r,t,w,*pairs=values;need(index==i,'whole ordered row indices')
        need(r in(1,2,3),'original root count')
        if r==2:need(t==0,'native two-root t sentinel');t=1
        neutral.append({'state':[r,t,w],'aps':[pairs[j:j+2]for j in range(0,18,2)]})
    return neutral
