"""Optional pinned-input comparison. Inputs are not used by the math checker.

Download frozen public inputs using --download-to DIR, or reuse them using
--input-dir DIR. No imported researcher code is executed by this program.
"""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--download-to',type=Path)
    group.add_argument('--input-dir',type=Path)
    parser.add_argument('--independent',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args();root=Path(__file__).absolute().parent
    source=json.loads((root/'INPUTS.json').read_text());folder=args.download_to or args.input_dir
    data={}
    for entry in source['files']:
        path=folder/entry['label']
        if args.download_to:
            request=urllib.request.Request(entry['raw_url'],headers={'User-Agent':'independent-math-review/1'})
            with urllib.request.urlopen(request,timeout=20) as response:
                if response.status!=200:raise ValueError('source status')
                content=response.read(200001)
            if len(content)>200000:raise ValueError('bounded compact input exceeded')
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(content)
        content=path.read_bytes()
        if len(content)!=entry['bytes'] or hashlib.sha256(content).hexdigest()!=entry['sha256']:
            raise ValueError('frozen input identity differs: '+entry['label'])
        data[entry['label']]=content
    p=json.loads(data['author8975/EXPECTED.json']);a=json.loads(data['author8975/AUDIT_EXPECTED.json'])
    independent=json.loads((args.independent or root/'EXPECTED.json').read_text());matches=[]
    def equal(label,x,y):
        if x!=y:raise ValueError('complete compared field differs: '+label)
        matches.append(label)
    if len(p['censuses'])!=len(a['censuses']) or len(p['censuses'])!=len(independent['censuses']):
        raise ValueError('census length')
    for n,(x,y,z) in enumerate(zip(p['censuses'],a['censuses'],independent['censuses'])):
        for key in ('a','b','f1','f2','ordinary_fives','admitted_records_sha256','terminal_rows_sha256'):
            equal('census%d/primary+audit/%s'%(n,key),x[key],y[key])
            equal('census%d/independent/%s'%(n,key),x[key],z[key])
        for key in ('ordinary_fours','classifications','full_row_records_sha256','raw_ordered_three_neighbor_triples'):
            equal('census%d/primary+independent/%s'%(n,key),x[key],z[key])
        equal('census%d/audit/admitted_classifications'%n,
              {key:v for key,v in z['classifications'].items() if key not in ('COMMON_CONTACT','QQ_SUPPLY')},
              y['admitted_classifications'])
    for branch in ('one_ordinary_original_aliases','two_ordinary_original_aliases'):
        for key in ('canonical_classifications','entrywise_sha256'):
            equal(branch+'/primary+audit/'+key,p[branch][key],a[branch][key])
            equal(branch+'/independent/'+key,p[branch][key],independent[branch][key])
        for key in ('final_QQ_prefixes_sha256','prefixes'):
            if key in p[branch]:equal(branch+'/'+key,p[branch][key],independent[branch][key])
        for key in ('full_F_fan_alignment_words','two_original_fan_quota_audits','full_original_H_fan_quota_audits'):
            if key in a[branch]:equal(branch+'/'+key,a[branch][key],independent[branch][key])
    if len(matches)!=374:raise ValueError('complete comparison coverage')
    context=json.loads(data['author8975/PROFILE_CONTEXT.json']);catalogues=[]
    for name,c in zip(('committed21','source18'),context['catalogues']):
        original=json.loads(data[name])['catalogue_corollary']['remaining_beta_profiles']
        if original!=c['profiles'] or len({json.dumps(x,sort_keys=True) for x in original})!=len(original):
            raise ValueError('original ordered profile identity or uniqueness')
        for row in original:
            r=row['r'];k,f1,f2=row['five_counts_f0_f1_f2'];a4,b4=row['a'],row['b']
            if k+f1+f2!=r or a4+2*b4+f1+2*f2!=6 or row['ordinary_fours']!=15-2*r-a4-b4:
                raise ValueError('original count budget')
        remaining=[x for x in original if x['r']!=3]
        receipt=next(x for x in p['catalogue_corollaries'] if x['name']==c['name'])
        if remaining!=receipt['remaining_profiles']:raise ValueError('conditional profile deletion')
        catalogues.append({'name':c['name'],'prior_counts':[sum(x['r']==r for x in original) for r in (1,2,3)],
                           'remaining_counts':[sum(x['r']==r for x in remaining) for r in (1,2,3)],
                           'prior_derivation_imported_not_regenerated':True})
    record={'status':'VERIFIED','actual_agent':'six-reviewer-3','role':'independent mathematical reviewer',
            'source_files_byte_verified':len(source['files']),'exact_field_equalities':len(matches),
            'catalogue_comparisons':catalogues,'author_modules_executed_or_imported':False,
            'trust':'Source identities and conditional deletion, not proof of prior catalogue or graph registration'}
    if args.output:args.output.write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps(record,sort_keys=True))


if __name__=='__main__':main()
