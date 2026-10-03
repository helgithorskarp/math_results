"""Small semantic false fixtures. No expected-output/hash rejection gate."""
import json
import semantic as s

def main():
    F=s.F;T=tuple(t for t in F if t%3==1 or t%9==0 or(t%3==2 and t%2==0))+ (6,)
    # Use the actual111 target with one point outside the110 support.
    T=tuple(sorted(set(t for t in F if t%3==1 or t%9==0 or(t%3==2 and t%2==0))|{6}))
    s.need(len(T)==111,'positive control target')
    base=[t for t in F if (4*t+3-3)%8==0]
    q=[3,9,24,720];pool=[d for d in s.D if d not in set(q)|{8,16,48}]
    G=[t for t in F if t%9==0 and t%4==3]
    positive=[('native-active',lambda:s.native(8,0,3,base)),('native-inactive',lambda:s.native(8,0,4,[])),('original-aliases',lambda:s.assignment([(3,1,0),(6,2,1),(12,3,2)])),('Q-all-omitted',lambda:s.qsize((-1,-1,-1),None,0)),('singleton-inactive',lambda:s.qsize((-1,-1,-1),3,0)),('entire-inventory',lambda:s.inventory(q,[8,16,48],pool)),('five-point-gap',lambda:s.gap(0,1,0,G)),('W-outside-Q-is-free',lambda:s.supplemental(list(set(F)-set(T))+list(T[:23]),T))]
    false=[('native-wrong-active-parity',lambda:s.native(8,0,3,[])),('native-inactive-fabricated',lambda:s.native(8,0,4,[0])),('owner-outside-domain',lambda:s.native(8,5,3,base)),('original-phase-missing',lambda:s.native(8,0,8,base)),('one-original-two-owners',lambda:s.assignment([(8,1,3),(8,2,3)])),('projected-alias-merged',lambda:s.inventory(q,[8,16,48],[d for d in pool if d!=12])),('extra-label-on-entire-Q',lambda:s.inventory(q+[8],[8,16,48],pool)),('Q-omission-fabricated',lambda:s.qsize((-1,-1,-1),None,1)),('Q-row-incorrect-count',lambda:s.qsize((1,0,0),None,111)),('singleton-inactive-counted',lambda:s.qsize((-1,-1,-1),3,1)),('binary-arm-wrong-parity',lambda:s.gap(0,0,0,G)),('gap-point-omitted',lambda:s.gap(0,1,0,G[:-1])),('gap-transversal-damaged',lambda:s.gap(0,1,0,G[:-1]+[G[0]+180])),('supplemental-intersection24',lambda:s.supplemental(T[:24],T)),('supplemental-outside-F',lambda:s.supplemental([3],T))]
    for name,fn in positive:fn()
    rejected=[]
    for name,fn in false:
        try:fn()
        except ValueError:rejected.append(name)
        else:raise ValueError('semantic false fixture accepted: '+name)
    return {'status':'COMPLETE_SEMANTIC_CONTROLS','positive':[n for n,f in positive],'rejected':rejected,'expected_or_hash_gate':False,'target_data_inputs':False}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True))
