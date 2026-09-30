"""Directed D4 images of the certified pair library, at unit scale."""
from corners import cells,footprint,image_cell,normalize,variants


def pattern_classes(data):
    tile=normalize(data['tile']);shapes=variants(tile);result=set()
    for orientation,x,y in data['forbidden_poses']:
        copies=[set(tile),footprint(shapes[orientation],(x,y))]
        for swap in (False,True):
            for sx in (-1,1):
                for sy in (-1,1):
                    images=[[image_cell(p,swap,sx,sy) for p in copy] for copy in copies]
                    origins=[(min(a for a,b in image),min(b for a,b in image)) for image in images]
                    a,b=map(normalize,images)
                    dx=origins[1][0]-origins[0][0];dy=origins[1][1]-origins[0][1]
                    result.add((a,b,dx,dy));result.add((b,a,-dx,-dy))
    return tuple(sorted(result))


def find_forbidden(copies,classes):
    lookup={(cells(shape),translation[0],translation[1]):i for i,(shape,translation) in enumerate(copies)}
    result=set()
    for shape,x,y in lookup:
        for a,b,dx,dy in classes:
            if shape!=a:continue
            other=(b,x+dx,y+dy)
            if other in lookup:
                result.add(tuple(sorted((lookup[(shape,x,y)],lookup[other]))))
    return sorted(result)
