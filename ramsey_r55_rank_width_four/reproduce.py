"""Check all published files and replay proof arithmetic and physical controls."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def run():
    root=Path(__file__).resolve().parent
    for line in (root/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        if hashlib.sha256((root/name).read_bytes()).hexdigest()!=digest:
            raise RuntimeError('manifest mismatch: '+name)
    summaries={}
    for flags in (['-B'],['-O','-B']):
        for stem in ('audit','controls'):
            result=subprocess.run([sys.executable,*flags,str(root/(stem+'.py'))],
                                  cwd=root,capture_output=True,check=True).stdout
            if result!=(root/('expected_'+stem+'.json')).read_bytes():
                raise RuntimeError('expected output differs: '+stem)
            summaries[stem+'_sha256']=hashlib.sha256(result).hexdigest()
        for name in ('fixture_cut','fixture_decomposition'):
            result=subprocess.run([sys.executable,*flags,str(root/'extract.py'),str(root/(name+'.json'))],
                                  cwd=root,capture_output=True,check=True).stdout
            if result!=(root/(name+'_certificate.json')).read_bytes():
                raise RuntimeError('fixture extraction differs')
            checked=subprocess.run([sys.executable,*flags,str(root/'verify.py'),str(root/(name+'.json')),
                                    str(root/(name+'_certificate.json'))],
                                   cwd=root,capture_output=True,check=True).stdout
            if json.loads(checked)['status']!='VERIFIED_PHYSICAL_EXCLUSION':
                raise RuntimeError('fixture verification failed')
    print(json.dumps(dict(summaries,status='REPRODUCED_GLOBAL_RANK_WIDTH_THREE_EXCLUSION',
                         ramsey_bound_improved=False,target_graph_found=False),sort_keys=True))


if __name__=='__main__':run()
