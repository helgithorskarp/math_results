#!/usr/bin/env python3
"""Fresh bounded verification of twelve kernels on four whole sections.

Actual author six-sendov-2, researcher,2026-10-01.
Public transport and trace/filter algorithms are openly adapted.
Every regenerated record is compared to a mandatory compact fixture.
A collector audits supplied records; it does not authenticate their runs.
"""
import argparse,copy,hashlib,importlib.util,json,tempfile
from pathlib import Path

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('credited_complete_cover',HERE/'cover.py')
c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
m=c.m
GATES=0
def require(ok,label):
    global GATES
    GATES+=1
    if not ok:raise ValueError(label)
def hashes():
    return {name:hashlib.sha256((HERE/name).read_bytes()).hexdigest()
            for name in ('cover.py','verify.py')}
def common():
    before=m.CHECKS
    geometry=json.loads(json.dumps(c.common()))
    return {'geometry':geometry,'mathematical_checks':m.CHECKS-before}
def derive_case(pair,cell):
    start=m.CHECKS
    if pair not in c.PAIRS or cell not in range(3):raise ValueError('outside complete twelve-cell cover')
    def hook(rank,index):
        if rank!=0 or index!=cell:raise ValueError('one exact selected cell')
        return c.c.geometry(pair,index)
    m.geometry=hook
    rows,meta=m.build_case(0,cell)
    signs=m.grouped_signs(rows[8]) if cell==2 else m.complete_strict_signs(rows[8])
    controls=c.full_controls(pair,cell,rows,meta)
    if pair==(1,5):
        old=m.full_controls(1 if cell==2 else 0,cell,rows,meta)
        m.require(controls==old,'entire new(1,5) controls equal credited backend')
    return {'pair':list(pair),'cell':cell,'complete_cover_cells':3,
            'meta':meta,'target_sha256':m.digest(rows[8].dump()),
            'certificate':signs,'complete_full_controls':controls,
            'mathematical_checks':m.CHECKS-start}
def assemble(whole,cases):
    wanted=[(*pair,cell) for pair in c.PAIRS for cell in range(3)]
    by_key={(*row['pair'],row['cell']):row for row in cases}
    require(len(by_key)==len(cases)==len(wanted)==12,'all twelve unique complete cases')
    require(set(by_key)==set(wanted),'entire intended four-section cover')
    ordered=[by_key[key] for key in wanted]
    strict=[row for row in ordered if row['cell']!=2]
    grouped=[row for row in ordered if row['cell']==2]
    totals={'sections':len(whole['geometry']),'kernels':len(ordered),
        'section_vertices':sum(len(row['full_vertices']) for row in whole['geometry']),
        'strict_coefficient_entries':sum(row['certificate']['entries'] for row in strict),
        'strict_zero_coefficients':sum(row['certificate']['zeros'] for row in strict),
        'high_transverse_entries':sum(row['certificate']['high_entries'] for row in grouped),
        'high_transverse_zeros':sum(row['certificate']['high_zeros'] for row in grouped),
        'scalar_tables':sum(len(row['certificate']['tables']) for row in grouped),
        'domination_tables':sum(len(row['certificate']['domination_tables']) for row in grouped),
        'scalar_sign_entries':sum(table['entries'] for row in grouped for table in row['certificate']['tables']),
        'domination_sign_entries':sum(table['entries'] for row in grouped for table in row['certificate']['domination_tables']),
        'full_defining_controls':sum(len(row['complete_full_controls']) for row in ordered),
        'mathematical_checks':whole['mathematical_checks']+sum(row['mathematical_checks'] for row in ordered)}
    totals['target_sign_entries']=sum(totals[key] for key in ('strict_coefficient_entries','high_transverse_entries','scalar_sign_entries','domination_sign_entries'))
    require(totals['sections']==4 and totals['section_vertices']==28 and totals['strict_coefficient_entries']==119600 and totals['high_transverse_entries']==58140 and totals['scalar_tables']==244 and totals['domination_tables']==24 and totals['target_sign_entries']==183364 and totals['full_defining_controls']==88,'entire four-section totals')
    return {'normalization':'balanced eight roots; positive max1; complete four optimizer-adjacent ordered six-level2+2+1^4 sections; all collisions retained',
            'threshold':'785753/1000','homogeneous_degree':22,
            'transport_sha256':c.PIN,'backend_sha256':c.c.PIN,
            'common':whole,'cases':ordered,'totals':totals}
