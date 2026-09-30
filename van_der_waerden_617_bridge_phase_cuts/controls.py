#!/usr/bin/env python3
"""Targeted malformed-certificate and weakened-coverage rejection controls."""
import argparse
import copy
import json
from pathlib import Path
import struct
import tempfile
import time

from check import verify, colors, check_implications, load_supplement


def run(certificate, supplement, workdir):
    start = time.monotonic()
    original = certificate.read_bytes()
    passed = []
    def rejects(name, action):
        try:
            action()
        except (ValueError, KeyError):
            passed.append(name)
        else:
            raise ValueError('control was not rejected: '+name)
    with tempfile.TemporaryDirectory(prefix='bridge-controls-',dir=workdir) as temp:
        target = Path(temp)/'bad.bin'
        def binary_test(name, data):
            target.write_bytes(data)
            rejects(name,lambda:verify(target,supplement,565))
        binary_test('truncated_header',original[:23])
        binary_test('truncated_final_record',original[:-1])
        binary_test('trailing_record',original+b'\0'*6)
        for name, offset, value in [('wrong_modulus',8,619),('wrong_AP_length',10,6),
                                    ('wrong_interval_length',12,3703),('weaker_bridge_header',14,553),
                                    ('stronger_bridge_header',14,566),('missing_left_phase',16,1),
                                    ('missing_rightmost_phase',18,616),('center_outside_bridge',24,1286),
                                    ('center_outside_interval',24,65535),('constant_first_AP',26,0),
                                    ('out_of_range_second_AP',28,1000)]:
            bad=bytearray(original);struct.pack_into('<H',bad,offset,value)
            binary_test(name,bad)
        bad=bytearray(original);struct.pack_into('<I',bad,20,760760)
        binary_test('incomplete_record_count',bad)
        bad=bytearray(original);bad[24:30]=b'\0'*6
        binary_test('new_unproved_hole',bad)
        v,d0,d1=struct.unpack_from('<3H',original,24)
        bad=bytearray(original);struct.pack_into('<H',bad,28,d0)
        binary_test('identical_opposed_APs',bad)
        bad=bytearray(original);struct.pack_into('<3H',bad,24,v,d1,d0)
        binary_test('swapped_premise_colors',bad)
        bad=bytearray(original);struct.pack_into('<H',bad,24,1852-617+d0)
        binary_test('free_template_pole_as_premise',bad)
        json_target=Path(temp)/'bad.json'
        content=json.loads(supplement.read_text())
        duplicate=copy.deepcopy(content);duplicate['records'].append(copy.deepcopy(duplicate['records'][0]))
        json_target.write_text(json.dumps(duplicate))
        rejects('duplicate_star_key',lambda:load_supplement(json_target,565))
        compatible=copy.deepcopy(content);compatible['records'][0]['key']=[0,0,0]
        json_target.write_text(json.dumps(compatible))
        rejects('compatible_star_key',lambda:load_supplement(json_target,565))
        q=colors(); record=content['records'][0]; key=tuple(record['key'])
        for name, mutate in [
            ('constant_star_petal',lambda r:r['steps'][0].__setitem__(3,0)),
            ('wrong_forced_star_color',lambda r:r['steps'][0].__setitem__(1,1-r['steps'][0][1])),
            ('repeated_forced_star_point',lambda r:r['steps'].__setitem__(1,copy.deepcopy(r['steps'][0]))),
            ('missing_star_petal',lambda r:r['steps'].pop()),
            ('constant_final_star_AP',lambda r:r['final_ap'].__setitem__(1,0)),
            ('final_star_AP_contains_unknown_points',lambda r:r.__setitem__('final_ap',[1850,1]))]:
            bad=copy.deepcopy(record);mutate(bad)
            rejects(name,lambda bad=bad:check_implications(bad,key,565,q))
    return {'status':'ALL_CERTIFICATE_REJECTION_CONTROLS_PASSED',
            'rejections_checked':len(passed),'controls':passed,
            'seconds':time.monotonic()-start}


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('certificate',type=Path)
    parser.add_argument('supplement',type=Path)
    parser.add_argument('--workdir',type=Path,required=True)
    args=parser.parse_args()
    args.workdir.mkdir(parents=True,exist_ok=True)
    print(json.dumps(run(args.certificate,args.supplement,args.workdir),indent=2))
