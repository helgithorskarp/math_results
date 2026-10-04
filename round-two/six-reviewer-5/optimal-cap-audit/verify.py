"""Source binding, serial independent reconstruction, whole record equality."""
import argparse,hashlib,json,pathlib,subprocess,sys
P=pathlib.Path(__file__).resolve().parent
a=argparse.ArgumentParser();a.add_argument('--output',required=True);v=a.parse_args()
for name,digest in json.loads((P/'CORE.json').read_text())['files'].items():
 if hashlib.sha256((P/name).read_bytes()).hexdigest()!=digest:raise ValueError('whole source binding '+name)
command=[sys.executable,'-I','-B']+(['-O'] if not __debug__ else [])+[str(P/'validate.py'),'--output',v.output]
raise SystemExit(subprocess.run(command,check=False).returncode)
