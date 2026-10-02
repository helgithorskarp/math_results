"""Late independent whole-record comparison. Target code is NOT imported."""
from fractions import Fraction as Q
from math import comb
import json,pathlib,argparse
import independent as I
P=pathlib.Path(__file__).resolve().parent

def token(v):return str(v[0])+':'+str(v[1])
def cycle(c):
    return min(tuple(c[i:]+c[:i]) for i in range(len(c)))
def main():
    args=argparse.ArgumentParser();args.add_argument('--author-dir',type=pathlib.Path,default=P/'author');options=args.parse_args()
    own=json.loads((P/'EVIDENCE.json').read_text());target=json.loads((options.author_dir/'CERTIFICATE.json').read_text())
    ca={tuple(r['word']):r for r in target['closure']}
    cb={tuple(r['word']):r for r in own['closures']}
    I.need(ca.keys()==cb.keys() and len(ca)==len(target['closure'])==12,'whole unique closure coverage')
    positions=bernstein_positions=0
    for w,a in ca.items():
        b=cb[w]
        for x,y in zip(a['final_boundary_vector'],b['final_vector']):
            I.need(I.K.trim(x or [0])==I.K.trim(y),'whole final vector coefficient comparison');positions+=len(x)
        g=I.K.trim(a['contact_polynomial']);I.need(g==I.K.trim(b['g']),'whole g coefficient comparison')
        bern=list(map(Q,a['bernstein']));n=len(g)-1;lo=Q(2,3);hi=Q(3,4)
        I.need(len(bern)==n+1 and (all(v>0 for v in bern) or all(v<0 for v in bern)),'closed Bernstein sign/shape')
        for j in range(n+1):
            u=Q(j,n) if n else Q(0)
            val=sum(bern[k]*comb(n,k)*u**k*(1-u)**(n-k) for k in range(n+1))
            I.need(val==I.K.value(g,lo+(hi-lo)*u),'all degree-bounded Bernstein identity abscissas')
        bernstein_positions+=len(bern)
    ra={(tuple(r['sides']),tuple(r['ports'])):r for r in target['rings']}
    rb={(tuple(r['q']),tuple(r['k'])):r for r in own['ports']}
    I.need(ra.keys()==rb.keys() and len(ra)==len(target['rings'])==27,'whole unique port coverage')
    vertices=arcs=0
    for key,a in ra.items():
        b=rb[key]
        cs=sorted(tuple(token(v) for v in c) for c in b['vertex_classes'])
        I.need(cs==sorted(tuple(c) for c in a['classes']),'all quotient classes')
        rep={tuple(v):min(map(tuple,c)) for c in b['vertex_classes'] for v in c}
        own_arcs=[];own_cycles=[]
        for c in b['cycles']:
            cy=c['darts'];own_cycles.append(cycle([token(rep[tuple(e)]) for e in cy]))
            for i,j in cy:own_arcs.append([token(rep[(i,j)]),token(rep[(i,(j+1)%key[0][i])])])
        I.need(sorted(own_arcs)==a['boundary_arcs'],'every directed boundary arc')
        I.need(sorted(own_cycles)==sorted(cycle(c) for c in a['boundary_cycles']),'every directed cycle up to rotation')
        I.need(a['mixed_corners_per_boundary']==[3,3] and a['vertices']==len(cs),'all mixed and vertex records')
        vertices+=len(cs);arcs+=len(own_arcs)
    out=dict(complete_closure_cases=12,complete_port_cases=27,full_vector_coefficient_positions=positions,full_Bernstein_positions=bernstein_positions,all_quotient_classes=vertices,all_directed_arcs=arcs,all_directed_cycles=54,whole_target_certificate_compared=True,author_executable_imported=False)
    (P/'comparison.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
