"""Complete independent combinatorial interfaces, never a full host census."""
import hashlib,json,math
from itertools import combinations,permutations,product
from pathlib import Path
import shell as s
import coordinate as c

def compositions(n,k):
    if k==1:yield(n,);return
    for i in range(n+1):
        for rest in compositions(n-i,k-1):yield(i,*rest)

def weight(row):
    v=math.factorial(sum(row))
    for a in row:v//=math.factorial(a)
    return v

def category(a,b,n):
    return [sum(((a>>j)&1)+2*((b>>j)&1)==k for j in range(n)) for k in range(4)]

def check():
    base=s.specification();s.need(base==c.specification(),'whole independent original pair models')
    red,blue=s.rows(base);record={}
    record['all231_original_pairs']=[[a,b,base[(a,b)]] for a,b in sorted(base)]
    s.need([len(red[v]) for v in ['u','v','a']]==[10,10,9],'literal root degrees')
    s.need([len(red[v]) for v in s.X]==[3,3,4,4,4,4],'literal X fixed degrees')
    for a,b in s.MIXED:s.need(red[s.X[a]]&red[s.X[b]]=={'u'},'mixed known pages')
    record['root_and_X_degrees']={v:len(red[v]) for v in ['u','v','a',*s.X]}
    # All labelled mask pairs are separately represented, with complete counts.
    tables={};hist={}
    for n in [5,6]:
        rows=[];h={}
        for a,b in product(range(1<<n),repeat=2):
            cat=category(a,b,n);rows.append([a,b,cat]);key=tuple(cat);h[key]=h.get(key,0)+1
        s.need(set(h)==set(compositions(n,4)),'whole category coverage')
        for key,count in h.items():s.need(count==weight(key),'all labelled multiplicities')
        tables[str(n)]=rows;hist[n]=h
    combined=[];covered=0
    for d,q in product(sorted(hist[5]),sorted(hist[6])):
        da=d[1]+d[3];db=d[2]+d[3];qa=q[1]+q[3];qb=q[2]+q[3]
        degree_sum=7+da+db+qa+qb
        red_slack=2-d[3]-q[3]
        rhs=d[0]+q[0]+red_slack
        s.need(20-degree_sum==rhs,'entire mixed slack identity')
        if red_slack>=0:
            s.need(degree_sum<=20,'uniform local degree sum upper bound')
            s.need((degree_sum==20)==(d[0]==q[0]==red_slack==0),'all equality cases')
        mult=hist[5][d]*hist[6][q];covered+=mult
        combined.append([list(d),list(q),degree_sum,red_slack,rhs,mult])
    s.need(covered==4**11,'every labelled eleven-point membership word')
    record['all_labelled_D_Q_category_tables']=tables
    record['all4704_mixed_slack_classes']=combined
    record['labelled_product_coverage']=covered
    # Exact universal union identity, all 6-point masks (not sampled hosts).
    covers=[(a,b) for a,b in product(range(64),repeat=2) if a|b==63]
    union=[]
    for a,b in covers:
        vals=[]
        for f in range(64):
            value=(f&a).bit_count()+(f&b).bit_count()-f.bit_count()
            s.need(value==(f&a&b).bit_count() and value>=0,'whole closed union budget')
            vals.append(value)
        union.append([a,b,vals])
    record['all729_union_pairs_and64_F_budgets']=union
    classes=[]
    for mask in range(64):
        v=s.cover(mask) and s.independent(mask)
        s.need(v==c.independent_cover(mask),'independent star-cover interpretation')
        classes.append([mask,s.cover(mask),s.independent(mask),v])
    s.need([a[0] for a in classes if a[3]]==[3,13,50,60],'all four original cover rows')
    record['all64_X_row_classes']=classes
    coverrows=[r for r in range(64) if s.cover(r)]
    # Actual two-spine known-page budgets for BOTH original T labels.
    doubled=[]
    for ti,(i,j),r,sy in product([1,2],s.MIXED,range(64),coverrows):
        if not((r>>i&1) and(r>>j&1)):continue
        spec=s.assign(base,f'T{ti}',s.X,r)
        spec=s.assign(spec,'SY1' if ti==1 else 'SY0',s.X,sy)
        pairpages=[]
        for k in [i,j]:
            rr,bb=s.rows(spec);pages=sorted(rr[f'T{ti}']&rr[s.X[k]])
            s.need(pages==c.pages(spec,f'T{ti}',s.X[k],1),'actual doubled physical pages')
            pairpages.append(pages)
        s.need(sum(map(len,pairpages))>=4,'four known distinct page occurrences')
        doubled.append([ti,i,j,r,sy,pairpages])
    s.need(len(doubled)==3200,'complete broader doubled-row domain')
    record['all3200_actual_doubled_spine_page_lists']=doubled
    # The complete endpoint neighborhood makes u-T and SX-SX counts exact.
    lower=[]
    for ti,f in product([1,2],range(64)):
        spec=s.assign(base,f'T{ti}',s.Q,f);rr,bb=s.rows(spec);pages=sorted(bb['u']&bb[f'T{ti}'])
        s.need(pages==c.pages(spec,'u',f'T{ti}',0) and len(pages)==9-f.bit_count(),'actual blue u-T lower rank')
        lower.append([ti,f,pages])
    record['all128_actual_u_T_blue_pages']=lower
    sx=[]
    for a,b in product(range(64),repeat=2):
        spec=s.assign(s.assign(base,'SX0',s.Q,a),'SX1',s.Q,b);rr,bb=s.rows(spec);pages=sorted(bb['SX0']&bb['SX1'])
        s.need(pages==c.pages(spec,'SX0','SX1',0),'whole SX physical pages')
        s.need(len(pages)==6+(63^(a|b)).bit_count(),'exact six fixed pages plus free-Q deficit')
        s.need((len(pages)<=6)==(a|b==63),'all free SX ranks')
        sx.append([a,b,pages])
    record['all4096_actual_SX_blue_page_lists']=sx
    # Every rank>=3 Q row in every SX covering pair, all P/S/L roles.
    # Binary entries are the TWO full actual red-spine page counts per cell.
    rolevalues=bytearray();roles=0;roleheaders=[]
    for pattern in [13,50,60]:
        for ti in [1,2]:
            start=len(rolevalues)
            # Known original red neighborhoods are derived from the set shell.
            core=s.assign(base,f'T{ti}',s.X,pattern);rr,bb=s.rows(core)
            known0=rr['SX0']&rr[f'T{ti}'];known1=rr['SX1']&rr[f'T{ti}']
            s.need(known0==set(c.pages(core,'SX0',f'T{ti}',1)) and known1==set(c.pages(core,'SX1',f'T{ti}',1)),'literal role base pages')
            for a,b in covers:
                for f in range(64):
                    if f.bit_count()<3:continue
                    n0=len(known0)+(a&f).bit_count();n1=len(known1)+(b&f).bit_count()
                    s.need(n0>3 or n1>3,'at least one actual red book violates cap')
                    rolevalues.extend([n0,n1]);roles+=1
            roleheaders.append([pattern,ti,start,len(rolevalues),sorted(known0),sorted(known1)])
    s.need(roles==183708,'entire role product')
    record['all183708_role_counts_hex']=rolevalues.hex();record['role_headers']=roleheaders
    final=s.assign(s.assign(base,'T1',s.X,3),'T2',s.X,3)
    rr,bb=s.rows(final);pages=sorted(bb['T1']&bb['T2'])
    s.need(pages==['T0','X2','X3','X4','X5','u','v'] and pages==c.pages(final,'T1','T2',0),'seven full original terminal pages')
    record['original_terminal_blue_pages']=pages
    # Explicit bijections on EVERY originally free incidence for all T namings.
    naming=[];free=sorted(p for p,v in base.items() if v is None)
    for perm in permutations(['T0','T1','T2']):
        rename=dict(zip(['T0','T1','T2'],perm))
        def image(p):return tuple(sorted(rename.get(v,v) for v in p))
        moved={image(p):v for p,v in base.items()};mapped=[image(p) for p in free]
        s.need(len(moved)==231 and len(set(mapped))==123,'whole naming bijection')
        movedc={image(p):v for p,v in c.specification().items()}
        s.need(moved==movedc and set(mapped)=={p for p,v in moved.items() if v is None},'all fixed/free labeling assignments')
        naming.append([list(perm),mapped,[[a,b,v] for (a,b),v in sorted(moved.items())]])
    record['six_whole_T_naming_bijections']=naming
    # Positive relaxed completions show the degree predicate is genuinely weaker.
    weaker=[]
    for degrees in [[9,9,11,11,11,11],[11,11,9,9,9,9]]:
        spec=base
        for i,degree in enumerate(degrees):
            spec=s.assign(spec,s.X[i],s.D,31);extra=degree-[3,3,4,4,4,4][i]-5
            spec=s.assign(spec,s.X[i],s.Q,(1<<extra)-1)
        rr,bb=s.rows(spec);actual=[len(rr[v]) for v in s.X]
        s.need(actual==degrees and all(actual[i]+actual[j]==20 for i,j in s.MIXED),'strict weakening control')
        weaker.append({'actual_X_degrees':actual,'fixed_shell_preserved':True,'book_caps_not_claimed':True})
    record['strictly_weaker_degree_predicate_controls']=weaker
    # Primary known 21-point witness: off-diagonal ZERO means RED.
    text=Path('BASELINE21.txt').read_text();mat,end=json.JSONDecoder().raw_decode(text)
    metadata=text[end:].strip()
    s.need(metadata=='search_function_used = tabu_nolimit\nseed_for_search_until_success = 0\ntotal_steps = 4260','whole credited primary fixture metadata')
    record['primary_nonmathematical_search_annotations']=metadata
    s.need(len(mat)==21 and all(len(r)==21 for r in mat),'primary21 fixture dimension')
    for i in range(21):
        s.need(mat[i][i]==0,'fixture diagonal')
        for j in range(21):s.need(mat[i][j] in [0,1] and mat[i][j]==mat[j][i],'primary simple symmetric encoding')
    nr=[{j for j in range(21) if j!=i and mat[i][j]==0} for i in range(21)]
    nb=[set(range(21))-{i}-nr[i] for i in range(21)];bm=[sum(1<<j for j in r) for r in nr]
    whole=[]
    for i,j in combinations(range(21),2):
        color=int(mat[i][j]==0);pages=sorted((nr if color else nb)[i]&(nr if color else nb)[j])
        if color:s.need(len(pages)==(bm[i]&bm[j]).bit_count(),'independent primary red bit count')
        else:
            bi=((1<<21)-1)^bm[i]^(1<<i);bj=((1<<21)-1)^bm[j]^(1<<j)
            s.need(len(pages)==(bi&bj).bit_count(),'independent primary blue bit count')
        s.need(len(pages)<=(3 if color else 6),'primary page cap')
        whole.append([i,j,color,pages])
    s.need(sum(r[2] for r in whole)==93,'credited incumbent red count')
    s.need(max(len(r[3]) for r in whole if r[2])==3 and max(len(r[3]) for r in whole if not r[2])==6,'credited incumbent maxima')
    record['primary_all210_spines']=whole
    record['source_independence']={'new_native_code_input_expected_certificate_access':False,'written_proof_exposed_not_blind':True,'host_census_claimed':False,'ordinary_proof_required':True}
    return record

if __name__=='__main__':print(json.dumps(check(),sort_keys=True,separators=(',',':')))
