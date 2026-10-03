#!/usr/bin/env python3
"""Post-seal comparison only. Producer modules NEVER establish the primary proof."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,sys,time
from fractions import Fraction as Q
import check as own

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def dense(p):return own.trim(tuple(Q(v) for v in p))
def sparse(p):return own.trim(tuple(p.get(i,Q(0)) for i in range(max(p,default=0)+1)))

def run(directory,start,stop):
    began=time.monotonic();own.need(0<=start<stop<=576,'bounded range')
    here=Path(__file__).parent;seal=json.loads((here/'INDEPENDENCE.json').read_text())
    for name,row in seal['files'].items():
        raw=(here/name).read_bytes();own.need(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'all pre-native primary seals unchanged')
    inputs=json.loads((here/'NATIVE_INPUTS.json').read_text())
    for row in inputs['pins']:
        raw=(directory/row['name']).read_bytes();own.need(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'all exact native source bytes')
    sys.path.insert(0,str(directory))
    producer=module('late9878producer',directory/'check.py');auditor=module('late9878auditor',directory/'audit.py')
    certificate=json.loads((directory/'CERTIFICATE.json').read_text());polys=auditor.prepare(certificate)
    owncases=own.typed_cases();allrows=certificate['rows'];converted={}
    for row in allrows:
        key=tuple(sorted(own.face(own.FRESH if v==13 else v for v in t) for t in producer.path(tuple(row[:5]))))
        own.need(key in owncases and key not in converted,'complete original placement image')
        own.need(owncases[key]['kind']==row[0],'literal type correspondence');converted[key]=row
    own.need(set(converted)==set(owncases),'ENTIRE original placement set equals primary set')
    original_h={dense(x['polynomial']) for x in certificate['root_free_polynomials']}
    expected=json.loads((here/'EXPECTED.json').read_text())
    independent_h={dense(x['h']) for x in expected['witnesses'].values()}
    own.need(original_h==independent_h and len(original_h)==38,'ENTIRE monic witness set')
    count=gramcount=norms=contacts=0;stream=hashlib.sha256();max_uv=0
    for ordinal in range(start,stop):
        own.need(time.monotonic()-began<55,'original55second late child guard')
        row=allrows[ordinal];case=tuple(row[:5]);key=tuple(sorted(own.face(own.FRESH if v==13 else v for v in t) for t in producer.path(case)))
        fs,p,ce,f,g=own.construct(key);h,u,v=own.bezout(f,g)
        ng,nf,nn=producer.construct(case,full_gram=True);bg,bf,bn=auditor.backward(case)
        own.need(dense(nf)==sparse(bf)==f and dense(nn)==sparse(bn)==g,'BOTH original cross-gap polynomials')
        nh,nu,nv=producer.bezout(nf,nn);bh,bu,bv=auditor.witness(bf,bn)
        own.need(dense(nh)==sparse(bh)==h==dense(certificate['root_free_polynomials'][row[5]]['polynomial']),'case-specific WHOLE root-free binding')
        own.need(dense(nu)==sparse(bu)==u and dense(nv)==sparse(bv)==v,'entire explicit Bezout coefficients')
        max_uv=max(max_uv,len(u)-1,len(v)-1)
        labels=sorted(producer.CORE|({13} if row[0]!='S' else set()));indices={v:i for i,v in enumerate(labels)}
        image=[]
        for x in sorted(p):
            line=[]
            for y in sorted(p):
                i=indices[13 if x==own.FRESH else x];j=indices[13 if y==own.FRESH else y]
                n=own.numerator(p[x],p[y]);own.need(n==dense(ng[i][j])==sparse(bg[i][j]),'EVERY physical Gram polynomial')
                line.append(own.packed(n));gramcount+=1
            image.append(line)
        bern=own.bernstein(h,own.J)
        own.need(tuple(producer.bernstein(nh,producer.LO,producer.HI))==tuple(auditor.bern(bh))==bern,'entire original Bernstein list')
        own.need(tuple(Q(v) for v in certificate['root_free_polynomials'][row[5]]['Bernstein'])==bern,'original supplied exact coefficients')
        stream.update(own.canonical(dict(ordinal=ordinal,bridges=key,gram=image,f=own.packed(f),g=own.packed(g),h=own.packed(h),u=own.packed(u),v=own.packed(v)))+b'\n')
        norms+=len(p);contacts+=len(ce);count+=1
    for x in certificate['core_noncontacts']:
        original=dense(x['gap']);row=next(v for v in expected['core_noncontacts'] if v['pair']==x['pair'])
        own.need(original==dense(row['gap']),'EVERY original strict core noncontact')
    return dict(agent='six-reviewer-2',role='independent mathematical reviewer',phase='late only; no target code proof input',all_primary_seals_unchanged=True,all_native_pins_unchanged=True,entire_576_case_set_equal=True,entire_38_h_set_equal=True,start=start,stop=stop,cases=count,norms=norms,contacts=contacts,gram_polynomials=gramcount,cross_gap_polynomials=2*count,explicit_identity_coefficient_lists=3*count,maximum_uv_degree=max_uv,whole_semantic_stream_sha256=stream.hexdigest())

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--native-dir',type=Path,required=True);ap.add_argument('--start',type=int,required=True);ap.add_argument('--stop',type=int,required=True);a=ap.parse_args();print(json.dumps(run(a.native_dir.resolve(),a.start,a.stop),sort_keys=True,separators=(',',':')))
