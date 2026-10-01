"""Positive, damaged-input and visible-incompleteness controls."""
from pathlib import Path
from itertools import combinations
from hashlib import sha256
import argparse, json, subprocess
from carrier import model, points, pairmask, write_native, PAIRS
from incidence import canonical, need
from literal import solve


def case(words, high, mandatory):
    q = [0]*15
    for w in words:
        for z in points(w, 15):q[z] += 1
    budget = sum((w & high).bit_count()*((w & high).bit_count()-1)//2 for w in words)
    return dict(columns=tuple(words), high=high, budget=budget, quotas=tuple(q), mandatory=mandatory)


def check_witness(rr, c):
    need(len(rr) >= 4 and rr[0] == 0 and rr[1] == 1 and len(rr) == 4+rr[3], 'malformed positive witness')
    covered = 0;q = [0]*15;budget = 0
    for w in rr[4:]:
        need(w in c['columns'] and not covered & pairmask(w), 'false positive column/pair')
        covered |= pairmask(w)
        for z in points(w, 15):q[z] += 1
        budget += (w & c['high']).bit_count()*((w & c['high']).bit_count()-1)//2
    need(tuple(q) == c['quotas'] and c['mandatory'] & ~covered == 0 and budget == c['budget'], 'false positive quota/budget')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--work-dir',required=True);ap.add_argument('--binary',required=True)
    args=ap.parse_args();work=Path(args.work_dir).resolve();work.mkdir(parents=True,exist_ok=True)
    binary=Path(args.binary).resolve();records=[]
    m=model(0,False)
    # Three pair-disjoint residual columns; no authored positive fixture.
    words=next(ws for ws in combinations(m['columns'],3)
               if all(not pairmask(u)&pairmask(v) for u,v in combinations(ws,2)))
    high=(1<<0)|(1<<1)|(1<<2)|(1<<3)|(1<<4)
    covered=0
    for w in words:covered |= pairmask(w)
    c=case(words,high,covered)
    inp=work/'positive.txt';out=work/'positive-out.txt';write_native([c],inp)
    p=subprocess.run([str(binary),str(inp),str(out)],capture_output=True,text=True,timeout=15)
    need(p.returncode==0,'native positive control failed');rr=tuple(map(int,out.read_text().split()));check_witness(rr,c)
    pp={PAIRS[i] for i in range(105) if covered>>i&1}
    answer=solve([points(w,15) for w in words],c['quotas'],pp,points(high,15),c['budget'])
    need(answer['sat'],'literal false negative on positive fixture')
    records.append(dict(control='three-word positive', native_nodes=rr[2], literal_states=answer['states'], witness=rr[4:]))
    bad={**c,'columns':c['columns'][1:]}
    write_native([bad],inp)
    p=subprocess.run([str(binary),str(inp),str(out)],capture_output=True,text=True,timeout=15)
    need(p.returncode==0 and out.read_text().split()[1]=='0','native false positive on missing-column fixture')
    r=solve([points(w,15) for w in bad['columns']],bad['quotas'],pp,points(high,15),bad['budget'])
    need(not r['sat'],'literal false positive on missing-column fixture')
    records.append(dict(control='removed necessary positive column', literal_states=r['states']))
    write_native([c],inp)
    for cap in ('0','200001','-1','1x'):
        p=subprocess.run([str(binary),str(inp),str(out),cap],capture_output=True,text=True,timeout=15)
        need(p.returncode!=0 and ('INCOMPLETE' in p.stderr if cap=='0' else 'cap' in p.stderr),'native guard failed closed')
        records.append(dict(control='native guard '+cap, message=p.stderr.strip()))
    for cap,seconds in ((0,10),(200001,10),(200000,1e-12)):
        try:solve([points(w,15) for w in words],c['quotas'],pp,points(high,15),c['budget'],cap,seconds)
        except ValueError as e:records.append(dict(control='literal guard',cap=cap,seconds=seconds,message=str(e)))
        else:raise ValueError('literal guard accepted incomplete/raised request')
    original=inp.read_text().splitlines()
    corruptions={
        'duplicate column':' '.join(map(str,(words[0],words[0],words[2]))),
        'nonquadruple':' '.join(map(str,(3,words[1],words[2]))),
        'out of range':' '.join(map(str,(1<<15,words[1],words[2])))}
    for name,row in corruptions.items():
        raw=original.copy();raw[3]=row;inp.write_text('\n'.join(raw)+'\n')
        p=subprocess.run([str(binary),str(inp),str(out)],capture_output=True,text=True,timeout=15)
        need(p.returncode!=0,'malformed native input accepted');records.append(dict(control=name,message=p.stderr.strip()))
    inp.write_text('\n'.join(original)+'\nextra\n')
    p=subprocess.run([str(binary),str(inp),str(out)],capture_output=True,text=True,timeout=15)
    need(p.returncode!=0 and 'trailing' in p.stderr,'trailing native data accepted')
    records.append(dict(control='trailing input',message=p.stderr.strip()))
    # Intrinsic group guard.
    try:canonical(m['anchors'],17,(tuple(range(15)),(15,16)),cap=0)
    except ValueError as e:need('INCOMPLETE' in str(e),'wrong incidence cap exception')
    else:raise ValueError('incidence cap accepted incomplete work')
    records.append(dict(control='incidence zero cap',message='INCOMPLETE incidence guard'))
    try:solve([(0,1,2,3),(0,1,2,3)],(1,1,1,1)+(0,)*11,(),(),0)
    except ValueError as e:records.append(dict(control='duplicate literal column',message=str(e)))
    else:raise ValueError('duplicate literal columns accepted')
    result=dict(agent='six-reviewer-2',role='independent mathematical reviewer',records=records)
    raw=json.dumps(result,sort_keys=True,separators=(',',':')).encode()
    result['sha256']=sha256(raw).hexdigest()
    (work/'controls.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':main()
