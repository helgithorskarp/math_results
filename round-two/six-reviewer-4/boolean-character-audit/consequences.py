"""Exact hole algebra and derivative control; ordinary proof supplies the premise."""
from geometry import canonical,need,crt
from math import gcd

def checks():
    classes=values=0;records=[]
    for r in (1,2,3):
        for h in range(4):
            for k in range(min(r,h)+1):
                e=h-k;m=103-r-e;low=9-e;upper=94-r;cut=85-r+e
                accepted=[d for d in range(m+1)if d+e>=9 and m-d+e>=9]
                need(accepted==list(range(low,upper+1)),'both complete distance/complement cuts')
                need(accepted==[d for d in range(m+1)if abs(m-2*d)<=cut],'entire exact correlation equivalence')
                classes+=1;values+=m+1;records.append([r,h,k,e,m,low,upper,cut])
    need(classes==26 and values==2620,'all zero-through-three-hole classes')
    # Late supplemental definition controls; no native imports.
    normalization=0
    for a in range(1,103):
        A=crt(a,1)
        need(gcd(A,618)==1,'every field normalization has a row-preserving CRT unit')
        for b in range(103):
            for shift in range(6):
                B=crt(b,shift)
                need(all((A*n+B)%103==(a*n+b)%103 and (A*n+B)%6==(n+shift)%6 for n in(0,1,617)),'all original field/phase CRT parameters on affine basis')
                normalization+=1
    lifts=0
    for residue in range(618):
        for d in range(1,309):
            first=residue or 618;integers=tuple(first+j*d for j in range(7));cyclic=tuple((residue+j*d)%618 for j in range(7))
            need(len(set(integers))==7 and tuple(n%618 for n in integers)==cyclic and 1<=integers[0] and integers[-1]<=2466,'all regular short-step positive-start lifts including zero residue')
            lifts+=1
    need(normalization==63036 and lifts==190344,'complete supplemental CRT/lift controls')
    return {'CRT_parameter_sets':normalization,'all_short_step_positive_lifts':lifts,'supplemental_code_written_after_native_access':True,'actual_agent':'six-reviewer-4','role':'independent mathematical reviewer','classes':classes,'integer_values':values,'records':records,'premise':'partial coloring u(field) XOR sigma(row) is AP7-free outside hole columns E; original reference roots omitted; arbitrary u need not be a character rule'}
if __name__=='__main__':print(canonical(checks()).decode(),end='')
