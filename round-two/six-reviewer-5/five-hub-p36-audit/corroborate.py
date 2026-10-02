"""Post-seal full native comparison; ancillary, not the independent premise."""
import json,pathlib,subprocess,sys
import audit as a

P=pathlib.Path(__file__).resolve().parent/'scratch/author'
native=json.loads((P/'native-normal-full.json').read_text())
other=json.loads((P/'native-optimized-full.json').read_text())
a.need(native==other,'full native normal/O output bytes decoded exactly')
first=json.loads((P/'first-record.json').read_text())
code="import json,producer;d=json.load(open('fixtures.json'));r,_=producer.rows_and_physical_bridge(d);s=producer.conservative_rows(d,r);print(json.dumps({'stars':d['stars'],'raw':r,'selected':s}))"
result=subprocess.run([sys.executable,'-B','-c',code],cwd=P/'original',capture_output=True,text=True,timeout=10)
result.check_returncode();author=json.loads(result.stdout)
own_fixture=json.loads((a.P/'fixtures.json').read_text())['stars']
a.need(author['stars']==own_fixture,'all literal23 star arrays, group metadata ignored')
raw,capped,types=a.raw_and_types(own_fixture)
def convert_type(t):
    a.need(t[10]==t[0]+t[1]-t[8],'native redundant hub-weight identity')
    return tuple(t[:5])+(t[5],t[8],t[6],t[9],t[7])
def converted_rows(rows):return {(r['fixture'],tuple(r['hub_high'])):convert_type(r['coordinates']) for r in rows}
def own_rows(rows):
    return {(r['star'],tuple(r['hubs'])):(r['e'],r['k'],r['q'],r['eligible'],r['h'],r['g1'],r['sigma'],r['psi'],r['I5'],r['margin']) for r in rows}
a.need(converted_rows(author['raw'])==own_rows(raw),'every426 native row field including excess/weight')
a.need(converted_rows(author['selected'])==own_rows(capped),'every410 conservative native row field')
a.need(sorted(convert_type(t) for t in native['types'])==types,'whole51type projection matches')
def key(c):return tuple(c[k] for k in ('T','X','tau','N5','Q','E','K','margin_budget'))
case_map={key(c):c for c in native['branches']}
a.need(set(case_map)=={key(c) for c in first['all_scalar_cases']},'entire27 scalar carrier')
counter=0;reason_map={'unit_endpoint':'UNIT_NEIGHBOR_CAPACITY','distinct_crossing':'DISTINCT_RADIUS_TWO_CROSSINGS','all_color_closure':'ALL_COLORS_CLOSED_PARTITION'}
closures=[]
for case in first['all_scalar_cases']:
    b=case_map[key(case)];their={}
    for vector,cert in zip(b['patterns'],b['certificates']):
        sparse=tuple(sorted((convert_type(t),n) for t,n in zip(native['types'],vector) if n))
        a.need(sparse not in their,'no duplicated native full vector');their[sparse]=cert
    a.need(len(their)==len(case['vectors']),'complete count in each case')
    for record in case['vectors']:
        sparse=tuple((tuple(t),n) for t,n in record['population']);c=their.pop(sparse);r=record['metrics']
        a.need(c['reason']==reason_map[record['all_original_cut_failures'][0]],'every native ordered exclusion reason')
        for k in ('D','I','C1','C2','B2'):a.need(c[k]==r[k],'every native endpoint coordinate')
        for own,nat in [('R','unit_roots_k0'),('U','unit_rows'),('A','ineligible_unit_rows'),('C','ineligible_nonunit_rows'),('B','eligible_nonunit_rows')]:
            a.need(r[own]==c[nat],'every native vertex-role count')
        a.need(r['closed_root']-r['R']==c['ineligible_nonunit_roots_k0'],'every actual nonunit radius root')
        if c['reason']=='ALL_COLORS_CLOSED_PARTITION':closures.append({'case':dict(zip(('T','X','tau','N5','Q','E','K','margin_budget'),key(case))),'actual_population':record['population'],'actual_metrics':r})
        counter+=1
    a.need(not their,'no unpaired native vector')
record={'agent':'six-reviewer-5','role':'independent mathematical reviewer','phase':'After both independent pre-native seals',
        'all23literal_stars_equal':True,'every426raw_and410selected_row_field_equal':True,
        'every51type27case136vector_and_full_role_certificate_equal':True,'matched_vectors':counter,
        'native_normal_O_whole_mathematical_hash':'77ebab7867e63eb1a88fad4bd8586559ff055fc598ac40782f69a30a9b3471dd',
        'actual_two_ordered_closure_residuals':closures,
        'correction':'Original body and source PROOF first closure bullet names five U0 plus one ineligible unit k1/q3 and seven eligible nonunits. This is a DIFFERENT actual necessary vector, excluded already by distinct crossings. The actual first residual has five U0, one ELIGIBLE unit k1/q0, four eligible nonunits k1/q0, three INELIGIBLE nonunits k1/q1; I20,C1=9,C3,B4. Native and fresh complete enumerations agree. No correction to source checker, counts or conditional P>=36 conclusion is required.'}
a.need(record==json.loads((a.P/'CORROBORATION.json').read_text()),'whole independent/native late corroboration including corrected closure roles');(P/'corroboration-record.json').write_bytes(a.encode(record));print(a.encode(record).decode())
