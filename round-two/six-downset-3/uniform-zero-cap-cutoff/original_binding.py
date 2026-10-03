"""Every actual member pair binds both complete new original cap frames."""
from pathlib import Path
from fractions import Fraction as F
import json
import cap


def verify(q,k):
    N,s=cap.r.parameters(q,k)
    members=cap.r.domain(q,0)[1:]
    table=cap.r.table(q)
    trivial=[[F(0)]*11 for _ in range(11)]
    standard=[[F(0)]*6 for _ in range(6)]
    norms=[0]*11
    census=[]
    for member in members:
        core,outside=member&7,(member>>3).bit_count()
        i=next(i for i,(groups,t) in enumerate(zip(cap.GROUPS,cap.TYPES))
               if core in groups and outside==t[1])
        value=int(bool(member&(1<<3)))-int(bool(member&(1<<4)))
        j=next((j for j,(groups,t) in enumerate(zip(cap.c.GROUPS,cap.c.TYPES))
                if core in groups and outside==t[1]),None) if value else None
        norms[i]+=1;census.append((member,i,j,value))
    for aa,i,j,x in census:
        for bb,ii,jj,y in census:
            # Actual C0 entry includes -J; J cancels in this original U.
            lower=cap.r.entry(q,s,table,aa,bb)[0]
            upper=F(N*int(aa==bb)-1)-lower
            trivial[i][ii]+=upper
            if j is not None and jj is not None:standard[j][jj]+=x*y*upper
    expected,mass=cap.full_trivial_gram(q,k)
    cap.require(norms==mass,'ENTIRE actual full11 indicator member census')
    cap.require(trivial==expected,'ALL121 full11 Gram entries from EVERY actual ordered pair')
    cap.require(standard==cap.standard(q,k)[1]['standard_gram'],
                'ALL36 standard6 Gram entries from EVERY actual ordered pair')
    return {'q':q,'k':k,'original_full_nonempty_members':len(members),
            'every_actual_ordered_pair_count':len(members)**2,
            'all11_original_census':norms,'all_complete_original_frames_match':True,
            'whole_actual_pair_record_sha256':cap.r.exact.digest(cap.r.encode([trivial,standard])),
            'this_undeleted_auxiliary_cap_is_not_asserted_positive':True}


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    value=[verify(q,k) for q,k in ((9,3),(12,4),(21,7))]
    args.out.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'all_original_ordered_pairs':sum(row['every_actual_ordered_pair_count'] for row in value)}))
