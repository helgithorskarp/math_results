"""Exact adverse controls for the new auxiliary-point reduction.

The large unsupported radius must fail a strict transfer margin. A literal
two-sphere-point example shows why inserting a nearby point without relaxing
its inner-product bound is invalid. Neither control is a fifteen-point code.
"""
from pathlib import Path
from fractions import Fraction as Q
import importlib.util,json

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('stability_checker',HERE/'check.py')
C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)

def main():
    config,epsilon=C.read_config()
    rejected=False;message=None
    try:C.verify(config,Q(1,1000))
    except ValueError as e:
        message=str(e);rejected=message.startswith('strict relaxed label-zero Bernstein margin')
    if not rejected:raise ValueError('unsupported radius was not rejected at its transfer margin')
    t=Q(593,1000);h=Q(1,100000);q=Q(25273147,50000000)
    x=(Q(1),Q(0),Q(0))
    p=((1-h*h)/(1+h*h),2*h/(1+h*h),Q(0))
    y=((1-q*q)/(1+q*q),2*q/(1+q*q),Q(0))
    def dot(a,b):return sum(a*b for a,b in zip(a,b))
    if any(dot(z,z)!=1 for z in (x,p,y)):raise ValueError('literal sphere controls')
    distance_squared=sum((a-b)**2 for a,b in zip(x,p))
    if not distance_squared<=epsilon**2 or not dot(x,y)<=t<dot(p,y):
        raise ValueError('unrelaxed auxiliary replacement must fail this control')
    if not dot(p,y)<=t+epsilon:raise ValueError('correct Cauchy--Schwarz relaxation')
    result={'agent':'six-tammes-2','role':'researcher',
            'status':'EXACT_ADVERSE_STABILITY_CONTROLS_PASS',
            'unsupported_radius':'1/1000','unsupported_radius_rejected':True,
            'rejection':message,'literal_unit_vectors':3,
            'nearby_point_distance_squared':str(distance_squared),
            'original_pair_inner_product':str(dot(x,y)),
            'unrelaxed_auxiliary_inner_product':str(dot(p,y)),
            'required_relaxation_positive':True,'correct_relaxed_bound_holds':True,
            'scope':'Adverse controls for the new radius/bridge; not independent mathematical review or a fifteen-point construction.'}
    expected_path=HERE/'CONTROLS_EXPECTED.json'
    if expected_path.exists() and result!=json.loads(expected_path.read_text()):
        raise ValueError('complete adverse-control receipt differs')
    return result

if __name__=='__main__':print(json.dumps(main(),indent=2,sort_keys=True))
