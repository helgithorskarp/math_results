"""Source-manifest and normal/-O replay, with no solver or external inputs."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys


def require(ok,message):
    if not ok:
        raise ValueError(message)


def main():
    root=Path(__file__).resolve().parent
    names=set()
    for line in (root/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        require(Path(name).name==name and name not in names,'manifest path')
        require(hashlib.sha256((root/name).read_bytes()).hexdigest()==digest,'manifest '+name)
        names.add(name)
    require(names=={p.name for p in root.iterdir() if p.is_file()}-{'SHA256SUMS'},'source file set')
    dependency=json.loads((root/'DEPENDENCIES.json').read_text())
    literal=json.loads((root/'CORE.json').read_text())
    require(literal['red_hex']==dependency['h3931_literal_equality_core'],'imported equality witness')
    for mode in ([],['-O']):
        for script,args,expected in (
                ('produce.py',[],'CERTIFICATE.json'),
                ('check.py',['CERTIFICATE.json'],'EXPECTED_CHECK.json'),
                ('controls.py',[],'EXPECTED_CONTROLS.json'),
                ('interface.py',['FIXTURE.json'],'EXAMPLE_CERTIFICATE.json'),
                ('verify_certificate.py',['FIXTURE.json','EXAMPLE_CERTIFICATE.json'],'EXPECTED_PHYSICAL.json')):
            run=subprocess.run([sys.executable,'-B']+mode+[str(root/script)]+[str(root/a) for a in args],capture_output=True,check=True)
            require(not run.stderr,'unexpected stderr '+script)
            require(run.stdout==(root/expected).read_bytes(),'replay mismatch '+script+str(mode))
    print(json.dumps(dict(status='REPRODUCED_COMPLETE_PENTAGON_PRODUCT_EXTENSION_EXCLUSION',
                          manifest_files=len(names),replay_modes=['normal','assertions_disabled'],
                          all_attachment_words_covered=33554432,outer_tag_classes=243,
                          global_fixed_core_free_edges=603,
                          complete_physical_family_excluded=True,h3887_tasks_decided=0,
                          target_solver_calls=0,good43_established=False),indent=2,sort_keys=True))


if __name__=='__main__':
    main()
