"""Whole public-source integrity only. No closed mathematical replay."""
import hashlib
import json
import pathlib
from fractions import Fraction

HERE=pathlib.Path(__file__).resolve().parent

def require(condition,message):
    if not condition:raise ValueError(message)

def sha(raw):return hashlib.sha256(raw).hexdigest()

def manifest(name):
    result={}
    for line in (HERE/name).read_text().splitlines():
        parts=line.split('  ')
        require(len(parts)==2,'manifest syntax')
        digest,file=parts
        require(len(digest)==64 and all(c in '0123456789abcdef' for c in digest) and pathlib.Path(file).name==file and file not in result,'manifest record')
        result[file]=digest
    for name,digest in result.items():
        require((HERE/name).is_file() and not (HERE/name).is_symlink(),'regular compact public source')
        require(sha((HERE/name).read_bytes())==digest,'whole source seal: '+name)
    return result

def main():
    pins=manifest('SHA256SUMS')
    if (HERE/'MANIFEST.sha256').exists():
        outer=manifest('MANIFEST.sha256')
        require(set(outer)=={x.name for x in HERE.iterdir() if x.is_file() and x.name!='MANIFEST.sha256' and not x.name.startswith('generated-') and x.name not in ('RECORD.json','VALIDATION.json')},'entire final public census')
    source=json.loads((HERE/'SOURCE.json').read_text())
    for name,digest in source['owned_exact_source_bytes'].items():
        require(sha((HERE/name).read_bytes())==digest,'whole unchanged scientific source')
    editorial=json.loads((HERE/'EDITORIAL.json').read_text())
    proof=(HERE/'PROOF.md').read_text()
    for edit in reversed(editorial['complete_proof_edits']):
        require(proof.count(edit['new'])==edit['count'],'whole editorial replacement cardinality')
        proof=proof.replace(edit['new'],edit['old'])
    require(sha(proof.encode())==editorial['private_complete_proof_sha256'],'entire complete proof reversal')
    entry=(HERE/'ENTRY.md').read_text()
    require(entry.startswith(editorial['entry_prefix']),'entry proof prefix')
    require(entry.endswith(editorial['entry_suffix']), 'entry proof suffix')
    excerpt=entry[len(editorial['entry_prefix']):-len(editorial['entry_suffix'])].encode()
    require(len(excerpt)==editorial['entry_math_excerpt_bytes'] and sha(excerpt)==editorial['entry_math_excerpt_sha256'],'entire unchanged entry mathematics')
    summary=json.loads((HERE/'SUMMARY.json').read_text())
    evidence=json.loads((HERE/'EVIDENCE.json').read_text())
    require(summary['roles']==dict(scalar=79,mean=9,standard=2,joint=49) and sum(summary['roles'].values())==summary['coverage']['leaves']==139,'complete role/coverage projection')
    require(summary['complete_record_sha256']==evidence['face_record_sha256'] and summary['complete_record_bytes']==evidence['face_record_bytes']==3070840,'entire face-record metadata binding')
    require(Fraction(summary['refinement']['epsilon'])==Fraction(1,340) and Fraction(summary['refinement']['polar_strict_margin'])>0 and Fraction(summary['refinement']['origin_strict_margin'])>0,'exact projected sufficient refinement')
    for component in ('entry_component','face_component'):
        value=evidence[component]
        require(len(value['replays'])==4 and value['whole_math_record_equal'] and len({r['complete_record_sha256'] for r in value['replays']})==1,'four whole paid mathematical records')
    record=dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',scope='Source integrity ONLY; closed mathematical replays0. Entire original entry/path and new face-source bytes unchanged.',payload_files=len(pins),whole_payload_pins=pins,entire_proof_reversal_sha256=sha(proof.encode()),entry_excerpt_sha256=sha(excerpt),whole_record_metadata_equal=True,face_record_sha256=summary['complete_record_sha256'],closed_mathematical_replays=0)
    print(json.dumps(record,sort_keys=True,separators=(',',':')))

if __name__=='__main__':main()
