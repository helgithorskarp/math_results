#!/usr/bin/env python3
"""Optional committed-frontier provenance and exact parameter-distinctness audit."""
import argparse
import json
from pathlib import Path
import model as M


def transforms(poly):
    x,y=M.sp.symbols('x y');f=M.A.expression(poly,x,y);out=[]
    for reflect in (False,True):
        xx,yy=x,-y if reflect else y
        for _ in range(3):
            p=M.sp.Poly(f.subs({x:xx,y:yy},simultaneous=True).expand(),x,y,domain=M.sp.QQ)
            _,p=p.clear_denoms(convert=True)
            out.append(M.A.geometry.primitive({(i,j):int(c) for (i,j),c in p.terms()}))
            xx,yy=(-xx-3*yy)/2,(xx-yy)/2
    return out


def provenance(residual=None):
    data,polys=M.load_cohort()
    tt={i:transforms(p) for i,p in polys.items()}
    for a,b in data['pairs']:
        M.need(sum({tt[a][g],tt[b][g]}=={polys[a],polys[b]} for g in range(6))==1,'asymmetric equation pair')
    if residual:
        r=json.loads(Path(residual).read_text());M.need(M.digest(r)==data['residual_canonical_sha256'],'pinned residual')
        M.need(r['remaining_pencil_signatures'][data['pencil_index']]==data['pencil'],'pencil provenance')
        _,_,factors,*_=M.A.architecture.build()
        M.need(M.digest(factors)==data['curve_inventory_sha256'],'inventory provenance')
        lookup={p:i for i,p in enumerate(factors)}
        remaining={tuple(row[:2]):row for kind in ('remaining_exact','remaining_six') for row in r[kind]}
        for index,(a,b) in enumerate(data['pairs']):
            M.need(polys[a]==factors[a] and polys[b]==factors[b],'source curve identity')
            canonical=min(tuple(sorted((lookup[tt[a][g]],lookup[tt[b][g]]))) for g in range(6))
            M.need(remaining.get(canonical)==data['canonical_residual_rows'][index],'remaining pair provenance')
    return {'status':'PASS','asymmetric_pairs':64,'pinned_residual_checked':bool(residual)}


def distinctness(charts):
    # Irrational charts use their actual projected coordinate s=x+2*y.
    # Rational charts are canonical constants over q=s. Thus equality of two
    # physical parameters would imply equality of their canonical chart.
    s=M.sp.Symbol('s');keys=set()
    for c in charts:
        pp=lambda k:M.sp.Poly(sum(M.sp.Rational(a)*s**i for i,a in enumerate(c[k])),s,domain=M.sp.QQ)
        q,x,y=map(pp,('q','x','y'))
        M.need(q==M.A.primitive(q,s) and q.is_irreducible,'canonical irreducible field')
        M.need(x.degree()<q.degree() and y.degree()<q.degree(),'reduced coordinate representatives')
        if q.degree()>1:M.need((x+2*y-M.sp.Poly(s,s,domain=M.sp.QQ)).rem(q).is_zero,'separating projected coordinate')
        else:M.need(c['q']==['0','1'],'canonical rational chart')
        key=M.digest({k:c[k] for k in ('q','x','y','real_embeddings')})
        M.need(key not in keys,'distinct full chart');keys.add(key)
    return {'status':'PASS','distinct_charts':len(keys),'distinct_real_parameters':sum(c['real_embeddings'] for c in charts)}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--residual',type=Path);p.add_argument('--full-certificate',type=Path);a=p.parse_args()
    r={'provenance':provenance(a.residual)}
    if a.full_certificate:r['parameters']=distinctness(json.loads(a.full_certificate.read_text())['components'])
    print(json.dumps(r,sort_keys=True,indent=2))
