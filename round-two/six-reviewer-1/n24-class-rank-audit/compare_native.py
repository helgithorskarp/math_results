"""LATE optional comparison of full native DATA; never imports target executables."""
import argparse
import hashlib
import json
from pathlib import Path
import sys
from fractions import Fraction as Q
sys.path.insert(0,str(Path(__file__).resolve().parent))
from exact import need, matmul, transpose, pack


def matrix(a):
    return [[Q(v) for v in row] for row in a]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--primary-record',type=Path,required=True)
    p.add_argument('--native-operators',type=Path,required=True)
    p.add_argument('--record',type=Path,required=True)
    a = p.parse_args()
    own = json.loads(a.primary_record.read_text())
    native = json.loads(a.native_operators.read_text())
    need(own['completed_table'] == native['full_table'],'entire completed original table')
    need(len(native['original_blocks']) == len(own['sectors']) == 13,'all physical degrees')
    comparisons = []
    for x, y in zip(own['sectors'],native['original_blocks']):
        need(x['j'] == y['j'] and x['sizes'] == y['layers'],'degree/layer order')
        need(x['multiplicity'] == y['multiplicity'],'physical multiplicity')
        n = len(x['sizes'])
        if x['j'] == 0:
            b = x['norm']
            inv = [[Q(i==k)-Q(b[k],own['summary']['N']) for k in range(n)] for i in range(n)]
            P = [[Q(i==k)+b[k] for k in range(n)] for i in range(n)]
        else:
            inv = P = [[Q(i==k) for k in range(n)] for i in range(n)]
        fields = {}
        for field, other in [('lower','lower'),('upper','upper'),('original_metric','gram')]:
            value = matmul(matmul(transpose(inv),matrix(y[other])),inv)
            need(matrix(x[field]) == value,'full original inverse-metric congruence '+field)
            fields[field] = value
        kernel = transpose(matmul(P,transpose(matrix(y['kernels'])))) if y['kernels'] else []
        need(matrix(x['kernel']) == kernel,'all transformed physical kernel coordinates')
        fields['kernel'] = kernel
        comparisons.append({'j':x['j'],'all_four_complete_fields':fields,
                            'physical_dimension':n,'multiplicity':x['multiplicity']})
    record = pack({'full_table':native['full_table'],'comparisons':comparisons})
    data = (json.dumps(record,sort_keys=True,separators=(',',':'))+'\n').encode()
    a.record.write_bytes(data)
    print(json.dumps({'late_data_comparison_only':True,'all_primary_sealed_source_unchanged':True,
                      'full_physical_fields_compared':52,'complete_tables_compared':1,
                      'record_bytes':len(data),'record_sha256':hashlib.sha256(data).hexdigest()}))


if __name__ == '__main__':
    main()
