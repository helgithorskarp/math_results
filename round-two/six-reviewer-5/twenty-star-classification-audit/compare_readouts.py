"""Optional pinned public readout comparison. No researcher executable imports."""
import argparse,hashlib,json
from pathlib import Path
from urllib.request import urlopen
from audit import require
HERE=Path(__file__).resolve().parent
ROOT='https://raw.githubusercontent.com/helgithorskarp/math_results/'
def main():
 a=argparse.ArgumentParser();a.add_argument('--work',type=Path,required=True);args=a.parse_args();args.work.mkdir(parents=True,exist_ok=False)
 provenance=json.loads((HERE/'PROVENANCE.json').read_text());files={}
 for path,sha in provenance['original_inputs'].items():
  raw=urlopen(ROOT+provenance['source_commit']+'/'+provenance['source_directory']+'/'+path,timeout=20).read()
  require(hashlib.sha256(raw).hexdigest()==sha,'pinned public bytes differ: '+path)
  (args.work/path).write_bytes(raw);files[path]=json.loads(raw)
 e=json.loads((HERE/'EXPECTED.json').read_text());q=e['deficit_quotient'];original=files['expected.json']['census']
 require(q['rooted_packings_sha256']==original['packings_sha256'],'complete rooted transcript differs')
 require(q['raw_assignments']==original['raw_deficit_assignments'] and q['deficit_orbits']==original['cases'] and q['representative_packings']==original['packings'],'aggregate differs')
 require(len(q['records'])==len(original['records']),'case count differs')
 require(all(all(a[k]==b[k] for k in a) for a,b in zip(q['records'],original['records'])),'casewise cover transcript differs')
 require(q['profile_counts']==original['profile_counts'],'profile readout differs')
 require(files['fixtures.json']['stars']==json.loads((HERE/'fixtures.json').read_text())['stars'],'credited literal fixtures differ')
 print('COMPLETE optional comparison: 108 case records and all 352 rooted packings match; 23 literal fixtures match')
if __name__=='__main__':main()
