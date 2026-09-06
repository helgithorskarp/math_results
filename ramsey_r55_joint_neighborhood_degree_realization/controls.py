"""Malformed-certificate controls, including degree- and density-preserving edits."""
import argparse
import copy
import itertools as it
import json
from pathlib import Path
import check
from generate import parse_status

HERE=Path(__file__).resolve().parent

def rejected(H,G):
    try:check.audit(H,G,92,full=False)
    except ValueError as exc:return str(exc)
    raise ValueError('malformed certificate accepted')

def main():
    p=argparse.ArgumentParser();p.add_argument('--report',type=Path,required=True);a=p.parse_args()
    H=json.loads((HERE/'H92.json').read_text());G=json.loads((HERE/'G92.json').read_text())
    bad=[]
    for name,edit in (
        ('order',lambda g:g.update(n=42)),
        ('boolean_order',lambda g:g.update(n=True)),
        ('extra_field',lambda g:g.update(extra=1)),
        ('duplicate',lambda g:g['red_edges'].append(g['red_edges'][0])),
        ('reversed_pair',lambda g:g['red_edges'].__setitem__(0,list(reversed(g['red_edges'][0])))),
        ('loop',lambda g:g['red_edges'].__setitem__(0,[0,0])),
        ('out_of_range',lambda g:g['red_edges'].__setitem__(0,[0,43])),
        ('boolean_vertex',lambda g:g['red_edges'].__setitem__(0,[False,10])),
        ('delete_free_edge',lambda g:g['red_edges'].remove(next(e for e in g['red_edges'] if e[0]>=20 and e[1]<29))),
        ('delete_H_edge',lambda g:g['red_edges'].remove([0,10])),
    ):
        g=copy.deepcopy(G);edit(g);bad.append(dict(name=name,rejection=rejected(H,g)))
    red=check.parse(G,43);blue=set(it.combinations(range(43),2))-red
    # Switch only edges inside X: all root contacts and the entire H remain fixed.
    # All four degrees and BOTH Q edge totals are unchanged.
    found={}
    for vs in it.combinations(range(20,29),4):
        matchings=[{tuple(sorted((vs[a],vs[b]))),tuple(sorted((vs[c],vs[d])))}
                   for a,b,c,d in ((0,1,2,3),(0,2,1,3),(0,3,1,2))]
        for removed in matchings:
            if not removed<=red:continue
            for added in matchings:
                if not added<=blue:continue
                rr=(red-removed)|added
                g={'n':43,'red_edges':[list(e) for e in sorted(rr)]}
                q=[v for v in range(43) if v!=0 and tuple(sorted((0,v))) not in rr]
                for color,k,es in (('red_K5',5,rr),('blue_K4',4,set(it.combinations(range(43),2))-rr)):
                    qe=check.subedges(q,es)
                    masks=sorted(check.bit_cliques(check.bit_rows(q,qe),sum(1<<v for v in q),k))
                    if masks and color not in found:
                        reason=rejected(H,g);check.need(reason=='Q Ramsey conditions','balanced corruption rejection stage')
                        found[color]=dict(removed=sorted(removed),added=sorted(added),rejection=reason,
                                          forbidden_vertices=[v for v in q if masks[0]&(1<<v)],
                                          unchanged='all43 degrees, H, root contacts, both Q edge totals')
        if len(found)==2:break
    check.need(len(found)==2,'both balanced corruption colors')
    invalid=[(10,''),(10,'s UNKNOWN\n'),(0,'s SATISFIABLE\n'),(20,'s SATISFIABLE\n'),
             (10,'s SATISFIABLE\ns SATISFIABLE\n'),(1,'s UNKNOWN\n'),(10,'s SATISFIABLE trailing\n')]
    for code,out in invalid:
        try:parse_status(code,out)
        except ValueError:pass
        else:raise ValueError('malformed status accepted')
    for code,status in ((0,'UNKNOWN'),(10,'SATISFIABLE'),(20,'UNSATISFIABLE')):
        parse_status(code,f'c ignored\ns {status}\n')
    report=dict(malformed_graphs=bad,balanced_corruptions=found,malformed_statuses_rejected=len(invalid),
                valid_status_controls=3,scope='author checker controls, not peer review')
    with a.report.open('x') as f:json.dump(report,f,sort_keys=True,indent=2);f.write('\n')
    print(json.dumps(report),flush=True)

if __name__=='__main__':main()
