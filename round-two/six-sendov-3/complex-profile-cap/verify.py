"""Reconstruct every coefficient before comparing the compact whole-record seal."""
from pathlib import Path
from hashlib import sha256
import argparse
import json
import resource
import sys
import time

HERE=Path(__file__).resolve().parent
STAGES=('algebra','lower_centers','literal','distance','roots',
        'real_center','imaginary_center','real_pair','imaginary_pair')
CONTROLS=('wrong_pair_compensation','omit_even_repair','omit_odd_center',
          'wrong_radical_relation','wrong_fourth_binomial','missing_critical_slot',
          'missing_ninth_original','wrong_skew_cubic','monomial_carry',
          'omit_lower_pair_cubic','wrong_chi_payment')


def need(condition,message):
    if not condition:raise RuntimeError(message)


def source_check():
    manifest=HERE/'SHA256SUMS'
    need(manifest.is_file(),'SOURCE missing source manifest')
    entries={}
    for line in manifest.read_text().splitlines():
        digest,name=line.split('  ',1)
        need(name==Path(name).name and name not in entries,'SOURCE invalid manifest name')
        need(len(digest)==64 and all(c in '0123456789abcdef' for c in digest),'SOURCE malformed hash')
        entries[name]=digest
    need({'profiles.py','checks.py','verify.py','DEPENDENCIES.json','EXPECTED.json','PROOF.md'}<=set(entries),
         'SOURCE incomplete critical source census')
    for name,digest in entries.items():
        need(sha256((HERE/name).read_bytes()).hexdigest()==digest,'SOURCE entire own byte seal '+name)


def expected_check(value):
    need(type(value) is dict and value.get('schema')=='complex-profile-cap-v1','TYPE expected schema')
    need(value.get('agent')=='six-sendov-3' and value.get('role')=='researcher','TYPE actual author')
    need(value.get('formalization') is False and value.get('independent_review') is False,'TYPE proof/review status')
    need(value.get('scope')=='displayed-fixed-compact-constructed-cap','TYPE quantified coverage')
    rows=value.get('stages')
    need(type(rows) is dict and set(rows)==set(STAGES),'TYPE complete stage census')
    for name,row in rows.items():
        need(type(row) is dict and type(row.get('identity_count')) is int and row['identity_count']>0,'TYPE identity count '+name)
        digest=row.get('whole_record_sha256')
        need(type(digest) is str and len(digest)==64 and all(c in '0123456789abcdef' for c in digest),'TYPE whole-record seal '+name)
        need(type(row.get('whole_record_bytes')) is int and row['whole_record_bytes']>0,'TYPE whole-record length '+name)


def control(name,p):
    s=p.s
    old=p.family
    if name in ('wrong_pair_compensation','omit_even_repair','omit_odd_center','missing_critical_slot'):
        def damaged(*args,**kwargs):
            if name=='omit_even_repair':
                kwargs['paid']=False
                args=tuple(args[1:]) if args else args
            points,B,D2=old(*args,**kwargs)
            if name=='wrong_pair_compensation':D2=s.pa(D2,{(6,0):s.gf(s.ns(p.VI,-1))})
            if name=='omit_odd_center':
                shift={(9,0):(s.N0,s.ns(p.nu,-1))}
                points=[s.pa(x,shift) for x in points];B=s.pa(B,shift)
            if name=='missing_critical_slot':points=points[:-1]
            return points,B,D2
        p.family=damaged
    elif name=='wrong_radical_relation':p.HALF_H=p.ar.ns(p.HALF_H,2)
    elif name=='wrong_fourth_binomial':
        def damaged(v,order=9):
            q=s.pa(v,{(0,0):s.gs(s.G1,-1)})
            return s.pa({(0,0):s.G1},s.ps(q,p.F(-1,2)),s.ps(s.pp(q,2,order),p.F(3,8)),
                        s.ps(s.pp(q,3,order),p.F(-5,16)),s.ps(s.pp(q,4,order),p.F(36,128)))
        p.reciprocal_distance=damaged
    elif name=='missing_ninth_original':p.prior['all_nine_shrinking_roots_epsilon0to9']=p.prior['all_nine_shrinking_roots_epsilon0to9'][:-1]
    elif name=='wrong_skew_cubic':p.TI=s.ns(p.TI,-1)
    elif name=='omit_lower_pair_cubic':p.LOWER_THIRD_PAIR_FACTOR=p.F(0)
    elif name=='wrong_chi_payment':p.chi=s.ns(p.chi,2)
    elif name=='monomial_carry':p.multiply(p.var(0),{15:p.ar.N1})


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage',choices=STAGES,default='algebra')
    parser.add_argument('--emit',action='store_true',help='author-only compact seal generation; coefficient equations still checked')
    parser.add_argument('--record',type=Path,help='optional full record OUTSIDE this source directory')
    parser.add_argument('--source-only',action='store_true')
    parser.add_argument('--control',choices=CONTROLS,help=argparse.SUPPRESS)
    args=parser.parse_args()
    if not args.emit:source_check()
    if args.source_only:
        need(not args.emit and not args.control,'TYPE source-only mode')
        print(json.dumps({'status':'PASS entire source seals','agent':'six-sendov-3','role':'researcher'}));return
    expected=None
    if not args.emit:
        expected=json.loads((HERE/'EXPECTED.json').read_text());expected_check(expected)
    sys.path.insert(0,str(HERE))
    import profiles as p
    import checks
    t0=time.monotonic()
    if args.control:control(args.control,p)
    if args.stage in ('algebra','lower_centers','literal','distance','roots'):
        record=getattr(checks,args.stage)()
    else:record=checks.repair_column(args.stage)
    need(record['independent_review'] is False and record['formalization'] is False,'TYPE actual record proof status')
    data=p.ar.canonical(record)
    compact={'identity_count':record['identity_count'],'whole_record_sha256':sha256(data).hexdigest(),
             'whole_record_bytes':len(data)}
    if expected is not None:need(compact==expected['stages'][args.stage],'RECORD entire reconstructed coefficient record '+args.stage)
    if args.record:
        target=args.record.resolve()
        need(not target.is_relative_to(HERE),'SOURCE bulky record must remain outside source directory')
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_bytes(data+b'\n')
    print(json.dumps({'agent':'six-sendov-3','role':'researcher','status':'PASS whole coefficient maps before seal',
        'stage':args.stage,**compact,'seconds':time.monotonic()-t0,
        'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        'formalization':False,'independent_review':False},sort_keys=True))


if __name__=='__main__':main()
