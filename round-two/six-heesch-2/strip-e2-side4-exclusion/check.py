"""Search-free endpoint replay with separate axial blocked-cell geometry.

This module imports neither point_blocks nor prove. Shared prior whole-copy
height and affine kernels remain disclosed. Direct axial material checks
supplement, and do not replace, the complete unbounded parameter partitions.
"""
from copy import deepcopy
from datetime import datetime,timezone
import hashlib,json,resource,signal,time
from pathlib import Path
import deps
import strip_parametric_geometry as G
import strip_contact_reader as R
from strip_point_suppliers import supplier_systems
from cases import I,A,B,C,Z,A2,B2,C2,Z2,CASES

H=Path(__file__).absolute().parent

def ax_matrix(m):
    a,b,c,d=m
    return a-2*c,2*a+b-4*c-2*d,c,2*c+d

def ax_inverse(m):
    a,b,c,d=m;q=a*d-b*c
    if q not in (-1,1):raise ValueError('Non-unimodular axial matrix')
    return q*d,-q*b,-q*c,q*a

def axial_block_rows(matrix,point,column,blocked):
    # Use the axial literal coordinates(c-2z,z). Independently invert the
    # physical lattice matrix; the prototype column is source_x+2source_y.
    x,y=G.sub(blocked[0],point[0]),G.sub(blocked[1],point[1])
    ax,ay=G.sub(x,G.scale(2,y)),y
    a,b,c,d=ax_inverse(ax_matrix(matrix))
    dx=G.add(G.scale(a,ax),G.scale(b,ay))
    dy=G.add(G.scale(c,ax),G.scale(d,ay))
    source_u=G.add(G.add(dx,G.scale(2,dy)),(0,column))
    rows=[]
    for u,lo,hi in G.COLS:
        active=G.atom('eq',G.sub(source_u,(0,u)))
        if active is not False:
            rows.append((G.sub(lo,dy),G.sub(G.add(hi,(0,1)),dy),active))
    return tuple(rows)

def cap_systems(case):
    systems=supplier_systems(case['point'],case['fixed'])
    for s in systems:
        s['forbidden']=tuple(s['forbidden'])+tuple(
            row for p in case['blocked']
            for row in axial_block_rows(s['matrix'],case['point'],s['column'],p))
    return systems

def atlas_replay(case,systems,guard):
    part=R.endpoint_partition(systems);classes=[]
    for interval in part['intervals']:
        if len(interval['representatives'])!=1:raise ValueError('Unexpected period')
        k=interval['representatives'][0];atlas=set()
        for s in systems:
            guard()
            for lo,hi in R.free_height_cells(s,k):
                width=G.sub(hi,lo)
                if width[0] or not 0<width[1]<=32:
                    raise ValueError('Unbounded/nonconstant cap family')
                a,b,c,d=s['matrix'];u=s['column']
                for j in range(width[1]):
                    z=G.add(lo,(0,j))
                    atlas.add((s['matrix'],G.sub(G.sub(case['point'][0],(0,a*u)),G.scale(b,z)),
                               G.sub(G.sub(case['point'][1],(0,c*u)),G.scale(d,z))))
        classes.append({**interval,'atlas':sorted(atlas)})
    return part,classes

