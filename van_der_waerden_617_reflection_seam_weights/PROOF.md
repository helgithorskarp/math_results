Author: six-vdw-3, role researcher. Symmetric two colors/seven terms.

The numerical lower bound below has complete exact verification for all
617 reference phases. It asserts no global nonexistence, sufficient repair
budget, edit optimum, new W bound or length-3704 witness.

Let I={0,...,3703}, b=1852 and p=617. Define q on nonzero residues modulo p
by q(r)=0 for squares and q(r)=1 for nonsquares. Poles, at which the argument
is zero, have no prescribed color. For s in {0,...,616}, set t=1-s modulo p
and use the partial reference

    T_s(x) = q(x-b+s)                   if x<b,
             q(x-b+t) XOR 1             if x>=b.

Any binary candidate F is allowed: it need satisfy no periodicity, affine
form, reflection condition or restriction on the pole colors. For c=0,1,
let E_c consist of nonpole positions of reference color c at which F differs
from that reference. The verified bound is at least 196 edits in EACH E_c,
hence at least 392 nonpole edits, whenever F has no monochromatic
nonconstant seven-term integer arithmetic progression. The complete
phase-resolved bounds are recorded in expected.json. A larger interval with
the same partial affine reference and at least1852 points on each flank
inherits the result by restricting to this balanced window and translating.

There are exactly617 normalized references here, all incompatible keys
(s,1-s,1). This is a subset of the760761 incompatible affine seam keys,
not the whole variable-key domain. Its intersection with the previously
studied equal-phase/opposite-orientation family is the single phase s=309.
The candidate remains arbitrary in both problems. The fixed aligned QR617
reference in other repair-distance work is another reference altogether.

Reflection proof. Since617 is prime and617=1 modulo4, -1 is a square and
q(-r)=q(r). With R(x)=3703-x, the coordinate y=x-b transforms to -1-y.
For x on the left, the right-side argument at R(x) is
(-1-y)+(1-s)=-(y+s). Thus T_s(R(x))=T_s(x) XOR1 on every nonpole. The same
calculation works starting on the right, and poles reflect to poles. R maps
an increasing AP(a,d) to AP(3703-a-6d,d), after reversing its seven terms.
The positive integer step and seam crossing are preserved. In particular,
any monochromatic color0 nonpole crossing AP reflects to a color1 AP.
There is no symmetry assumption on F or its edit set in this argument.

Weighted hitting proof. Suppose a finite collection of monochromatic
nonpole reference APs of color c has rational weights lambda_A>=0 and
point loads L_c(x)=sum_{A containing x}lambda_A<=1. Every such AP must
contain an edit in E_c: otherwise it remains a monochromatic seven-term AP
in F. Consequently

    sum_A lambda_A
      <= sum_A lambda_A * |A intersect E_c|
       = sum_{x in E_c} L_c(x)
      <= |E_c|.

For each phase, the certificate lists color0 APs(a,d) with positive integer
numerators n_A and one positive denominator D. The checker explicitly
checks both these APs and their reflected color1 APs. For BOTH colors it
checks the actual integer coordinates, positive steps, nonpoles and required
monochromatic color, then adds the numerators to each physical point's
capacity and requires every sum<=D. Each color has total numerator S.
It follows that |E_0|,|E_1|>=ceil(S/D). Summing these two integer bounds
gives2*ceil(S/D); it is not merely rounding the combined weight. Taking
the minimum of the617 separately checked integer bounds gives 196 per
color and 392 in total. The coverage check requires exactly all617
phase values and verifies that each filename matches its decoded phase.
It fails on a missing or malformed case.

Complement corollary. Each reference color has M_s positions, where
M_1=1848 and M_s=1849 for s!=1. Indeed, each1852-point flank has three
full617-periods and one extra residue. Its pole count is4 exactly at s=1,
and3 otherwise; reflection pairs the nonpole colors oppositely. Thus the
whole reference has8 poles at s=1 and6 elsewhere. Complementing the
candidate preserves AP avoidance and changes |E_c| to M_s-|E_c| for
each original reference color. Applying the same phase-specific lower
bound K_s=ceil(S/D) to that complement gives the necessary region

    K_s <= |E_0|, |E_1| <= M_s-K_s,
    2*K_s <= |E_0|+|E_1| <= 2*M_s-2*K_s.

No endpoint of this necessary region is asserted attainable. The separate
arithmetic checker verifies all617 reference symmetries, pole/class counts
and the pointwise complement identity. Translate x to x+1 to index the
candidate coloring on[1,3704].

Discovery algorithm. The generator scans positive steps1<=d<=617 and
all crossing starts max(0,b-6d)<=a<min(b,3704-6d). It obtains the reference
color by enumerating squares and keeps the color0 APs. It asks single-thread
HiGHS for a fractional packing, with one nonnegative variable per retained
AP, point capacities1, and objective to maximize the total weight. The
redundant upper bound lambda_A<=1 is allowed. HiGHS is floating guidance,
not a proof authority. The checker does not trust the objective, termination
message, LP model, color table or completeness of this AP enumeration.
Positive witnesses require no exhaustive list of all APs.

For guidance weights v_A, the generator sets n_A=max(0,min(1000000,
floor(1000000*v_A))) and D=max(1000000,max_x sum_{A containing x}n_A).
Thus it produces compact exact rational weights, with exact scaling if
the floating output overloads a point. The checker recalculates every
capacity directly. It uses Euler's criterion in place of the generator's
square table, imports no solver or generator, and computes with Python
arbitrary-precision integers. It separately confirms primality of617.
Floating objectives or agreement between solvers are not used as bounds.
Timeouts, failed guidance and incomplete phase coverage establish no
mathematical exclusion. The runner stops expensive discovery if a solver
does not complete, retaining any already checked positive certificates.

Relation to the previous dilation result. The general affine-seam dilation
lemma forces132 edits at every incompatible key with1851-point flanks,
by three disjoint arithmetic sublattices. The present result uses a longer
balanced1852-point window and weighted AP capacities in the617 references
above; it also quantifies each reference color class. Its proof is
self-contained and imports none of the previous44/18 packing counts.
The previous result motivated combining and reflecting AP supports.

Trust boundary. This is an exact computer-assisted lower bound on distance
from a specified partial reference family, combined with the elementary
reflection and weighted hitting arguments above. The elementary bridge is
unformalized. It has a same-author independent definition-level checker;
no external peer review is claimed. Large generated certificate collections
are kept out of the repository and regenerated from this compact source.
The compact example certificate is only one phase and proves no coverage
of the other616 phases on its own. Historical priority is not claimed for
reflection symmetry, fractional packings or weighted hitting inequalities.
The published independent fixed-QR review already states the classical
weighted hitting rule in a different reference and conditional-petal setting:
https://github.com/helgithorskarp/math_results/tree/main/van_der_waerden_27_qr617_56_edit_review2
That review supplies no assessment or numerical premise for this result.
