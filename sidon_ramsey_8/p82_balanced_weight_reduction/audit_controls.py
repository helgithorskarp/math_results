"""Small valid full pair trace plus adversarial mutations for the stream auditor."""
import struct,subprocess

def controls(program,weights,orbit):
    rows=[list(map(int,l.split()))for l in orbit.read_text().splitlines()]
    mask=lambda a:sum(1<<x for x in a)
    a,b=rows[8194],rows[8205];d=((1<<82)-1)^(mask(a)|mask(b))
    header=struct.pack('<3Q',1,8194,8205)
    # A complete, explicitly unknown trace is legitimate even with no emitted
    # nonempty query: the auditor validates entries/accounting, not recurrence.
    end=struct.pack('<6Q',4,1,2,1,0,0)
    good=header+end
    cases={'valid_unknown':good,'truncated':good[:-1],'missing_pair':b'','wrong_pair':struct.pack('<3Q',1,8194,8204)+end,'bad_unknown_count':header+struct.pack('<6Q',4,1,1,0,0,0),'bad_unsat_identity':header+struct.pack('<6Q',4,0,2,0,0,0),'wrong_type':header+struct.pack('<Q',7)}
    # Terminal contents are independently checked, including rejection of a
    # false positive Sidon flag on ten consecutive domain points.
    pts=[x for x in range(82)if d>>x&1][:10];last=mask(pts)
    terminal=struct.pack('<Q',3)+last.to_bytes(16,'little')+struct.pack('<2Q',4000000,1)
    cases['false_terminal']=header+terminal+end
    report=[]
    for name,data in cases.items():
        p=subprocess.run(list(map(str,[program,weights,orbit,4097,4098,0,1,1])),input=data,capture_output=True)
        assert (p.returncode==0)==(name=='valid_unknown'),(name,p.stderr)
        report.append(dict(name=name,accepted=p.returncode==0,stderr=p.stderr.decode().strip()))
    return report
