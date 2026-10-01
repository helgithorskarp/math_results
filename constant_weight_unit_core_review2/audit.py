"""Complete independent carriers, literal tree validation and native exclusions."""
from pathlib import Path
from itertools import combinations,product
from hashlib import sha256
from copy import deepcopy
import argparse,json,subprocess,time,resource
import carrier
from exact import insist,encoded

class Incomplete(RuntimeError):pass

def check_tree(rows,columns,tree,cap=200000):
    rows=tuple(rows);s=frozenset(rows);cols=tuple(carrier.edges(q) for q in columns)
    insist(len(rows)==len(s) and len(columns)==len(set(columns)),'duplicate normalized input')
    insist(all(len(q)==6 and q<=s for q in cols),'bad matrix column')
    nodes=0;start=time.monotonic()
    def visit(left,node):
        nonlocal nodes
        nodes+=1
        if nodes>cap or (nodes%128==0 and time.monotonic()-start>10):raise Incomplete('INCOMPLETE literal certificate guard')
        insist(bool(left),'a rejection tree reached a positive complete cover')
        insist(type(node)is list and len(node)==2 and type(node[0])is int and type(node[1])is list,'malformed proof node')
        pivot,children=node
        insist(0<=pivot<len(rows) and rows[pivot] in left,'pivot absent or out of range')
        actual={i for i,q in enumerate(cols) if rows[pivot] in q and q<=left}
        supplied=[]
        for child in children:
            insist(type(child)is list and len(child)==2 and type(child[0])is int,'malformed proof branch')
            supplied.append(child[0])
        insist(len(supplied)==len(set(supplied)) and set(supplied)==actual,'missing, repeated or extraneous complete branch')
        for i,child in children:visit(left-cols[i],child)
    visit(s,tree)
    return nodes

def native(work,rows,columns,name='matrix',exe='partition',cap=None):
    pair_index={e:i for i,e in enumerate(carrier.P)};wanted=set(rows)
    missing=[i for e,i in pair_index.items() if e not in wanted]
    words=[sum(1<<x for x in q) for q in columns]
    inp=work/(name+'.input');out=work/(name+'.jsonl')
    inp.write_text(f'17 {len(words)} 1\n'+'\n'.join(map(str,words))+'\n0 '+str(len(missing))+' '+' '.join(map(str,missing))+'\n')
    cmd=[str((work/exe).resolve()),str(inp.resolve()),str(out.resolve())]
    if cap is not None:cmd.append(str(cap))
    p=subprocess.run(cmd,capture_output=True,text=True,timeout=15)
    if p.returncode:raise Incomplete(p.stderr.strip())
    summary=json.loads(p.stdout);records=[json.loads(s) for s in out.read_text().splitlines()]
    insist(summary['status']=='COMPLETE' and summary['cases']==1 and len(records)==1,'incomplete native output')
    j=records[0];insist(j['index']==0 and j['states']==summary['states'] and len(j['covers'])==summary['covers'],'native normalization')
    for cover in j['covers']:
        insist(len(cover)==len(set(cover)),'duplicate cover words')
        actual=[tuple(x for x in range(17) if w>>x&1) for w in cover]
        insist(all(q in columns for q in actual),'unknown native word')
        pairs=[e for q in actual for e in carrier.edges(q)]
        insist(len(pairs)==len(set(pairs)) and set(pairs)==wanted,'literal native complete cover')
    return j

def affine_family():
    def mul(a,b):
        r=0
        for i in range(2):
            if b>>i&1:r^=a<<i
        return r^7 if r&4 else r
    vertical=[tuple(range(4*x,4*x+4)) for x in range(4)]
    rest=[tuple(4*x+(mul(m,x)^b) for x in range(4)) for m in range(4) for b in range(4)]
    results=[]
    for choices in product(range(4),repeat=4):
        removed=tuple(4*x+choices[x] for x in range(4))
        words=tuple(sorted(rest+[tuple(sorted((set(vertical[x])-{removed[x]})|{16})) for x in range(4)]))
        insist(len(words)==len(set(words))==20 and all(len(q)==4 for q in words),'affine word fixture')
        all_pairs=[e for q in words for e in carrier.edges(q)]
        insist(len(all_pairs)==len(set(all_pairs))==120,'affine fixture pair packing')
        rep=[sum(x in q for q in words) for x in range(17)];high=tuple(x for x in range(17) if rep[x]==4)
        insist(sorted(rep)==[4]*5+[5]*12 and set(high)==set(removed)|{16},'affine unit replication profile')
        leave=frozenset(set(carrier.P)-set(all_pairs));core=tuple(e for e in leave if set(e)<=set(high))
        insist(set(core)=={(x,16) for x in removed},'affine high-core four-edge star')
        results.append(words)
    insist(len(results)==len(set(results))==256,'affine transversal family distinctness')
    return results

