"""Post-seal mathematical fixture audit; author executables never imported/run."""
from pathlib import Path
from fractions import Fraction
import copy, hashlib, json
from check import run, F, require, times, scale, companion, meval, zdiff, mmul, mscale, ident, encode

KEYS={'angular_denominator_u','angular_numerator_u','complete_bernstein_denominator',
      'complete_bernstein_divided_gap','critical_quartic','discriminant',
      'discriminant_divided_by_inverse_denominator','domain','inverse_common_denominator','inverse_numerators'}
DOMAIN='QQ[r][z], r>1 and B=1+2r^2-r^4-r^6>0'
LENGTHS={'angular_denominator_u':19,'angular_numerator_u':19,
         'complete_bernstein_denominator':19,'complete_bernstein_divided_gap':18,
         'discriminant':37,'discriminant_divided_by_inverse_denominator':1,
         'inverse_common_denominator':37}

def pairs(rows):
    out={}
    for k,v in rows:
        require(k not in out,'duplicate JSON key')
        out[k]=v
    return out

def vector(row,n):
    require(type(row)is list and len(row)==n,'entire typed rational vector shape')
    out=[]
    for s in row:
        require(type(s)is str,'rational string type')
        q=Fraction(s)
        require(str(q)==s,'canonical rational spelling')
        out.append(q)
    return out

def parse(data):
    require(type(data)is dict and set(data)==KEYS,'entire ten-key certificate schema')
    require(data['domain']==DOMAIN,'exact specialization domain')
    out={k:vector(data[k],n)for k,n in LENGTHS.items()}
    for k,lengths in [('critical_quartic',[13,8,7,2,1]),('inverse_numerators',[26,25,20,19])]:
        require(type(data[k])is list and len(data[k])==len(lengths),'whole polynomial list shape')
        out[k]=[vector(v,n)for v,n in zip(data[k],lengths)]
    out['domain']=DOMAIN
    return out

def audit(data,own):
    c=parse(data)
    for native,ours in [('angular_denominator_u','Den'),('angular_numerator_u','Num'),
                        ('complete_bernstein_denominator','Den_Bernstein'),
                        ('complete_bernstein_divided_gap','gap_Bernstein'),
                        ('critical_quartic','H4'),('discriminant','norm_discriminant')]:
        require(encode(c[native])==own[ours],'whole mathematical fixture '+native)
    d=c['inverse_common_denominator'];w=c['discriminant_divided_by_inverse_denominator']
    require(times(d,w)==c['discriminant'],'all norm-to-native inverse scale coefficients')
    M=companion(c['critical_quartic']);R=meval(zdiff(c['critical_quartic']),M)
    invnum=meval(c['inverse_numerators'],M);target=mscale(ident(4),d)
    require(mmul(R,invnum)==target==mmul(invnum,R),'all16 left/right native inverse identities')
    return {'whole_native_inverse_numerator_matrix4':invnum,
            'all16_native_inverse_identity_matrix4':target,
            'whole_norm_to_inverse_scale':times(d,w),
            'matched_whole_fields':6,'schema_keys':10,
            'specialization_bridge':'four actual gap roots are distinct real, so determinant never zero'}

def main():
    path=Path(__file__).with_name('AUTHOR_CERTIFICATE.json');blob=path.read_bytes()
    data=json.loads(blob,object_pairs_hook=pairs)
    summary,raw=run();own=json.loads(raw)
    result=audit(data,own);rejected=[]
    for field in sorted(KEYS):
        damaged=copy.deepcopy(data)
        if field=='domain':damaged[field]='QQ[r][z], arbitrary complex r'
        elif field in ['critical_quartic','inverse_numerators']:
            damaged[field][0][-1]=str(F(damaged[field][0][-1])+1)
        else:damaged[field][-1]=str(F(damaged[field][-1])+1)
        try:audit(damaged,own)
        except ValueError:rejected.append(field)
        else:raise ValueError('undetected mathematical field damage '+field)
    for label,damage in [('noncanonical-rational',lambda d:d['angular_numerator_u'].__setitem__(0,'23328/2')),
                         ('wrong-rational-type',lambda d:d['angular_numerator_u'].__setitem__(0,11664)),
                         ('lost-terminal-slot',lambda d:d['angular_numerator_u'].pop()),
                         ('extra-key',lambda d:d.__setitem__('unproved',True))]:
        damaged=copy.deepcopy(data);damage(damaged)
        try:audit(damaged,own)
        except ValueError:rejected.append(label)
        else:raise ValueError('undetected typed damage '+label)
    try:json.loads('{"domain":1,"domain":2}',object_pairs_hook=pairs)
    except ValueError:rejected.append('duplicate-key')
    else:raise ValueError('duplicate key accepted')
    result.update(agent='six-reviewer-1',role='independent mathematical reviewer',
                  fixture_bytes=len(blob),fixture_sha256=hashlib.sha256(blob).hexdigest(),
                  generic_primary_record_bytes=len(raw),generic_primary_record_sha256=hashlib.sha256(raw).hexdigest(),
                  all15_controls_rejected=rejected,author_executables_read_imported_or_run=False)
    encoded=json.dumps(encode(result),sort_keys=True,separators=(',',':')).encode()
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'complete_record_bytes':len(encoded),'complete_record_sha256':hashlib.sha256(encoded).hexdigest(),
            'fixture_bytes':len(blob),'fixture_sha256':hashlib.sha256(blob).hexdigest(),
            'entire_ten_field_fixture_checked':True,'negative_controls':len(rejected),
            'all16_left_right_inverse_entries_verified':True},encoded

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--derive',action='store_true');p.add_argument('--record',type=Path);a=p.parse_args()
    summary,raw=main()
    if not a.derive:require(summary==json.loads(Path(__file__).with_name('CERTIFICATE_EXPECTED.json').read_text()),'whole supplementary record seal')
    if a.record:a.record.write_bytes(raw)
    print(json.dumps(summary,sort_keys=True,indent=2))
