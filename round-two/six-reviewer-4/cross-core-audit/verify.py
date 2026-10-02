"""Serial offline reproduction; explicit checks survive Python -O."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from core import require

BASE=Path(__file__).resolve().parent


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def run(mode):
    flag=['-O'] if mode=='optimized' else []
    values={}
    for name in ('audit','controls'):
        result=subprocess.run([sys.executable]+flag+[str(BASE/(name+'.py'))],
                              capture_output=True,text=True,timeout=30)
        require(result.returncode==0, name+' failed: '+result.stderr)
        values[name]=json.loads(result.stdout)
    audit=values['audit']
    require(hashlib.sha256(canonical(audit['core'])).hexdigest()==audit['core_sha256'],
            'whole independent core hash')
    record={'core_sha256':audit['core_sha256'],'summary':audit['summary'],
            'controls':values['controls']}
    expected=json.loads((BASE/'EXPECTED.json').read_text())
    require(record==expected['record'], 'whole independent record differs')
    digest=hashlib.sha256(canonical(record)).hexdigest()
    require(digest==expected['record_sha256'], 'whole record digest')
    return {'mode':mode,'status':'COMPLETE_CONDITIONAL_CROSS_CORE_AUDIT',
            'record_sha256':digest,'core_sha256':audit['core_sha256'],
            'summary':audit['summary']}


if __name__=='__main__':
    for mode in ('normal','optimized'):
        print(json.dumps(run(mode),sort_keys=True,separators=(',',':')))
