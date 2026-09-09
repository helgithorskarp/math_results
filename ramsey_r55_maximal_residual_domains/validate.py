"""Definition-level native validation, sanitizer coverage and corruptions."""
from pathlib import Path
from itertools import combinations
import argparse, json, subprocess, time
from reference import count, columns
HERE=Path(__file__).resolve().parent
def need(ok,why):
    if not ok:raise ValueError(why)
def graph6(n,edges):
    edges={tuple(sorted(e)) for e in edges};bits=[int((u,v) in edges) for v in range(1,n) for u in range(v)]
    bits += [0]*((-len(bits))%6)
    return chr(n+63)+''.join(chr(63+sum(bits[i+j]<<(5-j) for j in range(6))) for i in range(0,len(bits),6))
def run(out,producer,checker):
    out=Path(out);out.mkdir();started=time.monotonic();checked=0;truth=[]
    def call(args):
        r=subprocess.run(list(map(str,args)),capture_output=True,text=True);need(r.returncode==0,r.stderr);return json.loads(r.stdout)
    for n in range(1,5):
        pairs=list(combinations(range(n),2));graphs=[];expected=[]
        for word in range(1<<len(pairs)):
            edges=[e for bit,e in enumerate(pairs) if word>>bit&1];a=count(n,edges);b=columns(n,edges)
            need(a==b,'row/column definition');graphs.append(graph6(n,edges));expected.append(a);checked+=1
        file=out/f'all-{n}.g6';file.write_text('\n'.join(graphs)+'\n');table=out/f'all-{n}.tsv';profiles=out/f'all-{n}.bin'
        call([producer,n,file,0,len(graphs),table,profiles]);call([checker,n,table,profiles])
        rows=table.read_text().splitlines();need([int(x.split()[3]) for x in rows]==expected,'literal cover count')
        truth.append(dict(order=n,graphs=len(graphs),total=sum(expected)))
    n=15;file=out/'boundaries.g6';file.write_text(graph6(n,[])+'\n'+graph6(n,list(combinations(range(n),2)))+'\n')
    table=out/'boundaries.tsv';profiles=out/'boundaries.bin'
    call([producer,n,file,0,2,table,profiles]);call([checker,n,table,profiles])
    need([int(x.split()[3]) for x in table.read_text().splitlines()]==[15**15,0],'large and zero boundaries')
    base=(out/'all-3.tsv').read_text();raw=(out/'all-3.bin').read_bytes();cases=[]
    fields=base.splitlines()[0].split();fields[3]=str(int(fields[3])+1);cases.append(('cover','\t'.join(fields)+'\n'+'\n'.join(base.splitlines()[1:])+'\n',raw))
    fields=base.splitlines()[0].split();fields[2]=str(int(fields[2])+1);cases.append(('free','\t'.join(fields)+'\n'+'\n'.join(base.splitlines()[1:])+'\n',raw))
    cases.extend([('profile',base,bytes([raw[0]^1])+raw[1:]),('truncated',base,raw[:-1]),('trailing',base,raw+b'\0'),('missing_row','\n'.join(base.splitlines()[:-1])+'\n',raw)])
    for tag,rows,blob in cases:
        table=out/(tag+'.tsv');profiles=out/(tag+'.bin');table.write_text(rows);profiles.write_bytes(blob)
        r=subprocess.run([str(checker),'3',str(table),str(profiles)],capture_output=True,text=True)
        need(r.returncode!=0,'corruption accepted: '+tag)
    return dict(status='LITERAL_RESIDUAL_DEFINITION_CONTROLS_PASS',complete_small_graphs=checked,truth=truth,large_boundary_graphs=2,corruptions_rejected=len(cases),seconds=time.monotonic()-started)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('out');p.add_argument('producer');p.add_argument('checker');a=p.parse_args();r=run(a.out,a.producer,a.checker)
    (Path(a.out)/'VALIDATION.json').write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(json.dumps(r,sort_keys=True))
