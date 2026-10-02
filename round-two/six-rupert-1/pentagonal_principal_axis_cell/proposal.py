#!/usr/bin/env python3
"""Floating proposal helpers; exact supports and covering checks are separate."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
import numpy as np
ROOT=Path(__file__).resolve().parents[3]
GEOMETRY=Path(__file__).resolve().parent/'.generated/geometry.json'
PHI=(1.+5.**.5)/2
def quadratic(z):return float(F(z[0]))+PHI*float(F(z[1]))
def cubic(z,x):return sum(quadratic(q)*x**j for j,q in enumerate(z))
def load():
    data=json.loads(GEOMETRY.read_text());root=sum(float(F(q))for q in data['root_interval'])/2
    points=np.array([[cubic(z,root)for z in p]for p in data['exact_original_points']])
    polygon=np.array([[cubic(z,root)for z in p]for p in data['receiver_polygon']])
    facets=np.array([[quadratic(z)for z in w]for w in data['source_facets']])
    vertices=np.array([[quadratic(z)for z in v]for v in data['source_vertices']])
    return points,polygon,None,facets,vertices
def cayley(points,c):
    d=c@c
    return ((1-d)*points+2*(points@c)[:,None]*c+2*np.cross(c,points))/(1+d)
def hull(projected):
    order=sorted(range(len(projected)),key=lambda i:tuple(projected[i]))
    def turn(a,b,c):
        x=projected[b]-projected[a];y=projected[c]-projected[a]
        return x[0]*y[1]-x[1]*y[0]
    lower=[];upper=[]
    for target,sequence in ((lower,order),(upper,order[::-1])):
        for i in sequence:
            while len(target)>=2 and turn(target[-2],target[-1],i)<=1e-12:target.pop()
            target.append(i)
    return lower[:-1]+upper[:-1]
