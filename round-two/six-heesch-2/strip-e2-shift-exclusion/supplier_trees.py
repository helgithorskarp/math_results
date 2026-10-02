"""Complete finite supplier trees; all demands stay in the original halo."""
import deps
import reader as V
import strip_contact_reader as R
import strip_parametric_geometry as G
from strip_columns import require
from strip_point_suppliers import IDENTITY,finite_suppliers


def freeze_plan(plan):
    return {'point':R.freeze(plan['point']),
            'branches':tuple((R.freeze(g),freeze_plan(n)) for g,n in plan['branches'])}


def build(plan,fixed,guard):
    guard();suppliers=finite_suppliers(plan['point'],fixed)
    require(suppliers['finite'],'Growing height family: no finite proof produced')
    require(set(suppliers['atlas'])=={g for g,n in plan['branches']},'Incomplete declared cap tree')
    return {'point':plan['point'],'suppliers':suppliers,
            'children':[{'candidate':g,'node':build(n,(*fixed,g),guard)} for g,n in plan['branches']]}


def check(record,entry,guard,materialize=True):
    original=R.freeze(record['fixed']);points=R.freeze(record['points'])
    require(record['case']==entry['name'] and original==(IDENTITY,R.freeze(entry['pose']))
            and points==R.freeze(entry['points']),'Tree differs from the literal claim')
    V.universal([G.neg(G.intersection(G.relative(*original))),G.touching(G.relative(*original))],guard)
    count=0;cuts=set()
    def visit(saved,fixed):
        nonlocal count
        guard();count+=1;require(count<=64,'64-node tree guard')
        point=R.freeze(saved['point']);require(point in points,'New or unnamed demand')
        geometry=V.universal([V.in_halo(point,original),
                             *[G.neg(G.point_membership(g,point)) for g in fixed[2:]],
                             *[G.neg(G.intersection(G.relative(g,h)))
                               for j,h in enumerate(fixed) for g in fixed[:j]]],guard)
        suppliers=R.supplier_atlas(point,fixed,guard)
        require(R.freeze(suppliers)==R.freeze(saved['suppliers']),'Changed complete height reduction')
        if materialize:V.material(point,fixed,suppliers,guard)
        children=saved['children'];poses=[R.freeze(c['candidate']) for c in children]
        require(len(poses)==len(set(poses)) and set(poses)==set(suppliers['atlas']),
                'Missing or repeated exhaustive cap branch')
        cuts.update(geometry['cuts']);cuts.update(suppliers['partition']['cuts'])
        for c,g in zip(children,poses):
            V.universal([G.point_membership(g,point)],guard)
            visit(c['node'],(*fixed,g))
    visit(record['tree'],original)
    require(record['complete'],'Incomplete supplier tree')
    return {'case':entry['name'],'tree_nodes':count,'cuts':sorted(cuts),'record_sha256':R.sha(record)}
