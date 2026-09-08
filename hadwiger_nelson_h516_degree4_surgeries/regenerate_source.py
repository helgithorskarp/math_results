"""Recover the accepted H516 source; imports only its existing input loader.
No homomorphism propagation, deletion search, or SAT query is performed.
"""
import argparse,hashlib,importlib.util,json,pathlib
D=pathlib.Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=pathlib.Path,required=True);a=ap.parse_args()
    path=D.parent/'hadwiger_nelson_heule516_host_homomorphisms/build.py'
    spec=importlib.util.spec_from_file_location('h516_source_loader',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    plan,labels,pins,target,adj,edges=m.prepare()
    points,all_edges,large=m.B.geometry()
    source={'labels':labels,'coordinates':[points[v] for v in labels],'edges':edges,'degree4':sorted(v for v in labels if len(adj[v])==4)}
    data=(json.dumps(source,separators=(',',':'))+'\n').encode()
    if data!=(D/'SOURCE.json').read_bytes():raise ValueError('source mismatch')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(data)
    print(json.dumps({'same_source_bytes':True,'vertices':len(labels),'edges':len(edges),'sha256':hashlib.sha256(data).hexdigest(),'queries':0}))
if __name__=='__main__':main()
