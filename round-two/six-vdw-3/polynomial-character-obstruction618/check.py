"""Independent checker: square sets, explicit powers, literal APs and CRT."""
import argparse
import copy
import csv
import hashlib
import io
import json
from math import comb,gcd
from pathlib import Path

def need(condition,message):
    if not condition:raise ValueError(message)

def polynomial(coeff,x):
    return sum(c*x**j for j,c in enumerate(coeff))%103

def canonical_coefficients():
    out=[(1,0,0,0),(0,1,0,0)]
    for a in (0,1,3):out.append(((-a)%103,0,1,0))
    for a in (0,1,3):out.append((0,a,0,1))
    for b in (1,5,25):
        for a in range(103):out.append((b,a,0,1))
    return out

def decode(raw):
    try:table=list(csv.reader(io.StringIO(raw.decode('ascii'))))
    except (UnicodeError,csv.Error) as e:raise ValueError('malformed certificate') from e
    header=['index','c0','c1','c2','c3']
    for j in range(1,9):header.extend(['a'+str(j),'d'+str(j)])
    need(bool(table) and table[0]==header,'certificate header')
    need(len(table)==318,'complete 317-case coverage')
    rows=[]
    for row in table[1:]:
        need(len(row)==21,'eight actual AP pairs per case')
        need(all(x==str(int(x)) for x in row),'canonical integer encoding')
        rows.append([int(x) for x in row])
    return rows

def verify_rows(rows):
    expected=canonical_coefficients()
    squares={(s*s)%103 for s in range(1,103)}
    points=0;root_histogram={};start0=0;regular_field0=0
    steps={};transcript=hashlib.sha256()
    need(len(rows)==317,'complete 317-case coverage')
    for index,row in enumerate(rows):
        need(len(row)==21 and all(type(x) is int for x in row),'integer witness row')
        need(row[0]==index,'ordered unique case index')
        coeff=tuple(row[1:5])
        need(coeff==expected[index],'complete canonical coefficient cover')
        roots={x for x in range(103) if polynomial(coeff,x)==0}
        degree=max(j for j,c in enumerate(coeff) if c)
        need(len(roots)<=degree,'nonzero polynomial root bound')
        regular_field0+=int(0 not in roots)
        root_histogram[len(roots)]=root_histogram.get(len(roots),0)+1
        used=set()
        for j in range(8):
            a,d=row[5+2*j:7+2*j]
            need(0<=a<618 and 1<=d<=309,'actual start and nonzero short step')
            residues=[(a+k*d)%618 for k in range(7)]
            support={n%103 for n in residues}
            need(len(support)==7,'seven distinct field columns')
            need(not support&roots,'all roots avoided')
            need(not support&used,'pairwise disjoint field supports')
            colors=[]
            for n in residues:
                z=polynomial(coeff,n%103)
                need(z!=0,'character domain excludes zero')
                colors.append((int(z not in squares)+int(n%6 in (3,4,5)))%2)
            need(len(set(colors))==1,'literal monochromatic actual AP')
            first=a if a else 618
            integers=[first+k*d for k in range(7)]
            need(len(set(integers))==7 and 1<=integers[0] and integers[-1]<=2472,'positive distinct interval lift')
            need([n%618 for n in integers]==residues,'literal cyclic/integer residue equality')
            used.update(support);points+=7;start0+=int(a==0)
            g=gcd(d,618);steps[g]=steps.get(g,0)+1
            line=[index,j,coeff,sorted(roots),residues,sorted(support),colors,integers]
            transcript.update((json.dumps(line,separators=(',',':'))+'\n').encode('ascii'))
        need(len(used)==56,'eight disjoint seven-column supports')
    return {'canonical_polynomials':317,'packing_per_polynomial':8,'actual_APs':2536,
            'actual_points':points,'root_count_histogram':root_histogram,
            'cases_with_regular_field_zero':regular_field0,'start_zero_APs':start0,
            'step_gcd_histogram':steps,'literal_transcript_sha256':transcript.hexdigest()}

def compose(coeff,s,t):
    # Direct binomial expansion, without the producer's Horner evaluation.
    return tuple(sum(coeff[j]*comb(j,k)*s**k*t**(j-k)
                     for j in range(k,4))%103 for k in range(4))

