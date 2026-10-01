"""Native integer-array schemas for scoped logical proofs, with strict decoding.

This stores logical rows in plain JSON; it is not a compressed archive.
U=[0,a,d,x,b]; B=[1,x,b]; F=[2,x,b,trial_rows,trial_terminal].
The only trial assumption is x=1-b. Trial rows cannot contain another F.
Terminals: [0,a,d] actual mono AP, [1,c] count, [2,c] base defect.
"""


def need(ok,message):
    if not ok:raise ValueError(message)


def encode_terminal(t):
    if t['kind']=='mono_AP':return [0,*t['AP']]
    return [1 if t['kind']=='class_cap' else 2,t['class']]


def decode_terminal(t):
    need(type(t) is list and t and type(t[0]) is int,'Integer terminal tag')
    if t[0]==0:
        need(len(t)==3 and all(type(v) is int for v in t),'Actual AP terminal')
        return {'kind':'mono_AP','AP':t[1:]}
    need(t[0] in [1,2] and len(t)==2 and type(t[1]) is int,'Class terminal')
    return {'kind':'class_cap' if t[0]==1 else 'base_defect','class':t[1]}


def encode_rows(rows):
    out=[]
    for r in rows:
        if r['kind']=='unit':out.append([0,*r['AP'],r['point'],r['value']])
        elif r['kind']=='budget_fix':out.append([1,r['point'],r['value']])
        else:out.append([2,r['point'],r['value'],encode_rows(r['trial']['steps']),encode_terminal(r['trial']['terminal'])])
    return out


def decode_rows(rows,trial=False):
    need(type(rows) is list and len(rows)<=3704,'Bounded integer-row list')
    out=[]
    for r in rows:
        need(type(r) is list and r and type(r[0]) is int,'Integer implication tag')
        if r[0]==0:
            need(len(r)==5 and all(type(v) is int for v in r),'Actual unit tuple')
            out.append({'kind':'unit','AP':r[1:3],'point':r[3],'value':r[4]})
        elif r[0]==1:
            need(len(r)==3 and all(type(v) is int for v in r),'Packing-budget tuple')
            out.append({'kind':'budget_fix','point':r[1],'value':r[2]})
        else:
            need(not trial and r[0]==2 and len(r)==5 and all(type(v) is int for v in r[:3]),'One nonnested failed-literal tuple')
            x,b=r[1:3]
            out.append({'kind':'failed_literal','point':x,'value':b,
                        'trial':{'assumption':[x,1-b],'steps':decode_rows(r[3],True),'terminal':decode_terminal(r[4])}})
    return out


def encode(trace):
    need(trace['terminal'] is not None,'Only completed exclusions are publication certificates')
    return {'format':'QR617_COMPACT_SCOPED_UNITS_1','phase':trace['phase'],'caps':trace['caps'],'root':trace['root'],
            'base_certificate_sha256':trace['base_certificate_sha256'],'steps':encode_rows(trace['steps']),
            'terminal':encode_terminal(trace['terminal'])}


def decode(data):
    need(type(data) is dict and set(data)=={'format','phase','caps','root','base_certificate_sha256','steps','terminal'},'Exact compact schema')
    need(data['format']=='QR617_COMPACT_SCOPED_UNITS_1','Compact format')
    out=dict(data);out['format']='QR617_SCOPED_UNIT_TRACE_1';out['steps']=decode_rows(data['steps'])
    out['terminal']=decode_terminal(data['terminal']);out['next_cursor']=0
    return out


def forcing_core(trace):
    need(trace['root']==-1 and trace['caps']==[197,None] and trace['terminal']['kind']=='mono_AP','Root-free one-class actual-AP trace')
    def actual(a,d):return {a+j*d for j in range(7)}
    reasons={x:actual(a,d)-{x} for a,d,x,b in trace['units']}
    needed=actual(*trace['terminal']['AP']);pending=list(needed)
    while pending:
        x=pending.pop()
        for y in reasons.get(x,set()):
            if y not in needed:needed.add(y);pending.append(y)
    units=[r for r in trace['units'] if r[2] in needed]
    seed=sorted(needed-{r[2] for r in units})
    return {'format':'ACTUAL_AP_FORCING_CORE_1','N':3704,'color':0,'seed':seed,'units':units,'terminal_AP':trace['terminal']['AP']}
