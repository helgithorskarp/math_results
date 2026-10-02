"""All-k cap proof; every use of a moving-pair cell is an exact wedge inequality."""
from datetime import datetime,timezone
import hashlib,json,resource,signal,time
from pathlib import Path
import deps
import strip_parametric_geometry as G
from strip_contact_reader import freeze,sha
from strip_contact_rectangles import systems,order_atoms,selected_rectangles
from strip_notch_intervals import translated_supplier_forbidden,parameter_partition,allowed_intervals
from cases import I,A,B,C,Z,A2,B2,C2,Z2,CASES
from point_blocks import produce

H=Path(__file__).absolute().parent

def wedge(row,lower):
    """Ak+Bb+C>=0 for every k>=6, lower<=b<=k+2."""
    a,b,c=row
    if b>=0:tail=a;minimum=6*a+b*lower+c;edge='b='+str(lower)
    else:tail=a+b;minimum=6*(a+b)+2*b+c;edge='b=k+2'
    if tail<0 or minimum<0:raise ValueError('False exact wedge inequality')
    return {'row':row,'lower':lower,'edge':edge,'tail_slope':tail,'at_six':minimum}

def moving_membership(column,height,lower):
    """Source height is Ak+Bb+C in the shifted copy's column."""
    lo,hi=next((lo,hi) for c,lo,hi in G.COLS if c==column)
    a,b,c=height
    return [wedge((a-lo[0],b,c-lo[1]),lower),
            wedge((hi[0]-a,-b,hi[1]-c),lower)]

def all_true(predicates):
    p=G.partition(predicates)
    if not all(all(G.evaluate(q,k) for q in predicates) for k in p['representatives']):
        raise ValueError('False all-k fixed-pose assertion')
    return p

def earlier_cuts():
    inputs={}
    for directory,names in [('strip-e2-forced-p',['E02']),('strip-e2-shift-exclusion',['B05'])]:
        rows=json.loads((H.parent/directory/'inputs.json').read_text())['cases']
        for name in names:
            found=[r for r in rows if r['name']==name]
            if len(found)!=1:raise ValueError('Missing cited E1 input')
            inputs[name]=freeze(found[0]['pose'])
    if inputs['E02']!=Z:
        raise ValueError('Changed cited root E1 cuts')
    relative=G.relative(A,Z2)
    if inputs['B05']!=G.inverse(relative):raise ValueError('Changed cited B05 E1 cut')
    if G.relative(A,A2)!=((1,0,0,1),(0,6),(0,2)):
        raise ValueError('Wrong shifted-A side contact')
    predicates=[G.touching(Z),G.touching(relative),G.touching(G.relative(A,A2))]
    # Published9404: E1 identity-U6 permits only b=3-k or4-k.
    predicates.extend([G.neg(G.atom('eq',G.sub((0,2),(-1,3)))),
                       G.neg(G.atom('eq',G.sub((0,2),(-1,4))))])
    return {'literal_E1_inputs':inputs,'A_to_Z2':relative,'A_to_A2':G.relative(A,A2),
            'partition':all_true(predicates)}

def moving_collision_intervals(atlas,lower,guard):
    # Translate the moving copy(I;4,b) to the root. A candidate h becomes
    # h+(-4,-b); the published height kernel gives forbidden intervals in
    # t=-b. Reflect integer half-open[t0,t1) into[1-t1,1-t0).
    rows=[]
    for h in atlas:
        forbidden=tuple((G.sub((0,1),hi),G.sub((0,1),lo),active)
                        for lo,hi,active in translated_supplier_forbidden(h,a_shift=-4))
        rows.append({'supplier':h,'lo':(0,lower),'hi':(1,3),'forbidden':forbidden})
    part=parameter_partition(rows);classes=[]
    for interval in part['intervals']:
        guard();k=interval['representatives'][0]
        classes.append({**interval,'suppliers':[{'pose':s['supplier'],
            'allowed_b':allowed_intervals(s,k)} for s in rows]})
    return {'systems':rows,'partition':part,'classes':classes}

