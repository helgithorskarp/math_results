"""Draw the checked positive certificates as deterministic SVG."""
from pathlib import Path
import argparse
import html
import json

from check import TILE,audit,corners,orientations


def outline(shape):
    edges=set()
    for x,y in shape:
        square=((2*x,2*y),(2*x+2,2*y),(2*x+2,2*y+2),(2*x,2*y+2))
        for a,b in zip(square,square[1:]+square[:1]):
            if (b,a) in edges:edges.remove((b,a))
            else:edges.add((a,b))
    links=dict(edges);start=min(links);points=[start];p=links[start]
    while p!=start:
        points.append(p);p=links[p]
    return points


def render(data):
    shapes=orientations();width=1170;height=485;scale=6
    lines=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
           '<rect width="100%" height="100%" fill="white"/>',
           '<g font-family="sans-serif" fill="#172235">']
    for column,w in enumerate(data['witnesses']):
        result=audit(w);poses=w['pose_codes_doubled_translation'];providers={q['copy'] for q in result['providers']}
        xmin=min(2*x+tx for oi,tx,ty in poses for x,y in shapes[oi])
        xmax=max(2*x+tx+2 for oi,tx,ty in poses for x,y in shapes[oi])
        ymin=min(2*y+ty for oi,tx,ty in poses for x,y in shapes[oi])
        ymax=max(2*y+ty+2 for oi,tx,ty in poses for x,y in shapes[oi])
        origin_x=column*390+(390-scale*(xmax-xmin))/2-scale*xmin
        origin_y=100+scale*ymax
        def position(p):return f'{origin_x+scale*p[0]:.1f},{origin_y-scale*p[1]:.1f}'
        name='ABC'[column];vector=result['source_vector']
        lines.append(f'<text x="{column*390+195}" y="28" font-size="20" text-anchor="middle">Packing {name}</text>')
        lines.append(f'<text x="{column*390+195}" y="54" font-size="15" text-anchor="middle">v{name} = {html.escape(str(tuple(vector)))}</text>')
        for j,(oi,tx,ty) in enumerate(poses):
            points=' '.join(position((x+tx,y+ty)) for x,y in outline(shapes[oi]))
            color='#f5ba61' if j==0 else '#87c6a0' if j in providers else '#e5eaf0'
            lines.append(f'<polygon points="{points}" fill="{color}" stroke="#43536a" stroke-width="1.1" stroke-linejoin="round"/>')
        for q in result['providers']:
            for tip,label in zip(q['tips'],q['source_labels']):
                vx,vy=corners(1)[tip][0];a,b=map(float,position((2*vx,2*vy)).split(','))
                lines.append(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="4" fill="#172235"/>')
                lines.append(f'<text x="{a+6:.1f}" y="{b-5:.1f}" font-size="11" paint-order="stroke" stroke="white" stroke-width="2">{label}</text>')
        lines.append(f'<text x="{column*390+195}" y="408" font-size="14" text-anchor="middle">{result["copies"]} copies; area {result["area"]}; disc union</text>')
    lines.append('<text x="585" y="440" font-size="14" text-anchor="middle">Orange: root. Green: all incoming providers. Dot labels: intrinsic provider source index.</text>')
    lines.append('<text x="585" y="468" font-size="17" text-anchor="middle">3 vA + 2 vB + 2 vC = (8,8,8,8,8)</text>')
    lines.extend(['</g>','</svg>'])
    return '\n'.join(lines)+'\n'


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();data=json.loads(Path(__file__).with_name('witnesses.json').read_text())
    a.out.write_text(render(data))


if __name__=='__main__':main()
