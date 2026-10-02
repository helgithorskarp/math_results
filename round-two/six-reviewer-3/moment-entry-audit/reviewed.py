"""Explicit reuse of this reviewer's prior complete certificates, own inputs only."""
import hashlib,importlib.util,json,sys
from fractions import Fraction as F
from pathlib import Path
from polys import need

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':')).encode()

def record():
    rows=json.loads((HERE/'OWN_INPUTS.json').read_text())['files']
    for row in rows:
        body=(ROOT/row['path']).read_bytes()
        need(len(body)==row['bytes'] and hashlib.sha256(body).hexdigest()==row['sha256'],'own input binding '+row['label'])
        need(row['path'].startswith('round-two/six-reviewer-3/'),'author input cannot supply independent premise')
    old=HERE.parent/'normalized-neighborhood-audit';sys.path.insert(0,str(old))
    spec=importlib.util.spec_from_file_location('reviewed_normalized_9448',old/'verify.py');module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
    normalized=module.record();sha=hashlib.sha256(canonical(normalized)).hexdigest()
    need(sha=='3c4e81d5b786bdce59f485d489db51bf5a40e7be7091c69dccaf23508e80dc23','whole reviewed9448 numerical record')
    import kernel
    _,radial,radial_sha,_=kernel.radial_record();cover=radial['review9174_19eta_cover'];even=cover['even_matrix'];odd=cover['odd_matrix'];sine2=cover['original_root_sine_squared']
    J=[[tuple(map(F,entry)) for entry in row] for row in even];O=[[tuple(map(F,entry)) for entry in row] for row in odd]
    need(all(row[0][1]<-F(1,3) for row in J),'actual branch negative y derivatives')
    need(all(max(abs(x) for x in entry)<1 for row in J+O for entry in row),'all actual radial entries below1')
    detJ=tuple(map(F,cover['even_determinant']));detO=tuple(map(F,cover['odd_determinant']))
    need(detJ[0]>F(9,100) and detO[1]<-F(3,200),'full actual determinant intervals')
    need(all(F(pair[0])>F(1,9) and F(pair[1])<=1 for pair in sine2),'physical positive sine magnitude above1/3')
    # Physical G=diag(sin)O; triangle/cofactor bounds give max-row inverse <400.
    bound_even=F(2)/F(9,100);bound_odd=F(6)/F(3,200)
    need(max(bound_even,bound_odd)<800,'actual full inverse bound800')
    params=[tuple(map(F,pair)) for pair in cover['parameter_box'][:3]]
    need(all(max(abs(a),abs(b))<F(9,8) for a,b in params[:2]),'whole actual x/y bounds')
    need(1<params[2][0] and params[2][1]<F(25,16),'whole actual T bounds')
    return {'own_source_files':len(rows),'whole9448_record_sha256':sha,'whole9335_record_sha256':radial_sha,'actual_J_y':[[str(x) for x in row[0]] for row in J],'actual_parameter_box':[[str(x) for x in pair] for pair in params],'full_actual_J':even,'full_actual_O':odd,'physical_sine_squared':sine2,'even_inverse_upper':str(bound_even),'physical_odd_inverse_upper':str(bound_odd),'raw_second_bound':'2^39 inherited from the fully regenerated9448 record and its ordinary uniform Cauchy proof','reused_scope':'previous reviewed kernels, not a fresh independent audit of all original premises'}
