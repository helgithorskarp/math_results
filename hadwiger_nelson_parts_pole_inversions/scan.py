"""Complete finite-field supergraph census; norm-ratio formulation."""
import json,time,hashlib,argparse
from pathlib import Path
from collections import Counter
import numpy as np
import model as m

def setup():
    xy=np.array(m.projected(),dtype=np.int64);p=m.P
    m.require(4*(p-1)**2<2**63,'NumPy product bound')
    dx=xy[:,0,None]-xy[None,:,0];dy=xy[:,1,None]-xy[None,:,1]
    N=(dx*dx+3*dy*dy)%p
    m.require(np.count_nonzero(N)==509*508,'vanishing projected source distance')
    return xy,N,np.triu_indices(508,1)
def run(work,certificate=None,native_file=None):
    start=time.time();work=Path(work);work.mkdir(parents=True,exist_ok=True)
    xy,N,(A,B)=setup();p=m.P;hist=Counter();poles=[];residual=[];best=None;stream=hashlib.sha256();checked_words=0
    cert=None if certificate is None else {(r['pole'],r['residue']):r for r in certificate}
    native=None if native_file is None else np.memmap(native_file,dtype='<u4',mode='r')
    if native is not None:m.require(native.size==509*128778,'incomplete native stream')
    for pole in range(509):
        ids=np.array([i for i in range(509) if i!=pole]);inv=np.array([pow(int(N[pole,i]),-1,p) for i in ids],dtype=np.int64)
        R=N[ids[A],ids[B]]*inv[A]%p*inv[B]%p
        if native is not None:m.require(np.array_equal(R,native[pole*128778:(pole+1)*128778]),'entrywise inversion/ratio disagreement')
        stream.update(R.astype('<u4').tobytes())
        order=np.argsort(R,kind='stable');vals=R[order];starts=np.r_[0,np.flatnonzero(vals[1:]!=vals[:-1])+1];counts=np.diff(np.r_[starts,len(R)])
        hist.update(map(int,counts));rich=0;nonpeel=0
        # A simple graph with a nonempty4-core has at least10 edges.
        for lo,n in zip(starts[counts>=10],counts[counts>=10]):
            es=list(zip(map(int,A[order[lo:lo+n]]),map(int,B[order[lo:lo+n]])));rich+=1
            row={'pole':pole,'residue':int(vals[lo]),'edges':int(n)}
            if best is None or n>best['edges']:best=row|{'pair':[int(ids[A[order[lo]]]),int(ids[B[order[lo]]])]}
            if m.peel(es) is None:
                nonpeel+=1
                if cert is not None:
                    m.require((pole,int(vals[lo])) in cert,'missing residual certificate');c=cert[(pole,int(vals[lo]))]
                    m.require(c['edges']==int(n),'certificate edge count');m.word_check(c['word'],es);checked_words+=1
                residual.append(row|{'edge_list':es})
        poles.append({'pole':pole,'buckets':len(counts),'rich':rich,'nonpeel':nonpeel,'max_edges':int(max(counts))})
        if pole%100==0:print('pole',pole,'residual',len(residual),flush=True)
    if cert is not None:m.require(checked_words==len(cert)==len(certificate),'extra/repeated certificate row')
    out={'poles':509,'points_per_drawing':508,'scale_representatives':509*128778,'residue_buckets':sum(x['buckets'] for x in poles),'buckets_with_at_least_ten_edges':sum(x['rich'] for x in poles),'three_degenerate_buckets':sum(x['buckets'] for x in poles)-len(residual),'residual_buckets':len(residual),'largest_supergraph':best,'stream_sha256':stream.hexdigest(),'edge_histogram':dict(sorted(hist.items())),'word_checks':checked_words,'entrywise_native_comparison':native is not None,'seconds':time.time()-start}
    (work/'census.json').write_text(json.dumps(out,indent=2)+'\n');(work/'poles.json').write_text(json.dumps(poles,indent=2)+'\n');(work/'residual.json').write_text(json.dumps(residual)+'\n')
    print(json.dumps(out),flush=True);return out,residual
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--work',type=Path,required=True);args=ap.parse_args();run(args.work)
