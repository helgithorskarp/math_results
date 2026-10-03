"""Independent mathematical damages fail WITHOUT consulting a fixture."""
from pathlib import Path
import core
def check():
    text=Path(core.__file__).read_text()
    changes=[
      ('squared-polar-real-mean','sc(x,-Q(11,2))','sc(x,-Q(6))'),
      ('face-integration-degree9','route1=sc(integrate(mul(pw(f,8-m),pw(g,m))),9)','route1=sc(integrate(mul(pw(f,8-m),pw(g,m))),9); route1=core_omit(route1)'),
      ('Newton-fourth-moment','endpoint=Q(1,10);B[3]=sc(v,Q(1,11));B[4]=sc(pw(v,2),Q(3,32))','endpoint=Q(1,10);B[3]=sc(v,Q(1,11));B[4]=sc(pw(v,2),Q(1,8))'),
      ('retained-square-coefficient','sc(pw(w,2),-Q(976,225))','sc(pw(w,2),-Q(975,225))'),
    ]
    rows=[]
    for name,old,new in changes:
        if text.count(old)!=1:raise ValueError('exact source damage anchor '+name)
        namespace={'__name__':'independent_damage','__file__':core.__file__,'core_omit':lambda p:{ij:v for ij,v in p.items()if ij[0]!=9}}
        exec(compile(text.replace(old,new),core.__file__,'exec'),namespace)
        try:namespace['build']()
        except ValueError as exc:rows.append({'damage':name,'rejected_without_fixture':True,'reason':str(exc)})
        else:raise ValueError('accepted mathematical damage '+name)
    return rows
if __name__=='__main__':
    import json
    print(json.dumps({'status':'PASS','mathematical_damages':check()},sort_keys=True))