def reduction():
    common=[]
    for case in CASES:
        checks=[]
        for (u0,u1),(v0,v1) in case['blocked']:
            if u0 or v0!=1:raise ValueError('Unexpected common-block coordinate')
            checks.append({'point':((u0,u1),(v0,v1)),
                           'membership':moving_membership(u1-4,(1,-1,v1),case['b_min'])})
        common.append({'name':case['name'],'checks':checks})
    fixed=[G.point_membership(A,CASES[0]['point']),
           G.neg(G.point_membership(I,CASES[0]['point'])),
           G.point_membership(I,((0,2),(1,1))),
           G.neg(G.point_membership(I,CASES[1]['point'])),
           G.neg(G.point_membership(A,CASES[1]['point'])),
           G.point_membership(C,((0,3),(1,3))),
           G.point_membership(C,((0,4),(1,4))),
           G.point_membership(C2,((0,3),(1,5))),
           G.point_membership(C2,((0,4),(1,6))),
           G.point_membership(A,((0,2),(1,2))),
           G.point_membership(A,((0,2),(1,3))),
           G.neg(G.intersection(A))]
    one_parameter=all_true(fixed)
    # P1 and P2 have u=3. The moving copy has only its source-column -1
    # at u=3, height k+b; for b>=3/5 the demand lies strictly below it.
    empty=[wedge((0,1,-2),3),wedge((0,1,-4),5)]
    # P1 is adjacent to root(2,k+1); P2 is adjacent to moving(4,k+4).
    if (1,1) not in G.UV_DIRS or (1,0) not in G.UV_DIRS:
        raise ValueError('Wrong original-halo neighbor directions')
    demand2=moving_membership(0,(1,-1,4),5)
    # C collides at moving-column -1 when b=3, then at column0 for b>=4.
    c_collision=moving_membership(0,(1,-1,4),4)
    # B2 contains the actual moving terminal(3,k+b): its source column0
    # has height b-4 under B2. Check the whole b>=5 wedge exactly.
    b2_contains_terminal=[wedge((0,1,-4),5),wedge((1,-1,4),5)]
    # C2 collides at the moving-column -1 terminal when b=5, then at
    # column0 for b>=6. Each terminal comparison is a literal identity.
    c2_collision=moving_membership(0,(1,-1,6),6)
    return {'common_blocks':common,'fixed_geometry_partition':one_parameter,
            'moving_demand_empty_inequalities':empty,
            'P2_original_halo_neighbor':demand2,
            'C_collision_b3_terminal':'(3,k+3)',
            'C_collision_b_ge4':c_collision,
            'A_collision_b3_or4':'moving terminal(2,k+b-1) is in A',
            'B2_contains_terminal':b2_contains_terminal,
            'C2_collision_b5_terminal':'(3,k+5)',
            'C2_collision_b_ge6':c2_collision}

def main():
    start=time.monotonic();count=[0]
    def guard():
        count[0]+=1
        if deps.paused() or time.monotonic()-start>=43 or count[0]>100000:
            raise RuntimeError('Operational/time/work guard; incomplete is inconclusive')
    def alarm(a,b):raise RuntimeError('45s signal guard; incomplete is inconclusive')
    signal.signal(signal.SIGALRM,alarm);signal.alarm(45)
    s=next(s for s in systems() if s['matrix']==I[0] and s.get('a')==4)
    raw_partition=G.partition(order_atoms([s]))
    expected=(((0,3),(1,2)),((1,2),(1,3)))
    for interval in raw_partition['intervals']:
        if freeze(selected_rectangles(s,interval['representatives'][0]))!=expected:
            raise ValueError('Changed complete raw U4 domain')
    records=[]
    for case in CASES:
        record=produce(case,guard)
        if freeze(record['atlas'])!=case['expected']:
            raise ValueError('Wrong complete common-block supplier atlas')
        for cls in record['classes']:
            if freeze(cls['atlas'])!=case['expected']:
                raise ValueError('Different supplier class; cannot assert uniform inventory')
        records.append(record)
    root_b=moving_collision_intervals(CASES[0]['expected'],3,guard)
    expected_b={A:(((0,5),(1,2)),((1,2),(1,3))),
                Z:(((0,4),(1,2)),((1,2),(1,3))),B:(),C:()}
    for cls in root_b['classes']:
        for row in cls['suppliers']:
            if freeze(row['allowed_b'])!=expected_b[row['pose']]:
                raise ValueError('Wrong complete root point-supplier b domain')
    after_b=moving_collision_intervals((B2,C2),5,guard)
    if any(row['allowed_b'] for cls in after_b['classes'] for row in cls['suppliers']):
        raise ValueError('After-A packing alternative survives')
    math={'raw_system':s,'raw_partition':raw_partition,'raw_selected':expected,
          'raw_domain':'3<=b<=k+2','cap_records':records,
          'complete_root_point_supplier_b_domains':root_b,
          'after_A_B2_C2_moving_collision_domains':after_b,
          'earlier_E1_cuts':earlier_cuts(),'all_parameter_reduction':reduction(),
          'conclusion':'For every integer k>=6 and b, registered(I;4,b) is outsideE2; '
                       'the b=3 contact is already outsideE1',
          'scope':'Registered local original pair-halo filters, holes allowed; no Heesch conclusion'}
    controls=[]
    for row,lo in [((0,1,-4),3),((0,-1,7),3),((-1,0,6),3)]:
        try:wedge(row,lo)
        except ValueError:controls.append({'row':row,'lower':lo})
        else:raise ValueError('False wedge accepted')
    result={'agent':'six-heesch-2','role':'researcher','complete':True,'evidence':math,
            'mathematics_sha256':sha(math),'damaged_wedge_controls':controls,
            'seconds':round(time.monotonic()-start,3),
            'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'checked_utc':datetime.now(timezone.utc).isoformat()}
    (H/'generated').mkdir(exist_ok=True)
    mode='normal' if __debug__ else 'optimized'
    (H/'generated'/f'produced-{mode}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('agent','role','complete','mathematics_sha256',
                      'seconds','max_rss_kib')}|{'raw_cuts':raw_partition['cuts'],
                      'cap_sizes':[len(r['atlas']) for r in records],
                      'cap_cuts':[r['partition']['cuts'] for r in records],
                      'wedge_controls':len(controls)},sort_keys=True))
    signal.alarm(0)

if __name__=='__main__':main()
