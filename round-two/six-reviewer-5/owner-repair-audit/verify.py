"""Independent exact physical-triple audit. Stdlib; no author code imports."""
import argparse,hashlib,json,pathlib
import triple_check as t
import audit_packet as a
import bridges,controls,classical_refinement

ROOT=pathlib.Path(__file__).resolve().parent

def run(folder):
    for sealfile in ('first-seal.json','certificate-seal.json'):
        seal=json.loads((ROOT/sealfile).read_text())
        for filename,want in seal['files'].items():
            t.need(hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==want,'historical seal source bytes: '+filename)
    inputs=json.loads((ROOT/'INPUTS.json').read_text())
    for row in inputs['inputs']:
        raw=(folder/row['name']).read_bytes()
        t.need(len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],'fixed public input bytes: '+row['name'])
    bases=json.loads((ROOT/'BASES.json').read_text())
    first=t.first(bases)
    t.need(t.encode(first)==(ROOT/'first-record.json').read_bytes(),'regenerated whole pre-label record')
    core=a.run(folder)
    t.need(t.encode(core)==(ROOT/'independent-full-record.json').read_bytes(),'regenerated whole pre-author-executable certificate record')
    rec={'agent':'six-reviewer-5','role':'independent mathematical reviewer',
         'historical_seals_reproduced':True,'whole_pre_label_record_sha256':t.digest(first),
         'whole_pre_author_code_certificate_sha256':t.digest(core),
         'certificate':core,'post_seal_point_bit_bridge':bridges.run(bases),
         'semantic_damage_controls':controls.run(folder),
         'classical_radius_six':classical_refinement.run(folder),
         'coverage_dependency':'Antecedent whole base classification9351 imported, sufficient prior review9387 credited; no new census audit.',
         'ordinary_proof_boundary':'All-anchor sparse coverage, repair padding, point-relabeling transport and universal Steiner retention corollary are ordinary unformalized proof in REVIEW.md.'}
    return rec

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--inputs',type=pathlib.Path,required=True)
    parser.add_argument('--work',type=pathlib.Path,required=True)
    parser.add_argument('--check-expected',action='store_true')
    args=parser.parse_args()
    t.need(not args.work.exists(),'require a new output directory')
    raw=t.encode(run(args.inputs))
    if args.check_expected:t.need(raw==(ROOT/'EXPECTED.json').read_bytes(),'whole final independent record differs')
    args.work.mkdir(parents=True)
    (args.work/'EXACT_RESULT.json').write_bytes(raw)
    rec=json.loads(raw)
    print(json.dumps({'status':'COMPLETE_INDEPENDENT_PHYSICAL_CERTIFICATES',
                      'sha256':hashlib.sha256(raw).hexdigest(),
                      'critical_domains':sum(r['complete_critical_domains'] for r in rec['certificate']['five_type_audits']),
                      'critical_physical_pair_checks':sum(r['local_physical_pair_checks'] for r in rec['certificate']['five_type_audits']),
                      'semantic_damages_rejected':len(rec['semantic_damage_controls']['controls']),
                      'classical_radius_six':True},sort_keys=True))

if __name__=='__main__':main()
