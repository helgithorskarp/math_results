"""Verify the complete published residual certificate table without a solver."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
from encode import catalogue, witness, require

HERE=Path(__file__).resolve().parent
FIELDS=['index','task','whole_task_status','residual_status','clauses','cnf_sha256','residual_edgeword']

def verify(data,ledger):
    cores=catalogue(data)
    with Path(ledger).open(newline='') as stream:
        reader=csv.DictReader(stream,delimiter='\t')
        require(reader.fieldnames==FIELDS,'ledger header')
        rows=list(reader)
    require(len(rows)==362,'ledger cardinality')
    counts=[]
    for i,row in enumerate(rows):
        require(set(row)==set(FIELDS) and all(isinstance(v,str) for v in row.values()),'ledger fields')
        require(row['index']==str(i) and row['task']==f'bo1-q9-r5-c{i:06d}','ledger original identity')
        require(row['whole_task_status']=='UNKNOWN' and row['residual_status']=='SAT','ledger claim status')
        require(row['clauses'].isdigit() and 23804<=int(row['clauses'])<=30052,'clause count field')
        require(len(row['cnf_sha256'])==64 and all(c in '0123456789abcdef' for c in row['cnf_sha256']),'CNF hash format')
        counts.append(witness(cores[i],row['residual_edgeword'])['red_edges'])
    result={'verified_residual_witnesses':362,'new_whole_task_exclusions':0,'gate_pass':False,
            'whole_task_unknown_in_q9_r5':362,'whole_registry_unknown':2188660,
            'good43_found':False,'red_edge_range':[min(counts),max(counts)],
            'literal_four_subsets':362*8855,'literal_five_subsets':362*33649,
            'ledger_sha256':hashlib.sha256(Path(ledger).read_bytes()).hexdigest()}
    return result,rows

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--data',type=Path,required=True)
    parser.add_argument('--ledger',type=Path,default=HERE/'LEDGER.tsv')
    parser.add_argument('--models',type=Path)
    args=parser.parse_args()
    result,rows=verify(args.data,args.ledger)
    if args.models:
        require(not args.models.exists(),'models output exists')
        args.models.write_text(''.join(r['index']+'\t'+r['residual_edgeword']+'\n' for r in rows))
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