def controls():
    field=set(range(1,103));squares={s*s%103 for s in field}
    need(len(squares)==51 and 3 not in squares,'square class representatives')
    need({pow(5,j,103) for j in range(102)}==field,'primitive element five')
    cubes={s**3%103 for s in field};classes=[{b*c%103 for c in cubes} for b in (1,5,25)]
    need(len(cubes)==34 and set.union(*classes)==field,'all three cube classes covered')
    need(all(not classes[i]&classes[j] for i in range(3) for j in range(i)),'distinct cube classes')
    character={z:int(z not in squares) for z in field}
    mult=0
    for a in field:
        for b in field:
            need(character[a*b%103]==(character[a]^character[b]),'character multiplicativity')
            mult+=1
    inverse={x:next(y for y in range(1,103) if x*y%103==1) for x in field}
    square_root={}
    cube_root={}
    for x in range(1,103):
        square_root.setdefault(x*x%103,x);cube_root.setdefault(x**3%103,x)
    canon=set(canonical_coefficients());depressed=0;evals=0
    # Exhaust the depressed monic coefficient domain, not all original polynomials.
    for a in range(103):
        a0=0 if a==0 else (1 if a in squares else 3)
        s=1 if not a else square_root[a*inverse[a0]%103]
        q=((-a0)%103,0,1,0);lam=s*s%103
        need(compose(((-a)%103,0,1,0),s,0)==tuple(lam*c%103 for c in q),'quadratic normalization')
        need(q in canon,'quadratic in canonical cover');depressed+=1
        for b in range(103):
            if b==0:
                s=1 if not a else square_root[a*inverse[a0]%103]
                q=(0,a0,0,1)
            else:
                b0=next(r for r,cl in zip((1,5,25),classes) if b in cl)
                s=cube_root[b*inverse[b0]%103]
                q=(b0,a*inverse[s*s%103]%103,0,1)
            lam=s**3%103
            original=(b,a,0,1)
            need(q in canon,'cubic in complete canonical cover')
            need(compose(original,s,0)==tuple(lam*c%103 for c in q),'cubic normalization coefficient equality')
            # Direct value and root equality, including field zero.
            for x in range(103):
                left=polynomial(original,s*x%103);right=lam*polynomial(q,x)%103
                need(left==right,'cubic normalization point/root equality');evals+=1
            depressed+=1
    linear=0;basis=0;crt=0
    for s in range(1,103):
        for t in range(103):
            p=(((-s*t)%103),s,0,0)
            need(compose(p,1,t)==(0,s,0,0),'all linear coefficients normalized');linear+=1
            # Validate the four basis expansions for every affine parameter;
            # linearity of polynomial composition gives arbitrary coefficients.
            for j in range(4):
                unit=tuple(int(k==j) for k in range(4));expanded=compose(unit,s,t)
                for x in (0,1,2):
                    need(polynomial(expanded,x)==pow((s*x+t)%103,j,103),'affine basis identity');basis+=1
            alpha=s+103*((1-s)%6)
            need(0<alpha<618 and gcd(alpha,618)==1,'CRT multiplier is a unit')
            for c in range(6):
                beta=t+103*((-c-t)%6)
                need(0<=beta<618,'CRT translation range')
                for n in (0,1,617):
                    mapped=(alpha*n+beta)%618
                    need(mapped%103==(s*(n%103)+t)%103 and mapped%6==(n-c)%6,'CRT coordinate/phase identity')
                crt+=1
    phase=0;legal=[]
    rotations={tuple(int((y+c)%6>=3) for y in range(6)) for c in range(6)}
    illegal_witnesses=0
    for word in range(64):
        g=tuple((word>>y)&1 for y in range(6));bad=[]
        for y in range(6):
            for delta in range(1,6):
                phase+=1
                if len({g[(y+j*delta)%6] for j in range(7)})==1:bad.append((y,delta))
        if not bad:legal.append(g)
        else:
            witness=next(((y,delta) for y,delta in bad if delta in (2,3)),None)
            need(witness is not None,'short actual singleton-column illegal phase witness')
            y,delta=witness;d=103*delta
            for r in range(103):
                start=r+103*((y-r)%6)
                residues=[(start+j*d)%618 for j in range(7)]
                need(all(n%103==r for n in residues),'illegal phase fixed field column')
                need(len({g[n%6] for n in residues})==1,'illegal phase literal mono AP')
                # A full size-two/three cycle has a member in1..d.
                first=min(n if n else 618 for n in residues)
                lift=[first+j*d for j in range(7)]
                need(first<=d and lift[-1]<=2163 and len(set(lift))==7,'short illegal phase integer lift')
                need(all(n%103==r for n in lift) and len({g[n%6] for n in lift})==1,'illegal positive interval values')
                illegal_witnesses+=1
    need(len(legal)==6 and set(legal)==rotations,'all64 phase rows classified')
    mask_classes=distance_values=0
    for roots in range(4):
        for holes in range(4):
            for omitted_roots in range(min(roots,holes)+1):
                edited=holes-omitted_roots;m=103-roots-edited
                lower=8-edited;upper=95-roots;correlation_bound=87-roots+edited
                need(upper==m-lower and correlation_bound==m-2*lower,'mask cardinality algebra')
                for distance in range(m+1):
                    interval=lower<=distance<=upper
                    correlation=abs(m-2*distance)<=correlation_bound
                    need(interval==correlation,'all mask distance/correlation equivalences')
                    distance_values+=1
                mask_classes+=1
    return {'multiplicativity_inputs':mult,'depressed_normalizations':depressed,
            'cubic_normalization_value_checks':evals,'linear_normalizations':linear,
            'affine_basis_value_checks':basis,'CRT_phase_parameter_sets':crt,
            'phase_cycle_inputs':phase,'legal_phase_rows':len(legal),
            'actual_illegal_phase_column_witnesses':illegal_witnesses,
            'cube_class_sizes':[len(c) for c in classes],
            'zero_to_three_hole_root_count_classes':mask_classes,
            'integer_distance_correlation_values':distance_values}

