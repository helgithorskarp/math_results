"""Optional network/native corroboration; independent theorem replay is offline."""
import hashlib,json,os,pathlib,subprocess,sys,urllib.request
import audit as a

P=pathlib.Path(__file__).resolve().parent
if __name__=='__main__':
    d=P/'scratch/author';original=d/'original';original.mkdir(parents=True,exist_ok=True)
    receipt=json.loads((P/'AUTHOR_SOURCE.json').read_text())
    for row in receipt['files']:
        a.need('/ec7f3d0ee47f2f6dd3bbdbbac71bf93238807918/' in row['url'],'exact pinned author source')
        raw=urllib.request.urlopen(row['url'],timeout=20).read()
        a.need(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'every pinned author source byte')
        (original/row['name']).write_bytes(raw)
    (d/'first-record.json').write_bytes(a.encode(a.compute()))
    env={**os.environ,**{k:'1' for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS','VECLIB_MAXIMUM_THREADS')}}
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
        output=d/('native-'+mode+'-full.json')
        result=subprocess.run([sys.executable,'-B']+flags+[str(original/'verify.py'),'--output',str(output)],
                              capture_output=True,timeout=10,env=env)
        (d/(mode+'.stdout')).write_bytes(result.stdout);(d/(mode+'.stderr')).write_bytes(result.stderr)
        result.check_returncode()
    subprocess.run([sys.executable,'-B',str(P/'corroborate.py')],check=True,env=env,timeout=10)