def load_fixture(path):
    try:fixture=json.loads(path.read_text())
    except (OSError,ValueError) as e:raise ValueError('mandatory complete fixture unavailable') from e
    require(set(fixture)=={'record','record_sha256'},'complete expected schema')
    require(m.digest(fixture['record'])==fixture['record_sha256'],'fixture canonical record hash')
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
        variants.append(('changed full strict coefficient digest',v))
        v=copy.deepcopy(record);v['cases'][2]['certificate']['domination_tables'][0]['coefficient_sha256']='0'*64
        variants.append(('changed complete domination table',v))
        v=copy.deepcopy(record);v['common']['geometry'][0]['local_S_coefficients'][3]='1'
        variants.append(('changed whole physical local map',v))
        v=copy.deepcopy(record);v['cases'][2]['complete_full_controls'][-2]['Psi']='0'
        variants.append(('changed defining local Psi',v))
        v=copy.deepcopy(record);v['cases'].pop()
        variants.append(('incomplete twelve-cell cover',v))
        for label,v in variants:
            # Recompute the attacker-controlled hash; full comparison or
            # complete-cover validation must reject the mathematical damage.
            p.write_text(json.dumps({'record':v,'record_sha256':m.digest(v)}))
            try:
                damaged=load_fixture(p)
                require(damaged['record']==record,'full regenerated record comparison')
            except ValueError:rejected.append(label)
            else:raise ValueError('damaged mathematical fixture accepted: '+label)
    require(len(rejected)==6,'all six damaged/missing fixtures rejected')
    return rejected
def main():
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--case',help='doubled ranks and cell, for example1,5:0')
    g.add_argument('--collect-cases',nargs='+',type=Path)
    p.add_argument('--manifest',type=Path,default=HERE/'expected.json')
    p.add_argument('--write-case',type=Path)
    p.add_argument('--test-manifest-rejections',action='store_true')
    a=p.parse_args();fixture=load_fixture(a.manifest)
    fixture_hash=hashlib.sha256(a.manifest.read_bytes()).hexdigest()
    source_hashes=hashes();expected=fixture['record']
    if a.case:
        if a.test_manifest_rejections:raise ValueError('rejection controls require complete record union')
        if a.write_case and a.write_case.resolve()==a.manifest.resolve():raise ValueError('case output must not overwrite mandatory fixture')
        left,right=a.case.split(':');pair=tuple(map(int,left.split(',')));cell=int(right)
        whole=common()
        require(whole==expected['common'],'entire freshly derived geometry record')
        row=derive_case(pair,cell)
        targets=[r for r in expected['cases'] if (r['pair'],r['cell'])==(list(pair),cell)]
        require(len(targets)==1 and row==targets[0],'entire freshly derived case record')
        payload={'status':'PASS_CASE','source_sha256':source_hashes,
                 'manifest_sha256':fixture_hash,'common':whole,'case':row,
                 'case_sha256':m.digest(row)}
        if a.write_case:a.write_case.write_text(json.dumps(payload,indent=2)+'\n')
        cert=row['certificate']
        count=cert.get('entries') if cell!=2 else cert['high_entries']+sum(t['entries'] for t in cert['tables']+cert['domination_tables'])
        summary={'status':'PASS_CASE','pair':pair,'cell':cell,
                 'target_sign_entries':count,'full_defining_controls':len(row['complete_full_controls']),
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
            require(m.digest(row['case'])==row['case_sha256'],'whole supplied case hash')
            cases.append(row['case'])
        record=assemble(expected['common'],cases)
        require(record==expected,'entire assembled record comparison')
        require(m.digest(record)==fixture['record_sha256'],'whole canonical record hash')
        rejected=reject_controls(record) if a.test_manifest_rejections else []
        summary={'status':'PASS_RECORD_UNION','regenerates_cases':False,
                 'record_sha256':fixture['record_sha256'],**record['totals'],
                 'rejected_fixtures':len(rejected),'gate_checks':GATES}
    print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
