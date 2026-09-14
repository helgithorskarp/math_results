"""Mutation controls for the standalone state-gate verifier."""
from pathlib import Path
import subprocess,tempfile,shutil,json,sys

HERE=Path(__file__).parent;VERIFY=HERE/'verify.py'
def run(work,proof=None):
 command=[sys.executable,'-B',str(VERIFY),'--work',str(work)]
 if proof is not None:command.extend(['--lrat',str(proof)])
 return subprocess.run(command,capture_output=True,text=True)
def main():
 rejected=0
 with tempfile.TemporaryDirectory() as td:
  root=Path(td)
  for name in ('certificate.json','state.cnf'):shutil.copyfile(HERE/name,root/name)
  if run(root).returncode:raise RuntimeError('positive control')
  raw=(root/'certificate.json').read_bytes();(root/'certificate.json').write_bytes(raw.replace(b'"moser_vertices":7',b'"moser_vertices":8'))
  rejected+=run(root).returncode!=0;(root/'certificate.json').write_bytes(raw)
  raw=(root/'state.cnf').read_bytes();(root/'state.cnf').write_bytes(raw.replace(b'p cnf 30 522',b'p cnf 30 521'))
  rejected+=run(root).returncode!=0;(root/'state.cnf').write_bytes(raw)
  proof=(HERE/'state.lrat').read_bytes();bad=proof.replace(b'523 19',b'523 18',1);tmp=root/'bad.lrat';tmp.write_bytes(bad)
  rejected+=run(root,tmp).returncode!=0
 print(json.dumps({'status':'PASS','mutation_rejections':rejected},sort_keys=True));
 if rejected!=3:raise RuntimeError('control accepted')
if __name__=='__main__':main()
