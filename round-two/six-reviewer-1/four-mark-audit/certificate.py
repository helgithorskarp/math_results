"""Independent complete reader of four-mark disclosed coefficient DATA only. Own three-mark reader source61516022faa5df5f379af89637b7d3c74f410d10 is reused and credited; no author executable is imported."""
import json,math,hashlib
from pathlib import Path
from polynomials import identity,original_forms,value,degree


def verify(data=None,defect=None):
    root=Path(__file__).resolve().parent
    raw=(root/'CERTIFICATE_INPUT.json').read_bytes()
    if data is None:data=json.loads(raw)
    if set(data)!=set(['version','agent','role','domain','guards','forms','rows','updates','polynomials','fields']):
        raise ValueError('certificate root census')
    if data['version']!=1 or len(data['polynomials'])!=59 or len(data['fields'])!=55:
        raise ValueError('whole input census')
    if data['agent']!='six-downset-1' or data['role']!='researcher' or data['domain']!='u,v,w>=0; d=1+u,l=2+v,h=l+d,q=8+w':
        raise ValueError('whole four-mark data domain and attribution')
    # These are author DATA annotations; our execution uses stricter local
    # fixed45s/4MiB limits and never adopts the larger author packing guard.
    if data['guards']!={'child_seconds':60,'polynomial_terms':512,'packing_bytes':33554432,'native_threads':1}:
        raise ValueError('whole disclosed guard annotations')
    pp=[];den=[]
    for v in data['polynomials']:
        if set(v)!=set(['denominator','terms'])or type(v['denominator'])is not int or v['denominator']<=0:
            raise ValueError('polynomial denominator')
        a={}
        for e,c in v['terms']:
            if len(e)!=3 or any(type(x)is not int or x<0 for x in e)or tuple(e)in a:
                raise ValueError('all coefficient exponents')
            if not isinstance(c,str)or str(int(c))!=c or int(c)==0:
                raise ValueError('all integer coefficients')
            a[tuple(e)]=int(c)
        if not a or len(a)>512:raise ValueError('whole polynomial census')
        pp.append(a);den.append(v['denominator'])
    ff=[];used=set();positive_denominators=set()
    for f in data['fields']:
        if set(f)!=set(['numerator','denominator_factors'])or type(f['numerator'])is not int or not 0<=f['numerator']<59:
            raise ValueError('field numerator')
        ni=f['numerator'];num=[pp[ni]];numscalar=1;dscalar=den[ni];factors=[];seen=set();used.add(ni)
        for pi,power in f['denominator_factors']:
            if type(pi)is not int or type(power)is not int or not 0<=pi<59 or power not in [1,2]or pi in seen:
                raise ValueError('field denominator factors')
            seen.add(pi);used.add(pi);positive_denominators.add(pi)
            factors += [pp[pi]]*power;numscalar*=den[pi]**power
        ff.append((numscalar,num,dscalar,factors))
    if used!=set(range(59)):raise ValueError('entire polynomial pool referenced')
    for pi in positive_denominators:
        if pp[pi].get((0,0,0),0)<=0 or any(c<0 for c in pp[pi].values()):
            raise ValueError('whole denominator coefficient positivity')
    form=data['forms']
    if form!={'four-even-five-allq':[list(range(i*5,(i+1)*5))for i in range(5)]}:
        raise ValueError('25 full form addresses')
    initial,old=original_forms();records=[];field_used=set(range(25))
    for i in range(5):
        for j in range(5):
            n,d=initial[i][j];a,b,c,e=ff[5*i+j]
            if defect=='old-row-drop'and (i,j)==(0,0):n={}
            r=identity([(c,[n]+e),(-a,[d]+b)])
            records.append({'gate':'original five-form '+str((i,j)),**r})
    state=[row[:]for row in form['four-even-five-allq']];pivots=[];updates=data['updates'];rows=data['rows']
    expected_order=[(k,i,j)for k in range(4)for i in range(k+1,5)for j in range(k+1,5)]
    if len(updates)!=30 or [(r['k'],r['i'],r['j'])for r in updates]!=expected_order or len(rows)!=5:
        raise ValueError('entire ordered Schur coverage')
    position=0
    for k in range(5):
        pivot=state[k][k];pivots.append(pivot);f=data['fields'][pivot];num=pp[f['numerator']]
        r=rows[k]
        if set(r)!=set(['group','order','pivot','shifted_numerator','positive','denominator_positive','degree','terms','shifted_terms']):
            raise ValueError('whole pivot metadata census')
        if r['group']!='four-even-five-allq'or r['order']!=k+1 or r['pivot']!=pivot or r['shifted_numerator']!=f['numerator'] or r['positive']is not True or r['denominator_positive']is not True:
            raise ValueError('whole pivot working links')
        if num.get((0,0,0),0)<=0 or any(c<0 for c in num.values()):raise ValueError('all pivot coefficients')
        if len(num)!=r['terms']or len(num)!=r['shifted_terms']or max(map(sum,num))!=r['degree']:
            raise ValueError('whole pivot coefficient census')
        records.append({'gate':'positive pivot '+str(k+1),'field':pivot,'constant':str(num[(0,0,0)]),'all_coefficients':[{'e':list(e),'c':str(c)}for e,c in sorted(num.items())]})
        for i in range(k+1,5):
            for j in range(k+1,5):
                t=updates[position];position+=1
                if set(t)!=set(['group','k','i','j','before','left','right','pivot','after']):
                    raise ValueError('whole Schur metadata census')
                keys=[t[a]for a in ['before','left','right','pivot','after']]
                if t['group']!='four-even-five-allq'or keys[:4]!=[state[i][j],state[i][k],state[k][j],pivot]or any(type(z)is not int or not 0<=z<55 for z in keys):
                    raise ValueError('whole Schur working links')
                field_used.update(keys)
                nb,lb,db,rb=ff[keys[0]];nl,ll,dl,rl=ff[keys[1]];nr,lr,dr,rr=ff[keys[2]]
                np,lp,dp,rp=ff[keys[3]];na,la,da,ra=ff[keys[4]]
                # before - left*right/pivot - after = 0, complete denominator clearing.
                terms=[(nb*dl*dr*np*da,lb+rl+rr+lp+ra),
                       (-nl*nr*dp*db*da,ll+lr+rp+rb+ra),
                       (-na*db*dl*dr*np,la+rb+rl+rr+lp)]
                if defect=='Schur-sign'and position==30:terms[1]=(abs(terms[1][0]),terms[1][1])
                records.append({'gate':'whole Schur '+str((k,i,j)),**identity(terms)})
                state[i][j]=keys[4]
    if field_used!=set(range(55)):raise ValueError('entire field pool referenced')
    return {'agent':'six-reviewer-1','role':'independent mathematical reviewer',
            'input_author':'six-downset-1','input_is_disclosed_data_not_code':True,
            'input_bytes':len(raw),'input_sha256':hashlib.sha256(raw).hexdigest(),
            'full_polynomials':59,'full_fields':55,'full_initial_forms':25,'full_ordered_updates':30,
            'all_pivot_coefficients':sum(len(pp[data['fields'][k]['numerator']])for k in pivots),
            'all_denominator_factor_coefficients_positive':True,'records':records,
            'max_encoding_bound_bytes':max(r.get('encoding_bound_bytes',0)for r in records),
            'all_original_old_frame_polynomials':[[[[*e],str(c)]for e,c in sorted(p.items())]for row in old for p in row]}


if __name__=='__main__':
    import signal,sys
    signal.alarm(45)
    out=verify();raw=(json.dumps(out,sort_keys=True,indent=2)+'\n').encode()
    Path(sys.argv[1]).write_bytes(raw)
    print(json.dumps({k:v for k,v in out.items()if k not in ['records','all_original_old_frame_polynomials']}))
