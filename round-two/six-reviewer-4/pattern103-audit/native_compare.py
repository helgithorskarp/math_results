"""POST-SEAL schema adapter. Reconstructs full target positive transcripts.

No native executable imports. Target certificate/expected schemas were exposed
before this adapter was written; it is separate from the sealed primary proof.
"""
import argparse,csv,hashlib,json,struct
from pathlib import Path
Q=103
SQUARES={x*x%Q for x in range(1,Q)}
CHARS={x:int(x not in SQUARES) for x in range(1,Q)}
def need(test,why):
    if not test:raise ValueError(why)
def key(x,roots):
    need(x not in roots,'original root')
    return sum(b*CHARS[(x-r)%Q] for b,r in zip((4,2,1),roots))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--target',required=True);ap.add_argument('--mode',choices=['base','affine','packs','phases'],required=True);args=ap.parse_args()
    p=Path(args.target);raw=(p/'five-packs.csv').read_bytes();rows=[list(map(int,r)) for r in csv.reader(raw.decode().splitlines())];kernel=json.loads((p/'four-APs.json').read_text());expected=json.loads((p/'EXPECTED.json').read_text())[args.mode]
    need(len(rows)==128 and all(len(r)==11 for r in rows),'whole positive shape')
    need([r[0] for r in rows]==list(range(0,256,2)),'whole case domain')
    need(raw==''.join(','.join(map(str,r))+'\n' for r in rows).encode(),'canonical bytes')
    need(kernel['q']==103 and kernel['pole']==0 and kernel['roots']==[1,2,4],'original free columns')
    labels={x:key(x,[1,2,4]) for x in range(1,Q) if x not in (1,2,4)}
    packs=[];digest=hashlib.sha256()
    for row in rows:
        word=row[0];occupied=set();leaves=[]
        for a,d in zip(row[1::2],row[2::2]):
            need(0<=a<Q and 1<=d<=51,'oriented witness')
            points=[(a+j*d)%Q for j in range(7)];need(len(set(points))==7 and set(points)<=set(labels),'literal support')
            keys=[labels[x] for x in points];colors=[(word>>k)&1 for k in keys]
            need(len(set(colors))==1 and not occupied.intersection(points),'actual monochromatic/disjoint')
            occupied.update(points);digest.update(struct.pack('<3H7H7B7B',word,a,d,*points,*keys,*colors));leaves.append((a,d,points,keys,colors[0]))
        need(len(occupied)==35,'whole35-support');packs.append((word,leaves))
    ks=[]
    for (a,d),support in zip(kernel['APs'],kernel['pattern_supports'],strict=True):
        points=[(a+j*d)%Q for j in range(7)];keys=[labels[x] for x in points]
        need(sorted(set(keys))==support,'native kernel support');ks.append((a,d,points,keys))
    need([v for v in kernel['pattern_supports']]==[[1,2],[1,4],[1,5],[2,4,5]],'four-kernel logic')
    histogram=[0]*4
    for word in range(256):
        bad=next((i for i,r in enumerate(ks) if len({(word>>k)&1 for k in r[3]})==1),None)
        need(bad is not None,'all256 kernel');histogram[bad]+=1
    if args.mode=='base':
        result=dict(author='six-vdw-1',role='researcher',status='ALL128_ACTUAL_FIELD_FIVE_PACKS_AND_FOUR_AP_KERNEL_CHECKED',q=Q,pole=0,all_original_roots=[1,2,4],pattern_sizes=[list(labels.values()).count(k) for k in range(8)],gauged_tables=128,full_tables=256,five_pack_APs=640,five_pack_points=4480,columns_per_pack=35,kernel_APs=4,kernel_points=28,kernel_first_bad_full_table_histogram=histogram,leading_coefficient_cube_values=256*8*8,pack_bytes=len(raw),pack_sha256=hashlib.sha256(raw).hexdigest(),entire_literal_pack_transcript_sha256=digest.hexdigest(),repair_lower_bound=5,optimum_claim=False,numerical_W_improvement=False)
        for w in range(256):
            for sign in range(8):
                transformed=sum(((w>>(k^sign))&1)<<k for k in range(8))
                need(all((transformed>>k)&1==(w>>(k^sign))&1 for k in range(8)),'entire signed cube')
    elif args.mode=='affine':
        basis=hashlib.sha256();aps=hashlib.sha256();max_integer=0;configs=points_count=ap_count=0
        for pole in range(Q):
            for unit in range(1,Q):
                mapping=[(pole+unit*x)%Q for x in range(Q)];roots=[mapping[r] for r in (1,2,4)];flip=7*CHARS[unit]
                need(len(set(mapping))==Q and len({pole,*roots})==4,'affine entire/free');configs+=1
                for x in sorted(labels):
                    y=mapping[x];actual=key(y,roots);need(y!=pole and actual==labels[x]^flip,'original basis')
                    basis.update(struct.pack('<6H',pole,unit,x,y,labels[x],actual));points_count+=1
                for a,d,xs,keys in ks:
                    D=unit*d%Q;delta=next(k for k in range(1,Q) if 6*k%Q==D);source=a;xs=list(xs);keys=list(keys)
                    if delta>51:source=(a+6*d)%Q;delta=Q-delta;xs.reverse();keys.reverse()
                    field_start=(pole+unit*source)%Q;start=next(n for n in range(1,614,6) if n%Q==field_start)
                    seq=[start+6*delta*j for j in range(7)];res=[n%618 for n in seq]
                    need(max(seq)<=2449 and len(set(res))==7,'actual kernel lift')
                    need(all(n%Q==mapping[x] and n%Q!=pole and key(n%Q,roots)==k^flip for x,k,n in zip(xs,keys,seq,strict=True)),'actual kernel points')
                    aps.update(struct.pack('<4H7H7H',pole,unit,start,6*delta,*seq,*res));max_integer=max(max_integer,max(seq));ap_count+=1
        result=dict(author='six-vdw-1',role='researcher',status='ENTIRE10506_AFFINE_INPUT_BASES_AND_ORIGINAL_KERNEL_APS_CHECKED',configurations=configs,actual_field_points=points_count,actual_character_values=3*points_count,original_cyclic618_and_integer2449_APs=ap_count,original_AP_points=7*ap_count,entire_affine_input_basis_sha256=basis.hexdigest(),entire_original_kernel_AP_transcript_sha256=aps.hexdigest(),maximum_actual_integer=max_integer,all_root_columns_nonperiodically_free=True,all_pole_columns_nonperiodically_free=True,numerical_W_improvement=False)
    else:
        phases=[1] if args.mode=='packs' else list(range(1,7));transcript=hashlib.sha256();cases=aps=points_count=max_integer=0
        for unit in range(1,Q):
            roots=[unit*r%Q for r in (1,2,4)];flip=7*CHARS[unit]
            for word,leaves in packs:
                actual_word=sum(((word>>(k^flip))&1)<<k for k in range(8))
                for phase in phases:
                    occupied=set();cases+=1
                    for a,d,xs,keys,color in leaves:
                        D=unit*d%Q;delta=next(k for k in range(1,Q) if 6*k%Q==D);source=a;xs=list(xs)
                        if delta>51:source=(a+6*d)%Q;delta=Q-delta;xs.reverse()
                        A=unit*source%Q;start=next(n for n in range(phase,phase+613,6) if n%Q==A)
                        seq=[start+6*delta*j for j in range(7)];res=[n%618 for n in seq];physical=[n%Q for n in seq]
                        colors=[(actual_word>>key(y,roots))&1 for y in physical]
                        need(max(seq)<=phase+2448 and len(set(res))==7,'original phase integer/cyclic lift')
                        need(physical==[unit*x%Q for x in xs] and all(y!=0 for y in physical),'original field/pole transport')
                        need(colors==[color]*7 and not occupied.intersection(physical),'original color/disjoint')
                        occupied.update(physical);transcript.update(struct.pack('<6H7H7H7B',unit,word,actual_word,phase,start,6*delta,*seq,*res,*colors));aps+=1;points_count+=7;max_integer=max(max_integer,max(seq))
                    need(len(occupied)==35,'full transported pack')
        result=dict(author='six-vdw-1',role='researcher',status='ALL102_SCALES128_TABLES_ORIGINAL_FIVE_PACKS_CHECKED',scales=102,gauged_tables=128,physical_phases=phases,literal_cases=cases,original_cyclic618_and_integer_APs=aps,original_AP_points=points_count,maximum_actual_integer=max_integer,entire_original_pack_transcript_sha256=transcript.hexdigest(),all10506_translated_five_packs_by_ordinary_basis_substitution=True,literal_iteration_is_not_claimed_for_all_translated_packs=True,repair_column_lower_bound=5,cyclic_point_edit_lower_bound=5*len(phases),integer_all_phase_bound=2454 if len(phases)==6 else 2449,optimum_claim=False,numerical_W_improvement=False)
    need(result==expected,'WHOLE native mathematical record mismatch '+args.mode)
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
