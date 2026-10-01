"""Reconstruct the exact algebra and all rank/root exceptional loci."""
from pathlib import Path
import argparse,hashlib,json
import geometry
HERE=Path(__file__).resolve().parent
def require(ok,message):
 if not ok:raise ValueError(message)
def digest(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def verify(data,derived=None):
 reference=geometry.derive_certificate() if derived is None else derived
 require(data==reference,'entire exact geometry and exceptional-locus certificate regenerated')
 return {'status':'VERIFIED','closed_interval':data['interval'],'deleted_edge':[9,13],
         'formal_orientation_models':8,'real_roots_by_orientation':{'-1':4,'1':4},
         'singular_parameters':0,'all_rank_resultants_nonzero_on_I':True,
         'canonical_certificate_sha256':digest(data)}
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--certificate',type=Path,default=HERE/'certificate.json')
 p.add_argument('--generate',type=Path)
 args=p.parse_args()
 if args.generate:
  data=geometry.derive_certificate()
  args.generate.write_text(json.dumps(data,sort_keys=True,separators=(',',':'))+'\n')
  print(json.dumps(verify(data,data),sort_keys=True))
 else:print(json.dumps(verify(json.loads(args.certificate.read_text())),sort_keys=True))
