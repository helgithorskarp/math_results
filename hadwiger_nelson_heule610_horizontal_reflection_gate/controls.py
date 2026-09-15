#!/usr/bin/env python3
"""Compare orbit accounting with every Boolean map on small exact fixtures."""
from itertools import product
import json
from verify import count_orbits,reflect,require

def point(x,y):return (x,)+(0,)*7+(y,)+(0,)*7

def main():
    fixtures=[[],[point(0,0)],[point(0,1)],
              [point(0,1),point(0,-1)],
              [point(0,1),point(0,-1),point(2,0)],
              [point(0,1),point(0,-1),point(2,1),point(2,-1),point(3,0)],
              [point(0,1),point(1,1),point(2,1),point(3,1)]]
    assignments=0
    for pts in fixtures:
        actual=len(pts)
        for bits in product((0,1),repeat=len(pts)):
            image={reflect(p) if bit else p for p,bit in zip(pts,bits)}
            actual=min(actual,len(image));assignments+=1
        claimed,_,_=count_orbits(pts)
        require(actual==claimed,'exhaustive toy image minimum')
        require(all(reflect(reflect(p))==p for p in pts),'involution')
    rejected=0
    try:count_orbits([point(0,1),point(0,1)])
    except ValueError:rejected+=1
    require(rejected==1,'duplicate rejection')
    print(json.dumps({'all_checks':True,'fixtures':len(fixtures),'pointwise_maps_checked':assignments,'invalid_inputs_rejected':rejected},sort_keys=True))

if __name__=='__main__':main()
