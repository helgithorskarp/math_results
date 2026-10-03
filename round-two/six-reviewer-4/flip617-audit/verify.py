"""Verify compact source pins, then regenerate and compare the entire result."""
import argparse,hashlib,json,pathlib,subprocess,sys
def need(ok,why):
 if not ok:raise ValueError(why)
def run(output):
 src=pathlib.Path(__file__).resolve().parent
 manifest=json.loads((src/'MANIFEST.json').read_text())
 for name,pin in manifest['files'].items():
  raw=(src/name).read_bytes();need(len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256'],'source pin: '+name)
 seal=json.loads((src/'SEAL.json').read_text())
 for name,pin in seal['files'].items():need(hashlib.sha256((src/name).read_bytes()).hexdigest()==pin['sha256'],'independent seal: '+name)
 subprocess.run([sys.executable,str(src/'reproduce.py'),'--output',output],check=True)
 need((pathlib.Path(output)/'RESULT.json').read_bytes()==(src/'RESULT.json').read_bytes(),'entire expected result')
 print('PASS: source/seal pins and entire freshly regenerated independent result')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();run(a.output)
