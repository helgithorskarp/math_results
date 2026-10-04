"""Fresh complete scoped mathematical record; time and hashes never positivity premises."""
import copy,hashlib,json
from fractions import Fraction as F
from geometry import *
from blocks import inspect
from account import compare


def make(cert,comparison,damage='none'):
    cert=copy.deepcopy(cert);comparison=copy.deepcopy(comparison)
    if damage=='value':cert['free_original_entry_numerators'][0]+=2**26
    if damage=='float':cert['free_original_entry_numerators'][0]=float(cert['free_original_entry_numerators'][0])
    if damage=='boolean':cert['free_original_entry_numerators'][0]=True
    if damage=='key':cert['free_original_entry_orbit_keys'].pop()
    if damage=='triangle':cert['positive_sector_certificates']['TT_lower']['factor_lower_triangle_numerators'].pop()
    if damage=='scalar':cert['positive_sector_certificates']['ZZ_upper']['scalar_gram_numerator']+=1
    D,stars=literal();table,den=load_values(cert);C,U,L,M=build(D,table,den)
    if damage=='star':C[0][D[1:].index(1)]+=1
    if damage=='upper':U[0][0]+=1
    if damage=='empty':M[0][0]+=1
    need(all(sum(C[i][j] for j,A in enumerate(D[1:]) if A&1)==0 for i in range(277)),'full original lower star kernel')
    need(all(U[i][j]==278*den*(i==j)-den-C[i][j] for i in range(277) for j in range(277)),'full original opposite endpoint')
    need(all(sum(row)==220*den for row in M),'all original completed rows including empty')
    B,g=repairs(D);radius=F(1,65000) if damage=='radius' else F(1,65920)
    need(radius*1030<=F(1,64),'entire enlarged box spectral budget')
    oldbox=entry_box(D,M,den,B,F(1,3814656));newbox=entry_box(D,M,den,B,radius)
    psd=inspect(D,C,U,cert,damage);account=compare(D,table,den,C,L,M,comparison,damage)
    return dict(actual_agent='six-reviewer-5',role='independent mathematical reviewer',input_scope='Published author coefficient/factor and comparison data exposed; independently reconstructed literal matrices/basis/actions/residuals/generators. No current author programs/EXPECTED/validation.',carrier=dict(ground_points=21,N=len(D),s=max(stars),stars=stars,proper=277,all_original_support_and_row_positions=77284,all_original_point_and_spectral_kernel_identities=True),geometry=g,point_and_old_box=oldbox,enlarged_real_box=newbox,certificates=psd,comparison_and_capacity=account,matrix_whole_seals={k:hashlib.sha256(canon(v)).hexdigest() for k,v in [('C',C),('U',U),('L',L),('M_numerators',M)]},physical_floor_point='1/32',physical_floor_enlarged_box='1/64',original_lower_gap_point='1/7040',original_lower_gap_enlarged_box='1/14080',actual_entry_floor='1/2048',actual_upper_gap='1/2048',enlargement_ratio=str(F(3814656,65920)),analytic_bridges='Ordinary UNFORMALIZED full-frame/rank/congruence/real-box/Frobenius/Laplacian/capacity arguments; no global H/I or transported ancestor PSD verdict.')
