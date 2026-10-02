"""Postseal public author export adapter. Never input to independent audit.

Run from a repository checkout; every target source byte is checked BEFORE
any import. Export data should be written in scratch, not committed.
"""
import sys,json,argparse,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--target-directory',type=Path,default=P.parent.parent/'six-downset-3/core-edge-five-cutoff');parser.add_argument('--record',type=Path,required=True);args=parser.parse_args();folder=args.target_directory.resolve()
 data=json.loads((P/'TARGET_ACCESS.json').read_text())
 for name,pin in data['whole_files'].items():
  raw=(folder/Path(name).name).read_bytes()
  if len(raw)!=pin['bytes'] or hashlib.sha256(raw).hexdigest()!=pin['sha256']:raise ValueError('entire target byte gate '+name)
 sys.path.insert(0,str(folder));import verify as V
 out=[]
 for q in range(5,18):
  d=V.forms(q,5);low,c,lp=V.lower_dual(d);cap,coeff,cp,moment=V.cap_dual(d)
  row={'q':q,'keys':d['keys'],'weights':d['sizes'],'coefficient_forms':{name:d[name] for name in V.NAMES},'lower_dual':low,'cap_dual':cap,'c':c,'lower_pairs':lp,'cap_pairs':cp,'cap_coefficients':coeff,'cap_moment':moment}
  if q in (16,17):
   tb,sig=(12,-12) if q==16 else (4,-6);G,H=V.evaluate(d,V.KAPPA,V.F(tb),V.F(sig));w=d['sizes'];a=V.vectors(d)['star'];h=[x*y for x,y in zip(w,a)];m=len(w)
   row['positive_forms']={'lower':G,'upper':H,'lower_floor':[[G[i][j]-V.LOWER_FLOOR*(w[i]*int(i==j)-V.F(h[i]*h[j],d['s'])) for j in range(m)] for i in range(m)],'upper_floor':[[H[i][j]-V.CAP_FLOOR*w[i]*int(i==j) for j in range(m)] for i in range(m)]}
  out.append(row)
 if args.record.exists():raise ValueError('refuse to overwrite author export')
 args.record.parent.mkdir(parents=True,exist_ok=True);args.record.write_text(json.dumps(V.encode(out),indent=2)+'\n')
 print(json.dumps({'whole_orders':len(out),'author_coefficient_names':list(V.NAMES),'postseal_comparison_only':True,'whole_source_checked_before_import':True}))
if __name__=='__main__':main()
