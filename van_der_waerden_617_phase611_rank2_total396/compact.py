"""Plain JSON logical tuples with strict native-integer decoding.

U=[0,a,d,x,b], B=[1,x,b], F=[2,x,b,trial_rows,terminal].
Terminals: [0,a,d] actual AP, [1,c] count, [2,c] original packing
defect, [3,c] checked AP/triple packing defect. Trial assumptions are x=1-b.
This extends the attributed single198 contribution's logical-row schema.
"""


def need(ok,message):
    if not ok:raise ValueError(message)


FORMATS={'QR617_COMPACT_SHARED_TRACE_1':'QR617_SCOPED_UNIT_TRACE_1',
         'QR617_COMPACT_TRANSFER_TRACE_1':'QR617_PACKING_TRANSFER_TRACE_1'}


def encode_terminal(t):
    if t is None:return None
    if t['kind']=='mono_AP':return [0,*t['AP']]
    return [{'class_cap':1,'base_defect':2,'packing_defect':3}[t['kind']],t['class']]


def decode_terminal(t,allow_none=False):
    if t is None:
        need(allow_none,'Each failed literal has an actual contradiction');return None
    need(type(t) is list and t and type(t[0]) is int,'Native integer terminal tag')
    if t[0]==0:
        need(len(t)==3 and all(type(v) is int for v in t),'Actual AP terminal tuple')
        return {'kind':'mono_AP','AP':t[1:]}
    need(t[0] in (1,2,3) and len(t)==2 and type(t[1]) is int,'Original-class terminal tuple')
    return {'kind':{1:'class_cap',2:'base_defect',3:'packing_defect'}[t[0]],'class':t[1]}


def encode_rows(rows):
    out=[]
    for r in rows:
        if r['kind']=='unit':out.append([0,*r['AP'],r['point'],r['value']])
        elif r['kind']=='budget_fix':out.append([1,r['point'],r['value']])
        elif r['kind']=='failed_literal':
            out.append([2,r['point'],r['value'],encode_rows(r['trial']['steps']),encode_terminal(r['trial']['terminal'])])
        else:raise ValueError('Unknown logical row')
    return out


def decode_rows(rows,trial=False):
    need(type(rows) is list and len(rows)<=3704,'At most3704 fresh facts in each scope')
    out=[]
    for r in rows:
        need(type(r) is list and r and type(r[0]) is int,'Native integer logical tag')
        if r[0]==0:
            need(len(r)==5 and all(type(v) is int for v in r),'Actual unit tuple')
            out.append({'kind':'unit','AP':r[1:3],'point':r[3],'value':r[4]})
        elif r[0]==1:
            need(len(r)==3 and all(type(v) is int for v in r),'Unchanged budget tuple')
            out.append({'kind':'budget_fix','point':r[1],'value':r[2]})
        else:
            need(not trial and r[0]==2 and len(r)==5 and all(type(v) is int for v in r[:3]),'One nonnested failed literal')
            x,b=r[1:3]
            out.append({'kind':'failed_literal','point':x,'value':b,
                        'trial':{'assumption':[x,1-b],'steps':decode_rows(r[3],True),'terminal':decode_terminal(r[4])}})
    return out


def encode(raw):
    reverse={v:k for k,v in FORMATS.items()};need(raw['format'] in reverse,'Known logical proof format')
    out=dict(raw);out.pop('next_cursor');out['format']=reverse[raw['format']]
    out['steps']=encode_rows(raw['steps']);out['terminal']=encode_terminal(raw['terminal'])
    return out


def decode(data):
    need(type(data) is dict and data.get('format') in FORMATS,'Known compact logical proof format')
    fields={'format','phase','caps','root','base_certificate_sha256','steps','terminal'}
    transfer=data['format']=='QR617_COMPACT_TRANSFER_TRACE_1'
    if transfer:fields|={'shared_trace_sha256','packing_sha256'}
    need(set(data)==fields,'Exact compact proof header')
    out=dict(data);out['format']=FORMATS[data['format']];out['next_cursor']=0
    out['steps']=decode_rows(data['steps']);out['terminal']=decode_terminal(data['terminal'],not transfer)
    return out
