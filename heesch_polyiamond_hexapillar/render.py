"""Compact vector illustrations; decimal display only, never proof evidence."""
import json
import math
from pathlib import Path
from check import mesh,cell

BASE=Path(__file__).resolve().parent


def screen(p):
    return math.sqrt(3)*(p[0]+p[1])/2,(p[0]-p[1])/2


def svg(bounds,content,title):
    lo_x,hi_x,lo_y,hi_y=bounds;pad=0.7
    width=1200;scale=width/(hi_x-lo_x+2*pad)
    height=math.ceil(scale*(hi_y-lo_y+2*pad))
    x=-scale*(lo_x-pad);y=-scale*(lo_y-pad)
    return ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'viewBox="0 0 %d %d" width="%d" height="%d">\n'
            '<title>%s</title>\n<rect width="%d" height="%d" fill="white"/>\n'
            '<g transform="matrix(%.9f 0 0 %.9f %.9f %.9f)">%s</g>\n</svg>\n')%(
                width,height,width,height,title,width,height,scale,scale,x,y,content)


def limits(vertices):
    pts=[screen(p) for p in vertices]
    return min(x for x,y in pts),max(x for x,y in pts),min(y for x,y in pts),max(y for x,y in pts)


def main():
    tile={cell(t) for t in json.loads((BASE/'tile.json').read_text())['triangles']}
    _,vs,polygon=mesh(tile)
    outline='M '+' L '.join('%d,%d'%p for p in polygon)+' Z'
    transform='matrix(%.12f .5 %.12f -.5 0 0)'%(math.sqrt(3)/2,math.sqrt(3)/2)
    fine=[]
    for t in sorted(tile):fine.append('<path d="M %s Z"/>'%' L '.join('%d,%d'%p for p in t))
    body=('<g transform="%s"><g fill="#edf5f0" stroke="#a1afa5" stroke-width=".025">%s</g>'
          '<path d="%s" fill="none" stroke="#163b27" stroke-width=".09"/></g>')%(transform,''.join(fine),outline)
    (BASE/'tile.svg').write_text(svg(limits(vs),body,'The215-cell polyiamond; geometric unit triangles'))
    placements=json.loads((BASE/'coronas.json').read_text())['placements']
    colors=['#202a44','#4798ca','#e8bd46','#72b09a','#a391bc','#e8a26c']
    uses=[];all_vertices=set()
    for p in placements:
        a,b,c,d=p['matrix'];x,y=p['translation'];k=p['level']
        all_vertices.update((a*u+b*v+x,c*u+d*v+y) for u,v in vs)
        uses.append('<use xlink:href="#tile" transform="matrix(%d %d %d %d %d %d)" fill="%s"/>'%(a,c,b,d,x,y,colors[k]))
    body='<defs><path id="tile" d="%s"/></defs><g transform="%s" stroke="#263344" stroke-width=".035">%s</g>'%(outline,transform,''.join(uses))
    (BASE/'five_coronas.svg').write_text(svg(limits(all_vertices),body,'Five complete disc coronas; reproduction of the hexapillar fixture'))


if __name__=='__main__':main()
