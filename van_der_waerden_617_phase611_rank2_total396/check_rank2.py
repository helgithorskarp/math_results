"""Definition-level AP/triple weighted packing checker on full checked domains.

Imports no proposal, bit-mask, square-enumeration or numerical implementation.
Every dependency is replayed, all progressions are actual, and all arithmetic
in the certificate check uses exact native Python integers.
"""
import argparse
import hashlib
import json
from pathlib import Path
import base_verify
import check_branch

need=base_verify.need


def check(base,shared,certificate,branch=None,context=None):
    fields={'format','phase','caps','root','original_class','base_certificate_sha256','shared_trace_sha256','branch_trace_sha256',
            'denominator','AP_weights','triple_weights'}
    need(type(certificate) is dict and set(certificate)==fields,'Rank2 packing schema')
    need(certificate['format']=='QR617_KNOWN_RANK2_PACKING_1','Rank2 packing format')
    ctx=check_branch.Context(base,shared,certificate['caps']) if context is None else context
    need(certificate['caps']==ctx.caps and type(certificate['phase']) is int and certificate['phase']==ctx.phase,'Actual phase and cap hypothesis')
    need(certificate['base_certificate_sha256']==ctx.base_sha and certificate['shared_trace_sha256']==ctx.shared_sha,'Exact replayed base and shared dependencies')
    root=certificate['root'];need(type(root) is int,'Native integer branch or none')
    if branch is None:
        need(root==-1 and certificate['branch_trace_sha256'] is None,'No hidden branch assumption');known=ctx.known
    else:
        raw=branch.read_bytes();trace=json.loads(raw);checked=ctx.check(trace)
        need(not checked['excluded'] and root==trace['root'] and certificate['branch_trace_sha256']==hashlib.sha256(raw).hexdigest(),'Actual post-proof branch dependency')
        known=dict(checked['known_candidate_values'])
    c=certificate['original_class'];D=certificate['denominator']
    need(type(c) is int and c in (0,1) and ctx.caps[c] is not None,'One actual finite original class')
    need(type(D) is int and D>0,'Positive integer capacity')
    V={x for x in range(3704) if ctx.colors[x]==c and x not in known}
    T={x for x,b in known.items() if ctx.colors[x]==c and b!=c}
    loads={x:0 for x in V};W=0;actual_count=0

    def petal(ap):
        nonlocal actual_count
        need(type(ap) is list and len(ap)==2,'Actual AP coordinate pair')
        A=base_verify.actual_ap(*ap);actual_count+=1
        need(all(known[x]==c if x in known else ctx.colors[x]==c for x in A),'Every predecessor is known candidate colour or undecided original colour; no unknown poles or other-class vertices')
        p=A-set(known)
        need(p and p<=V,'Full nonempty independently inherited unknown petal')
        return p

    need(type(certificate['AP_weights']) is list and type(certificate['triple_weights']) is list,'Exact row lists')
    seen=set()
    for row in certificate['AP_weights']:
        need(type(row) is list and len(row)==3 and all(type(v) is int for v in row),'Integer single-AP row')
        a,d,w=row;need(w>0 and (a,d) not in seen,'Distinct positively weighted APs');seen.add((a,d))
        p=petal([a,d]);W+=w
        for x in p:loads[x]+=w
    seen=set()
    for row in certificate['triple_weights']:
        need(type(row) is list and len(row)==2,'Triple-weight row')
        triple,w=row;need(type(triple) is list and len(triple)==3 and type(w) is int and w>0,'Three actual APs and positive integer weight')
        need(all(type(ap) is list and len(ap)==2 and all(type(v) is int for v in ap) for ap in triple),'Native triple coordinates')
        key=tuple(sorted(tuple(ap) for ap in triple));need(len(set(key))==3 and key not in seen,'Three distinct APs and no repeated triple');seen.add(key)
        ps=[petal(ap) for ap in triple];need(not set.intersection(*ps),'No single unknown edit can hit all three APs')
        U=set.union(*ps);W+=2*w
        for x in U:loads[x]+=w
    need(all(load<=D for load in loads.values()),'Exact capacity at EVERY point of the FULL inherited domain')
    residual=ctx.caps[c]-len(T)
    return {'agent':'six-vdw-3','role':'researcher','phase':ctx.phase,'caps':ctx.caps,'root':root,'original_class':c,
            'base_certificate_sha256':ctx.base_sha,'shared_trace_sha256':ctx.shared_sha,'unknown_domain_size':len(V),
            'forced_edits':len(T),'remaining_cap':residual,'denominator':D,'weighted_numerator':W,'strict_gap':W-residual*D,
            'conditional_integer_floor':len(T)+(W+D-1)//D,'excluded':W>residual*D,
            'positive_AP_weights':len(certificate['AP_weights']),'positive_triple_weights':len(certificate['triple_weights']),
            'actual_AP_rows_checked':actual_count,'all_domain_capacities_checked':True,'native_solver_trusted':False,
            'candidate_symmetry_assumed':False,'new_W_bound':False}


def main():
    p=argparse.ArgumentParser();p.add_argument('--base',type=Path,required=True);p.add_argument('--shared',type=Path,required=True)
    p.add_argument('--certificate',type=Path,required=True);p.add_argument('--branch',type=Path);p.add_argument('--output',type=Path)
    a=p.parse_args();out=check(a.base,a.shared,json.loads(a.certificate.read_text()),a.branch)
    if a.output:a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out),flush=True)


if __name__=='__main__':main()
