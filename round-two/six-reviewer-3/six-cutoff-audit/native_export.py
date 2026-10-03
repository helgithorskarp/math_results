"""POSTSEAL comparison adapter. Producer output is not an independent premise.

The complete16-file target plus both mandatory siblings are byte-gated before
any target import. Native counted forms are exported for full entry comparison.
"""
import argparse,json,hashlib,sys
from pathlib import Path

def gate(root):
 access=json.loads(Path(__file__).with_name('TARGET_ACCESS.json').read_text())
 for name,v in access['whole_files'].items():
  b=(root/name).read_bytes()
  if len(b)!=v['bytes'] or hashlib.sha256(b).hexdigest()!=v['sha256']:raise ValueError('whole target source changed before import: '+name)
 for name,v in access['mandatory_executable_inputs'].items():
  b=(root.parent/name).read_bytes()
  if len(b)!=v['bytes'] or hashlib.sha256(b).hexdigest()!=v['sha256']:raise ValueError('whole mandatory sibling changed before import: '+name)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('output',type=Path);args=ap.parse_args();root=args.root.resolve();gate(root)
 sys.path.insert(0,str(root));import forms,polycap
 ordinary=polycap.coefficients();quot=polycap.divide(ordinary['residual_numerator'],polycap.mul(polycap.Q,ordinary['cost_denominator']))
 shifted=polycap.coefficients(polycap.add(polycap.constant(6),polycap.scale(polycap.K,3),polycap.Q),polycap.add(polycap.constant(2),polycap.K))
 record={'forms':{str(q):forms.forms(q,6) for q in range(6,24)},'ordinary_polynomials':{k:[[i,j,str(v)] for (i,j),v in sorted(p.items())] for k,p in ordinary.items()},'P':[[i,j,str(v)] for (i,j),v in sorted(quot.items())],'shifted':{k:[[i,j,str(v)] for (i,j),v in sorted(shifted[k].items())] for k in ['cap_block_denominator','Delta_numerator']}}
 args.output.write_text(json.dumps(forms.encode(record),sort_keys=True,separators=(',',':'))+'\n')
 print(json.dumps({'all18_preimport_byte_gates':True,'all_actual_orders':18,'whole_export_sha256':hashlib.sha256(args.output.read_bytes()).hexdigest()}))
