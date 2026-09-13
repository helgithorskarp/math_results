#!/usr/bin/env python3
"""Small exact controls for the two algebraic routes and physical decoder."""
import json
from pathlib import Path
import algebra as A
import physical
import importlib.util
_spec=importlib.util.spec_from_file_location("hn_c0_verifier",Path(__file__).parent/"verify.py")
V=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(V)


def main():
    x,y,s=A.sp.symbols('x y s')
    # Two points with the same rational x; a linear-fiber-only routine loses them.
    left=((1,0,1),)
    right=((0,0,-1),(0,2,1))
    actual=V.resultant_components(left,right,x,y,s)
    A.need({(tuple(c['x']),tuple(c['y']),n) for c,n in actual}=={(('0',),('-1',),1),(('0',),('1',),1)},'vertical fiber control')
    # Irrational projection and a uniquely determined y.
    left=((0,0,-2),(2,0,1));right=((0,1,1),(1,0,-1))
    actual=V.resultant_components(left,right,x,y,s)
    A.need(len(actual)==1 and actual[0][1]==2 and actual[0][0]['x']==actual[0][0]['y']==['0','1'],'algebraic linear fiber')
    # Only nonreal x: no physical parameter.
    A.need(V.resultant_components(((0,0,1),(2,0,1)),((0,1,1),),x,y,s)==[],'nonreal projection')
    # A resultant caused by simultaneous leading-coefficient loss, with no affine root.
    A.need(V.resultant_components(((0,0,1),(1,1,1)),((0,0,2),(1,1,1)),x,y,s)==[],'spurious resultant factor')
    # Exercise every record shape used by the collision decoder.
    cert=json.loads((Path(__file__).parent/'certificate.json').read_text())
    collapsed=[c for c in cert['components'] if c['point_count']<243]
    A.need(len(collapsed)==3,'collision component records')
    bad_words=0
    for c in collapsed:
        points,labels,edges,triangle=physical.graph(c)
        A.need((len(points),len(edges)) in {(27,63),(84,312)},'known collapsed point count')
        physical.check_word(c['three_colouring'],len(points),edges)
        word=list(c['three_colouring']);a,b=edges[0];word[a]=word[b]
        try:
            physical.check_word(word,len(points),edges)
        except ValueError as e:
            A.need(str(e)=='monochromatic physical unit edge','right rejection')
            bad_words+=1
        else:
            raise ValueError('corrupted colouring accepted')
    A.need(bad_words==3,'all corrupted witnesses rejected')
    # The C0-circle intersection has x=0 or 1/2, independently of the CAS elimination.
    _,_,factors,_,_,_,_,_=A.architecture.build()
    f=A.expression(factors[0],x,y)
    remainder=A.sp.rem(A.sp.Poly(f,y),A.sp.Poly(x*x+3*y*y-1,y)).as_expr().expand()
    A.need(A.sp.expand(remainder-2*x*(2*x-1))==0,'C0 unit-circle identity')
    print(json.dumps({'status':'PASS','algebraic_controls':4,'physical_collision_records':3,'corrupt_colourings_rejected':3,'circle_identity':True},sort_keys=True))


if __name__=='__main__':
    main()
