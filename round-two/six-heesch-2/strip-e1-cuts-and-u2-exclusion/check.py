"""Search-free reader with separate interval sweeps and literal axial audits.

No import of the producer. Shared older symbolic/height kernels and literal
premise bindings are explicit trust boundaries, not independent peer review.
"""
from copy import deepcopy
from datetime import datetime,timezone
import json,resource,signal,time
from pathlib import Path
import model as M
import strip_parametric_geometry as G
import strip_contact_reader as R

HERE=Path(__file__).resolve().parent
AX_DIRS=((1,0),(0,1),(-1,1),(-1,0),(0,-1),(1,-1))

def axial(p,k):
    (a,b,c,d),u,v=p;x,y=G.value(u,k),G.value(v,k)
    return (a-2*c,2*a+b-4*c-2*d,c,2*c+d),x-2*y,y

def inverse_axial(p):
    (a,b,c,d),x,y=p;det=a*d-b*c
    M.require(det in (-1,1),'Nonunit axial determinant')
    n=(det*d,-det*b,-det*c,det*a)
    return n,-n[0]*x-n[1]*y,-n[2]*x-n[3]*y

def relative_axial(p,q):
    m,x,y=inverse_axial(p);n,u,v=q
    return (m[0]*n[0]+m[1]*n[2],m[0]*n[1]+m[1]*n[3],
            m[2]*n[0]+m[3]*n[2],m[2]*n[1]+m[3]*n[3]), \
        m[0]*u+m[1]*v+x,m[2]*u+m[3]*v+y

def material(data,node,sup,k,guard):
    guard();tile={(0,0),(-2*k,k-1),(-2*k-1,k)}
    for r in range(k):
        tile.update({(-2*r-1,r+1),(-2*r-1,r+2),(-2*r-2,r+1),(-2*r-2,r+2)})
    oriented={m:{(m[0]*x+m[1]*y,m[2]*x+m[3]*y) for x,y in tile} for m in R.E.matrices()}
    def footprint(p):
        m,x,y=axial(p,k)
        M.require(m in oriented,'Nonrigid axial matrix')
        return {(u+x,v+y) for u,v in oriented[m]}
    fixed=M.freeze(node['fixed']);feet=[footprint(f) for f in fixed]
    occupied=set().union(*feet)
    M.require(len(occupied)==len(tile)*len(fixed),'Material fixed packing overlaps')
    root_neighbors={(x+dx,y+dy) for x,y in feet[0] for dx,dy in AX_DIRS}
    M.require(not feet[1].isdisjoint(root_neighbors),'Material root pair is not touching')
    u,v=map(lambda z:G.value(z,k),node['point']);p=(u-2*v,v)
    near={(x+dx,y+dy) for s in feet[:2] for x,y in s for dx,dy in AX_DIRS}
    M.require(p not in occupied and p in near,'Material demand is not an original empty halo cell')
    raw=set()
    for m,s in oriented.items():
        guard()
        for x,y in s:
            a,b=p[0]-x,p[1]-y
            if occupied.isdisjoint((z+a,w+b) for z,w in s):raw.add((m,a,b))
    proposed={axial(q,k) for q in M.freeze(sup['atlas'])}
    M.require(raw==proposed,'Literal source alignment differs from complete atlas')
    for block in node['blocks']:
        q=M.freeze(block['pose']);j=block['fixed_index'];s=footprint(q)
        h={(x+dx,y+dy) for x,y in feet[j] for dx,dy in AX_DIRS}
        M.require(s.isdisjoint(feet[j]) and not s.isdisjoint(h),'E1 blocker is not a disjoint touching pair')
        r=relative_axial(axial(fixed[j],k),axial(q,k));cut=data['cuts'][block['cut']]
        if block['cut']=='strip-contact-domains/identity_U6':
            scalar=False
            for matrix,x,y in (r,inverse_axial(r)):
                scalar|=matrix==(1,0,0,1) and x+2*y==6 and y not in (3-k,4-k)
            M.require(scalar,'Scalar identity-U6 premise does not apply')
        else:
            t=axial(M.freeze(cut['pose']),k)
            M.require(r in (t,inverse_axial(t)),'Scalar relative pose differs from cited E1 exclusion')

