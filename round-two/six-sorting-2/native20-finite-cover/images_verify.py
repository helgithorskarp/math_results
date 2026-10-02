"""Independent complete image reduction and weighted-tree checks.
Bulk column truth tables and balanced-subset trees differ from row exchanges
and stepwise merge enumeration in the producer.
"""
import hashlib,json,resource,struct,sys,time
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import os
HERE=Path(__file__).resolve().parent
ROOT=Path(os.environ.get('NATIVE20_WORKDIR','scratch/native20-evidence')).resolve()
ROOT.mkdir(parents=True,exist_ok=True)
PREV=ROOT
EXPAND=tuple(struct.pack('<8H',*[b>>j&1 for j in range(8)]) for b in range(256))
def need(ok,msg):
    if not ok:raise ValueError(msg)
def encode(values):return b''.join(int(x).to_bytes(2,'little') for x in values)
def columns(image):return [sum(1<<i for i,x in enumerate(image) if x>>p&1) for p in range(13)]
def apply(cols,word):
    cols=list(cols)
    for a,b in word:
        need(0<=a<b<13,'nonstandard literal gate')
        cols[a],cols[b]=cols[a]&cols[b],cols[a]|cols[b]
    return cols
def spread(col,count):
    return int.from_bytes(b''.join(EXPAND[b] for b in col.to_bytes((count+7)//8,'little')),'little')
def decode(cols,count):
    packed=sum(spread(col,count)<<p for p,col in enumerate(cols))
    return sorted(set(struct.unpack('<'+'H'*count,packed.to_bytes(2*count,'little'))))
def h22_image():
    word=json.loads((PREV/'p20-intake.json').read_text())['cases'][1]['gates']
    outputs=[]
    for x in range(8192):
        row=[x>>p&1 for p in range(13)]
        for a,b in word:row[a],row[b]=min(row[a],row[b]),max(row[a],row[b])
        outputs.append(sum(y<<p for p,y in enumerate(row)))
    image=sorted(set(outputs));need(len(image)==209,'numeric full H22 image differs')
    return image
def keyprofile(case):return tuple(map(tuple,case['low'])),tuple(map(tuple,case['high']))
def joint():
    start=time.monotonic()
    verified=json.loads((ROOT/'verify-phase-tf.json').read_text())
    need(verified['status']=='NUMERIC_PHASE_AND_DNF_FUNCTION_COVER_VERIFIED','phase/function verification missing')
    tfdata=json.loads((ROOT/'tf-cover.json').read_text())['TF']
    phase=json.loads((PREV/'pre6-cover.json').read_text())
    packet=json.loads((ROOT/'joint-cover.json').read_text());records=packet['joint_roots']
    image=h22_image();count=len(image);base=columns(image)
    expected={};all_cases=0;matching=set()
    recordkeys={}
    for i,r in enumerate(records):
        k=(keyprofile(r),encode(r['full_image']))
        need(k not in recordkeys,'duplicate joint profile/image')
        need(r['prefix_length']==22+len(r['word']),'joint prefix length differs')
        tf=tfdata[r['tf_index']];gate=list(sorted((6,r['partner'])))
        need(r['word']==tf['word']+[gate] and r['state_id']==tf['state_id'],'joint provenance differs')
        need(r['partner']!=4,'excluded partner4 retained')
        recordkeys[k]=i
    for ti,tf in enumerate(tfdata):
        cols=apply(base,tf['word'])
        expanded=[spread(col,count)<<p for p,col in enumerate(cols)]
        packed=sum(expanded)
        for case in phase['first6_cases'][tf['state_id']]['cases']:
            r=case['partner']
            if r==4:continue
            a,b=sorted((6,r))
            low=cols[a]&cols[b];high=cols[a]|cols[b]
            result=packed-expanded[a]-expanded[b]+(spread(low,count)<<a)+(spread(high,count)<<b)
            actual=sorted(set(struct.unpack('<'+'H'*count,result.to_bytes(2*count,'little'))))
            k=(keyprofile(case),encode(actual));length=22+len(tf['word'])+1
            need(k in recordkeys,'actual joint image omitted')
            i=recordkeys[k];chosen=records[i]
            need(chosen['prefix_length']<=length,'joint folding increased length')
            expected[k]=min(expected.get(k,1000),length)
            if chosen['tf_index']==ti and chosen['partner']==r:
                need(chosen['low']==case['low'] and chosen['high']==case['high'],'chosen joint profiles differ')
                matching.add(i)
            all_cases+=1
    need(len(expected)==len(records)==len(matching),'unreachable or incorrect joint representative')
    need(all(records[i]['prefix_length']==length for k,length in expected.items() for i in [recordkeys[k]]),'joint representative not shortest in covered family')
    result={'agent':'six-sorting-2','role':'researcher','status':'BULK_COLUMN_ALL_JOINT_IMAGES_AND_MINIMUM_LENGTHS_VERIFIED','complete_h22_inputs':8192,'h22_full_image':count,'all_joint_cases':all_cases,'distinct_profile_images':len(expected),'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'boundary':'Exact phase/full-function checks imported from this standalone checker. Bulk truth columns independently replay every conditional Boolean row; no producer function imported. No suffix exclusion.'}
    (ROOT/'verify-joint.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True),flush=True)
def live(rows,side):
    out=[]
    for lo,hi,d in rows:
        mask=(lo if side=='low' else hi)&~(1<<(0 if side=='low' else 12))
        need(mask and not mask&(mask-1),'secondary not singleton')
        out.append((mask.bit_length()-1,d))
    return tuple(sorted(out))
def scalar_signature(word,ports):
    index={p:i for i,p in enumerate(ports)};n=len(ports);result=[]
    for x in range(1<<n):
        values=[x>>p&1 for p in range(n)]
        for a,b in word:
            i,j=index[a],index[b]
            values[i],values[j]=min(values[i],values[j]),max(values[i],values[j])
        result.append(sum(y<<p for p,y in enumerate(values)))
    return tuple(result)
@lru_cache(None)
def weighted_trees(initial,side):
    ports=[p for p,d in initial];weights=[2**d for p,d in initial];n=len(ports)
    need(sum(weights)==512,'tree total not512')
    @lru_cache(None)
    def recurse(mask):
        if not mask&(mask-1):return ((),)
        first=mask&-mask
        total=sum(weights[i] for i in range(n) if mask>>i&1)
        need(not total&(total-1),'subtree weight is not a power of two')
        out=[];part=(mask-1)&mask
        while part:
            other=mask^part
            if part&first and sum(weights[i] for i in range(n) if part>>i&1)==total//2:
                pa=[ports[i] for i in range(n) if part>>i&1];pb=[ports[i] for i in range(n) if other>>i&1]
                a=min(pa) if side=='low' else max(pa)
                b=min(pb) if side=='low' else max(pb)
                gate=tuple(sorted((a,b)))
                for wa in recurse(part):
                    for wb in recurse(other):out.append(wa+wb+(gate,))
            part=(part-1)&mask
        need(out,'balanced weighted partition missing')
        return tuple(out)
    allwords=recurse((1<<n)-1)
    functions={}
    for word in allwords:
        need(len(word)==n-1,'tree event length differs')
        signature=scalar_signature(word,ports)
        functions.setdefault(signature,[list(g) for g in word])
    return functions
def post():
    start=time.monotonic()
    verified=json.loads((ROOT/'verify-joint.json').read_text())
    need(verified['status']=='BULK_COLUMN_ALL_JOINT_IMAGES_AND_MINIMUM_LENGTHS_VERIFIED','joint verification missing')
    families=json.loads((ROOT/'postjoint-family-covers.json').read_text());covers={}
    for f in families:
        initial=tuple(map(tuple,f['initial']));side=f['kind'];ports=[p for p,d in initial]
        actual=weighted_trees(initial,side)
        observed={}
        for word in f['words']:
            need(len(word)==len(ports)-1,'event representative too long')
            sig=scalar_signature(word,ports)
            need(sig in actual,'event word not in complete balanced-tree functions')
            observed[sig]=word
        need(set(observed)==set(actual) and len(observed)==len(f['words']),'event functions missing or repeated')
        covers[initial,side]=list(actual.values())
    joint=json.loads((ROOT/'joint-cover.json').read_text())['joint_roots']
    packet=json.loads((ROOT/'postjoint-cover.json').read_text());records=packet['roots']
    observed={encode(r['middle_image']):r for r in records}
    need(len(observed)==len(records),'duplicate nine-core image')
    expected={};all_pairs=0
    for ji,r in enumerate(joint):
        image=r['full_image'];count=len(image);base=columns(image)
        lows=covers[live(r['low'],'low'),'low'];highs=covers[live(r['high'],'high'),'high']
        for lw in lows:
            lowcols=apply(base,lw)
            for hw in highs:
                cols=apply(lowcols,hw);actual=decode(cols,count)
                for x in actual:
                    weight=x.bit_count();sorted_x=((1<<weight)-1)<<(13-weight)
                    need((x&6147)==(sorted_x&6147),'four held outputs incorrect')
                middle=sorted({(x>>2)&511 for x in actual});key=encode(middle)
                length=r['prefix_length']+len(lw)+len(hw)
                need(key in observed,'actual nine-core image omitted')
                need(observed[key]['prefix_length']<=length,'nine-image folding increased length')
                expected[key]=min(expected.get(key,1000),length);all_pairs+=1
    need(len(expected)==len(records),'unreachable nine-core image')
    base_image=h22_image();base_cols=columns(base_image)
    for record in records:
        ji=record['joint_root'];parent=joint[ji]
        need(record['prefix_length']==22+len(record['word']) and record['suffix_budget']==44-record['prefix_length'],'nine-root budget differs')
        need(record['word'][:len(parent['word'])]==parent['word'],'nine-root parent prefix differs')
        actual=decode(apply(base_cols,record['word']),len(base_image))
        for x in actual:
            weight=x.bit_count();sorted_x=((1<<weight)-1)<<(13-weight)
            need((x&6147)==(sorted_x&6147),'chosen root outer outputs differ')
        need(sorted({(x>>2)&511 for x in actual})==record['middle_image'],'chosen nine-root literal image differs')
        need(record['prefix_length']==expected[encode(record['middle_image'])],'nine representative not shortest in covered family')
    ordered=sorted(records,key=lambda x:(x['prefix_length'],x['middle_image']))
    digest=hashlib.sha256()
    for r in ordered:digest.update(bytes([r['suffix_budget']])+encode(r['middle_image'])+b'\xff\xff')
    result={'agent':'six-sorting-2','role':'researcher','status':'BALANCED_SUBSET_TREE_AND_ALL_NINE_CORE_IMAGES_VERIFIED','family_profiles':len(covers),'joint_roots':len(joint),'all_postjoint_compositions':all_pairs,'distinct_nine_core_images':len(records),'root_image_budget_sha256':digest.hexdigest(),'seconds':time.monotonic()-start,'maximum_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'boundary':'Balanced equal-weight subset trees differ from producer stepwise merge recursion. Numeric truth signatures check complete canonical event function sets; bulk columns check every literal conditional image, held outer output and minimum covered prefix length. Unformalized normalization bridges and imported S11>=35 remain explicit. Residual suffixes are not excluded.'}
    (ROOT/'verify-postjoint.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True),flush=True)
if __name__=='__main__':
    {'joint':joint,'post':post}[sys.argv[1]]()