def damage_controls(rows):
    trials=[]
    def add(name,change):
        copy_rows=copy.deepcopy(rows);change(copy_rows);trials.append((name,copy_rows))
    add('missing polynomial',lambda r:r.pop())
    add('duplicate index',lambda r:r[1].__setitem__(0,0))
    add('zero polynomial',lambda r:r[0].__setitem__(slice(1,5),[0,0,0,0]))
    add('omitted third cube class',lambda r:r[214].__setitem__(1,5))
    add('field coefficient outside domain',lambda r:r[0].__setitem__(1,104))
    add('missing witness pair',lambda r:r[0].pop())
    add('zero step',lambda r:r[0].__setitem__(6,0))
    add('negative step',lambda r:r[0].__setitem__(6,-1))
    add('out of range start',lambda r:r[0].__setitem__(5,618))
    add('field constant step',lambda r:r[0].__setitem__(6,103))
    add('overlapping supports',lambda r:r[0].__setitem__(slice(7,9),r[0][5:7]))
    add('root-containing AP',lambda r:r[1].__setitem__(5,0))
    def nonmono(r):
        squares={x*x%103 for x in range(1,103)};coeff=r[1][1:5]
        occupied={(r[1][5+2*k]+j*r[1][6+2*k])%103 for k in range(1,8) for j in range(7)}
        for d in range(1,310):
            for a in range(618):
                ns=[(a+j*d)%618 for j in range(7)];support={n%103 for n in ns}
                if len(support)!=7 or support&occupied:continue
                zs=[polynomial(coeff,n%103) for n in ns]
                if 0 not in zs and len({(int(z not in squares)+int(n%6>=3))%2 for n,z in zip(ns,zs)})>1:
                    r[1][5:7]=[a,d];return
        raise ValueError('failed to construct nonmonochromatic damage')
    add('nonmonochromatic AP',nonmono)
    rejected=[]
    for name,data in trials:
        try:verify_rows(data)
        except ValueError as e:rejected.append({'name':name,'reason':str(e)})
        else:raise ValueError('damage accepted: '+name)
    return rejected

def main():
    p=argparse.ArgumentParser();p.add_argument('--certificate',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    raw=args.certificate.read_bytes();rows=decode(raw)
    result={'status':'COMPLETE_INDEPENDENT_LITERAL_CERTIFICATE_AND_NORMALIZATION_CHECK',
            'certificate_sha256':hashlib.sha256(raw).hexdigest(),
            'geometry':verify_rows(rows),'controls':controls(),
            'damage_rejections':damage_controls(rows)}
    args.out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))

if __name__=='__main__':main()