def check(data,evidence,guard,with_material=True):
    M.bind(data)
    M.require(evidence['inputs_sha256']==R.sha(data) and evidence['all_k_minimum']==6
              and evidence['E1_exclusions']==list(M.E1_CONTACTS)
              and evidence['E2_exclusions']==list(M.E2_CONTACTS)
              and evidence['Heesch_number_conclusion'] is False,'Changed evidence binding or scope')
    M.require(len(evidence['trees'])==len(M.CONTACTS),'Missing evidence tree')
    output=[]
    for tree,saved_tree in zip(data['trees'],evidence['trees']):
        M.require(saved_tree['contact_name']==tree['contact_name']
                  and saved_tree['level']==tree['level'] and len(saved_tree['nodes'])==len(tree['nodes']),'Changed tree binding')
        nodes=[]
        for node,saved in zip(tree['nodes'],saved_tree['nodes']):
            guard();fixed=M.freeze(node['fixed']);p=M.freeze(node['point'])
            fresh=R.supplier_atlas(p,fixed,guard)
            M.require(fresh['finite'] and M.freeze(fresh)==M.freeze(saved['suppliers']),
                      'Changed complete source-height reduction')
            wanted=set(M.freeze(node['expected']))|{M.freeze(b['pose']) for b in node['blocks']}
            M.require(set(fresh['atlas'])==wanted,'Uncertified or missing source-aligned supplier')
            # Rebuild original demand, packing, survivor and exact E1-transport conditions.
            empty=G.neg(G.either(*(G.point_membership(f,p) for f in fixed)))
            neighbor=G.either(*(G.point_membership(f,(G.sub(p[0],(0,u)),G.sub(p[1],(0,v))))
                              for f in fixed[:2] for u,v in G.UV_DIRS))
            rows=[G.both(empty,neighbor),G.touching(G.relative(fixed[0],fixed[1]))]
            rows.extend(G.neg(G.intersection(G.relative(a,b)))
                        for j,b in enumerate(fixed) for a in fixed[:j])
            for q in M.freeze(node['expected']):
                rows.append(G.both(G.point_membership(q,p),
                    *(G.neg(G.intersection(G.relative(f,q))) for f in fixed)))
            rows.extend(M.blocker(data,node,b) for b in node['blocks'])
            part=R.splitter(rows)
            M.require(part==G.partition(rows) and part==saved['partition']
                      and saved['name']==node['name'],'Changed exact parameter partition')
            for k in part['representatives']:
                guard();M.require(all(G.evaluate(r,k) for r in rows),'False all-k proof condition')
            if with_material:
                for k in sorted(set(part['representatives'])|{6,7,8,9,12,40}):
                    material(data,node,fresh,k,guard)
            nodes.append({'name':node['name'],'raw_suppliers':len(fresh['atlas']),
                          'survivors':len(node['expected']),'blocked':len(node['blocks']),
                          'inventory_cuts':fresh['partition']['cuts'],
                          'geometry_cuts':part['cuts'],'period':part['period']})
        output.append({'contact_name':tree['contact_name'],'level':tree['level'],'nodes':nodes,'all_k_rejected':True})
    return output

def main():
    start=time.monotonic();calls=[0]
    def guard():
        calls[0]+=1
        if M.deps.paused() or time.monotonic()-start>=43 or calls[0]>100000:
            raise RuntimeError('Operational/time/work guard; incomplete is inconclusive')
    def alarm(a,b):raise RuntimeError('45s guard; incomplete is inconclusive')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(45)
    data=json.loads((HERE/'inputs.json').read_text())
    mode='normal' if __debug__ else 'optimized'
    record=json.loads((HERE/'generated'/f'produced-{mode}.json').read_text())
    M.require(record['complete'],'Incomplete production')
    evidence=record['evidence'];trees=check(data,evidence,guard)
    damages=[]
    controls=('missing_branch','false_original_demand','wrong_anchor','wrong_cut',
              'false_premise_binding','missing_blocker','cropped_supplier','cropped_tail',
              'E1_circular_pruning','changed_level','changed_contact','missing_E1_premise_tree')
    e2=3
    blocked=next(i for i,node in enumerate(data['trees'][e2]['nodes']) if node['blocks'])
    for label in controls:
        bad_data=deepcopy(data);bad_evidence=deepcopy(evidence)
        if label=='missing_branch':bad_data['trees'][0]['nodes'][0]['children'].pop()
        elif label=='false_original_demand':bad_data['trees'][0]['nodes'][0]['point']=[[0,100],[0,100]]
        elif label=='wrong_anchor':bad_data['trees'][e2]['nodes'][blocked]['blocks'][0]['fixed_index']=0
        elif label=='wrong_cut':
            a=bad_data['trees'][e2]['nodes'][blocked]['blocks'][0]
            b=bad_data['trees'][e2]['nodes'][2]['blocks'][0]
            a['cut'],b['cut']=b['cut'],a['cut']
        elif label=='false_premise_binding':bad_data['cuts']['local/E1_12']['pose'][1][1]+=1
        elif label=='missing_blocker':
            missing=bad_data['trees'][e2]['nodes'][blocked]['blocks'].pop()
            bad_data['cuts'].pop(missing['cut'])
        elif label=='cropped_supplier':bad_evidence['trees'][0]['nodes'][0]['suppliers']['atlas'].pop()
        elif label=='cropped_tail':bad_evidence['trees'][0]['nodes'][0]['suppliers']['classes'][-1]['hi']=100
        elif label=='E1_circular_pruning':
            first=bad_data['trees'][0]['nodes'][0]
            supplier=first['expected'].pop();first['children'].pop()
            first['blocks'].append({'pose':supplier,'fixed_index':0,'cut':'local/E1_12'})
        elif label=='changed_level':bad_data['trees'][0]['level']=2
        elif label=='changed_contact':bad_data['trees'][e2]['nodes'][0]['fixed'][1][1][1]+=1
        else:bad_data['trees'].pop(0);bad_evidence['trees'].pop(0)
        # Bypass the digest only: each damaged control reaches mathematical validation.
        bad_evidence['inputs_sha256']=R.sha(bad_data)
        try:check(bad_data,bad_evidence,guard,False)
        except ValueError:damages.append(label)
        else:raise ValueError('Damaged mathematical certificate accepted: '+label)
    math={'trees':trees,'damaged_controls':damages,'all_k_minimum':6,
          'E1_exclusions':list(M.E1_CONTACTS),'E2_exclusions':list(M.E2_CONTACTS),
          'material_parameters':[6,7,8,9,12,40],'Heesch_number_conclusion':False}
    result={'agent':'six-heesch-2','role':'researcher','complete':True,'evidence':math,
            'mathematics_sha256':R.sha(math),'seconds':round(time.monotonic()-start,3),
            'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'checked_utc':datetime.now(timezone.utc).isoformat()}
    (HERE/'generated'/f'checked-{mode}.json').write_text(json.dumps(result,indent=2)+'\n')
    signal.alarm(0)
    print(json.dumps({k:v for k,v in result.items() if k!='evidence'},sort_keys=True),flush=True)

if __name__=='__main__':main()
