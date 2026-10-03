"""Fresh original-role and CRT branch census; no native target data.

Reads only this reviewer's fresh inventory record. DP reachable vectors and
literal row-axis assignment trees give full entry-level two-method products.
"""
import functools,itertools,json,math,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from capacities import D,bits,need,submasks

def main(mode,source,threshold=87):
    data=json.loads(Path(source).read_bytes());U=data['all_group_upper_bounds'];C={int(k):v for k,v in data['single_maxima'].items()}
    @functools.cache
    def slice_cap(cofactors,branch):
        n=(2 if branch==0 else 3,5,6);volume=math.prod(n)
        if 3 in cofactors:return volume
        axes=[tuple(j for j,p in enumerate((9,5,7))if d%p==0)for d in cofactors]
        need(all(axes),'each non-whole row fixes an axis')
        if mode=='vectors':
            counts={(0,0,0)}
            for choices in axes:
                nxt=set()
                for v in counts:
                    for j in choices:
                        w=list(v);w[j]+=1;nxt.add(tuple(w))
                counts=nxt
            return min(volume-math.prod(max(n[j]-v[j],0)for j in range(3))for v in counts)
        best=volume
        for assignment in itertools.product(*axes):
            v=[assignment.count(j)for j in range(3)]
            best=min(best,volume-math.prod(max(n[j]-v[j],0)for j in range(3)))
        return best
    roles=[];inventories=[];expanded=0;worst_expanded=0;worst_pruned=0;essential_rejected=0
    for inv in (r for r in data['inventories']if r['bound']>=threshold):
        H,Q=inv['H_mask'],inv['Q_mask'];start=len(roles);maximum=0
        for HA in submasks(H):
            HB=H^HA
            for qb in submasks(Q):
                for qa in submasks(Q^qb):
                    qother=Q^qb^qa
                    row={'H':inv['H'],'Q':inv['Q'],'HA':[D[i]for i in bits(HA)],'HB':[D[i]for i in bits(HB)],'Qa':[D[i]for i in bits(qa)],'Qb':[D[i]for i in bits(qother)],'QB':[D[i]for i in bits(qb)]}
                    if not qb:
                        essential_rejected+=1;row.update(status='EXCLUDED_BY_ESSENTIAL32',bound=0);roles.append(row);continue
                    overlap=min(U[qa],U[qother],sum(C[math.lcm(D[i],D[j])]for i in bits(qa)for j in bits(qother)))
                    coarse=min(U[HA]+overlap,U[HB]+U[qb],150);row['coarse_bound']=coarse
                    if coarse<threshold:
                        row.update(status='COARSE_PRUNED',bound=coarse);worst_pruned=max(worst_pruned,coarse)
                    else:
                        # Original H/Q identities are distinct, including equal
                        # cross-type cofactors. One branch per actual original.
                        labels=[('H',d)for d in inv['H']]+[('Q',d)for d in inv['Q']]
                        split=[label for label in labels if label[1]%3==0];cases=[]
                        for choices in itertools.product((0,2),repeat=len(split)):
                            branchmap=dict(zip(split,choices));bounds=[];projected=[]
                            for branch in (0,2):
                                def active(kind,ds):return tuple(d for d in ds if d%3 or branchmap[kind,d]==branch)
                                aa=active('H',row['HA']);bb=active('H',row['HB']);left=active('Q',row['Qa']);right=active('Q',row['Qb']);bottom=active('Q',row['QB'])
                                # Do not collapse repeated LCM rows.
                                upper=tuple(sorted(aa+tuple(math.lcm(a,b)for a in left for b in right)));lower=tuple(sorted(bb+bottom))
                                a,b=slice_cap(upper,branch),slice_cap(lower,branch);bounds.append(min(a,b));projected.append({'branch':branch,'upper_multiset':upper,'lower_multiset':lower,'upper_cap':a,'lower_cap':b})
                            bound=min(coarse,sum(bounds));cases.append({'original_branch_choices':[[kind,d,b]for (kind,d),b in zip(split,choices)],'projected':projected,'bound':bound});expanded+=1;worst_expanded=max(worst_expanded,bound)
                        row.update(status='BRANCH_CHECKED',cases=cases,bound=max(c['bound']for c in cases))
                    maximum=max(maximum,row['bound']);roles.append(row)
        inventories.append({'H':inv['H'],'Q':inv['Q'],'original_coarse_bound':inv['bound'],'roles_interval':[start,len(roles)],'new_bound':maximum})
    return {'source_interval':data['h_interval'],('all_46_inventories'if threshold==87 else'all_selected_inventories'):inventories,'all_physical_roles':roles,'summary':{'inventories':len(inventories),'physical_roles':len(roles),'essential32_rejected_roles':essential_rejected,'expanded_coupled_cases':expanded,'maximum_expanded':worst_expanded,'maximum_coarse_pruned':worst_pruned,'maximum_refined_inventory':max(x['new_bound']for x in inventories),'same_original_branch_labels':True,'repeated_LCM_rows_retained':True}}

if __name__=='__main__':
    need(len(sys.argv)in(4,5),'mode source output [support threshold]');need(sys.argv[1]in('vectors','assignments'),'mode')
    result=main(sys.argv[1],sys.argv[2],87 if len(sys.argv)==4 else int(sys.argv[4]));raw=json.dumps(result,sort_keys=True,separators=(',',':')).encode()+b'\n';Path(sys.argv[3]).write_bytes(raw);print(json.dumps({'bytes':len(raw),'summary':result['summary']}))
