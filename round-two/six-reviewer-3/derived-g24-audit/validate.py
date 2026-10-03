#!/usr/bin/env python3
"""Serial checks, algebra-kernel controls and deliberate defining-evidence damages."""
import argparse, copy, importlib.util, json, os, resource, subprocess, sys, tempfile, time
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('independent_audit',ROOT/'audit.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)

def fractional_remainder(p,q):
    p=[F(x) for x in p];q=[F(x) for x in q]
    while p and len(p)>=len(q):
        c=p[-1]/q[-1];d=len(p)-len(q)
        for i,v in enumerate(q):p[i+d]-=c*v
        while p and not p[-1]:p.pop()
    return tuple(p)
def kernel_controls():
    n=0
    for k in range(1,25):
        p=tuple(((j*j+3*k*j+2*k)%17)-8 for j in range(8))+(k+1,)
        q=(k%3-1,2-k%5,1+k%7,(-1)**k*(k+2))
        r=fractional_remainder(p,q);s=a.prem(p,q)
        a.require(bool(r)==bool(s),'independent remainder zero agreement')
        if r:
            ratio=F(s[-1])/r[-1];a.require(ratio>0 and tuple(ratio*x for x in r)==s,'signed primitive remainder bridge')
        n+=1
    tests=[((1,),F(0),F(1),True),((-1,),F(0),F(1),False),((0,1),F(0),F(1),False),((1,-2,1),F(0),F(2),False),((1,-2,1),F(2),F(3),True),((-2,0,1),F(1),F(2),False),((-2,0,1),F(2),F(3),True),((6,-5,1),F(0),F(4),False),((1,0,1),F(-4),F(4),True),((4,-4,1),F(2),F(3),False)]
    for p,l,h,want in tests:a.require(a.positive(p,l,h)==want,'closed/repeated/irrational-root Sturm control')
    return {'signed_remainder_controls':n,'sturm_controls':len(tests)}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--expected',required=True);ap.add_argument('--output',required=True);args=ap.parse_args();base=json.loads(Path(args.expected).read_text());results=[];env=os.environ.copy()
    for k in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:env[k]='1'
    env['PYTHONDONTWRITEBYTECODE']='1';controls=kernel_controls()
    with tempfile.TemporaryDirectory(prefix='g24-independent-controls-') as temp:
        temp=Path(temp)
        def run(mode,source,expected,name,reject=False):
            out=temp/(name+mode+'.json');cmd=[sys.executable]+(['-O'] if mode=='optimized' else [])+[str(source),'--expected',str(expected),'--output',str(out)]
            t=time.monotonic();p=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=45)
            a.require((p.returncode!=0)==reject,'wrong control result: '+name)
            if reject:a.require('ValueError:' in p.stderr and 'guard' not in p.stderr,'damage must fail by explicit check: '+name)
            else:a.require(json.loads(out.read_text())==base,'whole typed baseline mismatch')
            results.append({'name':name,'mode':mode,'rejected':reject,'seconds':time.monotonic()-t,'exit_code':p.returncode,'terminal':p.stderr.strip().splitlines()[-1] if p.stderr else p.stdout.strip()})
        normal=temp/'normal.json';normal.write_text(json.dumps(base,indent=3))
        reverse=temp/'reverse.json';reverse.write_text(json.dumps(dict(reversed(list(base.items()))),indent=1))
        for mode in ['normal','optimized']:run(mode,ROOT/'audit.py',normal if mode=='normal' else reverse,'whole_baseline')
        text=(ROOT/'audit.py').read_text();changes=[('wrong_reflection', 'r=2*t/(1+t)','r=3*t/(1+t)'),('wrong_fresh_label','p[13]=reflect(2,10,1)','p[13]=reflect(2,10,4)'),('wrong_metric','return (1-t)*sum','return (1+t)*sum'),('wrong_threshold_factor',"require(gap==mul((-1,0,3),(-1,1,17,23))", "require(gap==mul((-1,0,4),(-1,1,17,23))")]
        for name,before,after in changes:
            a.require(text.count(before)==1,'unambiguous mutation');shadow=temp/(name+'.py');shadow.write_text(text.replace(before,after))
            for mode in ['normal','optimized']:run(mode,shadow,normal,name,True)
        bads=[]
        damaged=copy.deepcopy(base);damaged['triples'].pop();bads.append(('missing_active_triple',damaged))
        damaged=copy.deepcopy(base);damaged['interval'][1]='59/100';bads.append(('clipped_upper_endpoint',damaged))
        damaged=copy.deepcopy(base);next(t for t in damaged['triples'] if not t['singular'])['leaves'][0]['polynomial']='0'*64;bads.append(('wrong_sign_polynomial',damaged))
        for name,damaged in bads:
            f=temp/(name+'.json');f.write_text(json.dumps(damaged));run('normal',ROOT/'audit.py',f,name,True)
    result={'status':'PASS',**controls,'children':results,'maximum_child_seconds':max(x['seconds'] for x in results),'peak_child_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'serial':True,'per_child_guard_seconds':45,'native_threads':1}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='children'}))
if __name__=='__main__':main()
