from paths import INPUTS, WORK
"""Replay all commuting affine Frobenius images of the positive69 trade."""
import json
from pathlib import Path
import sys
import carrier as C
from quotient import encoded

HERE=Path(__file__).resolve().parent


def main():
    import steiner
    data=json.loads((WORK/'swapped-steiner-one-cap-trades.json').read_text())
    S=set(steiner.code());base=data['positive'][0];subfield=(0,1,6,7)
    field=tuple(subfield[x]^steiner.multiply16(subfield[y],2) for y in range(4) for x in range(4))
    coords={a:i for i,a in enumerate(field)}
    images=set();maps=[]; stabilizer=[]
    for e in range(4):
        for b in range(16):
            q=tuple(coords[steiner.power16(field[v],1<<e)^b] for v in range(16))+(16,17)
            C.require(sorted(q)==list(range(18)) and all(q[C.STANDARD_G[v]]==C.STANDARD_G[q[v]]
                        for v in range(18)),'actual commuting field map')
            C.require({C.image(w,q) for w in S}==S,'field map does not preserve Steiner plane')
            mapped=tuple(sorted(C.image(w,q) for w in base['words']))
            C.check_code(mapped,C.STANDARD_G);images.add(mapped);maps.append(q)
            if mapped==tuple(base['words']):
                stabilizer.append({'frobenius_exponent':e,'field_translation':b,'mapping':q})
    C.require(images=={tuple(r['words']) for r in data['positive']},'field orbit differs from trade family')
    h=next(r for r in stabilizer if r['frobenius_exponent']==2 and r['field_translation']==2)
    C.require(tuple(h['mapping'][h['mapping'][v]] for v in range(18))==C.STANDARD_G,
              'order4 generator square')
    C.require(len(stabilizer)==4,'semiaffine stabilizer size')
    result={'agent':'six-code-2','role':'researcher','status':'COMPLETE_POSITIVE_69_CONSTRUCTION_FAMILY',
            'field_polynomial':'X^4+X+1','actual_maps':len(maps),'distinct_codes':len(images),
            'fixed_cap':base['cap'],'omissions':base['omissions'],'base_words':base['words'],
            'scope':'one10-block Steiner substitution plus cap, under every affine Frobenius map commuting with g',
            'mathematical_new_unrestricted_record':False,'actual_semiaffine_stabilizer':stabilizer,
            'order4_generator':h,'order4_cycle_type':'4^4*1^2','full_automorphism_group_claimed':False}
    (WORK/'swapped-steiner-field-family.json').write_bytes(encoded(result))
    print(json.dumps({k:v for k,v in result.items() if k not in ('base_words','omissions')},sort_keys=True))


if __name__=='__main__':main()
