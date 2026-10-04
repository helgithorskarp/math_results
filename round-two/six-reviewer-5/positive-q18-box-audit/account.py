"""Independent old/new original row and NN-mass accounting, not a PSD premise."""
from fractions import Fraction as F
from geometry import need,build,integer


def compare(D,table,den,C,L,M,data,damage='none'):
    oldden=integer(data['comparison_free_denominator'],'comparison denominator');need(oldden==16384,'old denominator')
    nums=data['comparison_free_numerators'];need(type(nums) is list and len(nums)==143,'complete comparison values');nums=[integer(x,'comparison value integer') for x in nums]
    oldtable=dict(zip(sorted(table),nums));Co,Uo,Lo,Mo=build(D,oldtable,oldden)
    proper=D[1:];bad=[i for i,A in enumerate(proper) if not A&1 and Mo[0][i+1]<0]
    need(len(bad)==81,'all old bad NN rows');badtypes=sorted({(A&7,((A>>3)&511).bit_count(),((A>>12)&511).bit_count()) for i,A in enumerate(proper) if i in bad});need(len(badtypes)==3,'nonstar old negative row orbit census')
    allbad=[i for i in range(278) if Mo[0][i]<0];allbadtypes=sorted({(A&7,((A>>3)&511).bit_count(),((A>>12)&511).bit_count()) for i,A in enumerate(D) if i in allbad});need(len(allbad)==82 and len(allbadtypes)==4 and 7 in [D[i] for i in allbad],'all four old negative empty-row orbits including abc')
    d=sum(-F(Mo[0][i+1],oldden) for i in bad);ell=F(Mo[0][0],oldden)
    need(d==F(2497887,16384) and ell==F(2021552,16384),'entire actual empty deficits and loop C-units')
    P=F(0);T=F(0);up=0;down=0;zero=0
    for i,A in enumerate(proper):
        if A&1:continue
        for j,G in enumerate(proper[:i]):
            if G&1 or A&G:continue
            delta=F(C[i][j],den)-F(Co[i][j],oldden)
            if delta>0:P+=delta;up+=1
            elif delta<0:T-=delta;down+=1
            else:zero+=1
    need((up,down,zero)==(9919,9603,0),'all signed nonstar increments')
    need(P==F(802154061,262144) and T==F(3266119971,1048576),'whole NN positive and negative masses')
    if damage=='loop':T+=1
    change=F(M[0][0],den)-F(Mo[0][0],oldden)
    need(change==2*(P-T)==-F(57503727,524288),'entire original empty loop identity')
    bound=(d-ell)/2;need(bound==F(476335,32768)>0 and P>=bound,'necessary old signed-center mass budget')
    return dict(all_old_negative_empty_rows=allbad,all_old_negative_empty_types=[list(x) for x in allbadtypes],old_bad_nonstar_rows=bad,old_bad_types=[list(x) for x in badtypes],old_deficit_C_units=str(d),old_loop_C_units=str(ell),necessary_positive_NN_mass=str(bound),new_positive_NN_mass=str(P),new_negative_NN_mass=str(T),new_up_edges=up,new_down_edges=down,new_zero_changes=zero,original_loop_C_change=str(change),original_new_loop_M=str(F(M[0][0],220*den)),old_PSD_not_a_premise=True,capacity_optimality_not_asserted=True)
