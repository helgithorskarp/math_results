"""Regenerate compact exact certificates; no floating bound is accepted."""
import argparse
import json
import math
from pathlib import Path
import tempfile

from audit import verify
from model import run as coordinate_rounding
from round import run as sum_rounding


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source',default='seed.json')
    p.add_argument('--output',required=True);args=p.parse_args()
    source=json.loads(Path(args.source).read_text());word=source['word'];a=(len(word)+1)//5
    family=dict(seed_word=word,seed_axis_factor=a,chambers=[])
    with tempfile.TemporaryDirectory(prefix='schur-axis-') as temporary:
        for u in range(1,a//2+1):
            if math.gcd(u,a)>1:continue
            output=str(Path(temporary)/('axis_%02d.json'%u))
            cert=coordinate_rounding(word,u,output)
            if u==11:cert=sum_rounding(args.source,u,output,target=108)
            cert.pop('tests',None);family['chambers'].append(cert)
    Path(args.output).write_text(json.dumps(family,separators=(',',':'))+'\n')
    result=verify(args.output)
    assert result['integer_axis_upper_bound']==107
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
