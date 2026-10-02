"""Prototype literal verification of additions to a checked G22 state.

Actual author six-tammes-2, researcher. UNVALIDATED at end of pass fifteen.
The validity premise is a successful pinned checker run for the exact
old state and receipt. A supplied JSON receipt alone is not a standalone
proof of that premise. Reproduction must start with the full base replay.
No mathematical predicate is changed: the pinned v2 reader checks every
new literal, new boundedness flag and new packing exclusion.
"""
from pathlib import Path
from collections import Counter
from fractions import Fraction as Q
import argparse, hashlib, importlib.util, json, signal, time

HERE=Path(__file__).resolve().parent
READER_HASH='b4584fb3eea81296f5ae8dcc01b038121c0bb32d943f1ada4c3091655dbfe7c0'
reader_path=HERE/'g22-cap-replay-v2.py'
if hashlib.sha256(reader_path.read_bytes()).hexdigest()!=READER_HASH:
    raise ValueError('pinned unchanged mathematical reader')
spec=importlib.util.spec_from_file_location('delta_literal_reader',reader_path)
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r);c=r.c

def structure(old,new):
    """Check the complete new partition and every old retained entry."""
    old_shape=r.shape(old);new_shape=r.shape(new)
    r.require(len(new['nodes'])>=len(old['nodes']),'old nodes retained')
    for index,prior in enumerate(old['nodes']):
        node=new['nodes'][index]
        for field in ('cell','bounded_inherited'):
            r.require(node[field]==prior[field],'unchanged old cell/inherited bound')
        r.require(node['proofs'][:len(prior['proofs'])]==prior['proofs'],
                  'every old selected record retained exactly in order')
        r.require(not prior['bounded'] or node['bounded'],'old boundedness retained')
        if 'split' in prior or 'prune' in prior or prior.get('complete'):
            r.require(node==prior,'old partitioned or closed node unchanged')
    return old_shape,new_shape

