"""Full original-phase and BASE gluing of the sole relaxed survivor."""
import argparse
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
from struct import pack

PREFIX=((8,0),(9,0),(10,1),(14,0),(12,10),(28,4))

def require(ok,message):
    if not ok:raise ValueError(message)


def build(raw=None):
    R=[x for x in range(2520) if all(x%m!=a for m,a in PREFIX)]
    require(len(R)==1396,'Initial physical BASE holes changed')
    index={x:i for i,x in enumerate(R)}
    blocks=[]
    for r,moduli,placed,threshold in ((2,(80,144,240),(16,2),72),(6,(48,96),(32,6),90),(4,(112,336),None,15)):
        xs=[x for x in R if x%8==r]
        phases=[list(range(r,m,8)) for m in moduli]
        masks=[[sum(1<<(4*i+k) for i,x in enumerate(xs) for k in range(4) if (x+2520*k)%m==a) for a in aa]
               for m,aa in zip(moduli,phases)]
        fixed=0 if placed is None else sum(1<<(4*i+k) for i,x in enumerate(xs) for k in range(4) if (x+2520*k)%placed[0]==placed[1])
        anchor=sum(1<<(4*i) for i in range(len(xs)))
        values=[];qualifying=[]
        for inds in product(*(range(len(p)) for p in phases)):
            union=fixed
            for p,i in zip(masks,inds):union|=p[i]
            repaired=union&(union>>1)&(union>>2)&(union>>3)&anchor
            count=repaired.bit_count();values.append(count)
            if count>=threshold:
                require(count==threshold,'Prior exceptional parent capacity violated')
                shape=[x for i,x in enumerate(xs) if repaired&(1<<(4*i))]
                qualifying.append([[p[i] for p,i in zip(phases,inds)],shape])
        blocks.append({'parent':r,'original_moduli':list(moduli),'phase_lists':phases,'placed':placed,
                       'all_raw_phase_repair_counts':values,'capacity':max(values),'qualifying_original_phases_and_shapes':qualifying})
    require([len(b['all_raw_phase_repair_counts']) for b in blocks]==[5400,72,588],'Complete original-phase census missing')
    require([len(b['qualifying_original_phases_and_shapes']) for b in blocks]==[40,1,20],'Qualifying original phase count changed')
    combined=[];shapes={}
    for p2,p6,p4 in product(*(b['qualifying_original_phases_and_shapes'] for b in blocks)):
        shape=tuple(sorted(p2[1]+p6[1]+p4[1]));require(len(shape)==177,'Exceptional repair shape must have177 holes')
        phases=p2[0]+p6[0]+p4[0];combined.append([phases,list(shape)])
        shapes[shape]=sum(1<<index[x] for x in shape)
    require(len(combined)==800 and len(shapes)==400,'Whole literal completion/shape census changed')
    originals=[m for m in range(8,2521) if 2520%m==0 and m not in {m for m,a in PREFIX}]
    phase_masks={m:[sum(1<<index[x] for x in range(a,2520,m) if x in index) for a in range(m)] for m in originals}
    allmask=(1<<len(R))-1;gluing=[]
    for xs,shape in sorted(shapes.items()):
        outside=allmask^shape;rows=[];tot=0
        for m in originals:
            values=[];cap=0;valid=[]
            for a,ap in enumerate(phase_masks[m]):
                protected=(ap&shape).bit_count();needed=(ap&outside).bit_count()
                values.append([protected,needed])
                if protected==0:valid.append(a);cap=max(cap,needed)
            # Omission always allowed: if no phase avoids S, this ORIGINAL
            # contributes0 and cannot appear in a hypothetical covering.
            data=b''.join(pack('>HH',*v) for v in values)
            if raw is not None:raw.extend(data)
            stream=sha256(data).hexdigest()
            rows.append([m,len(values),stream,valid,cap]);tot+=cap
        gluing.append({'protected_shape':list(xs),'shape_size':len(xs),'outside_holes':outside.bit_count(),
                       'all_original_phase_blocks':rows,'sum_max_outside':tot})
    return {'agent':'six-covering-2','role':'researcher','status':'AUTHOR-CHECKED complete exceptional phase/BASE gluing; independent review pending',
            'full_marked_prefix':[[8,0],[9,0],[10,1],[14,0],[12,10],[16,2],[28,4],[32,6]],
            'originals_divide10080':True,'minimum_exactly8':True,'essential_originals_explicit':[16,32],
            'productive_inventory':[16,32,48,80,96,112,144,240,336],
            'all_parent_full_physical_phase_blocks':blocks,'all_800_original_phase_completions':combined,
            'all_400_BASE_gluing_shapes':gluing,'all_original_phase_streams_encoding':'ordered a0..m-1; big-endian unsigned16 protected then outside counts',
            'gluing_maximum':max(g['sum_max_outside'] for g in gluing),'gluing_minimum':min(g['sum_max_outside'] for g in gluing),
            'outside_required':1219,'BASE177_public9934_imported':True,'capacity_sharpness_claimed':False,
            'new_tenth_tail_bound_claimed':False,'ordinary_proof_formalized':False,'independent_reviewer':False,'global_bound_changed':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--raw-stream',type=Path);a=p.parse_args();raw=bytearray() if a.raw_stream is not None else None;r=build(raw=raw)
    if a.raw_stream is not None:a.raw_stream.write_bytes(raw)
    a.out.write_text(json.dumps(r,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'whole_sha256':sha256(json.dumps(r,sort_keys=True,separators=(',',':')).encode()).hexdigest(),
        'gluing_range':[r['gluing_minimum'],r['gluing_maximum']],'required':r['outside_required'],
        'full_original_phase_tuples':sum(len(b['all_raw_phase_repair_counts']) for b in r['all_parent_full_physical_phase_blocks']),
        'all_BASE_phase_entries':sum(row[1] for g in r['all_400_BASE_gluing_shapes'] for row in g['all_original_phase_blocks'])}))
