"""Independent exact obstruction replay: Euler quotient labels, direct CRT colors.

Imports no native/generator search. Full coverage is required for exclusion.
"""
import argparse
import hashlib
import json
import itertools
import math
from pathlib import Path
import struct
import time

MAGIC=b'VDW618H17_1\n'
COUNT=6**6


def labels():
    if not all(103%d for d in range(2,11)): raise ValueError("103 is not prime")
    if not all(pow(5,102//d,103)!=1 for d in [2,3,17]): raise ValueError("5 is not primitive")
    image={pow(5,17*j,103):j for j in range(6)}
    if len(image)!=6: raise ValueError("quotient image is incomplete")
    result=[6]+[image[pow(x,17,103)] for x in range(1,103)]
    if not all(result.count(j)==17 for j in range(6)): raise ValueError("quotient fiber size mismatch")
    return result


def replay(raw):
    if not raw.startswith(MAGIC): raise ValueError('header mismatch')
    if len(raw)!=len(MAGIC)+4*COUNT: raise ValueError('incomplete/extra certificate coverage')
    group=labels()
    checked=0
    for word in range(COUNT):
        a,d=struct.unpack_from('<HH',raw,len(MAGIC)+4*word)
        if not (0<=a<618 and 1<=d<618): raise ValueError('invalid cyclic progression')
        # Reverse a large step to realize an interval progression below2472.
        if d>309: a=(a+6*d)%618; d=618-d
        colors=[]
        for j in range(7):
            t=a+j*d
            if not 0<=t<2472: raise ValueError("invalid interval realization")
            index=group[t%103]
            phase=0 if index==6 else (word//(6**index))%6
            colors.append(int('000111'[(t%6-phase)%6]))
        if len(set(colors))!=1: raise ValueError(f'nonmonochromatic obstruction at word{word}')
        checked+=1
    return {'status':'VERIFIED_H17_PHASE_FAMILY_EXCLUSION','normalized_words_checked':checked,
            'original_words_covered_up_to_crt_translation':6**7,'point_colors_checked':7*checked,
            'q':103,'period':618,'column_phase_subgroup_order':17,
            'interval_realizations_all_below':2472,'target_interval_length':3704,
            'certificate_bytes':len(raw),'certificate_sha256':hashlib.sha256(raw).hexdigest(),
            'scope':'Only H17-invariant CRT column phases; no unrestricted period/interval exclusion.'}


def controls(raw):
    tests=[]
    mutations={'bad_header':b'X'+raw[1:],'missing_word':raw[:-4],'extra_record':raw+b'\0'*4}
    for name,a,d in [('zero_step',0,0),('outside_start',618,6),('nonmonochromatic_pair',0,1)]:
        broken=bytearray(raw)
        struct.pack_into('<HH',broken,len(MAGIC),a,d)
        mutations[name]=bytes(broken)
    for name,broken in mutations.items():
        try: replay(broken)
        except ValueError: tests.append(name)
        else: raise AssertionError('invalid certificate accepted:'+name)
    if len(tests)!=6: raise ValueError("negative-control coverage mismatch")
    return tests


def bridge_controls():
    admitted=[]
    for bits in itertools.product([0,1],repeat=6):
        anti=all(bits[y]!=bits[(y+3)%6] for y in range(6))
        order3=all(len({bits[(y+2*j)%6] for j in range(3)})>1 for y in range(6))
        if anti and order3: admitted.append(''.join(map(str,bits)))
    base='000111'
    rotations=sorted({base[k:]+base[:k] for k in range(6)})
    if sorted(admitted)!=rotations: raise ValueError('six-phase normal form mismatch')
    units=[a for a in range(618) if math.gcd(a,618)==1]
    order17=[a for a in units if a!=1 and pow(a,17,618)==1]
    if len(units)!=204 or len(order17)!=16: raise ValueError('unit-group count mismatch')
    checked=0
    for a in order17:
        if a%6!=1 or pow(a%103,17,103)!=1 or a%103==1:
            raise ValueError('order17 multiplier CRT mismatch')
        geometric=sum(pow(a,j,618) for j in range(17))%618
        for b in range(618):
            identity=geometric*b%618==0
            if identity!=(b%6==0): raise ValueError('order17 affine translation mismatch')
            if not identity: continue
            center=b*pow(1-a,-1,103)%103
            lift=6*(center*pow(6,-1,103)%103)
            if lift%103!=center or lift%6!=0 or (a*lift+b-lift)%618:
                raise ValueError('affine center conjugation mismatch')
            checked+=1
    if checked!=1648: raise ValueError('affine order17 case coverage mismatch')
    return {'six_bit_words_checked':64,'valid_local_phases':rotations,
            'unit_multipliers':len(units),'order17_unit_multipliers':len(order17),
            'order17_affine_maps_conjugated':checked}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('certificate',type=Path)
    ap.add_argument('--output',type=Path)
    ap.add_argument('--controls',action='store_true')
    args=ap.parse_args()
    start=time.monotonic()
    raw=args.certificate.read_bytes()
    result=replay(raw)
    result['bridge_controls']=bridge_controls()
    if args.controls: result['negative_controls_rejected']=controls(raw)
    result['seconds']=time.monotonic()-start
    if args.output: args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__': main()
