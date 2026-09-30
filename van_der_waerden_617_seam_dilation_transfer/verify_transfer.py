#!/usr/bin/env python3
"""Independent exact arithmetic check of the six finite dilation identities."""
import json
import time

P=617


def require(test,message):
    if not test:raise ValueError(message)


def inverse(m):
    require(type(m) is int and m>0 and m%P!=0,'positive dilation prime to617')
    value=pow(m,-1,P);require(m*value%P==1,'inverse identity');return value


def colors():
    require(all(P%d for d in range(2,25)),'primality617')
    result=[None]
    for r in range(1,P):
        e=pow(r,308,P);require(e in (1,P-1),'Euler criterion');result.append(int(e==P-1))
    return result


def verify():
    start=time.monotonic();q=colors();partitions=0;identities=0;phase_entries=0;boundaries=0
    for m in range(1,7):
        u=inverse(m)
        for radius in (308,617):
            seen=set()
            for j in range(m):
                points={m*z+j for z in range(-radius,radius)}
                require(len(points)==2*radius and not seen.intersection(points),'class disjointness')
                require(all(-m*radius<=x<m*radius and x%m==j for x in points),'window/class containment')
                seen.update(points);partitions+=len(points)
            require(seen==set(range(-m*radius,m*radius)),'exact window partition')
        for j in range(m):
            require({u*(s+j)%P for s in range(P)}==set(range(P)),'phase bijection')
            phase_entries+=P
            for z in range(-617,617):
                y=m*z+j;require((y<0)==(z<0),'seam boundary');boundaries+=1
            for s in range(P):
                sp=u*(s+j)%P
                for z in range(-617,617):
                    actual=q[(m*z+j+s)%P];base=q[(z+sp)%P]
                    expected=None if base is None else base^q[m]
                    require(actual==expected,'nonpole/pole/color transfer');identities+=1
    controls=[]
    for m in (0,-1,P,2*P):
        try:inverse(m)
        except ValueError:controls.append('invalid_dilation_'+str(m))
        else:raise ValueError('invalid dilation accepted')
    require(q[3]!=0 and q[3]!=q[1],'color-exchange fixture')
    controls.append('omitting_whole_color_exchange')
    for name,m,j,s in [('omitting_inverse',2,0,1),('omitting_class_shift',3,1,0)]:
        wrong=s+j if name=='omitting_inverse' else inverse(m)*s
        require(any(q[(m*z+j+s)%P]!=(None if q[(z+wrong)%P] is None else q[(z+wrong)%P]^q[m]) for z in range(-617,617)),'wrong phase formula survived')
        controls.append(name)
    require(not ((3*(-1)+3<0)==(-1<0)),'off-by-one class fixture')
    controls.append('including_class_index_m')
    # A whole-color exchange applies on both sides; the relative bit is fixed.
    require((1^q[3])==0,'relative-orientation fixture')
    controls.append('applying_color_exchange_to_only_one_side')
    return {'agent':'six-vdw-3','role':'researcher','status':'VERIFIED_FINITE_TRANSFER_IDENTITIES',
            'dilations':[1,2,3,4,5,6],'point_phase_identities':identities,'partition_points':partitions,
            'seam_boundary_pairs':boundaries,'phase_permutation_entries':phase_entries,
            'arithmetic_controls_rejected':controls,'seconds':time.monotonic()-start,
            'scope':'Finite identity check for target dilations. The elementary written proof establishes the general positive dilation theorem.'}


if __name__=='__main__':print(json.dumps(verify(),indent=2))
