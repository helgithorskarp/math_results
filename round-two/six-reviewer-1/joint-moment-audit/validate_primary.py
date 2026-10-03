"""Whole typed primary fixture + build-only semantic rejection controls."""
import json,hashlib,copy
from pathlib import Path
from core import run


def same(a,b):
    if type(a) is not type(b):return False
    if isinstance(a,dict):return a.keys()==b.keys() and all(same(a[k],b[k]) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
    return a==b


def main():
    root=Path(__file__).resolve().parent
    computed=run();expected=json.loads((root/'EXPECTED.json').read_text())
    if not same(computed,expected):raise ValueError('entire typed independent record mismatch')
    damages=[]
    for name in ['pivot','drop-fifth','matrix','moment','boundary']:
        try:run(name)
        except ValueError:damages.append(name)
        else:raise ValueError('math build damage survived: '+name)
    fixture=[]
    for name in ['missing','extra','integer-to-bool','last-coefficient','missing-fifth-row','boundary-constant']:
        bad=copy.deepcopy(expected)
        if name=='missing':bad.pop('matrix')
        if name=='extra':bad['extra']=None
        if name=='integer-to-bool':bad['schema']=True
        if name=='last-coefficient':bad['P'][-1][-1][1]+=1
        if name=='missing-fifth-row':bad['matrix'].pop()
        if name=='boundary-constant':bad['boundary_minor_gcd']['gcd'][0]='10/56'
        if same(computed,bad):raise ValueError('typed fixture damage survived '+name)
        fixture.append(name)
    data=json.dumps(computed,sort_keys=True,separators=(',',':')).encode()
    return {'status':'PASS','agent':'six-reviewer-1','record_sha256':hashlib.sha256(data).hexdigest(),'whole_identities':len(computed['whole_identities']),'all5_rows':True,'all10_minors':True,'math_build_only_rejections':damages,'whole_typed_fixture_rejections':fixture,'boundary_common_zeros':[['-3/8','0','-224/9'],['-3/7','0','0']], 'trust':'No newest producer module or fixture; OWN68bf078a arithmetic explicitly reused; displayed formulas exposed, not blind.'}

if __name__=='__main__':print(json.dumps(main(),sort_keys=True))
