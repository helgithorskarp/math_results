"""Check the local convex-hull obstruction using only integer arithmetic."""
from copy import deepcopy
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import hashlib,json


def require(condition, message):
    if not condition: raise ValueError(message)


def integer(value):
    return type(value) is int


def geometry():
    points=[(x,y,z) for z in range(5) for x in range(5) for y in range(5)]
    index={p:i for i,p in enumerate(points)}
    lines={tuple(sorted(index[tuple((a[j]+t*(b[j]-a[j]))%5 for j in range(3))]
                        for t in range(5))) for a,b in combinations(points,2)}
    normals=[d for d in product(range(5),repeat=3) if any(d) and next(x for x in d if x)==1]
    planes={tuple(i for i,p in enumerate(points) if sum(a*b for a,b in zip(p,d))%5==t)
            for d in normals for t in range(5)}
    require(len(points)==125 and len(lines)==775 and len(planes)==155,'geometry sizes')
    return points,sorted(lines),planes


def verify(data, geo=None):
    points,lines,planes=geometry() if geo is None else geo
    require(data['field']==5 and data['point_order']=='index=25*z+5*x+y','coordinate convention')
    d=data['denominator'];q=data['point_numerators']
    require(integer(d) and d>0 and len(q)==125 and all(integer(v) and 0<=v<=d for v in q),
            'point weights')
    grid=sum(1<<(5*x+y) for x in range(4) for y in range(4))
    require(data['fixed_z0_selected_mask']==grid,'grid normalization')
    require(all(q[i]==(d if grid>>i&1 else 0) for i in range(25)),'fixed maximum plane')
    require(data['fixed_hole']==25 and q[25]==0,'fixed low-plane hole')
    require((data['small_plane_z'],data['small_plane_cap'],data['small_plane_line_cap'])==(1,10,3),
            'small-plane definition')
    require(sum(q)>73*d,'certificate needs mass above73')
    mass=Fraction(sum(q),d)
    alpha=Fraction(55,1)/(mass-16)
    thinned=[Fraction(v,d) if i<25 else alpha*Fraction(v,d) for i,v in enumerate(q)]
    require(0<alpha<1 and sum(thinned)==71,'exact thinning identity')
    seen=set();terms=0;minimum_slack=None;low_component_sizes=set();ordinary_sizes=set()
    maximum_expected_deletions=Fraction(0)
    for record in data['planes']:
        plane=tuple(record['points'])
        require(all(integer(i) for i in plane) and plane in planes and plane not in seen,
                'missing, repeated or invalid affine plane')
        seen.add(plane);position={p:j for j,p in enumerate(plane)}
        local_lines=[sum(1<<position[i] for i in line) for line in lines if set(line)<=set(plane)]
        require(len(local_lines)==30,'local line count')
        is_low=all(points[i][2]==1 for i in plane)
        mandatory=sum(1<<j for j,i in enumerate(plane) if i<25 and grid>>i&1)
        prohibited=sum(1<<j for j,i in enumerate(plane) if (i<25 and not(grid>>i&1)) or i==25)
        sums=[0]*25;total=0;seen_masks=set()
        for mask,weight in record['mixture']:
            require(integer(mask) and 0<=mask<(1<<25) and mask not in seen_masks,'component mask')
            seen_masks.add(mask)
            require(integer(weight) and weight>0,'mixture weight')
            require(mask&mandatory==mandatory and mask&prohibited==0,'component violates fixed points')
            require(mask.bit_count()<=16,'component exceeds planar cap')
            require(all(mask&line!=line for line in local_lines),'component has full line')
            if is_low:
                require(mask.bit_count()<=10 and all((mask&line).bit_count()<=3 for line in local_lines),
                        'component violates low-plane conditions')
                low_component_sizes.add(mask.bit_count())
                require(mask.bit_count()==10,'low component must have ten points')
            else:
                require(mask.bit_count()>=14,'ordinary component must have at least fourteen points')
                ordinary_sizes.add(mask.bit_count())
            for j in range(25):
                if mask>>j&1:sums[j]+=weight
            total+=weight;terms+=1
        require(total==d,'mixture coefficients do not sum to one')
        for j,i in enumerate(plane):
            slack=sums[j]-q[i]
            require(slack>=0,'local mixture does not dominate point marginal')
            minimum_slack=slack if minimum_slack is None else min(minimum_slack,slack)
        deletion=[Fraction(0) if sums[j]==0 else 1-thinned[i]/Fraction(sums[j],d)
                  for j,i in enumerate(plane)]
        require(all(0<=v<=1 for v in deletion),'invalid deletion probability')
        for mask,_ in record['mixture']:
            probability=sum(deletion[j] for j in range(25) if mask>>j&1)
            require(probability<=mask.bit_count()-7,'cannot preserve seven selected points')
            maximum_expected_deletions=max(maximum_expected_deletions,probability)
    require(seen==planes,'incomplete plane coverage')
    return {'status':'PLANAR_LOCAL_OBSTRUCTION_VERIFIED','points':125,'lines':775,'planes':155,
            'mixture_terms':terms,'mass':str(mass),'denominator':d,'minimum_domination_slack':minimum_slack,
            'small_plane_component_sizes':sorted(low_component_sizes),
            'ordinary_component_sizes':sorted(ordinary_sizes),
            'bounded_deletion_preserves_minimum_section_size':7,
            'maximum_expected_deletions_less_than_six':maximum_expected_deletions<6,
            'resulting_ordinary_sizes_contained_in':[7,16],
            'resulting_small_plane_sizes_contained_in':[7,10],
            'thinning_factor_to_mass71':str(alpha),'target_mass':71,
            'scope':'Fractional planar marginal certificate, not a line-free point set.'}


def main():
    here=Path(__file__).resolve().parent;path=here/'CERTIFICATE.json'
    data=json.loads(path.read_text());geo=geometry();out=verify(data,geo)
    corruptions=[]
    a=deepcopy(data);a['point_numerators'][0]=a['denominator']+1;corruptions.append(a)
    a=deepcopy(data);a['planes'].pop();corruptions.append(a)
    a=deepcopy(data);a['planes'][0]['mixture'][0][1]=-1;corruptions.append(a)
    a=deepcopy(data);a['planes'][0]['mixture'][0][1]+=1;corruptions.append(a)
    a=deepcopy(data);a['planes'][0]['mixture'][0][0]=(1<<25)-1;corruptions.append(a)
    a=deepcopy(data);a['planes'][1]['points']=a['planes'][0]['points'];corruptions.append(a)
    rejected=0
    for bad in corruptions:
        try:verify(bad,geo)
        except ValueError:rejected+=1
    require(rejected==len(corruptions),'malformed certificate accepted')
    out['malformed_controls_rejected']=rejected
    out['certificate_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    print(json.dumps(out,indent=2,sort_keys=True))


if __name__=='__main__':main()
