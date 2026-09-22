"""Exact certificate checker; no imported hull code, floating point, or solver."""
from copy import deepcopy
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def dot(x, y):
    return sum((a*b for a,b in zip(x,y)), F(0))


def transpose(a):
    return list(map(list, zip(*a)))


def multiply(a, b):
    return [[dot(row, col) for col in transpose(b)] for row in a]


def cross(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


def input_corners(widths, positive):
    choices = (0,1) if positive else (-1,1)
    return sorted({tuple(a*s for a,s in zip(w, signs))
                   for w in widths for signs in product(choices,repeat=len(w))})


def image_points(matrix, corners):
    return sorted({tuple(dot(row,x) for row in matrix) for x in corners})


def certify_polygon(points, polygon, area):
    """Every listed vertex is a generator; every generator satisfies every facet."""
    require(len(polygon)>=3 and len(set(polygon))==len(polygon), "invalid polygon vertices")
    require(all(v in points for v in polygon), "polygon vertex is not an image generator")
    slacks=[]
    for a,b in zip(polygon,polygon[1:]+polygon[:1]):
        row=[cross(a,b,x) for x in points]
        require(min(row)>=0 and max(row)>0, "failed supporting edge")
        slacks.extend(row)
    shoelace=sum(a[0]*b[1]-a[1]*b[0] for a,b in zip(polygon,polygon[1:]+polygon[:1]))/2
    require(shoelace==area and area>0, "wrong oriented area")
    return len(slacks)


def section_area(points):
    """Area of conv(points) from vertical slices, without using polygon data.

An extremum in a section is a convex combination of at most two generators.
The upper/lower boundaries are linear between consecutive generator x-values,
because every hull vertex is a generator. Integrate their difference exactly.
"""
    xs=sorted({p[0] for p in points})
    heights=[]
    for x in xs:
        levels=[p[1] for p in points if p[0]==x]
        for a,b in combinations(points,2):
            if a[0]>b[0]:
                a,b=b,a
            if a[0]<b[0] and a[0]<=x<=b[0]:
                levels.append(a[1]+(b[1]-a[1])*(x-a[0])/(b[0]-a[0]))
        require(bool(levels), "empty section")
        heights.append(max(levels)-min(levels))
    area=sum((xs[i+1]-xs[i])*(heights[i]+heights[i+1])/2
             for i in range(len(xs)-1))
    return area,len(xs)-1


def check(w, strict=True):
    a=[list(map(F,row)) for row in w["matrix"]]
    widths=[list(map(F,row)) for row in w["box_halfwidths"]]
    require(len(a)==2 and all(len(row)==4 for row in a), "matrix dimensions")
    require(widths and all(len(row)==4 and min(row)>=0 for row in widths), "bad boxes")
    require(any(min(row)>0 for row in widths), "missing full-dimensional box")
    gram=multiply(a,transpose(a))
    det=gram[0][0]*gram[1][1]-gram[0][1]*gram[1][0]
    require(det>0, "map rank below two")
    inv=[[gram[1][1]/det,-gram[0][1]/det],
         [-gram[1][0]/det,gram[0][0]/det]]
    projection=multiply(multiply(transpose(a),inv),a)
    supplied=[[F(x,w["projection_denominator"]) for x in row]
              for row in w["projection_numerator"]]
    require(projection==supplied, "wrong projection matrix")
    require(multiply(projection,projection)==projection and transpose(projection)==projection,
            "not an orthogonal projection")
    require(sum(projection[i][i] for i in range(4))==2, "projection rank")
    areas=[];counts=[]
    for positive,key,area_key in [(False,"full_hull","full_area"),
                                 (True,"positive_hull","positive_area")]:
        corners=input_corners(widths,positive)
        points=image_points(a,corners)
        polygon=[tuple(map(F,p)) for p in w[key]]
        area=F(w[area_key])
        tests=certify_polygon(points,polygon,area)
        sliced,slabs=section_area(points)
        require(sliced==area, "independent section area mismatch")
        areas.append(area)
        counts.append(dict(input_corners=len(corners),image_generators=len(points),
                           polygon_vertices=len(polygon),facet_tests=tests,vertical_slabs=slabs))
    if strict:
        require(areas[0]>4*areas[1], "no strict counterexample")
    return dict(gram=[[str(x) for x in row] for row in gram],gram_determinant=str(det),
                full_area=str(areas[0]),positive_area=str(areas[1]),
                area_ratio=str(areas[0]/areas[1]),normalized_ratio=str(areas[0]/(4*areas[1])),
                excess=str(areas[0]-4*areas[1]),certificates=counts)


def family(w):
    """Endpoint certificates cover every real t in [17/6,3]; see PROOF.md."""
    records=[]
    data=[]
    for t in (F(17,6),F(3)):
        v=deepcopy(w)
        v["box_halfwidths"][1][1]=t
        # The only moving boundary vertices are opposite rectangle corners.
        v["full_hull"]=[[-5,-5],[-3,-9],[2,-2*t],[3,-5],[5,1],
                        [5,5],[3,9],[-2,2*t],[-3,5],[-5,-1]]
        v["full_area"]=86+12*t
        r=check(v,strict=t>F(17,6))
        records.append(dict(t=str(t),**r))
        data.append(v)
    # All input-corner and proposed-hull x-coordinates are t-independent.
    for positive in (False,True):
        # Preserve original generator labels, since sorting can change with t.
        labelled=[]
        for v in data:
            labelled.append([tuple(dot(row,tuple(F(ai)*si for ai,si in zip(width,signs)))
                                   for row in v["matrix"])
                             for width in v["box_halfwidths"]
                             for signs in product((0,1) if positive else (-1,1),repeat=4)])
        require([p[0] for p in labelled[0]]==[p[0] for p in labelled[1]],
                "moving x-coordinate invalidates affine endpoint certificate")
    require([p[0] for p in data[0]["full_hull"]]==[p[0] for p in data[1]["full_hull"]],
            "hull x-coordinate is not fixed")
    return records


def negative_controls(w):
    corruptions=[]
    x=deepcopy(w);x["full_area"]-=1;corruptions.append(("wrong area",x))
    x=deepcopy(w);del x["full_hull"][2];corruptions.append(("missing protruding corner",x))
    x=deepcopy(w);x["positive_hull"][0][0]-=1;corruptions.append(("invented positive vertex",x))
    x=deepcopy(w);x["projection_numerator"][0][0]+=1;corruptions.append(("wrong projection",x))
    x=deepcopy(w);x["box_halfwidths"][0]=[0]*4;corruptions.append(("missing interior box",x))
    x=deepcopy(w);x["matrix"][1]=x["matrix"][0][:];corruptions.append(("rank-one map",x))
    for name,x in corruptions:
        try:
            check(x)
        except ValueError:
            continue
        raise ValueError("accepted corruption: "+name)
    return [name for name,_ in corruptions]


def smooth_certificate():
    # Explicit k=1000 support smoothing; no transcendental approximation.
    k=1000
    require(501**k>3*500**k, "Bernoulli power bound")
    dilation_squared_upper=F(501,500)*F(251,250)**2
    ratio_lower=F(61,60)/dilation_squared_upper
    require(ratio_lower>1, "smooth violation margin")
    return dict(k=k,firey_exponent=2*k,ellipsoid_epsilon=str(F(1,k*k)),
                dilation_squared_upper=str(dilation_squared_upper),
                normalized_ratio_strict_lower=str(ratio_lower))


def main():
    w=json.loads((Path(__file__).parent/"WITNESS.json").read_text())
    r=check(w)
    # Known positive-control body: deleting the added rectangle gives equality.
    control=deepcopy(w)
    del control["box_halfwidths"][1]
    control["full_hull"]=[[-5,-5],[-3,-9],[3,-5],[5,1],[5,5],[3,9],[-3,5],[-5,-1]]
    control["full_area"]=120
    require(check(control,strict=False)["normalized_ratio"]=="1", "base equality control")
    out=dict(status="VERIFIED_UNCONDITIONAL_ORTHANT_COUNTEREXAMPLE",witness=r,
             parameter_family=family(w),smooth=smooth_certificate(),
             rejected_corruptions=negative_controls(w),
             base_without_rectangle_ratio="1",
             scope="Exact finite witness and endpoint/smoothing certificates; product theorem is analytic.")
    print(json.dumps(out,sort_keys=True,indent=2))


if __name__=="__main__":
    main()
