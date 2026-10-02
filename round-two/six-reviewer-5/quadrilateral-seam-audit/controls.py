"""Post-seal semantic damages and representation controls for own evidence."""
import json,pathlib,copy,itertools
from fractions import Fraction as F
import audit as I
import kernel as K

def check(a):
    expected={(q,k) for q in itertools.product((4,5),repeat=3) for k in itertools.product(*(range(2,n-1) for n in q))}
    records={(tuple(r['q']),tuple(r['k'])):r for r in a['ports']}
    K.need(set(records)==expected and len(a['ports'])==27,'full literal domain')
    for r in a['ports']:
        classmap={tuple(v):tuple(map(tuple,c)) for c in r['vertex_classes'] for v in c}
        membership={tuple(map(tuple,c)):i for i,cy in enumerate(r['cycles']) for c in cy['vertices']}
        K.need(len(r['cycles'])==2 and len(membership)==sum(r['q'])-6,'all boundary vertices')
        sm={s['faces'][0]:s for s in r['seam_boundaries']}
        K.need(set(sm)=={0,1,2} and len(r['seam_boundaries'])==3,'exact three seams')
        for i,k in enumerate(r['k']):
            s=sm[i];ep=[classmap[(i,k)],classmap[(i,k+1)]]
            K.need(s['faces']==[i,(i+1)%3] and [tuple(map(tuple,x)) for x in s['endpoints']]==ep,'seam physical endpoint binding')
            sides=[membership[x] for x in ep]
            K.need(s['boundaries']==sides and set(sides)=={0,1},'opposite boundary membership')
    K.need(len(a['discriminants'])==3 and {r['t'] for r in a['discriminants']}=={1,2,3},'all t')
    for r in a['discriminants']:
        p=K.trim(r['polynomial']);t=r['t']
        K.need(len(p)-1==t+1,'cleared degree')
        for c in range(t+2):K.need(K.value(p,F(c))==I.discriminant(c,t)['numerator'],'rational numerator identity')
        b=I.bernstein(p,F(9,20),F(1))
        K.need(list(map(str,b))==r['bernstein'] and all(x<0 for x in b),'whole strict signs')
    n=a['new_bound'];K.need(n==dict(cleared_excess=['-1','0','5'],threshold_squared='1/5',old_band_squared_gap='1/400',strict_diagonal=True),'new physical strict bound binding')
    b=a['boundary_control'];edges=sorted([(0,j) for j in range(1,6)]+[tuple(sorted((j,1+j%5))) for j in range(1,6)])
    K.need(b['complete_edges']==[list(e) for e in edges],'complete icosahedral wheel')
    K.need(b['deleted_contacts']==[[0,2],[0,4]] and b['incomplete_edges']==[list(e) for e in edges if e not in [(0,2),(0,4)]],'fake faces versus actual diagonals')
    K.need(len(a['prism'])==15 and all(F(r['dot'])==(F(1,7) if r['i']%3==r['j']%3 or r['i']//3==r['j']//3 else F(-5,7)) for r in a['prism']),'all prism off-diagonal products')

def main():
    p=pathlib.Path(__file__).resolve().parent;a=json.loads((p/'EVIDENCE.json').read_text());check(a)
    damages=[lambda b:b['ports'].pop(),lambda b:b['ports'][0]['seam_boundaries'].pop(),lambda b:b['ports'][0]['seam_boundaries'][0].update(boundaries=[0,0]),lambda b:b['ports'][0]['seam_boundaries'][0]['endpoints'][0].pop(),lambda b:b['discriminants'][0]['polynomial'].__setitem__(0,'2'),lambda b:b['discriminants'][2]['bernstein'].__setitem__(0,'0'),lambda b:b['new_bound'].update(strict_diagonal=False),lambda b:b['new_bound']['cleared_excess'].__setitem__(2,'4'),lambda b:b['boundary_control']['complete_edges'].pop(),lambda b:b['prism'][0].update(dot='0')]
    for d in damages:
        b=copy.deepcopy(a);d(b)
        try:check(b)
        except (ValueError,KeyError,IndexError):continue
        raise ValueError('damaged evidence accepted')
    b=copy.deepcopy(a);b['ports'].reverse();b['discriminants'].reverse()
    for r in b['ports']:r['seam_boundaries'].reverse();r['vertex_classes'].reverse()
    check(b)
    print(json.dumps(dict(semantic_damages_rejected=len(damages),valid_record_representation_accepted=True,ordinary_geometry_unformalized=True)))
if __name__=='__main__':main()
