"""Two independent original-congruence/quarter kernels; shared record schema only."""
import argparse
from hashlib import sha256
import json
from pathlib import Path


def envelope(parent, rows, raw):
    return {'agent':'six-covering-2','role':'researcher','schema':1,'stage':'two-seven-physical-bridge',
        'literal_prefix':[[8,0],[9,0],[10,1],[14,0],[12,10],[16,2],[28,4],[32,6]],
        'minimum_exactly':8,'original_moduli_divide':10080,'productive_TAILs_exactly':9,
        'actual_hole_parent_counts':[2,7],'essential_originals_explicit':[16,32],
        'all_other_original_labels_phases_omissions_free':True,'unproductive_selected_tails_allowed':True,
        'actual_LCM_may_be_proper_divisor':True,'global_bound_changed':False,
        'quarter_bit_order':[6,14,22,30],'initial_R6':parent,'all_original_phase_masks':rows,
        'physical_n_phase_membership_checks':len(rows)*len(parent)*4,
        'raw_bytes':len(raw),'raw_sha256':sha256(raw).hexdigest(),
        'ordinary_proof_formalized':False,'independent_person_reviewed':False,
        'shared_between_algorithms':'argument driver and literal record schema; no shared arithmetic kernel'}


def direct():
    prefix=((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))
    xs=[x for x in range(6,2520,8) if all(x%m!=a for m,a in prefix)]
    ds=[d for d in range(3,316) if 315%d==0]
    rows=[];raw=bytearray()
    for family,two,bands in (('H',16,(6,14)),('Q',32,(6,14,22,30))):
        for d in ds:
            for b in bands:
                expected_mask=sum(1<<i for i,q in enumerate((6,14,22,30)) if q%two==b)
                for a in range(d):
                    phase=(a+d*((b-a)*pow(d,-1,two)%two))%(two*d)
                    values=[]
                    for x in xs:
                        bits=0
                        for k in range(4):
                            n=x+2520*k
                            if n%(two*d)==phase:
                                bits|=1<<((n%32-6)//8)
                        if bits!=(expected_mask if x%d==a else 0):
                            raise ValueError('Original phase does not have stated quarter/odd support')
                        values.append(bits)
                    rows.append([family,d,b,a,phase,expected_mask,values]);raw.extend(values)
    return envelope(xs,rows,raw),bytes(raw)


def progression():
    removed=set()
    for m,a in ((8,0),(9,0),(10,1),(14,0),(12,10),(28,4)):
        removed.update(range(a,2520,m))
    xs=sorted(set(range(6,2520,8))-removed);lookup={x:i for i,x in enumerate(xs)}
    ds=sorted({3**i*5**j*7**k for i in range(3) for j in range(2) for k in range(2)}-{1})
    rows=[];stream=bytearray()
    for family,two,bands in (('H',16,(6,14)),('Q',32,(6,14,22,30))):
        for d in ds:
            for b in bands:
                compatible_phases={a%d:a for a in range(b,two*d,two)}
                expected=sum(2**i for i,q in enumerate([6,14,22,30]) if q%two==b)
                for a in range(d):
                    phase=compatible_phases[a];values=[0]*len(xs)
                    for n in range(phase,10080,two*d):
                        x=n%2520
                        if x not in lookup:continue
                        values[lookup[x]]|=2**([6,14,22,30].index(n%32))
                    if values!=[expected if x%d==a else 0 for x in xs]:
                        raise ValueError('Literal AP kernel violates projected odd/quarter description')
                    rows.append([family,d,b,a,phase,expected,values]);stream.extend(values)
    return envelope(xs,rows,stream),bytes(stream)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--audit',action='store_true');p.add_argument('--out',type=Path,required=True);p.add_argument('--raw',type=Path,required=True)
    p.add_argument('--reference',type=Path);p.add_argument('--reference-raw',type=Path);a=p.parse_args()
    r,raw=progression() if a.audit else direct()
    b=(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n').encode()
    if a.audit and (b!=a.reference.read_bytes() or raw!=a.reference_raw.read_bytes()):
        raise ValueError('Whole original phase record or raw stream differs between kernels')
    a.out.write_bytes(b);a.raw.write_bytes(raw)
    print(json.dumps({'mode':'audit' if a.audit else 'direct','all_original_rows':len(r['all_original_phase_masks']),
                      'membership_checks':r['physical_n_phase_membership_checks'],'raw_bytes':len(raw),
                      'sha256':sha256(b).hexdigest()}))