def controls(work,cases7,cases8,cert7,cert8):
    fixture=affine_family()[0];rows=tuple(sorted(set(e for q in fixture for e in carrier.edges(q))))
    positive=native(work,rows,fixture,'affine-positive')
    masks=sorted(sum(1<<x for x in q) for q in fixture)
    insist(positive['covers']==[masks] and (15,16) in rows,'native136th-pair-bit positive control')
    failures=0
    def rejects(function):
        nonlocal failures
        try:function()
        except (ValueError,RuntimeError,TypeError,IndexError):failures+=1;return
        raise ValueError('corrupted proof was accepted')
    row,col=cases7[0][1:];root=cert7['trees'][0]
    bad=deepcopy(root);bad[1]=bad[1][1:];rejects(lambda:check_tree(row,col,bad))
    bad=deepcopy(root);bad[1].append(deepcopy(bad[1][0]));rejects(lambda:check_tree(row,col,bad))
    bad=deepcopy(root);bad[0]=len(row);rejects(lambda:check_tree(row,col,bad))
    bad=deepcopy(root);bad[1][0][0]=len(col);rejects(lambda:check_tree(row,col,bad))
    rejects(lambda:check_tree(row,col,[root[0],[]]))
    rejects(lambda:check_tree(row,col,[True,[]]))
    rows4=tuple(combinations(range(4),2));cols4=((0,1,2,3),)
    rejects(lambda:check_tree(rows4,cols4,[0,[]]))
    rejects(lambda:check_tree(rows4,cols4,[0,[[0,[1,[]]]]]))
    try:check_tree(row,col,root,cap=0)
    except Incomplete as e:insist('INCOMPLETE' in str(e),'literal guard not visible')
    else:raise ValueError('zero literal guard accepted')
    try:native(work,rows,fixture,'affine-zero',cap=0)
    except Incomplete as e:insist('INCOMPLETE' in str(e),'native guard not visible')
    else:raise ValueError('zero native guard accepted')
    source=Path(__file__).with_name('partition.cpp')
    subprocess.run(['g++','-std=c++17','-O1','-g','-fsanitize=address,undefined','-fno-sanitize-recover=all',str(source),'-o',str(work/'partition-sanitized')],check=True,timeout=45)
    sanitized=native(work,rows,fixture,'affine-sanitized',exe='partition-sanitized')
    insist(sanitized['covers']==positive['covers'],'sanitizer positive comparison')
    proof=native(work,cases7[0][1],cases7[0][2],'negative-sanitized',exe='partition-sanitized')
    insist(not proof['covers'],'sanitized negative cover')
    # Invalid dimensions / duplicate columns / out-of-range or repeated pairs.
    invalid=['18 0 0\n','17 2 0\n15\n15\n','17 1 1\n15\n0 1 136\n','17 1 1\n15\n0 2 135 135\n']
    for text in invalid:
        inp=work/'invalid.input';out=work/'invalid.jsonl';inp.write_text(text)
        p=subprocess.run([str((work/'partition').resolve()),str(inp),str(out)],text=True,capture_output=True,timeout=15)
        insist(p.returncode!=0,'invalid native input accepted')
    return {'false_or_corrupted_trees_rejected':failures,'native_invalid_inputs_rejected':len(invalid),
            'literal_zero_guard_incomplete':True,'native_zero_guard_incomplete':True,
            'sanitized136_pair_bit_positive_and_actual_negative':True,'affine_transversals':256,'affine_high_core_edges':4,'fixture':fixture}

