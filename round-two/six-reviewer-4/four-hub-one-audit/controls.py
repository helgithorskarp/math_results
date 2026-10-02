"""Exact independent tiny controls for Boolean columns, coupled tuples,
support union, and friend-graph degrees. No target import; tiny cases call the independently written column kernel.
"""
from itertools import combinations
from audit import column_choices,joint,PAIRS
from rows import need,encoded
import json

def must_reject(f):
    try:f()
    except ValueError:return True
    raise ValueError('semantic damage was accepted')

def verify_kernel(v,options,mask,a,d,expected):
    got=column_choices(v,options,mask,a,d)
    need(tuple(expected)==got,'column semantic witness mismatch')

def main():
    opts={(0,0,0):((1,1),)}
    need(column_choices([2],opts,0,0,2)==(2,),'two vertices form one friend edge')
    need(not column_choices([1],opts,0,0,1),'one vertex cannot have one friend')
    need(not column_choices([3],opts,0,0,3),'odd friend handshake rejects')
    low={(0,0,0):((0,0),(1,0))}
    need(column_choices([3],low,0,0,2)==(2,),'LOW options and isolated friends')
    need(joint([(3,)]*4,12,[4]*6,[4]*6)==((3,3,3,3),),'same coupled positive tuple')
    need(not joint([(3,)]*4,11,[4]*6,[4]*6),'wrong coupled support sum')
    need(not joint([(3,)]*4,12,[3,4,4,4,4,4],[2,4,4,4,4,4]),'one excessive leave quota')
    damages=[]
    for name,f in [
        ('friend support',lambda:verify_kernel([1],opts,0,0,1,[1])),
        ('friend parity',lambda:verify_kernel([3],opts,0,0,3,[3])),
        ('omitted positive support count',lambda:verify_kernel([3],low,0,0,2,[1])),
        ('missing admissible column',lambda:verify_kernel([2],opts,0,0,2,[])),
        ('fabricated LOW deficit',lambda:verify_kernel([3],low,0,0,2,[2,3])),
    ]:
        need(must_reject(f),'damage rejection');damages.append(name)
    # Complete four-column membership systems on four centers: every center
    # independently belongs to any subset of the four support columns.
    systems=0;strict=0
    for word in range(16**4):
        centers=[(word>>(4*i))&15 for i in range(4)]
        n=[sum(m>>a&1 for m in centers)for a in range(4)]
        c=[sum((m>>a&1)and(m>>b&1)for m in centers)for a,b in PAIRS]
        unions=[sum(bool(m & ((1<<a)|(1<<b)))for m in centers)for a,b in PAIRS]
        need(unions==[n[a]+n[b]-cc for (a,b),cc in zip(PAIRS,c)],'exact pair union')
        kk=sum(m.bit_count()for m in centers)
        overlap=sum(m.bit_count()*(m.bit_count()-1)//2 for m in centers)
        need(sum(unions)==3*kk-overlap,'exact six-union identity')
        strict+=overlap>0;systems+=1
    graphs=0
    for n in range(1,6):
        edges=list(combinations(range(n),2))
        for word in range(1<<len(edges)):
            degrees=[sum(bool(word>>i&1)and v in edge for i,edge in enumerate(edges))for v in range(n)]
            need(sum(degrees)%2==0 and sum(degrees)<=n*(n-1),'friend handshake/capacity')
            need(all(d<n for d in degrees),'friend degree bound');graphs+=1
    print(json.dumps({'valid_kernel_controls':3,'semantic_damages_rejected':damages,
                      'support_membership_systems':systems,'strict_union_systems':strict,
                      'friend_graphs':graphs},sort_keys=True))

if __name__=='__main__':main()
