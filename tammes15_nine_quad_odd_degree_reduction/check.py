"""Necessary q9 Tammes-15 odd-degree reduction; six-tammes-1, researcher.
CPython>=3.11 standard library. Geometry and scope are in PROOF.md.
No point-coordinate, full contact-map or realizability enumeration.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import comb
import hashlib,json

LO,HI=F(1,2),F(3,5)

def need(ok,message):
    if not ok:raise ValueError(message)

def add(a,b):
    return tuple((a[k] if k<len(a) else 0)+(b[k] if k<len(b) else 0) for k in range(max(len(a),len(b))))

def mul(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return tuple(out)

def value(p,x):
    out=F(0)
    for a in reversed(p):out=out*x+a
    return out

def bernstein(p):
    n=len(p)-1
    power=[sum(F(p[j])*comb(j,k)*LO**(j-k)*(HI-LO)**k for j in range(k,n+1)) for k in range(n+1)]
    return tuple(sum(power[k]*F(comb(i,k),comb(n,k)) for k in range(i+1)) for i in range(n+1))

def basic_arithmetic():
    D=(1,2,-1);H=(1,2)
    P=(1,4,2,-4,-11,-24)
    need(add(mul(D,D),(0,0,0,0,-12,-24))==P,'beta polynomial equals D^2-12c^4H')
    margin=add(D,(0,0,-2,-4))
    need(margin==mul((1,1),(1,1,-4)),'y>pi-alpha tangent numerator')
    polynomials={'D':D,'H':H,'1+c-4c^2':(1,1,-4),
                 'minus_beta_derivative':(-4,-4,12,44,120),
                 'H_edge_lower_plus_one_third_numerator':(-2,-2,12)}
    records={}
    for name,p in polynomials.items():
        bs=bernstein(p)
        need(all(x>=0 for x in bs) and any(x>0 for x in bs),'positive interior Bernstein coefficients: '+name)
        records[name]={'power':p,'Bernstein_on_closed_half_three_fifths':list(map(str,bs))}
    need(value(P,F(119,200))>0 and value(P,HI)<0,'beta isolated in (119/200,3/5)')
    need(F(3,8)>F(4,11),'three small corners at a one-T four cannot sum with one T')
    need(512<529,'alpha>3pi/8 exact squared comparison')
    need(F(1,25)<F(1,16),'small-diagonal side bound')
    need(F(-1,3)*F(1,16)==F(-1,48),'side-product lower bound')
    need((F(-1,3)-F(1,9))/F(8,9)==F(-1,2),'H triangle cosine lower threshold')
    need((F(1,16)+F(1,48))/F(8,9)==F(3,32),'H triangle cosine upper threshold')
    return {'polynomials':records,'beta_polynomial':P,
            'beta_endpoint_values':[str(value(P,F(119,200))),str(value(P,HI))],
            'y_minus_pi_minus_alpha_tangent_numerator':margin,
            'r4_rows':[{'a':6-2*b,'b':b,'ordinary_fours':1+b,
                        'at_least_four_distinct_ordinary_fours':1+b>=4,
                        'if_b3_common_neighbors_of_two_zero_T_fours':4 if b==3 else None} for b in range(4)]}

def compositions(total,length):
    if length==1:yield (total,)
    else:
        for k in range(total+1):
            for rest in compositions(total-k,length-1):yield (k,)+rest

def raw_profiles(r):
    n4=15-2*r;out=[]
    for f in compositions(r,5):
        used=sum(j*f[j] for j in range(5))
        if used>6:continue
        for b in range((6-used)//2+1):
            a=6-used-2*b
            if a+b<=n4:
                need(a+2*(n4-a-b)+sum((4-j)*f[j] for j in range(5))==24,'eight triangles: 24 corners')
                out.append((a,b)+f)
    return tuple(sorted(out))

def caps(row):
    a,b,f0,f1,f2,f3,f4=row
    need(not f3 and not f4,'deficient-five deficit at most two')
    return tuple([2]*a+[3]*b+[2]*f1+[3]*f2), tuple([2]*a+[4]*b+[1]*f1+[2]*f2),a+b

def h_valid(row,mask):
    hc,uc,first_five=caps(row);n=len(hc);pairs=tuple(combinations(range(n),2))
    if type(mask) is not int or mask<0 or mask>=1<<len(pairs):return False
    deg=[0]*n;adj=[0]*n
    for k,(i,j) in enumerate(pairs):
        if mask>>k&1:deg[i]+=1;deg[j]+=1;adj[i]|=1<<j;adj[j]|=1<<i
    if any(deg[i]>hc[i] or (i>=first_five and deg[i]!=hc[i]) for i in range(n)):return False
    return not any(adj[i]&adj[j] for i,j in pairs if adj[i]>>j&1)

def h_masks(row):
    hc,uc,first_five=caps(row);n=len(hc);pairs=tuple(combinations(range(n),2));adj=[0]*n;deg=[0]*n;out=[]
    def visit(k,mask):
        if k==len(pairs):
            if all(i<first_five or deg[i]==hc[i] for i in range(n)):
                need(h_valid(row,mask),'whole generated H entry is valid');out.append(mask)
            return
        i,j=pairs[k]
        visit(k+1,mask)
        if deg[i]<hc[i] and deg[j]<hc[j] and not adj[i]&adj[j]:
            deg[i]+=1;deg[j]+=1;adj[i]|=1<<j;adj[j]|=1<<i
            visit(k+1,mask|1<<k)
            deg[i]-=1;deg[j]-=1;adj[i]^=1<<j;adj[j]^=1<<i
    visit(0,0)
    return tuple(sorted(out))

def u_valid(row,r,family):
    hc,uc,first_five=caps(row);n=len(uc)
    if len(family)!=r or len(set(family))!=r:return False
    if any(len(t)!=3 or tuple(sorted(set(t)))!=t or any(v not in range(n) for v in t) for t in family):return False
    if any(sum(v>=first_five for v in t)>1 for t in family):return False
    deg=Counter(v for t in family for v in t)
    if any(deg[i]>uc[i] for i in range(n)):return False
    common=Counter(p for t in family for p in combinations(t,2))
    return not any(k>2 for k in common.values())

def u_families(row,r):
    hc,uc,first_five=caps(row);out=[]
    for family in combinations(tuple(combinations(range(len(uc)),3)),r):
        if u_valid(row,r,family):out.append(family)
    return tuple(out)

def digest(entries):
    return hashlib.sha256(json.dumps(entries,separators=(',',':')).encode()).hexdigest()

def finite_cover():
    rows=[];rejections={};raw_counts={}
    for r in range(1,8):
        raw=raw_profiles(r);raw_counts[r]=len(raw);why=Counter()
        for row in raw:
            a,b,f0,f1,f2,f3,f4=row
            if r>=4:why['r_at_least_four_excluded_by_written_contact_incidence_proof']+=1;continue
            if f3 or f4:why['five_deficit_at_least_three']+=1;continue
            if 3*r+f1+2*f2>12:why['degree_three_contact_capacity']+=1;continue
            h=h_masks(row)
            if not h:why['no_necessary_triangle_free_H']+=1;continue
            u=u_families(row,r)
            if not u:why['no_necessary_degree_three_neighbor_family']+=1;continue
            rows.append({'r':r,'a':a,'b':b,'five_counts_f0_f1_f2':[f0,f1,f2],
                         'ordinary_fours':15-2*r-a-b,'H_labeled_count':len(h),'H_masks_sha256':digest(h),
                         'U_unlabeled_family_count':len(u),'U_families_sha256':digest(u),
                         'first_H_mask':h[0],'first_U_family':u[0]})
        rejections[r]=dict(sorted(why.items()))
    counts=dict(sorted(Counter(x['r'] for x in rows).items()))
    need(counts=={1:9,2:12,3:11},'complete necessary count profile cover')
    return {'raw_deficit_six_counts':raw_counts,'rejection_counts':rejections,
            'surviving_count_profiles_by_r':counts,'total_necessary_count_profiles':len(rows),'profiles':rows}

def star_audit():
    records=[]
    for d,t,cap in [(3,0,3),(4,0,4),(4,1,2),(4,2,1),(5,2,2),(5,3,1),(5,4,0)]:
        words=[]
        for positions in combinations(range(d),t):
            word=tuple('T' if i in positions else 'Q' for i in range(d))
            qq=sum(word[i]==word[(i+1)%d]=='Q' for i in range(d))
            need(qq<=cap,'every cyclic star Q-Q capacity')
            if d==4 and t<=1:
                need(all(word[i]!='Q' or word[(i-1)%d]=='Q' or word[(i+1)%d]=='Q' for i in range(d)),
                     'each deficient-four Q touches a Q-Q edge in the r4 equality case')
            words.append({'word':''.join(word),'Q_Q_edges':qq})
        need(max(w['Q_Q_edges'] for w in words)==cap,'capacity includes its maximum cyclic star')
        records.append({'degree':d,'triangles':t,'maximum_Q_Q_contacts':cap,'all_cyclic_words':words})
    return records

def controls():
    # Row order: a,b,f0,f1,f2,f3,f4.
    ordinary=(0,3,1,0,0,0,0)
    need(not h_valid(ordinary,7),'H triangle negative control')
    five=(4,0,0,0,1,0,0)
    need(not h_valid(five,0),'missing exact five H degree negative control')
    need(not u_valid(ordinary,2,((0,1,2),(0,1,2))),'two degree threes share three contacts negative control')
    highcommon=(6,0,3,0,0,0,0)
    need(not u_valid(highcommon,3,((0,1,2),(0,1,3),(0,1,4))),'three common contacts of one D pair negative control')
    limited=(1,2,0,1,0,0,0)
    need(not u_valid(limited,2,((0,1,3),(0,2,3))),'deficit-one five has at most one degree-three contact negative control')
    two_fives=(4,0,0,2,0,0,0)
    need(not u_valid(two_fives,2,((0,4,5),(1,2,3))),'one degree-three cannot contact two degree fives negative control')
    need(h_valid(ordinary,0),'empty necessary H positive control')
    need(u_valid(ordinary,1,((0,1,2),)),'one degree-three necessary star positive control')
    return {'negative_controls_rejected':6,'positive_controls_accepted':2}

def main():
    out={'agent':'six-tammes-1','role':'researcher','local_degree_bound_interval':['1/2','3/5'],
         'H_and_32_profile_interval':['1/2','beta'],
         'geometry_trust_boundary':'written unformalized proof; all-degree-four lower exclusion is an external published dependency',
         'arithmetic':basic_arithmetic(),'cyclic_star_audit':star_audit(),'cover':finite_cover(),'controls':controls(),
         'conclusion':'q9 branch has 1<=n3=n5<=3; on beta it has 32 necessary count profiles, with a triangle-free small-corner graph and necessary original-neighbor stars. No realizability or global bound claimed.'}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
