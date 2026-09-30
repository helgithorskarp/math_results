#!/usr/bin/env python3
"""Targeted rejection controls for coverage, AP semantics and erasure cuts."""
import copy
import json
from pathlib import Path
import struct
import tempfile

from check import (HEADER, RECORD, implications, load_binary, load_supplement,
                   opposed, qr, verify)


def run(first, second, stars, supplement, workdir):
    rejected = []
    def rejects(name, function):
        try:
            function()
        except (ValueError, KeyError, TypeError, StopIteration):
            rejected.append(name)
        else:
            raise ValueError('corruption accepted: '+name)
    workdir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='controls-', dir=workdir) as temp:
        temp = Path(temp)
        a, b = first.read_bytes(), second.read_bytes()
        def binary(name, data, magic):
            p = temp/(name+'.bin')
            p.write_bytes(data)
            rejects(name, lambda: load_binary(p, magic))
        for prefix, data, magic in [('first', a, b'QRD617P1'), ('second', b, b'QRD617P2')]:
            binary(prefix+'_magic', b'BADMAGIC'+data[8:], magic)
            binary(prefix+'_truncated', data[:-1], magic)
            binary(prefix+'_trailing', data+b'\0', magic)
            for name, offset, value in [('prime',8,619), ('length',12,3703),
                                        ('half_width',14,564), ('begin',16,1), ('end',18,616)]:
                changed=bytearray(data);struct.pack_into('<H',changed,offset,value)
                binary(prefix+'_'+name,changed,magic)
            changed=bytearray(data);struct.pack_into('<I',changed,20,760760)
            binary(prefix+'_count',changed,magic)
        # These mutations target the first explicit key (0,0,1), so full
        # verification reaches the damaged record immediately.
        def complete_mutation(name, first_record=None, second_record=None):
            x,y=bytearray(a),bytearray(b)
            if first_record is not None:RECORD.pack_into(x,HEADER.size,*first_record)
            if second_record is not None:RECORD.pack_into(y,HEADER.size,*second_record)
            pa,pb=temp/(name+'-a.bin'),temp/(name+'-b.bin')
            pa.write_bytes(x);pb.write_bytes(y)
            rejects(name,lambda:verify(pa,pb,stars,supplement))
        first_record=RECORD.unpack_from(a,HEADER.size)
        second_record=RECORD.unpack_from(b,HEADER.size)
        v,d0,d1=first_record
        complete_mutation('constant_AP',first_record=(v,0,d1))
        complete_mutation('outside_bridge_center',first_record=(1286,d0,d1))
        complete_mutation('outside_interval_AP',first_record=(v,618,d1))
        complete_mutation('first_wrong_premise_color',first_record=(v,d1,d0))
        w,e0,e1=second_record
        complete_mutation('second_wrong_premise_color',second_record=(w,e1,e0))
        complete_mutation('first_missing_proof',first_record=(0,0,0))
        complete_mutation('second_missing_proof',second_record=(0,0,0))
        complete_mutation('overlapping_supports',second_record=first_record)
        # Erasing a proof's own protected support must invalidate that proof.
        q=qr();seed=load_supplement(stars,'QR617_AP_IMPLICATIONS_V1')
        key=sorted(seed)[0];proof=seed[key];support=implications(proof,key,q)
        rejects('ignored_erasure',lambda:implications(proof,key,q,erased=support))
        changed=copy.deepcopy(proof);changed['steps'][0][1]^=1
        rejects('implication_wrong_color',lambda:implications(changed,key,q))
        changed=copy.deepcopy(proof);changed['steps']=changed['steps'][1:]
        rejects('implication_missing_step',lambda:implications(changed,key,q))
        changed=copy.deepcopy(proof);changed['steps'].append(changed['steps'][0])
        rejects('implication_reassigns_point',lambda:implications(changed,key,q))
        changed=copy.deepcopy(proof);changed['final_ap'][1]=0
        rejects('implication_constant_final_AP',lambda:implications(changed,key,q))
        fixture=json.loads(stars.read_text());fixture['records'].append(fixture['records'][0])
        file=temp/'duplicate.json';file.write_text(json.dumps(fixture))
        rejects('duplicate_supplement_key',lambda:load_supplement(file,'QR617_AP_IMPLICATIONS_V1'))
        fixture['records']=[{'key':[0,0,0]}];file.write_text(json.dumps(fixture))
        rejects('compatible_supplement_key',lambda:load_supplement(file,'QR617_AP_IMPLICATIONS_V1'))
    return {'status':'VERIFIED_REJECTION_CONTROLS','rejections_checked':len(rejected),'controls':rejected}