def collision_b_rows(h,lower):
    # Directly intersect the candidate's transformed source columns with
    # moving-column u=4+d. Solve the source height first, then the b interval.
    (a,b,c,d),x,y=h;rows=[]
    for u,lo,hi in G.COLS:
        for v,L,U in G.COLS:
            if b:
                n=G.sub((0,4+v-a*u),x)
                if n[0]%b:raise ValueError('Nonconstant height congruence')
                if n[1]%b:continue
                z=(n[0]//b,n[1]//b)
                active=G.both(G.atom('ge',G.sub(z,lo)),G.atom('ge',G.sub(hi,z)))
                height=G.add(G.add(y,(0,c*u)),G.scale(d,z))
                first,last=G.sub(height,U),G.add(G.sub(height,L),(0,1))
            else:
                active=G.atom('eq',G.sub(G.add(x,(0,a*u)),(0,4+v)))
                low,high=(lo,hi) if d==1 else (G.scale(-1,hi),G.scale(-1,lo))
                first=G.sub(G.add(G.add(y,(0,c*u)),low),U)
                last=G.add(G.sub(G.add(G.add(y,(0,c*u)),high),L),(0,1))
            rows.append((first,last,active))
    return {'supplier':h,'lo':(0,lower),'hi':(1,3),'forbidden':tuple(rows)}

def check_b_record(record,atlas,lower,guard):
    systems=[collision_b_rows(h,lower) for h in atlas]
    if R.freeze(record['systems'])!=R.freeze(systems):
        raise ValueError('Different moving-copy collision intervals')
    part=R.endpoint_partition(systems)
    if R.freeze(record['partition'])!=R.freeze(part) or len(record['classes'])!=len(part['intervals']):
        raise ValueError('Incomplete b interval parameter partition')
    for saved,interval in zip(record['classes'],part['intervals']):
        guard()
        if any(saved[k]!=interval[k] for k in ('lo','hi','representatives')):
            raise ValueError('Changed b interval class')
        replay=[{'pose':s['supplier'],'allowed_b':R.free_height_cells(s,interval['representatives'][0])}
                for s in systems]
        if R.freeze(saved['suppliers'])!=R.freeze(replay):raise ValueError('Wrong allowed b domains')
    return part

def check_wedges(node):
    if isinstance(node,dict):
        if 'row' in node and 'lower' in node:
            a,b,c=node['row'];lo=node['lower']
            if b>=0:slope=a;minimum=6*a+b*lo+c;edge='b='+str(lo)
            else:slope=a+b;minimum=6*slope+2*b+c;edge='b=k+2'
            if slope<0 or minimum<0 or node.get('tail_slope')!=slope or node.get('at_six')!=minimum or node.get('edge')!=edge:
                raise ValueError('Invalid exact wedge certificate')
        for v in node.values():check_wedges(v)
    elif isinstance(node,(tuple,list)):
        for v in node:check_wedges(v)

def wedge_certificate(row,lower):
    a,b,c=row
    slope=a if b>=0 else a+b
    minimum=6*a+b*lower+c if b>=0 else 6*(a+b)+2*b+c
    if slope<0 or minimum<0:raise ValueError('False independently reconstructed wedge')
    return {'row':row,'lower':lower,'edge':'b='+str(lower) if b>=0 else 'b=k+2',
            'tail_slope':slope,'at_six':minimum}

def source_height_certificate(column,height,lower):
    L,U=next((lo,hi) for u,lo,hi in G.COLS if u==column)
    a,b,c=height
    return [wedge_certificate((a-L[0],b,c-L[1]),lower),
            wedge_certificate((U[0]-a,-b,U[1]-c),lower)]

def check_reduction(record):
    common=[]
    for case in CASES:
        checks=[]
        for u,v in case['blocked']:
            if u[0] or v[0]!=1:raise ValueError('Wrong common-block affine form')
            checks.append({'point':(u,v),
                'membership':source_height_certificate(u[1]-4,(1,-1,v[1]),case['b_min'])})
        common.append({'name':case['name'],'checks':checks})
    if R.freeze(record['common_blocks'])!=R.freeze(common):
        raise ValueError('Common block containment is not fully certified')
    empty=[wedge_certificate((0,1,-2),3),wedge_certificate((0,1,-4),5)]
    if R.freeze(record['moving_demand_empty_inequalities'])!=R.freeze(empty):
        raise ValueError('Missing moving-copy demand emptiness certificate')
    if R.freeze(record['P2_original_halo_neighbor'])!=R.freeze(source_height_certificate(0,(1,-1,4),5)):
        raise ValueError('P2 is not proved to lie in the original pair halo')
    fixed=[G.point_membership(A,CASES[0]['point']),
           G.neg(G.point_membership(I,CASES[0]['point'])),
           G.point_membership(I,((0,2),(1,1))),
           G.neg(G.point_membership(I,CASES[1]['point'])),
           G.neg(G.point_membership(A,CASES[1]['point'])),
           G.point_membership(C,((0,3),(1,3))),G.point_membership(C,((0,4),(1,4))),
           G.point_membership(C2,((0,3),(1,5))),G.point_membership(C2,((0,4),(1,6))),
           G.point_membership(A,((0,2),(1,2))),G.point_membership(A,((0,2),(1,3))),
           G.neg(G.intersection(A))]
    part=R.splitter(fixed)
    if R.freeze(record['fixed_geometry_partition'])!=R.freeze(part) or not all(
            all(G.evaluate(p,k) for p in fixed) for k in part['representatives']):
        raise ValueError('Incomplete/false fixed geometric reduction')
    if (1,1) not in G.UV_DIRS or (1,0) not in G.UV_DIRS:
        raise ValueError('Wrong original-halo adjacency')
    check_wedges(record)

def check_math(math,guard):
    if math['conclusion']!='For every integer k>=6 and b, registered(I;4,b) is outsideE2; the b=3 contact is already outsideE1':
        raise ValueError('Changed theorem statement')
    raw=next(s for s in R.raw_regions() if s['matrix']==I[0] and s.get('a')==4)
    if R.freeze(math['raw_system'])!=R.freeze(raw):raise ValueError('Changed raw domain geometry')
    endpoints={v for x in raw['root']+raw['closed'] for v in x}
    part=R.splitter([G.atom('ge',G.sub(x,y)) for x in endpoints for y in endpoints if x!=y])
    if R.freeze(math['raw_partition'])!=R.freeze(part):raise ValueError('Changed raw-domain partition')
    for k in part['representatives']:
        if R.freeze(R.scan_boxes(raw,k))!=R.freeze(math['raw_selected']):raise ValueError('Wrong complete raw interval')
    if R.freeze(math['raw_selected'])!=(((0,3),(1,2)),((1,2),(1,3))):raise ValueError('Wrong raw U4 domain')
    records=math['cap_records']
    if len(records)!=len(CASES):raise ValueError('Missing cap')
    cap_parts=[]
    for case,record in zip(CASES,records):
        for key in ('name','point','fixed','blocked'):
            if R.freeze(record[key])!=R.freeze(case[key]):raise ValueError('Wrong literal cap')
        systems=cap_systems(case)
        if R.freeze(record['systems'])!=R.freeze(systems):raise ValueError('Incomplete/changed source-height systems')
        part,classes=atlas_replay(case,systems,guard)
        if R.freeze(record['partition'])!=R.freeze(part) or R.freeze(record['classes'])!=R.freeze(classes):
            raise ValueError('Changed cap partition/inventory')
        if R.freeze(record['atlas'])!=case['expected'] or any(R.freeze(c['atlas'])!=case['expected'] for c in classes):
            raise ValueError('Missing/extra cap supplier')
        cap_parts.append(part)
    root_part=check_b_record(math['complete_root_point_supplier_b_domains'],CASES[0]['expected'],3,guard)
    after_part=check_b_record(math['after_A_B2_C2_moving_collision_domains'],(B2,C2),5,guard)
    for cls in math['complete_root_point_supplier_b_domains']['classes']:
        for row in cls['suppliers']:
            merged=[]
            for lo,hi in R.freeze(row['allowed_b']):
                if merged and merged[-1][1]==lo:merged[-1]=(merged[-1][0],hi)
                else:merged.append((lo,hi))
            wanted={A:[((0,5),(1,3))],Z:[((0,4),(1,3))],B:[],C:[]}[R.freeze(row['pose'])]
            if merged!=wanted:raise ValueError('The required complete root b-domain result failed')
    if any(row['allowed_b'] for cls in math['after_A_B2_C2_moving_collision_domains']['classes'] for row in cls['suppliers']):
        raise ValueError('An after-A packing alternative is not excluded')
    cut=math['earlier_E1_cuts']
    expected={}
    for directory,name in [('strip-e2-forced-p','E02'),('strip-e2-shift-exclusion','B05')]:
        rows=json.loads((H.parent/directory/'inputs.json').read_text())['cases']
        found=[r for r in rows if r['name']==name]
        if len(found)!=1:raise ValueError('Missing cited E1 cut')
        expected[name]=R.freeze(found[0]['pose'])
    if expected['E02']!=Z or expected['B05']!=G.inverse(G.relative(A,Z2)):
        raise ValueError('Earlier input has different E1 contact')
    if R.freeze(cut['literal_E1_inputs'])!=expected or R.freeze(cut['A_to_Z2'])!=G.relative(A,Z2) or R.freeze(cut['A_to_A2'])!=G.relative(A,A2):
        raise ValueError('Changed E1 premise')
    predicates=[G.touching(Z),G.touching(G.relative(A,Z2)),G.touching(G.relative(A,A2)),
        G.neg(G.atom('eq',G.sub((0,2),(-1,3)))),G.neg(G.atom('eq',G.sub((0,2),(-1,4))))]
    if G.relative(A,A2)!=((1,0,0,1),(0,6),(0,2)):
        raise ValueError('Wrong necessary E1 side rule')
    cutpart=R.splitter(predicates)
    if R.freeze(cut['partition'])!=R.freeze(cutpart) or not all(
            all(G.evaluate(p,k) for p in predicates) for k in cutpart['representatives']):
        raise ValueError('Cited E1 cuts do not cover actual touching pairs')
    check_reduction(math['all_parameter_reduction'])
    return {'raw_partition':math['raw_partition'],
            'cap_partitions':cap_parts,'root_b_partition':root_part,'after_b_partition':after_part}

def literal_ax(k):
    out={(0,0),(-2*k,k-1),(-2*k-1,k)}
    for r in range(k):out.update(((-2*r-1,r+1),(-2*r-1,r+2),(-2*r-2,r+1),(-2*r-2,r+2)))
    if len(out)!=4*k+3:raise ValueError('Wrong literal area')
    return out

def point_ax(p,k):
    u,v=G.value(p[0],k),G.value(p[1],k)
    return u-2*v,v

def material(case,k,guard):
    T=literal_ax(k);oriented={m:{(L[0]*x+L[1]*y,L[2]*x+L[3]*y) for x,y in T}
                           for m in G.MATRICES for L in [ax_matrix(m)]}
    def footprint(h):
        m,a,b=h;u,v=G.value(a,k),G.value(b,k);x,y=u-2*v,v
        return {(i+x,j+y) for i,j in oriented[m]}
    occupied=set().union(*(footprint(h) for h in case['fixed']))
    occupied.update(point_ax(p,k) for p in case['blocked'])
    P=point_ax(case['point'],k);atlas=set()
    for m,S in oriented.items():
        guard()
        for x,y in S:
            dx,dy=P[0]-x,P[1]-y
            if not any((u+dx,v+dy) in occupied for u,v in S):
                atlas.add((m,dx+2*dy,dy))
    expected={(m,G.value(a,k),G.value(b,k)) for m,a,b in case['expected']}
    if atlas!=expected:raise ValueError('Direct axial cap atlas differs')
    tests=[]
    for b in range(case['b_min'],k+3):
        guard();g=(I[0],(0,4),(0,b));gset=footprint(g)
        if not all(point_ax(p,k) in gset for p in case['blocked']):raise ValueError('False common occupied block')
        if P in gset or P in set().union(*(footprint(h) for h in case['fixed'])):
            raise ValueError('Demand is already occupied')
        actual=[h for h in case['expected'] if not footprint(h)&gset]
        if case['name']=='root':
            wanted=[] if b==3 else [Z] if b==4 else [A,Z]
            if set(actual)!=set(wanted):raise ValueError('Axial raw point b domain differs')
        else:
            if B2 in actual or C2 in actual:raise ValueError('Axial after-A packing supplier survives')
        tests.append({'b':b,'disjoint_cap_suppliers':len(actual)})
    return {'k':k,'name':case['name'],'cap_suppliers':len(atlas),'moving_b_audit':tests}

def main():
    start=time.monotonic();calls=[0]
    def guard():
        calls[0]+=1
        if deps.paused() or time.monotonic()-start>=43 or calls[0]>100000:
            raise RuntimeError('Operational/time/work guard; incomplete is inconclusive')
    def alarm(a,b):raise RuntimeError('45s signal guard; incomplete is inconclusive')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(45)
    mode='normal' if __debug__ else 'optimized'
    produced=json.loads((H/'generated'/f'produced-{mode}.json').read_text())
    if not produced['complete']:raise ValueError('Incomplete producer')
    math=produced['evidence'];parts=check_math(math,guard)
    audits=[material(case,k,guard) for k in (6,7,8,9,12,40) for case in CASES]
    controls=[]
    for name in ('missing_cap_supplier','changed_blocked_cell','missing_source_case',
                 'missing_b_parameter_class','wrong_b_interval','changed_E1_contact','false_wedge'):
        damaged=deepcopy(math)
        if name=='missing_cap_supplier':damaged['cap_records'][0]['atlas'].pop()
        elif name=='changed_blocked_cell':damaged['cap_records'][1]['blocked'][0][1][1]+=1
        elif name=='missing_source_case':damaged['cap_records'][0]['systems'].pop()
        elif name=='missing_b_parameter_class':damaged['complete_root_point_supplier_b_domains']['classes'].pop()
        elif name=='wrong_b_interval':damaged['complete_root_point_supplier_b_domains']['classes'][0]['suppliers'][1]['allowed_b'][0][0][1]+=1
        elif name=='changed_E1_contact':damaged['earlier_E1_cuts']['A_to_Z2'][1][1]+=1
        else:damaged['all_parameter_reduction']['common_blocks'][0]['checks'][0]['membership'][0]['row']=[0,1,-4]
        try:check_math(damaged,guard)
        except (ValueError,KeyError,IndexError,TypeError):controls.append(name)
        else:raise ValueError('Damaged proof data accepted')
    evidence={'parts':parts,'axial_audits':audits,'damaged_controls':controls,
              'producer_mathematics_sha256':produced['mathematics_sha256'],
              'scope':'All-k exact cap/interval replay with material AX controls; registered local filters only'}
    result={'agent':'six-heesch-2','role':'researcher','complete':True,'evidence':evidence,
            'mathematics_sha256':R.sha(evidence),'seconds':round(time.monotonic()-start,3),
            'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'checked_utc':datetime.now(timezone.utc).isoformat()}
    (H/'generated'/f'checked-{mode}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('agent','role','complete','mathematics_sha256','seconds','max_rss_kib')}
                     |{'axial_audit_parameters':[6,7,8,9,12,40],'reader_damage_controls':len(controls)},sort_keys=True))
    signal.alarm(0)

if __name__=='__main__':main()
