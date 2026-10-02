"""Reparse every actual coefficient and join six complete source products."""
from pins import verify_pins
verify_pins()
from pathlib import Path
import argparse,copy,json
from assembly import assemble
from forest import load_forest
from kernel import source_geometry,make_domain,F,Q,Z,need,digest
from check_cell import CELLS
HERE=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser();p.add_argument('--cell',choices=list(CELLS),required=True)
    p.add_argument('--inputs',type=Path,nargs=6,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    need(not a.output.exists(),'fresh complete cell record required')
    parts=[json.loads(x.read_text()) for x in a.inputs]
    need(all(r['cell']==a.cell for r in parts),'incorrect original receiving cell')
    data,roots,volume=source_geometry();domain=make_domain(data,tuple(map(Q,CELLS[a.cell])))
    forest=load_forest(a.cell,domain);result=assemble(parts,forest)
    expected=json.loads((HERE/'expected.json').read_text())['cells'][a.cell]
    need(all(result[k]==v for k,v in expected.items() if k!='parts'),'entire expected actual source stream differs')
    controls=[]
    for title,mutation in [
        ('omit one complete source product',lambda p:p.pop()),
        ('omit one actual coefficient',lambda p:next(r for r in p[0]['all_leaf_control_records'] if r[2]!='branch')[4].pop()),
        ('negative actual coefficient with refreshed hash',lambda p:next(r for r in p[0]['all_leaf_control_records'] if r[2]!='branch')[4].__setitem__(0,['-1','0'])),
        ('change the closed source interval',lambda p:p[0].__setitem__('root_interval',[1,18]))]:
        bad=copy.deepcopy(parts);mutation(bad)
        for r in bad:r['all_leaf_control_records_sha256']=digest(r['all_leaf_control_records'])
        try:assemble(bad,forest)
        except ValueError as e:controls.append({'control':title,'rejected':str(e)});continue
        raise ValueError('damaged whole-source assembly accepted')
    result.update(cell=a.cell,four_semantic_assembly_damages_rejected=controls,
                  all_expected_source_control_streams_match=True)
    a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['cell','counts','minimum','whole_actual_records_sha256']}),flush=True)

if __name__=='__main__':main()
