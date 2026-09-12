"""New decoder controls, including sanitizer checks on valid positive records."""
from pathlib import Path
import json,subprocess
HERE=Path(__file__).resolve().parent

def run(catalog,witnesses,output):
 output=Path(output);output.mkdir(parents=True,exist_ok=False)
 raw=Path(witnesses).read_bytes();n=1024
 (output/'partial-catalog.g6').write_bytes(Path(catalog).read_bytes()[:12*n]);(output/'partial-witnesses').write_bytes(raw[:14*n]);(output/'none.txt').write_text('')
 checker=output/'sanitized-checker'
 subprocess.run(['g++','-O1','-g','-std=c++17','-fsanitize=address,undefined','-fno-omit-frame-pointer',str(HERE/'check_witnesses.cpp'),'-o',str(checker)],check=True)
 checks=[]
 def reject(name,cat,wit,expected):
  proc=subprocess.run([str(checker),str(cat),str(wit),str(output/'none.txt')],capture_output=True,text=True)
  if proc.returncode!=1 or proc.stderr.strip()!=expected:raise ValueError((name,proc.returncode,proc.stderr))
  checks.append(dict(name=name,rejected=True,reason=expected,sanitizer_errors=False))
 reject('1024 valid graphs then incomplete scope',output/'partial-catalog.g6',output/'partial-witnesses','incomplete core catalog')
 (output/'padding').write_bytes(bytes(13)+bytes([1]));reject('bad 104-bit padding',catalog,output/'padding','nonzero witness padding')
 (output/'all-blue').write_bytes(bytes(14));reject('false literal graph',catalog,output/'all-blue','blue K5 in model')
 (output/'truncated').write_bytes(raw[:13]);reject('truncated physical word',catalog,output/'truncated','truncated witness')
 (output/'unexpected-sentinel').write_bytes(bytes([255])*14);reject('unlisted negative case',catalog,output/'unexpected-sentinel','UNSAT sentinel mismatch')
 result=dict(status='ALL_NEW_DECODER_CONTROLS_PASSED',positive_graphs_sanitizer_checked=1024,checks=checks)
 (output/'CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n');return result
