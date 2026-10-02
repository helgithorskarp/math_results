"""Complete ordered positive-check merge; bulky literal digests stay private."""
import hashlib,json
from geometry import canonical,need,orbit_cover

def merge(parts):
    cover=orbit_cover(103);reps=[o[0]for o in cover];offset=0;cases=[];samples=[];totals={k:0 for k in('representative_APs','representative_points','all_raw_states','all_transported_APs','all_transported_points')};flips={'0':0,'1':0};maxend=0;certificate=None;repdigest=None
    need(type(parts)is list and len(parts)==9,'all nine positive ranges')
    for p in parts:
        need(type(p)is dict and p['case_start']==offset and p['case_end']==min(offset+256,2176),'complete contiguous nonoverlapping case ranges')
        if certificate is None:certificate=p['whole_certificate_sha256'];repdigest=p['whole_representatives_sha256']
        need(p['whole_certificate_sha256']==certificate and p['whole_representatives_sha256']==repdigest,'same entire neutral certificate and full representative domain')
        need(p['nine_disjoint_regular_columns_verified']is True,'positive completion status')
        local=p['case_transcript_digests'];end=p['case_end'];need(len(local)==end-offset,'all whole cases present')
        rawcount=0
        for k,state,size,digest in local:
            need(type(k)is int and k==offset and tuple(state)==reps[k] and type(size)is int and size==len(cover[k]),'entry-level state/root-count/orbit coverage')
            need(type(digest)is str and len(digest)==64 and all(c in'0123456789abcdef'for c in digest),'whole literal transcript digest')
            rawcount+=size;cases.append([k,state,size,digest]);offset+=1
        need(p['all_raw_states']==rawcount and p['all_transported_APs']==9*rawcount and p['all_transported_points']==63*rawcount,'all actual raw-state AP/point totals')
        need(p['representative_APs']==9*len(local) and p['representative_points']==63*len(local),'all actual representative AP/point totals')
        need(sum(p['flip_histogram'].values())==rawcount,'entire output flip coverage')
        for k in totals:totals[k]+=p[k]
        for k,v in p['flip_histogram'].items():flips[str(k)]+=v
        maxend=max(maxend,p['maximum_literal_lift_endpoint']);samples+=p['positive_samples']
    need(offset==2176 and totals==dict(zip(totals,(19584,137088,12938,116442,815094))),'complete2176-class/12938-state positive verification')
    return {'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','schema':1,'status':'COMPLETE_INDEPENDENT_BOOLEAN618_AP9_REPRODUCTION',
            'whole_certificate_sha256':certificate,'whole_representatives_sha256':repdigest,
            'ordered_case_transcript_root_sha256':hashlib.sha256(b''.join(canonical(z)for z in cases)).hexdigest(),
            'total_cases':2176,**totals,'flip_histogram':flips,'maximum_literal_lift_endpoint':maxend,
            'positive_samples':samples,'root_counts_retained':True,'all_original_ignored_roots_excluded':True,
            'encoding':'SHA256 of ordered newline sorted compact JSON [index,own_state,orbit_size,whole_case_transcript_digest]; different deterministic inverse transports from native',
            'trust':'exact ordinary Python and independent ordinary proof bridges, no solver or proof assistant; positive CSV is fully decoded and each AP point checked'}
