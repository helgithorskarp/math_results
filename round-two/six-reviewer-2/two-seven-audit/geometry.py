"""Original arithmetic progression / four-lift audit, all original phases.

No target code, expected results or proof corpora are inputs. Both physical
coordinates and all cofactor branches are reconstructed from definitions.
"""
import itertools,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from capacities import P,D,residual,need

def main(mode):
    R=residual('sets'if mode=='progressions'else'literal')
    parents={p:tuple(x for x in R if x%8==p)for p in(2,6)};rows=[];memberships=0
    for p in(2,6):
        pts=parents[p];index={x:i for i,x in enumerate(pts)}
        for d in(1,)+D:
            for factor in(16,32):
                m=factor*d
                for a in range(p,m,8):
                    masks=[0]*len(pts)
                    if mode=='progressions':
                        for n in range(a,10080,m):
                            x=n%2520
                            if x in index:masks[index[x]]|=1<<((n%32-p)//8)
                    else:
                        for i,x in enumerate(pts):
                            for k in range(4):
                                n=x+2520*k
                                if n%m==a:masks[i]|=1<<((n%32-p)//8)
                                memberships+=1
                    expected=[]
                    for x in pts:
                        odd=x%d==a%d
                        pattern=sum(1<<q for q in range(4)if(p+8*q)%factor==a%factor)
                        expected.append(pattern if odd else 0)
                    need(masks==expected,'actual physical original phase disagrees with CRT row')
                    rows.append({'parent':p,'original_modulus':m,'phase':a,'all_four_quarter_masks':masks})
    product=[]
    for branch,axis9 in((0,(3,6)),(2,(2,5,8))):
        coords=list(itertools.product(axis9,range(5),range(1,7)))
        physical=[]
        for a,b,c in coords:
            matches=[x for x in range(6,2520,8)if(x%9,x%5,x%7)==(a,b,c)]
            need(len(matches)==1,'CRT unique literal residue');physical.append(matches[0])
        actual=[x for x in parents[6]if x%3==branch]
        need(sorted(physical)==actual,'entire CRT branch equality')
        product.append({'branch':branch,'axis9':axis9,'axis5':list(range(5)),'axis7':list(range(1,7)),'coordinate_tuples':coords,'literal_points':sorted(physical)})
    need(sorted(x for r in product for x in r['literal_points'])==list(parents[6]),'whole parent branch coverage')
    # Complete truth-table audit of the missing quarter conjunction.
    truth=[]
    for HA,HB,Qa,Qb,QB in itertools.product((False,True),repeat=5):
        full=all((True,HA or Qa,HB or QB,HA or Qb))
        formula=(HA or(Qa and Qb))and(HB or QB)
        need(full==formula,'missing original quarter formula')
        if not QB and full:need(HB,'32 redundant if no quarter22 Q at a repaired hole')
        truth.append({'HA':HA,'HB':HB,'Qa':Qa,'Qb':Qb,'QB':QB,'all_quarters_filled':full})
    return {'prefix':P,'R':R,'parents':parents,'all_original_phase_rows':rows,'CRT_products':product,'quarter_truth_table':truth,'physical_membership_count':len(rows)*150*4,'row_count':len(rows),'same_original_phase_not_quotiented':True,'placed_original16_32_included':True}

if __name__=='__main__':
    need(len(sys.argv)==3,'mode output');need(sys.argv[1]in('progressions','lifts'),'mode')
    x=main(sys.argv[1]);raw=json.dumps(x,sort_keys=True,separators=(',',':')).encode()+b'\n';Path(sys.argv[2]).write_bytes(raw);print(json.dumps({'bytes':len(raw),'phase_rows':x['row_count'],'physical_memberships':x['physical_membership_count'],'branch_sizes':[len(r['literal_points'])for r in x['CRT_products']]}))
