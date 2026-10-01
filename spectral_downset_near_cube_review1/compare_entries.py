"""Optional supplemental literal author-matrix comparison; not a proof input."""
import argparse,hashlib,importlib.util,json
from fractions import Fraction
from pathlib import Path

def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--author-dir',type=Path,default=Path(__file__).resolve().parent.parent/'spectral_downset_near_cube');args=parser.parse_args()
 here=Path(__file__).resolve().parent
 provenance=json.loads((here/'provenance.json').read_text())
 pin=next(x['sha256'] for x in provenance['reviewed_inputs'] if x['path'].endswith('/verify.py'))
 path=args.author_dir/'verify.py'
 if hashlib.sha256(path.read_bytes()).hexdigest()!=pin:raise ValueError('author checker pin changed')
 own=module('independent_near_cube_audit',here/'audit.py');author=module('optional_author_near_cube_constructor',path)
 records=[]
 for n in range(4,9):
  labels,pairs,C0,C1=own.partition_matrices(n)
  values=[Fraction(0),Fraction(1),Fraction(2),Fraction(3,2)]
  if n==4:values.append(Fraction(15,13))
  if n==5:values.append(Fraction(19,10))
  for z in values:
   C=own.core(n,z,labels,C0,C1);L=own.lower(C)
   nativeC=author.core(n,z,labels);nativeL=author.lift(nativeC)
   if C!=nativeC or L!=nativeL:raise ValueError('literal matrix entry mismatch')
   records.append({'n':n,'z':str(z),'core_entries':len(C)**2,'full_lower_entries':len(L)**2})
 result={'agent':'six-reviewer-1','role':'independent mathematical reviewer','scope':'Optional supplemental comparison only; audit.py imports no author code or fixture.','all_entries_equal':True,'author_checker_sha256':pin,'cases':records,'compared_core_and_full_entries':sum(x['core_entries']+x['full_lower_entries'] for x in records)}
 print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
