#!/usr/bin/env python3
"""Small arithmetic controls and corrupt-certificate rejection on the frozen graph."""
import copy,json
import verify as V


def run():
    for i,r in enumerate(V.RAD):
        a=tuple(int(j==i) for j in range(8))
        V.need(V.radical(a,r)==(r,0,0,0,0,0,0,0),'radicand square')
    V.need(119**2+9*247==128**2,'exact spindle rotation norm')
    p=(V.ZERO,V.ZERO);q=((V.SCALE,0,0,0,0,0,0,0),V.ZERO)
    V.need(V.normdiff(p,q)==(V.SCALE**2,0,0,0,0,0,0,0),'horizontal unit pair')
    q=(V.ZERO,(0,V.SCALE//3,0,0,0,0,0,0))
    V.need(V.normdiff(p,q)==(V.SCALE**2//3,0,0,0,0,0,0,0),'short marked distance')
    cert=json.loads((V.HERE/'certificate.json').read_text());geom=V.geometry();V.verify(cert,geom)
    badword=cert['union_colour_word'].copy();i,j=geom[4][0];badword[j]=badword[i]
    cmap=cert['complement_to_union'].copy();cmap[3]=cmap[0]
    changes=[('union_colour_word',badword),('pins',[0,0,0]),('union_edges',cert['union_edges']-1),
             ('overlap_count',3),('extra_cross_edges',cert['extra_cross_edges'][:-1]),
             ('outside_native_field_indices',[]),('complement_to_union',cmap),
             ('union_point_sha256','0'*64),('record_candidate',True)]
    for k,v in changes:
        bad=copy.deepcopy(cert);bad[k]=v
        try:V.verify(bad,geom)
        except ValueError:pass
        else:raise ValueError('accepted corruption '+k)
    return {'status':'PASS','radicand_square_controls':8,'geometry_identity_controls':3,'corruptions_rejected':len(changes)}


if __name__=='__main__':print(json.dumps(run(),sort_keys=True,indent=2))
