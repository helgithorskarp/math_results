"""Portable source-only native replay and independently rebuilt correspondence.

All17 pinned whole inputs must match before any target code is executed.
Native code runs only as a separate process, with a fixed45-second guard.
No native module is imported into the independent correspondence engine.
"""
import concurrent.futures,hashlib,json,os,pathlib,subprocess,sys,tempfile,urllib.request
for name in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS','BLIS_NUM_THREADS','NUMEXPR_NUM_THREADS','VECLIB_MAXIMUM_THREADS']:os.environ[name]='1'
from correspond import compare
P=pathlib.Path(__file__).resolve().parent
manifest=json.loads((P/'AUTHOR-SOURCE.json').read_text())
with tempfile.TemporaryDirectory(prefix='repeated-profile-correspondence-') as tmp:
    folder=pathlib.Path(tmp)
    def fetch(row):
        request=urllib.request.Request(row['url'],headers={'User-Agent':'six-reviewer-5 source-only correspondence'})
        with urllib.request.urlopen(request,timeout=20) as response:raw=response.read()
        if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']:raise ValueError('ENTIRE pinned native input differs')
        if pathlib.PurePosixPath(row['path']).name!=row['path']:raise ValueError('flat pinned source path')
        (folder/row['path']).write_bytes(raw)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:list(pool.map(fetch,manifest['files']))
    path=folder/'native-full.json'
    command=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(folder/'verify.py'),'--record',str(path)]
    outcome=subprocess.run(command,cwd=folder,capture_output=True,text=True,timeout=45)
    if outcome.returncode:raise RuntimeError('native replay failed: '+outcome.stderr)
    native=json.loads(path.read_text());common=compare(native,json.loads((P/'PRIMARY.json').read_text()))
    if common!=json.loads((P/'COMMON.json').read_text()):raise ValueError('ENTIRE independently rebuilt correspondence differs')
    print(json.dumps(dict(status='PASS',pinned_whole_inputs=len(manifest['files']),
        native_record_sha256=native['record_sha256'],native_only_counts=json.loads(outcome.stdout)['counts'],
        whole_independent_correspondence_sha256=hashlib.sha256(json.dumps(common,sort_keys=True,separators=(',',':')).encode()).hexdigest()),sort_keys=True))
