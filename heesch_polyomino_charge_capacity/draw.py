"""Render the exact compact witness as a standalone SVG."""
from pathlib import Path
import argparse
import json
from oracle import orientations,audit_witness,types


def polygon(shape):
    squares=set(shape);edges={}
    for x,y in squares:
        for neighbor,a,b in [((x,y-1),(x,y),(x+1,y)),((x+1,y),(x+1,y),(x+1,y+1)),
                             ((x,y+1),(x+1,y+1),(x,y+1)),((x-1,y),(x,y+1),(x,y))]:
            if neighbor not in squares:edges[a]=b
    start=min(edges);vertices=[start];point=edges[start]
    while point!=start:vertices.append(point);point=edges[point]
    return vertices


def draw(out):
    data=json.loads((Path(__file__).resolve().parent/'six_charge.json').read_text())
    audit_witness(data);tile=tuple(map(tuple,data['tile']));shapes=orientations(tile)
    raw=data['pose_codes_doubled_translation']
    points=[(x+a/2,y+b/2) for i,a,b in raw for x,y in polygon(shapes[i])]
    xmin=min(x for x,y in points)-1;xmax=max(x for x,y in points)+1
    ymin=min(y for x,y in points)-1;ymax=max(y for x,y in points)+2
    width,height=xmax-xmin,ymax-ymin
    colors=['#7aa8e6','#ffd28a','#9ccf9a','#bea4db','#e8a4ac']
    lines=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{xmin:g} {-ymax:g} {width:g} {height:g}" width="920" height="{round(920*height/width)}">',
           '<title>Seventeen-copy disc packing with six received root charges</title>',
           '<desc>Blue is the root. Copies1 through4 are its incoming providers. All five colored copies lie strictly inside the disc packing. Six red points mark charged root tips. Grey copies complete the neighborhood.</desc>',
           f'<rect x="{xmin:g}" y="{-ymax:g}" width="{width:g}" height="{height:g}" fill="white"/>']
    for index,(i,a,b) in enumerate(raw):
        vertices=[(x+a/2,-y-b/2) for x,y in polygon(shapes[i])]
        path='M '+' L '.join(f'{x:g},{y:g}' for x,y in vertices)+' Z'
        color=colors[index] if index<len(colors) else '#edf0f3'
        lines.append(f'<path d="{path}" fill="{color}" stroke="#374151" stroke-width="0.055" stroke-linejoin="round"/>')
        if index<5:
            cx=sum(x+.5 for x,y in shapes[i])/17+a/2;cy=-(sum(y+.5 for x,y in shapes[i])/17+b/2)
            lines.append(f'<text x="{cx:g}" y="{cy:g}" fill="#111827" font-size="0.72" font-family="sans-serif" text-anchor="middle" dominant-baseline="middle">{index}</text>')
    tips=types(tile,1)
    for index in data['expected_received_tips']:
        (x,y),q=tips[index]
        lines.append(f'<circle cx="{x}" cy="{-y}" r="0.15" fill="#b91c1c" stroke="white" stroke-width="0.035"/>')
    lines.append(f'<text x="{xmin+.3:g}" y="{-ymax+.8:g}" fill="#111827" font-size="0.62" font-family="sans-serif">Blue root: six charged tips. Colored providers1-4. Seventeen copies.</text>')
    lines.append('</svg>');out.write_text('\n'.join(lines)+'\n')


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    draw(parser.parse_args().out)
