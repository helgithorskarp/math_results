#!/usr/bin/env python3
"""Fresh bounded verification of39 exact kernels on11 complete sections.

Actual author six-sendov-2, researcher,2026-10-01.
The complete geometry and trace/filter arithmetic are openly credited.
The mandatory compact fixture is compared in full. A record collector
audits supplied records; it does not regenerate or authenticate them.
"""
import argparse,copy,hashlib,importlib.util,json,tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('credited_transport_cover',HERE/'cover.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
GATES=0
def require(ok,label):
    global GATES
    GATES+=1
    if not ok:raise ValueError(label)
def hashes():
    return {name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
            for name in ('cover.py','verify.py')}
def common():
    before=c.m.CHECKS
    geometry=json.loads(json.dumps(c.all_geometry()))
    c.m.require(c.F(2,25)<c.F(87,1000)<c.F(9,100),'credited scalar test point in the stated interval')
    c.m.require(c.m.j_value(c.F(87,1000))-c.F(785753,1000)>c.F(1,1250),'exact strict scalar gap above every certified section')
    return {'geometry':geometry,'mathematical_checks':c.m.CHECKS-before}
def derive_case(pair,cell,whole):
    start=c.m.CHECKS
    count=len(c.path_cells(pair)[-1])
    if not 0<=cell<count:raise ValueError('cell outside complete cover')
    def hook(rank,index):
        if rank!=0 or index!=cell:raise ValueError('one exact selected cell')
        return c.geometry(pair,cell)
    c.m.geometry=hook
    rows,meta=c.m.build_case(0,cell)
    signs=c.m.complete_strict_signs(rows[8])
    controls=c.m.full_controls(0,cell,rows,meta)
    return {'pair':list(pair),'cell':cell,'complete_cover_cells':count,
            'meta':meta,'target_sha256':c.m.digest(rows[8].dump()),
            'certificate':signs,'complete_full_controls':controls,
            'mathematical_checks':c.m.CHECKS-start}
def assemble(whole,cases):
    ordered=[]
    wanted=[(*row['doubled_ranks'],cell['cell'])
            for row in whole['geometry'] for cell in row['cells']]
    by_key={(*row['pair'],row['cell']):row for row in cases}
    require(len(by_key)==len(cases)==len(wanted)==39,'all39 unique complete cases')
    require(set(by_key)==set(wanted),'entire intended case cover')
    for key in wanted:ordered.append(by_key[key])
    totals={'sections':len(whole['geometry']),'kernels':len(ordered),
        'section_vertices':sum(len(row['full_vertices']) for row in whole['geometry']),
        'coefficient_entries':sum(row['certificate']['entries'] for row in ordered),
        'zero_coefficients':sum(row['certificate']['zeros'] for row in ordered),
        'full_defining_controls':sum(len(row['complete_full_controls']) for row in ordered),
        'mathematical_checks':whole['mathematical_checks']+sum(row['mathematical_checks'] for row in ordered)}
    require(totals['sections']==11 and totals['section_vertices']==81 and totals['coefficient_entries']==583050 and totals['full_defining_controls']==234,'entire11-section totals')
    return {'normalization':'balanced eight roots; positive max1; six ordered levels2+2+1^4; nonadjacent doubled ranks; all collisions retained',
            'threshold':'785753/1000','homogeneous_degree':22,
            'backend_sha256':c.PIN,'common':whole,'cases':ordered,'totals':totals}
def load_fixture(path):
    try:fixture=json.loads(path.read_text())
    except (OSError,ValueError) as e:raise ValueError('mandatory complete fixture unavailable') from e
    require(set(fixture)=={'record','record_sha256'},'complete expected schema')
    require(c.m.digest(fixture['record'])==fixture['record_sha256'],'fixture canonical record hash')
    record=fixture['record']
    require(assemble(record['common'],record['cases'])==record,'complete fixture schema and cover consistency')
    return fixture
def reject_controls(record):
    rejected=[]
    with tempfile.TemporaryDirectory() as directory:
        p=Path(directory)/'expected.json'
        try:load_fixture(p)
        except ValueError:rejected.append('missing whole fixture')
        variants=[]
        v=copy.deepcopy(record);v['cases'][0]['certificate']['coefficient_sha256']='0'*64
        variants.append(('changed complete coefficient digest',v))
        v=copy.deepcopy(record);v['cases'][0]['meta']['gap_vertices'][0][0]='1'
        variants.append(('changed weighted gap vertex',v))
        v=copy.deepcopy(record);v['cases'][0]['complete_full_controls'][0]['Psi']='0'
        variants.append(('changed full defining Psi',v))
        v=copy.deepcopy(record);v['cases'].pop()
        variants.append(('incomplete39-cell cover',v))
        for label,v in variants:
            # Recompute the attacker-controlled hash; literal mathematics
            # or full-cover comparison, not a stale hash, must reject it.
            p.write_text(json.dumps({'record':v,'record_sha256':c.m.digest(v)}))
            try:
                damaged=load_fixture(p)
                require(damaged['record']==record,'full regenerated record comparison')
            except ValueError:rejected.append(label)
            else:raise ValueError('damaged mathematical fixture accepted: '+label)
    require(len(rejected)==5,'all five damaged/missing fixtures rejected')
    return rejected
def main():
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--case',help='doubled ranks and cell, for example1,2:0')
    g.add_argument('--collect-cases',nargs='+',type=Path)
    p.add_argument('--manifest',type=Path,default=HERE/'expected.json')
    p.add_argument('--write-case',type=Path)
    p.add_argument('--test-manifest-rejections',action='store_true')
    a=p.parse_args();fixture=load_fixture(a.manifest)
    fixture_hash=hashlib.sha256(a.manifest.read_bytes()).hexdigest()
    source_hashes=hashes();expected=fixture['record']
    if a.case:
        if a.test_manifest_rejections:raise ValueError('rejection controls require complete record union')
        left,right=a.case.split(':');pair=tuple(map(int,left.split(',')));cell=int(right)
        if pair not in c.SECTIONS:raise ValueError('section outside complete11-section domain')
        whole=common()
        require(whole==expected['common'],'entire freshly derived geometry record')
        row=derive_case(pair,cell,whole)
        targets=[r for r in expected['cases'] if (r['pair'],r['cell'])==(list(pair),cell)]
        require(len(targets)==1 and row==targets[0],'entire freshly derived case record')
        payload={'status':'PASS_CASE','source_sha256':source_hashes,
                 'manifest_sha256':fixture_hash,'common':whole,'case':row,
                 'case_sha256':c.m.digest(row)}
        if a.write_case:a.write_case.write_text(json.dumps(payload,indent=2)+'\n')
        summary={'status':'PASS_CASE','pair':pair,'cell':cell,
                 'coefficient_entries':row['certificate']['entries'],
                 'full_defining_controls':len(row['complete_full_controls']),
                 'case_sha256':payload['case_sha256'],
                 'mathematical_checks':whole['mathematical_checks']+row['mathematical_checks'],
                 'gate_checks':GATES}
    else:
        if a.write_case:raise ValueError('write-case requires fresh selected case')
        cases=[]
        for path in a.collect_cases:
            row=json.loads(path.read_text())
            require(row['status']=='PASS_CASE','passed supplied case status')
            require(row['source_sha256']==source_hashes,'same declared executable sources')
            require(row['manifest_sha256']==fixture_hash,'same complete fixture bytes')
            require(row['common']==expected['common'],'same complete common geometry')
            require(c.m.digest(row['case'])==row['case_sha256'],'whole supplied case hash')
            cases.append(row['case'])
        record=assemble(expected['common'],cases)
        require(record==expected,'entire assembled record comparison')
        require(c.m.digest(record)==fixture['record_sha256'],'whole canonical record hash')
        rejected=reject_controls(record) if a.test_manifest_rejections else []
        summary={'status':'PASS_RECORD_UNION','regenerates_cases':False,
                 'record_sha256':fixture['record_sha256'],**record['totals'],
                 'rejected_fixtures':len(rejected),'gate_checks':GATES}
    print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
