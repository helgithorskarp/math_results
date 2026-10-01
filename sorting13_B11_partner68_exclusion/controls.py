"""Semantic rejection controls; mutations bypass summary hashes on purpose.

Tests actual coverage, first-touch phase, local lower-bound, marked-charge and scalar-cap
checks. No generated file is changed, and no solver is imported.
"""
import argparse
import copy
import inspect
import json
from pathlib import Path
import sys
import time
import signal
import traceback
import verify
import tail_audit
from shared import HERE,inputs,program,read


def rejection(name,action,source_fragment):
    try:
        action()
    except AssertionError as error:
        site=traceback.extract_tb(error.__traceback__)[-1]
        assert source_fragment in (site.line or ''),(name,site)
        return dict(control=name,status='SEMANTIC_CORRUPTION_REJECTED',
                    function=site.name,assertion=site.line)
    finally:
        signal.alarm(0)
    raise AssertionError(('Corruption was accepted',name))


def main():
    assert __debug__
    parser=argparse.ArgumentParser()
    parser.add_argument('--repository',type=Path,default=HERE.parent)
    parser.add_argument('--output',type=Path,default=HERE/'generated')
    args=parser.parse_args();began=time.monotonic();results=[]
    old_read,old_argv=verify.read,sys.argv
    try:
        sys.argv=['verify.py','--repository',str(args.repository),
                  '--output',str(args.output),'--class-index','389']
        cert=read(HERE/'certificate.json');bad=copy.deepcopy(cert)
        bad['new_classes'].pop()
        verify.read=lambda path: copy.deepcopy(bad) if path==HERE/'certificate.json' else old_read(path)
        results.append(rejection('missing complete cohort class',verify.main,
                                 "cert['new_classes']==fresh"))
        leaf_path=args.output/'class389.json'
        bad=copy.deepcopy(read(leaf_path));bad['basic_boundary'].pop()
        verify.read=lambda path: copy.deepcopy(bad) if path==leaf_path else old_read(path)
        results.append(rejection('missing boundary completion leaf',verify.main,
                                 'set(keys)=='))
        bad=copy.deepcopy(read(leaf_path))
        bad['table']['triples'][0][1]=53
        verify.read=lambda path: copy.deepcopy(bad) if path==leaf_path else old_read(path)
        results.append(rejection('false actual first-touch phase gate',verify.main,
                                 "json.loads(json.dumps(t))==saved['table']"))
    finally:
        verify.read=old_read;sys.argv=old_argv
    f,selected,fresh,old=inputs(args.repository)
    v=program(args.repository,'verify')
    root,outgoing,entries,graph=v.full_graph(f['prefix22'])
    monoids,_=v.rank_monoids()
    index,code,events,orders=next(r for r in fresh if r[0]==389)
    seed=dict(f,class_code=code,parent_effective_words=orders)
    saved=read(args.output/'class389.json');table=saved['table']
    record=next(r for r in saved['extended_boundary'] if r['internal_lower_bound']==4)
    word=v.prefix_word(seed,table,monoids,record['case'],root,outgoing)
    rows=table['images9'][record['image']]
    full=v.original_image(seed,word,rows)
    bad=copy.deepcopy(record);bad['internal_lower_bound']+=1;bad['required_touches']+=1
    results.append(rejection('false four-wire internal lower bound',
                             lambda: verify.extended(bad,full,rows,v),
                             'Incorrect internal lower bound'))
    bad=copy.deepcopy(record);bad['prefix_passages']+=1
    results.append(rejection('false actual marked prefix charge',
                             lambda: verify.extended(bad,full,rows,v),
                             "charge==record['prefix_passages']"))
    scalar,clauses=tail_audit.prepare(args.repository,args.output)
    bad=copy.deepcopy(read(args.output/'tail_class390_image000.metadata.json'))
    bad['caps'][0][2]+=1
    # The substituted audit_data has a synthetic source filename; retain
    # its text in linecache so the assertion location remains reviewable.
    import linecache
    text=inspect.getsource(tail_audit.load(
        args.repository/'sorting13_B11_additional_ten_event_exclusions/audit_data.py',
        'unmodified_scalar_source').audit_data)
    text=text.replace("32 + meta['budget']","len(prefix) + meta['budget']")
    filename='<pinned scalar audit with actual-prefix capacities>'
    linecache.cache[filename]=(len(text),None,text.splitlines(True),filename)
    results.append(rejection('false pooled actual-prefix capacity',
                             lambda: scalar.audit_data(bad),'caps'))
    result=dict(agent='six-sorting-2',role='researcher',
                status='SIX_SEMANTIC_REJECTION_CONTROLS_PASSED',
                controls=results,seconds=time.monotonic()-began,
                scope='Hash gates bypassed; assertions from the actual public independent checkers')
    (args.output/'rejection-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__=='__main__':main()
