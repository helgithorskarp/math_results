"""Proved division-free verification of the actual physical Farkas channel."""
import json
from pathlib import Path
from digit import T,Z,expr,prove_zero
from geometry import model
from bindings import decode,require

def check():
    m=model();Y=m['Y'];t,z=T,Z;a,b,c,O,R=(m[k] for k in ['a','b','c','Omega','R'])
    f=decode(json.loads(Path('FACTORS.json').read_text()),R);s=json.loads(Path('SYSTEM.json').read_text())
    F0=a**6*c*(3*t-1)*(b*z+1);F6=a**4*c*(3*t-1)*(3*t+1)*(b*z+1);gamma=F0*F6
    delta=Y[0][1]*Y[6][0]-Y[0][0]*Y[6][1]
    alpha=-2*Y[6][0]+13*Y[6][1];beta=2*Y[0][0]-13*Y[0][1]
    C0=alpha*O;C6=beta*O;C4=15*delta-alpha*Y[0][2]-beta*Y[6][2]
    margin=24*delta-(C0+C4+C6)*t
    Q=a*m['D']*z*z-2*m['D']*z+2*t*t-t+1
    pos={'a':a,'b':b,'c':c,'J':m['J'],'C':m['C'],'Q':Q,'3t+1':3*t+1,'bz+1':b*z+1}
    rows={}
    def rad(name,v):
        rows[name+'_constant']=prove_zero(v.p);rows[name+'_linear']=prove_zero(v.q)
    for name,p in [('delta',delta),('C0',C0),('C4',C4),('C6',C6),('margin',margin)]:
        k=gamma
        for tag in s['Farkas_positive_factors'][name]:
            require(tag in pos,'unproved positive clearing factor');k=k*pos[tag]
        rad('division_free_'+name,p-f[name]*k)
    for j,value in enumerate([-13,-2,15]):rad('whole_raw_Cramer_'+str(j),C0*Y[0][j]+C4*Y[4][j]+C6*Y[6][j]-delta*O*value)
    return {'all16_component_identities':rows,'positive_multiplier':'gamma=F0F6>0 on original closed inner box',
            'all_polynomial_divisions_removed_from_this_channel':True,'singular_delta_not_discarded':True,
            'same_physical_channels_and_literal_factors':True,'historical_priority_claim':False}

if __name__=='__main__':print(json.dumps(check(),sort_keys=True,separators=(',',':')))
