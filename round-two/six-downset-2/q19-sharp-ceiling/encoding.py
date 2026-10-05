"""Self-contained exact unrestricted invariant entry/lower-PSD encoding.

Own published defining model is reused explicitly, not its old factors.
Soundness/completeness and all-real averaging are ordinary proof obligations.
"""
from binding import check_current
check_current()
from pathlib import Path
from fractions import Fraction as F
import hashlib
import importlib
import sys

PARENT=Path(__file__).resolve().parent
PINS={'model.py':'49dfed65ae8cd910009de7747e990c18e9f98761d72cb536dd9ec21928a54b8d',
      'physical.py':'1dccabf17fdb51ea24ed2cdb2bed690988a06227fb3ea6f981d24330711b9ad9',
      'COEFFICIENTS.json':'65f2b0a5170e0a7585d4892c33d72aca7e4479d0e3484dc98ee32b0ad27f1105'}
for name,pin in PINS.items():
    if hashlib.sha256((PARENT/name).read_bytes()).hexdigest()!=pin:
        raise ValueError('Entire explicitly reused defining parent source: '+name)
sys.path.insert(0,str(PARENT))
model=importlib.import_module('model')
physical=importlib.import_module('physical')


def comparison():
    return model.comparison(model.coefficient_input(PARENT/'COEFFICIENTS.json'),9,10)


def scalar_rows(table):
    b=model.type_budgets(table,9,10)
    rows={('proper',)+pair:1+a for pair,a in table.items()}
    nn=[t for t in b['types'] if not t[0]&1]
    stars=[t for t in b['types'] if t[0]&1]
    for t in nn:
        val=F(b['s'])
        for u in stars:
            number=0 if t[0]&u[0] else model.choose(9-t[1],u[1])*model.choose(10-t[2],u[2])
            if number:val-=number*(1+table[tuple(sorted((t,u)))])
        rows[('anchor',t)]=val
    for t in b['types']:rows[('empty',t)]=b['ell'][t]
    rows[('empty_anchor',)]=b['anchor'];rows[('loop',)]=b['loop']
    model.require(len(rows)==180,'all original entry types of unrestricted invariant family')
    return rows


def classify(base):
    b=model.type_budgets(base,9,10);K=set(b['bad_nn'])
    parts={'KK':[],'KG':[],'GG':[],'star':[]}
    for pair in sorted(base):
        t,u=pair
        tag='star' if t[0]&1 or u[0]&1 else 'KK' if t in K and u in K else 'KG' if t in K or u in K else 'GG'
        parts[tag].append(pair)
    return parts,b


def affines():
    base=comparison();keys=sorted(base);row0=scalar_rows(base)
    forms0={k:v for k,v in model.sector_forms(base,9,10).items() if k.endswith('lower')}
    rowdir={r:[] for r in row0};formdir={r:[] for r in forms0}
    for pair in keys:
        unit=base.copy();unit[pair]+=1
        rows=scalar_rows(unit);forms=model.sector_forms(unit,9,10)
        model.require(set(rows)==set(row0),'whole scalar row set at every independent generator')
        for key in rows:rowdir[key].append(rows[key]-row0[key])
        for tag,b in forms0.items():
            formdir[tag].append([[forms[tag]['matrix'][i][j]-b['matrix'][i][j]
                                 for j in range(len(b['types']))] for i in range(len(b['types']))])
    parts,b=classify(base)
    eqkeys=[('empty',t) for t in b['bad_nn']]+[('loop',)]
    return dict(base=base,keys=keys,parts=parts,budgets=b,row0=row0,rowdir=rowdir,
                forms0=forms0,formdir=formdir,eqkeys=eqkeys)


def schur_forms(table):
    """Eliminate the fixed positive star principal blocks EXACTLY."""
    s=61;forms=model.sector_forms(table,9,10);out={}
    for tag in ('trivial_lower','X_standard_lower','Y_standard_lower'):
        form=forms[tag];types=form['types'];A=form['matrix'];w=form['metric']
        st=[i for i,t in enumerate(types) if t[0]&1]
        nn=[i for i,t in enumerate(types) if not t[0]&1]
        if tag=='trivial_lower':
            inverse=[[F(int(i==j),s*w[st[i]])+F(1,s) for j in range(len(st))] for i in range(len(st))]
        else:
            inverse=[[F(int(i==j),s*w[st[i]]) for j in range(len(st))] for i in range(len(st))]
        model.require(all(sum(A[st[i]][st[a]]*inverse[a][j] for a in range(len(st)))==int(i==j)
                          and sum(inverse[i][a]*A[st[a]][st[j]] for a in range(len(st)))==int(i==j)
                          for i in range(len(st)) for j in range(len(st))),
                      'both full fixed-star physical inverse products: '+tag)
        Q=[[A[i][j]-sum(A[i][st[a]]*inverse[a][b]*A[st[b]][j]
                            for a in range(len(st)) for b in range(len(st))) for j in nn] for i in nn]
        model.require(all(Q[i][j]==Q[j][i] for i in range(len(nn)) for j in range(len(nn))),
                      'entire physical Schur symmetry')
        out[tag]=dict(types=[types[i] for i in nn],metric=[w[i] for i in nn],matrix=Q,
                      eliminated_star_dimensions=len(st),fixed_star_inverse=inverse)
    for tag,form in forms.items():
        if tag.endswith('lower') and tag not in out:out[tag]=form
    model.require([len(out[t]['types']) for t in ('trivial_lower','X_standard_lower','Y_standard_lower')]==[13,5,6],
                  'full nonstar physical Schur block dimensions')
    return out
