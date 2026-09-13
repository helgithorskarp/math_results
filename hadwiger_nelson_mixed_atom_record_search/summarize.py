"""Compare a regenerated structural search census with the compact expected one."""
from atoms import *
W=workdir();HERE=Path(__file__).resolve().parent

def census():
 sources=json.loads((W/'sources.json').read_text());results=[json.loads((W/f'result_{i}.json').read_text())for i in range(len(sources))]
 field=[json.loads((W/f'field_result_{d}_{k}.json').read_text())for d in(5,13)for k in('GMM','MMG')]
 for x in results:
  require(x['tally'].get('SAT',0)==x['total_quadratics'] and not x['unresolved'],'incomplete main source')
 for x in field:require(x['tally'].get('SAT',0)==x['phases'],'incomplete fixed field')
 return {'main':{'sources':len(sources),'quadratics':sum(x['total_quadratics']for x in results),'SAT':sum(x['tally']['SAT']for x in results),'UNSAT':0,'UNKNOWN':0,'max_vertices':max(x['vertices']for x in results),'max_edges':max(r['edges']for x in results for r in x['results']),'source_rows':[{'index':x['source_index'],'vertices':x['vertices'],'base_edges':x['base_edges'],'quadratics':x['total_quadratics'],'max_edges':max((r['edges']for r in x['results']),default=x['base_edges'])}for x in results]},'fixed_fields':[{'d':x['d'],'kind':x['kind'],'phases':x['phases'],'SAT':x['tally']['SAT'],'UNSAT':0,'UNKNOWN':0,'max_vertices':max(r['vertices']for r in x['records']),'max_edges':max(r['edges']for r in x['records'])}for x in field]}
if __name__=='__main__':
 actual=census();expected=json.loads((HERE/'EXPECTED.json').read_text())
 for key in actual:require(actual[key]==expected[key],'structural census mismatch: '+key)
 print(json.dumps({'status':'PASS','main_quadratics':actual['main']['quadratics'],'fixed_field_phases':sum(x['phases']for x in actual['fixed_fields']),'UNSAT':0,'UNKNOWN':0},indent=2))