def verify_delta(old,new,old_receipt,progress=None,require_complete=False):
    old_shape,out=structure(old,new)
    if require_complete:r.shape(new,True)
    old_counts=Counter(row[1] for n in old['nodes'] for row in n['proofs'])
    total_counts=Counter(row[1] for n in new['nodes'] for row in n['proofs'])
    r.require(old_receipt['status'] in ('CHECKED_PARTIAL_AUTHOR_WITNESSES_NOT_FULL_THEOREM',
                  'CHECKED_COMPLETE_AUTHOR_G22_CAP_COVER'),'successful checked-input receipt')
    r.require(old_receipt['frozen_model_sha256']==r.MODEL_HASH and
              old_receipt['public_model_sha256']==r.PUBLIC_HASH and
              old_receipt['literal_reader_sha256']==READER_HASH,'same exact mathematical predicates')
    r.require(old_receipt['node_count']==old_shape['node_count'] and
              old_receipt['pending_nodes']==old_shape['pending_nodes'] and
              old_receipt['normalized_rectangle_areas']==old_shape['normalized_rectangle_areas'],
              'input receipt identifies the exact old partition')
    r.require(old_receipt['witness_count']==sum(old_counts.values()) and
              Counter(old_receipt['witness_counts'])==old_counts,'every old record accounted for')
    r.require(old_receipt['bounded_nodes']==sum(n['bounded'] for n in old['nodes']) and
              old_receipt['packing_witnesses']==sum('prune' in n for n in old['nodes']),
              'old boundedness/packing premises accounted for')
    checked=Counter();fresh_regular=fresh_bounded=fresh_pruned=0
    started=time.monotonic();last=started
    state=Path('/scratch/research-team-sol61-six-20260929/state')
    for index,node in enumerate(new['nodes']):
        if any((state/(name+'.json')).exists() for name in ('PAUSED','HANDOVER')):
            raise RuntimeError('operational pause barrier; stopped')
        prior=old['nodes'][index] if index<len(old['nodes']) else None
        offset=len(prior['proofs']) if prior else 0
        proofs=node['proofs'][offset:]
        new_bound=node['bounded'] and not (prior and prior['bounded'])
        new_prune='prune' in node and not (prior and 'prune' in prior)
        new_complete=node.get('complete') and not (prior and prior.get('complete'))
        if proofs or new_bound or new_prune or new_complete:
            P,t,raw=c.m.enclosed(*c.box(*node['cell']));base=dict(P=P,t=t);fresh_regular+=1
            geo=None
            if new_bound or new_complete or any(row[1] in ('C','G','H','N','F') for row in proofs):
                geo=c.geometry(P,t);geo['products']=base.setdefault('products',{})
            if new_bound:r.verify_bounded(geo);fresh_bounded+=1
            if new_prune:
                row=node['prune']
                r.require(type(row)is list and len(row)==3 and row[0]=='pair' and
                          tuple(row[1:]) in c.m.e.PAIRS,'literal newly selected packing pair')
                r.require(c.m.pair_gap(P,t,tuple(row[1:])).v.l>0,'new packing pair strictly exceeds t')
                fresh_pruned+=1
            for row in proofs:
                r.verify_record(row,base,geo,node['bounded_inherited'] or node['bounded'])
                checked[row[1]]+=1
        if progress is not None and time.monotonic()-last>5:
            progress(dict(last_node=index,checked_new_witnesses=sum(checked.values()),
                          seconds=round(time.monotonic()-started,3)))
            last=time.monotonic()
    r.require(checked==total_counts-old_counts,'every added literal checked exactly once')
    margin=2*c.RHO**2-1;r.require(margin>Q(593,1000),'exact cap capacity margin')
    out.update(status='CHECKED_COMPLETE_AUTHOR_G22_CAP_COVER' if require_complete else
        'CHECKED_PARTIAL_AUTHOR_WITNESSES_NOT_FULL_THEOREM',agent='six-tammes-2',role='researcher',
        regular_nodes=sum(bool(n['proofs'] or n['bounded'] or n.get('complete') or 'prune' in n)
                          for n in new['nodes']),
        bounded_nodes=sum(n['bounded'] for n in new['nodes']),
        packing_witnesses=sum('prune' in n for n in new['nodes']),
        witness_count=sum(total_counts.values()),witness_counts=dict(total_counts),
        checked_new_witnesses=sum(checked.values()),new_witness_counts=dict(checked),
        new_regular_checks=fresh_regular,new_bounded_checks=fresh_bounded,new_packing_checks=fresh_pruned,
        frozen_model_sha256=r.MODEL_HASH,public_model_sha256=r.PUBLIC_HASH,
        literal_reader_sha256=READER_HASH,enclosure_version='v2',cap_pair_lower_bound=str(margin),
        imported_critical_lemma='bafkreif3recyji2krueruwtszh6v7gjdnktl64mmmifpla6xhlw5in6ate',
        input_validity_premise='successful pinned full/delta checker execution for exact input and receipt',
        trust_boundary='same-author conditional extension of checked input; shares unchanged pinned model/kernel')
    return out

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('checked_input');parser.add_argument('new_state')
    parser.add_argument('--verified-input-receipt',required=True)
    parser.add_argument('--expected-input-receipt-sha256',required=True)
    parser.add_argument('--receipt',required=True);parser.add_argument('--prefix',required=True)
    parser.add_argument('--require-complete',action='store_true');args=parser.parse_args()
    old_bytes=Path(args.checked_input).read_bytes();new_bytes=Path(args.new_state).read_bytes()
    receipt_bytes=Path(args.verified_input_receipt).read_bytes()
    r.require(hashlib.sha256(receipt_bytes).hexdigest()==args.expected_input_receipt_sha256,
              'pinned successful input receipt bytes')
    old_receipt=json.loads(receipt_bytes)
    old_hash=hashlib.sha256(old_bytes).hexdigest();new_hash=hashlib.sha256(new_bytes).hexdigest()
    r.require(old_receipt['plan_sha256']==old_hash,'exact checked input bytes')
    old,new=json.loads(old_bytes),json.loads(new_bytes)
    started=time.monotonic()
    prefix=dict(status='CHECKED_DELTA_PREFIX_ONLY',last_node=-1,checked_new_witnesses=0,
                plan_sha256=new_hash,input_plan_sha256=old_hash,
                input_replay_receipt_sha256=args.expected_input_receipt_sha256,
                literal_reader_sha256=READER_HASH,agent='six-tammes-2',role='researcher')
    def progress(update):
        prefix.update(update);Path(args.prefix).write_text(json.dumps(prefix,indent=2)+'\n')
    progress({})
    signal.signal(signal.SIGALRM,lambda *_:(_ for _ in ()).throw(
        TimeoutError('160-second delta replay guard; incomplete')))
    signal.alarm(160)
    try:
        out=verify_delta(old,new,old_receipt,progress,args.require_complete)
        out.update(plan_sha256=new_hash,input_plan_sha256=old_hash,
                   input_replay_receipt_sha256=args.expected_input_receipt_sha256,
                   seconds=round(time.monotonic()-started,3),guard_seconds=160)
        progress(dict(last_node=len(new['nodes'])-1,
                      checked_new_witnesses=out['checked_new_witnesses'],seconds=out['seconds']))
    except Exception as exc:
        out=dict(status='DELTA_REPLAY_FAILED_OR_INCOMPLETE',error_type=type(exc).__name__,
                 reason=str(exc),plan_sha256=new_hash,saved_prefix=prefix,
                 seconds=round(time.monotonic()-started,3),agent='six-tammes-2',role='researcher')
        Path(args.receipt).write_text(json.dumps(out,indent=2)+'\n');raise
    finally:signal.alarm(0)
    Path(args.receipt).write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))
