#!/usr/bin/env python3
"""Fast negative controls for the row checker."""
from __future__ import annotations
import base64,copy,json
from pathlib import Path
import geometry as G
import verify

HERE=Path(__file__).parent


def pack(word):
    b=bytearray((len(word)+3)//4)
    for i,c in enumerate(word):b[i//4]|=c<<(2*(i%4))
    return base64.b64encode(b).decode()


def rejected(row,hp,up,key):
    try:verify.check_row(row,hp,up,key)
    except (ValueError,ArithmeticError):return True
    return False


def main():
    cert=verify.load(HERE/'certificate.json');row=cert['rows'][0]
    h=G.high_generators()[0][2];u=G.augmentation_generators()[0]
    hp,up=G.powers(h,31),G.powers(u,7);key=(0,0,0,2)
    verify.check_row(row,hp,up,key)
    tests={}
    x=copy.deepcopy(row);x[6]+=1;tests['vertex_count']=rejected(x,hp,up,key)
    x=copy.deepcopy(row);x[7]+=1;tests['edge_count']=rejected(x,hp,up,key)
    x=copy.deepcopy(row);x[5]+=1;tests['copy_count']=rejected(x,hp,up,key)
    x=copy.deepcopy(row);x[0]=1;tests['row_key']=rejected(x,hp,up,key)
    x=copy.deepcopy(row);x[8]=x[8][:-4];tests['truncated_word']=rejected(x,hp,up,key)
    colours=list(verify.unpack(row[8],row[6]));trans=G.box(hp,up,0,row[3],2)
    _,edges=G.residue_graph(trans);i,j=edges[0];colours[j]=colours[i]
    x=copy.deepcopy(row);x[8]=pack(colours);tests['monochromatic_edge']=rejected(x,hp,up,key)
    raw=bytearray(base64.b64decode(row[8]));raw[-1]|=0xc0
    x=copy.deepcopy(row);x[8]=base64.b64encode(raw).decode();tests['nonzero_padding']=rejected(x,hp,up,key)
    if not all(tests.values()):raise ValueError(tests)
    print(json.dumps({'controls_passed':True,'rejections':tests},indent=2))


if __name__=='__main__':main()
