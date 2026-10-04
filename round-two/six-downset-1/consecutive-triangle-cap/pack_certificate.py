"""Lossless interning of every mathematical field; no proof-data omission."""
import json
from pathlib import Path


def pack(data):
    ps=[];fs=[];pi={};fi={}
    def poly(p):
        k=json.dumps(p,sort_keys=True,separators=(',',':'))
        if k not in pi:pi[k]=len(ps);ps.append(p)
        return pi[k]
    def field(f):
        encoded={'numerator':poly(f['numerator']),
                 'denominator_factors':[[poly(z['factor']),z['power']] for z in f['denominator_factors']]}
        k=json.dumps(encoded,sort_keys=True,separators=(',',':'))
        if k not in fi:fi[k]=len(fs);fs.append(encoded)
        return fi[k]
    forms={g:[[field(z) for z in row] for row in a] for g,a in data['forms'].items()}
    rows=[{k:field(v) if k=='pivot' else poly(v) if k=='shifted_numerator' else v
           for k,v in z.items()} for z in data['rows']]
    updates=[{k:field(v) if k in ('before','left','right','pivot','after') else v
              for k,v in z.items()} for z in data['updates']]
    return dict(version=1,agent=data['agent'],role=data['role'],domain=data['domain'],
                guards=data['guards'],forms=forms,rows=rows,updates=updates,
                polynomials=ps,fields=fs)


def unpack(data):
    if set(data)!={'version','agent','role','domain','guards','forms','rows','updates','polynomials','fields'}:
        raise ValueError('complete compact schema')
    if data['version']!=1 or data['agent']!='six-downset-1' or data['role']!='researcher':
        raise ValueError('exact version/author/role')
    ps,fs=data['polynomials'],data['fields']
    if len({json.dumps(p,sort_keys=True,separators=(',',':')) for p in ps})!=len(ps):
        raise ValueError('duplicate polynomial intern')
    if len({json.dumps(f,sort_keys=True,separators=(',',':')) for f in fs})!=len(fs):
        raise ValueError('duplicate field intern')
    usedp=set();usedf=set()
    def poly(i):
        if type(i) is not int or not 0<=i<len(ps):raise ValueError('polynomial ID')
        usedp.add(i);return ps[i]
    def field(i):
        if type(i) is not int or not 0<=i<len(fs):raise ValueError('field ID')
        usedf.add(i);f=fs[i]
        if set(f)!={'numerator','denominator_factors'}:raise ValueError('full interned field')
        return dict(numerator=poly(f['numerator']),denominator_factors=[
            dict(factor=poly(j),power=e) for j,e in f['denominator_factors']])
    forms={g:[[field(z) for z in row] for row in a] for g,a in data['forms'].items()}
    rows=[{k:field(v) if k=='pivot' else poly(v) if k=='shifted_numerator' else v
           for k,v in z.items()} for z in data['rows']]
    updates=[{k:field(v) if k in ('before','left','right','pivot','after') else v
              for k,v in z.items()} for z in data['updates']]
    if usedp!=set(range(len(ps))) or usedf!=set(range(len(fs))):raise ValueError('unreferenced intern')
    return dict(agent=data['agent'],role=data['role'],domain=data['domain'],guards=data['guards'],
                forms=forms,rows=rows,updates=updates)


if __name__=='__main__':
    folder=Path.cwd()
    src=json.loads((folder/'GAUSSIAN-HARMONIC-FIRST.json').read_text())
    compact=pack(src);back=unpack(compact)
    for k in ('domain','guards','forms','rows','updates'):
        if back[k]!=src[k]:raise ValueError('WHOLE lossless field reconstruction')
    raw=json.dumps(compact,separators=(',',':'))+'\n'
    if len(raw.encode())>32*1024*1024:raise ValueError('unchanged32MiB packing guard')
    (folder/'CERTIFICATE.json').write_text(raw)
    print(json.dumps(dict(complete_lossless=True,bytes=len(raw.encode()),
                         polynomials=len(compact['polynomials']),fields=len(compact['fields']),
                         pivots=len(compact['rows']),updates=len(compact['updates']))))
