"""Actual full-checker semantic damages, one guarded child per requested case."""
import argparse
import hashlib
import json
from pathlib import Path

import check_complete
import check_filters
import check_rows


def require(ok,message):
    if not ok:
        raise ValueError(message)


def run(case,root):
    root=Path(root)
    records=root/'CUT_ROWS-normal.jsonl'
    columns=root/'COLUMN_CERT-normal.jsonl'
    fixed=root/'FIXED-normal.json'
    first=root/'PAIR-0-25.json'
    second=root/'PAIR-25-2850.json'
    proposed=root/'COMPLETE-normal.json'
    damaged=root/('damage-'+case+'.json')
    if case in ('remove-valid-row','insert-invalid-row','boolean-row-word'):
        lines=records.read_bytes().splitlines(keepends=True)
        index=next(i for i,line in enumerate(lines) if any(json.loads(line)[1]))
        graph,domains=json.loads(lines[index])
        i=next(i for i,domain in enumerate(domains) if domain)
        if case=='remove-valid-row':
            removed=domains[i].pop(0)
            expected='Whole literal low-spine row domain differs'
        elif case=='insert-invalid-row':
            require(0 not in domains[i],'Zero cut row unexpectedly valid')
            domains[i]=sorted(domains[i]+[0])
            removed=None;expected='Whole literal low-spine row domain differs'
        else:
            domains[i][0]=True
            removed=None;expected='Bad literal nine-bit row word'
        lines[index]=json.dumps([graph,domains],separators=(',',':')).encode()+b'\n'
        damaged.write_bytes(b''.join(lines))
        call=lambda:check_rows.run(damaged)
        detail=dict(graph_index=index,row=i,omitted_valid_word=removed)
    elif case=='false-unsupported-pair':
        packet=json.loads(second.read_bytes())
        actual=json.loads(fixed.read_bytes())['cases'][0]
        index=actual['graph_index']
        target=next(row for row in packet['cases'] if row['graph_index']==index)
        cut=[0,actual['current_domains'][0][0],1]
        target['cuts'].append(cut)
        damaged.write_text(json.dumps(packet,sort_keys=True,separators=(',',':'))+'\n')
        expected='Deleted word has a literal ordinary compatible partner'
        call=lambda:check_filters.run(records,columns,[first,damaged],root/'should-not-exist-fixed.json')
        detail=dict(graph_index=index,false_cut=cut,valid_nonempty_fixed_point_used=True)
    elif case=='fabricated-complete-cut':
        packet=json.loads(proposed.read_bytes())
        actual=json.loads(fixed.read_bytes())['cases'][0]
        matrix=[domain[0] for domain in actual['current_domains']]
        encoded=json.dumps([matrix],separators=(',',':')).encode()
        packet.update(matrices=[matrix],physical_cut_matrices=1,
                      whole_matrix_bytes=len(encoded),whole_matrix_sha256=hashlib.sha256(encoded).hexdigest())
        damaged.write_text(json.dumps(packet,sort_keys=True,separators=(',',':'))+'\n')
        expected='Whole independent cut domain differs from producer'
        call=lambda:check_complete.run(fixed,damaged)
        detail=dict(each_fake_matrix_row_individually_valid=True,fake_matrix=matrix)
    else:
        raise ValueError('Unknown semantic control')
    rejected=None
    try:
        call()
    except ValueError as error:
        rejected=str(error)
    require(rejected==expected,'Damage did not reach the intended semantic failure: '+str(rejected))
    return dict(agent='six-books-3',role='researcher',status='ACTUAL_SEMANTIC_DAMAGE_REJECTED',
        case=case,actual_failure=rejected,detail=detail,
        actual_damaged_bytes=damaged.stat().st_size,
        actual_damaged_sha256=hashlib.sha256(damaged.read_bytes()).hexdigest(),
        operational_limit_counted_as_rejection=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--case',required=True)
    parser.add_argument('--root',required=True)
    args=parser.parse_args()
    print(json.dumps(run(args.case,args.root),sort_keys=True,separators=(',',':')))