def run(args):
    started=time.monotonic();args.work.mkdir(parents=True,exist_ok=True)
    pinned=json.loads(Path(__file__).with_name('INPUT.json').read_text())
    for q in pinned['target_runtime']:
        raw=(args.target/q['filename']).read_bytes()
        insist(len(raw)==q['bytes'] and sha256(raw).hexdigest()==q['sha256'],'pinned target input differs')
    source=Path(__file__).with_name('partition.cpp')
    subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-Wpedantic',str(source),'-o',str(args.work/'partition')],check=True,timeout=45)
    high=carrier.cores();cases8,summary8=carrier.eight();cases7,summary7,zero=carrier.seven()
    e8=json.loads((args.target/'unit_eight_expected.json').read_text());e7=json.loads((args.target/'unit_seven_expected.json').read_text())
    c8=json.loads((args.target/'unit_eight_certificate.json').read_text());c7=json.loads((args.target/'unit_seven_certificate.json').read_text())
    insist(len(cases8)==len(c8['cases'])==7 and len(cases7)==len(c7['trees'])==3688,'complete instance count')
    insist(carrier.digest(cases8)==e8['input_stream_sha256']==c8['carrier_summary'].get('input_stream_sha256',e8['input_stream_sha256']),'eight full matrix stream differs')
    insist(carrier.digest(cases7)==e7['input_stream_sha256']==c7['input_stream_sha256'],'seven full matrix stream differs')
    expected_summary=[{k:v for k,v in branch.items() if k not in ('rows','column_range','nodes','maximum_nodes_per_case')} for branch in e7['branches']]
    insist(encoded(summary7)==encoded(expected_summary) and carrier.digest(summary7)==c7['carrier_summary_sha256'],'complete seven carriers differ')
    insist(summary8['raw_frames']==2448 and summary8['group_order']==3072 and summary8['orbits']==7,'eight carrier census')
    for k in ('group_sha256','raw_frames_sha256'):insist(summary8[k]==c8['carrier_summary'][k],'eight literal domain differs')
    (args.work/'matrices.json').write_bytes(encoded({'seven':cases7,'eight':cases8}))
    totals=[]
    for mode,cases,certificate,expected in [('eight',cases8,c8,e8),('seven',cases7,c7,e7)]:
        nodes=[];native_states=[]
        for i,(prefix,rows,columns) in enumerate(cases):
            tree=certificate['trees'][i] if mode=='seven' else certificate['cases'][i]['tree']
            if mode=='eight':
                insist(encoded(prefix)==encoded(certificate['cases'][i]['fixed_quads']) and carrier.digest([prefix,rows,columns])==certificate['cases'][i]['input_sha256'],'eight actual certificate input differs')
            nodes.append(check_tree(rows,columns,tree));result=native(args.work,rows,columns)
            insist(not result['covers'],'independent native search found a cover')
            native_states.append(result['states'])
            if i%500==0:print({'mode':mode,'complete_cases':i+1,'total':len(cases)},flush=True)
        insist(sum(nodes)==expected['nodes'] and max(nodes)==expected['maximum_nodes_per_case'],'complete literal certificate node census')
        totals.append({'mode':mode,'cases':len(cases),'input_stream_sha256':carrier.digest(cases),'literal_nodes':sum(nodes),'max_literal_nodes':max(nodes),'native_states':sum(native_states),'max_native_states':max(native_states),'native_state_stream_sha256':carrier.digest(native_states)})
    checks=controls(args.work,cases7,cases8,c7,c8)
    result={'agent':'six-reviewer-2','role':'independent mathematical reviewer','status':'COMPLETE independent all-unit high-core upper6 and upper7 dependency audit',
            'high_core_class_counts':[len(high[e]) for e in range(4,11)],
            'k4_free_class_counts':[sum(not q['has_k4'] for q in high[e]) for e in range(4,11)],
            'eight_carrier':summary8,'seven_carrier':summary7,'zero_incidence_assignment':zero,'exclusions':totals,'controls':checks,
            'local_extremal_interval':[4,6],'sharpness6':'not established','global_A18_6_5_interval':[69,72]}
    raw=encoded(result)
    if args.record:args.expected.write_bytes(raw)
    else:insist(raw==args.expected.read_bytes(),'complete stable expected record differs')
    metrics={'status':result['status'],'expected_sha256':sha256(raw).hexdigest(),'seconds':time.monotonic()-started,
             'parent_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'child_peak_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}
    (args.work/'metrics.json').write_bytes(encoded(metrics));print(json.dumps(metrics,sort_keys=True),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    p.add_argument('--target',type=Path,default=Path(__file__).resolve().parents[1]/'constant_weight_18_6_5_equality_structure')
    p.add_argument('--expected',type=Path,default=Path(__file__).with_name('expected.json'));p.add_argument('--record',action='store_true');run(p.parse_args())
