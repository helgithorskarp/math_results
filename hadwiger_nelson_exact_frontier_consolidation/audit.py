#!/usr/bin/env python3
"""Check consolidation source identities and the exact seven-point scope guard.

This is not a replay or independent review of the historical theorems.
"""
import argparse
from collections import Counter
import hashlib
import json
from math import comb
from pathlib import Path
from scope_guard import verify_guard

def digest(raw):return hashlib.sha256(raw).hexdigest()

def contained(root,relative):
    rel=Path(relative)
    if rel.is_absolute():raise ValueError('absolute source path')
    path=(root/rel).resolve()
    if not path.is_relative_to(root.resolve()):raise ValueError('source path escapes repository')
    return path

def check(registry,root):
    if registry['format']!=1 or registry['record_improvement'] or registry['new_candidate_searches']:
        raise ValueError('wrong consolidation scope')
    identities={};manifest_rows=0;reviews=0;counts=Counter();source_counts={}
    def pin(row):
        path=contained(root,row['path']);raw=path.read_bytes()
        if len(raw)!=row['bytes'] or digest(raw)!=row['sha256']:
            raise ValueError('pinned source changed: '+row['path'])
        identities[row['path']]=row['sha256'];return raw
    for entry in registry['entries']:
        counts[entry['scope_kind']]+=1
        pin(entry['principal_proof']);raw=pin(entry['source_manifest'])
        package=contained(root,entry['directory']);checked=0
        for line in raw.decode().splitlines():
            if not line.strip():continue
            expected,name=line.split(maxsplit=1);name=name.strip()
            if name.startswith('*'):name=name[1:]
            path=contained(package,name)
            if len(expected)!=64 or digest(path.read_bytes())!=expected:
                raise ValueError('historical manifest mismatch: '+str(path))
            relative=str(path.relative_to(root.resolve()));identities[relative]=expected
            checked+=1;manifest_rows+=1
        source_counts[entry['id']]=checked
        if 'document' in entry['review']:pin(entry['review']['document']);reviews+=1
    # Arithmetic consequences of the recorded family parameters, not new enumeration.
    copies=(508-21)//18
    consequences={'heptagon_max_target_copies':copies,'heptagon_max_target_vertices':21+18*copies,
                  'heptagon_target_subsets':sum(comb(35,k) for k in range(copies+1)),
                  'snail_labelled_cases':29*28,'triangular_exceptional_angles':1350+396,
                  'saved_pilot_labelled_outputs':32+4+1,
                  'degrey_lower_critical_order':2*256-1,
                  't721_lower_critical_order':475+99}
    return {'source_identity_audit_passed':True,'registry_entries':len(registry['entries']),
            'scope_kind_counts':dict(sorted(counts.items())),
            'historical_manifest_rows_checked':manifest_rows,
            'unique_pinned_files_checked':len(identities),'source_manifest_counts':source_counts,
            'accepted_review_documents_pinned':reviews,'graph_cutoff':registry['graph_cutoff'],
            'file_identity_stream_sha256':digest(json.dumps(identities,sort_keys=True,separators=(',',':')).encode()),
            'derived_arithmetic_only':consequences,'historical_verifiers_rerun':False,
            'historical_theorems_reproved_by_this_audit':False,'record_improvement':False}

def main():
    here=Path(__file__).resolve().parent
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo-root',type=Path,default=here.parent)
    args=p.parse_args();raw=(here/'registry.json').read_bytes()
    result=check(json.loads(raw),args.repo_root)
    result['registry_sha256']=digest(raw)
    guard=(here/'scope_guard.json').read_bytes()
    result['scope_guard']=verify_guard(json.loads(guard));result['scope_guard_sha256']=digest(guard)
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
