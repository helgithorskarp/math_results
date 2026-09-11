"""Replay all three exact certificate layers needed for the unrestricted theorem."""
import hashlib,json,subprocess,sys
from pathlib import Path
assert __debug__,'Run without -O.'
root=Path(__file__).resolve().parent
out=[]
for folder in (root.parent,root.parent/'link_envelopes',root):
 result=subprocess.run([sys.executable,str(folder/'verify.py')],cwd=folder,
                       capture_output=True,text=True,check=True)
 data=json.loads(result.stdout)
 expected_name='expected.json' if folder==root else 'EXPECTED_OUTPUT.json'
 expected=json.loads((folder/expected_name).read_text())
 assert data==expected
 out.append({'layer':folder.name,'output_sha256':hashlib.sha256(result.stdout.encode()).hexdigest()})
print(json.dumps({'all_layers_verified':True,'layers':out},indent=2,sort_keys=True))
