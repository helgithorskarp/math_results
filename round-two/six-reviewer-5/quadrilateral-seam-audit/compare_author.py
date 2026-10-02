"""Post-seal full field comparison; no target executable import."""
from fractions import Fraction as F
import json,pathlib,argparse
import kernel as K
import audit as I

def cyc(c):return min(tuple(c[i:]+c[:i]) for i in range(len(c)))
def token(v):return str(v[0])+':'+str(v[1])
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--author-dir',type=pathlib.Path,required=True);args=ap.parse_args()
    p=pathlib.Path(__file__).resolve().parent
    own=json.loads((p/'EVIDENCE.json').read_text());tar=json.loads((args.author_dir/'CERTIFICATE.json').read_text())
    K.need(tar['algebraic_closed_band']==['9/20','1'] and tar['physical_upper_endpoint_excluded'] is True,'physical band binding')
    K.need(tar['application_closed_band']==['1/2','3/5'],'original application binding')
    stars={r['t']:r for r in tar['star_cases']};K.need(set(stars)=={1,2,3} and len(tar['star_cases'])==3,'full star domain')
    fields=coefficients=0
    for r in own['discriminants']:
        t=r['t'];a=stars[t]
        K.need(K.trim(a['Delta']['numerator'])==K.trim(r['polynomial']),'whole numerator coefficients')
        K.need(a['Delta_numerator_Bernstein']==r['bernstein'],'whole Bernstein coefficient list')
        coefficients+=len(r['polynomial'])+len(r['bernstein'])
        for field in ('B_over_A','P','S_over_A','solver_divisor_over_A','Delta'):
            fn=a[field];n=K.trim(fn['numerator']);d=K.trim(fn['denominator'])
            K.need(len(n)<=5 and len(d)<=4,'explicit cross-multiplied identity degree at most seven')
            # Nine distinct regular abscissas prove these rational identities.
            for c in range(9):
                c=F(c);bt={1:F(1),2:c/(1+2*c),3:(c-1)/(1+3*c)}[t]
                r0=I.discriminant(c,t)
                expected={'B_over_A':bt,'P':r0['p'],'S_over_A':r0['u'],'solver_divisor_over_A':1+c*bt,'Delta':r0['d']}[field]
                K.need(K.value(d,c)!=0 and K.value(n,c)==expected*K.value(d,c),'all cross-product identity abscissas')
            fields+=1
        for prefix,field in (('Delta_denominator','Delta'),('solver_divisor_numerator','solver_divisor_over_A'),('solver_divisor_denominator','solver_divisor_over_A')):
            part='numerator' if prefix.endswith('numerator') else 'denominator'
            b=I.bernstein(K.trim(a[field][part]),F(9,20),F(1))
            K.need(list(map(str,b))==a[prefix+'_Bernstein'] and all(v>0 for v in b),'complete positive divisor certificate')
            coefficients+=len(b)
    ra={(tuple(r['sides']),tuple(r['ports'])):r for r in tar['rings']}
    rb={(tuple(r['q']),tuple(r['k'])):r for r in own['ports']}
    K.need(ra.keys()==rb.keys() and len(ra)==len(tar['rings'])==27,'complete unique port coverage')
    count=arcs=seams=0
    for key,a in ra.items():
        b=rb[key];cs=sorted(tuple(token(v) for v in c) for c in b['vertex_classes'])
        K.need(cs==sorted(tuple(c) for c in a['classes']),'every quotient class')
        rep={tuple(v):min(map(tuple,c)) for c in b['vertex_classes'] for v in c}
        oa=[];oc=[]
        for c in b['cycles']:
            cy=c['darts'];oc.append(cyc([token(rep[tuple(e)]) for e in cy]))
            for i,j in cy:oa.append([token(rep[(i,j)]),token(rep[(i,(j+1)%key[0][i])])])
        K.need(sorted(oa)==sorted(a['boundary_arcs']),'every directed boundary arc')
        K.need(sorted(oc)==sorted(cyc(c) for c in a['boundary_cycles']),'both whole boundary cycles')
        om={r['faces'][0]:[token(min(map(tuple,c))) for c in r['endpoints']] for r in b['seam_boundaries']}
        am={r['face']:r['endpoints'] for r in a['seams']}
        K.need(om==am and a['mixed_corners_per_boundary']==[3,3],'every seam and mixed corner')
        count+=len(cs);arcs+=len(oa);seams+=len(om)
    gram=[['1' if i==j else None for j in range(6)] for i in range(6)]
    for r in own['prism']:gram[r['i']][r['j']]=gram[r['j']][r['i']]=r['dot']
    K.need(gram==tar['prism_calibration']['Gram'],'all 36 classical prism Gram entries')
    contacts=[[('U' if i<3 else 'V')+str(i%3),('U' if j<3 else 'V')+str(j%3)] for i in range(6) for j in range(i+1,6) if gram[i][j]=='1/7']
    K.need(contacts==tar['prism_calibration']['contact_pairs'],'all nine named prism contacts')
    fac=tar['adjacent_angle_factorization']
    K.need(K.mul(K.mul(tuple(map(F,fac['right_factors'][0])),tuple(map(F,fac['right_factors'][1]))),tuple(map(F,fac['right_factors'][2])))==K.trim(fac['left']),'full alternate-proof factor identity')
    out=dict(rational_fields=fields,whole_coefficient_positions=coefficients,ports=27,quotient_classes=count,directed_arcs=arcs,directed_cycles=54,seams=seams,mixed_corner_counts=54,prism_Gram_entries=36,alternate_factorization=True,target_executable_imported=False)
    (p/'comparison.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
