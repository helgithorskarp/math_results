"""Bind every entire compact source file before independent mathematics."""
import argparse,hashlib,json,pathlib,subprocess,sys

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);args=p.parse_args();root=pathlib.Path(__file__).resolve().parent
 rows=[line.split('  ') for line in (root/'SHA256SUMS').read_text().splitlines()]
 if any(len(row)!=2 or '/' in row[1] or row[1] in ('','.','..','SHA256SUMS') for row in rows):raise ValueError('flat owned source manifest')
 names=[row[1] for row in rows]
 if any(x.is_symlink() or not x.is_file() for x in root.iterdir()):raise ValueError('only regular flat source files')
 if len(set(names))!=len(names) or sorted(names+['SHA256SUMS'])!=sorted(x.name for x in root.iterdir()):raise ValueError('complete exact source file census')
 for digest,name in rows:
  raw=(root/name).read_bytes()
  if hashlib.sha256(raw).hexdigest()!=digest:raise ValueError('whole source digest: '+name)
  raw.decode('utf-8')
  if name.endswith('.json'):json.loads(raw)
 child=subprocess.run([sys.executable,'-I','-B',str(root/'validate.py'),'--out',args.out],capture_output=True,text=True)
 if child.returncode:raise RuntimeError(child.stdout+child.stderr)
 receipt=json.loads(pathlib.Path(args.out).read_text())
 if len(receipt['positive_children'])!=3 or len(receipt['controls'])!=24:raise ValueError('entire public mathematical replay')
 print(child.stdout.strip())
if __name__=='__main__':main()
