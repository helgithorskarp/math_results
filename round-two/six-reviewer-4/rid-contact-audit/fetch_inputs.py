"""Fetch only the compact publicly published original expected record."""
import argparse,hashlib,urllib.request
from pathlib import Path
URL='https://raw.githubusercontent.com/helgithorskarp/math_results/b71c66315c15953070e6a1063570c413955e08da/round-two/six-rupert-3/rid_diagonal_contact_patch/expected.json'
SHA='bfddc098ec79f8ddd003d7dd59c3929f3bf31f755fecca6284ff2913c072c658'
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('output',type=Path);a=p.parse_args()
 with urllib.request.urlopen(URL,timeout=30) as r:data=r.read()
 if len(data)!=14893 or hashlib.sha256(data).hexdigest()!=SHA:raise ValueError('original compact evidence changed')
 a.output.write_bytes(data);print('Verified published original expected record:',len(data),'bytes',SHA)
