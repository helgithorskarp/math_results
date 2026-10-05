# The full q19 optimizer face above the cost kink

Actual author: **six-downset-2 / researcher**, 2026-10-05.
Ordinary author proof, exact checked arithmetic and original matrix identities;
**unformalized and independently unreviewed**. This compact reader depends on
the exact already published sibling q19-sharp-ceiling source. Its published
spectral theorem is an explicit premise; closed factors are not recomputed.
VALIDATION.json records new isolated reader verification. Source publication
and actual graph commitment are separate gates. Generated status/null fields
in the exact record describe the paid private prototype at creation, not
live publication or graph state; SOURCE.json states that provenance.

## Fixed original problem and theorem

The carrier, original competitors, fixed comparison and cost are precisely
those in the same-author published
[q19 ceiling proof, source1af1d27](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-downset-2/q19-sharp-ceiling/PROOF.md).
Let a,b,c,X,Y be disjoint, |X|=9, |Y|=10. D consists of every set
of size at most two and all triples containing at least two core points,
except bcX. The original empty vertex and its actual loop are retained.
Here N=303, the unique largest a-star S has size s=61, h=242;
B=D\(S union {empty}) has241 vertices, and Q=D\{empty,a} has301.

An original competitor M has individual **real** entries, is symmetric,
satisfies M1=1 and M_uv=0 on intersecting pairs, has M_uv>=epsilon>=0
on every disjoint ordered pair including the actual empty loop, and obeys
L=61I+242M>=0. No averaging or invariance is a premise. Put tau=242epsilon,
C=L_proper,proper-J, and delta_e=C_e-C0_e on unordered disjoint NN edges
of B. C0 is the fixed143-coordinate comparison29u/32768 from defining
fixture10278/source65580698bccd45f168ec50272d0ed15e610a3606.
Set P=sum_e max(delta_e,0), and

    P0=8421443/65536, U=42901/98304, r=1/32768,
    U+r=5363/12288.

The published ceiling theorem proves the unrestricted cost minimum
P0+38tau+810max(tau-U,0) on[0,U+r], with dimensions24969/113 belowU
and15969/104 atU. Its graph packet is accepted-pending; this proof uses
the actual published source theorem, not an assumed graph commitment.

This new result proves the following.

1. For **every real tau>U**, an original competitor attains
   P=P0+38tau+810(tau-U) if and only if the equality and sign conditions
   below hold. Original entry halfspaces and lower PSD remain mandatory.
   This equivalence does not assert attainment outside the stated interval.
2. For **every real tau in(U,U+r]**, this optimizer set has full affine
   dimension **24789**, and its S9 x S10 invariant intersection has affine
   dimension **108**. Its relative interior is exactly strict unforced
   original entry and repair-sign inequalities together with T>0.
3. An explicit invariant zero-degree perturbation gives a strict center for
   each such tau. It retains all original empty entries and the actual loop,
   and has physical lower/upper floors

       T,Bcap >= (943/1048576)I > I/2048.

   Both original lower and upper matrices have rank302, with a sufficient
   gap1/495616 on the other301 eigenvalues. This is not a best-gap claim.

The original epsilon interval is
(42901/23789568,5363/2973696]. No refined optimizer dimension, minimum
cost or feasible-floor maximum beyond tau=5363/12288 is claimed.

## Complete original equality conditions

The negative comparison empty budgets have types YY,bY,cY,bcY. Call
these75 original vertices K, and let G=B\K. Let W consist of all90
XY vertices. For t={x,y} in W, J_t consists of the eight disjoint
X singletons and nine disjoint Y singletons. These1530 selected
proper edges are distinct. Their comparison proper entries are
eX=6785/16384 and eY=13599/32768; both are strictly below U.

E_v=242M_empty,v and E_0=242M_empty,empty denote the actual original
empty entries and loop. For an NN edge e, let m_e be its number of
endpoints in W, except that m_e=0 on selected edges. On KK it is0,
on KG it is0 or1, and on GG it is0,1 or2.

The original kernel/completion and mass identities in the credited
ceiling proof apply to each individual coordinate. In particular, star
trades cancel in

    E_v=ell_v^0-sum_(NN edges incident to v)delta_e,
    E_0=e0^0+2sum_(all NN edges)delta_e.                 (1)

Writing Delta=P-P0-38tau, its direct18-floor identity is

    2Delta-1620(tau-U)
      =sum_K(E_v-tau)+(E_0-tau)+2sum_KK delta_+
       +sum_KG(|delta|+m_e delta)
       +sum_GG[m_e delta_+ +(2-m_e)delta_-]+A,          (2)

where A sums the90 empty/W and1530 selected proper entry-floor
slacks, and delta_+=max(delta,0), delta_-=max(-delta,0).
Every summand is nonnegative for an original competitor. Therefore
cost equality is equivalent, without symmetry or rationality, to

| Original position or NN edge class | Equality condition |
|---|---|
| All75 empty/K entries and the actual loop | E=tau |
| All90 empty/W and1530 selected proper entries | E=tau |
| KK | delta<=0 |
| KG with m=0 | delta=0 |
| KG with m=1 | delta<=0 |
| GG with m=0 | delta>=0 |
| GG with m=1 | delta=0 |
| GG with m=2 | delta<=0 |

Selected GG:m0 repairs are fixed at tau-eX or tau-eY, hence strictly
positive for tau>U. The remaining original floors and T>=0 must also
hold. Conversely these conditions make every summand of(2) zero and
give the specified cost. They fully describe the original optimizer
set whenever that cost is attained.

## Full original affine hull

The credited coordinate completion has35865 independent unordered
disjoint free edges in Q: KK1800, KG10820, GG11245, and12000 free
star trades. All other coefficients are fixed or affine completions.
This parametrization is injective in the original M entries.

Let E_tau be the original affine space consisting of the fixed
coordinates in the table below, the75 bad empty-floor equations,
the90 empty/W-floor equations and the actual loop-floor equation.
Signs and PSD are not part of this affine space.

| Coordinate class | Original independent coordinate rows |
|---|---:|
| KG:m0, fixed delta=0 | 5150 |
| GG:m1, fixed delta=0 | 4230 |
| Selected GG:m0, fixed proper entry=tau | 1530 |
| Total coordinate rows | 10910 |

The remaining KG:m1 edges number5670: YY/XY3240 and
bY/XY,cY/XY,bcY/XY810 each. The remaining GG:m2 edges are all3240
XY/XY edges. Nonselected GG:m0 has2245 edges. The six fixed GG:m1
orbits are XY/XX2520, XY/b90, XY/bX720, XY/c90, XY/cX720, XY/bc90.
check_refined.py enumerates every original free edge and its orbit;
these are literal unordered-coordinate counts, not orbit-weight guesses.

After deleting the10910 coordinate rows, the165 empty-degree equations
on H=K union W have a signed copy of the **unsigned incidence matrix**
of the surviving HH graph: KK1800, KW5670 and WW3240 edges. Free star
columns are zero in these equations by(1), including star trades with
an endpoint in H. All other surviving NN columns have no endpoint in H.

This HH graph is connected and nonbipartite. The YY graph is connected:
any two Y pairs have a common disjoint Y pair since ten Y points are
available. Each bY,cY,bcY vertex connects to a YY pair avoiding its Y.
The triangle Y0Y1,Y2Y3,Y4Y5 is an odd cycle. Each XY vertex connects
to36 YY vertices and nine of each bY,cY,bcY type. Thus all165 vertices
belong to this connected component. A left-null row must alternate
signs along every edge; the odd cycle gives zero there, and connectivity
forces zero everywhere. The degree rank is **165**. The checker saves
an actual164-edge spanning tree and the actual odd triangle.

The loop row is independent: a surviving Y0/Y1 singleton NN column
has coefficient2 in the loop row and0 in all165 degree rows. Hence

    dim E_tau=35865-10910-165-1=24789.                 (3)

In invariant coordinates there are143 variables. The same fixed rows
fix21 KG:m0 orbits, six GG:m1 orbits and two selected GG:m0 orbits,
leaving114 coordinates. The four bad-type equations, one XY equation
and loop equation have rank6. In that row order, columns
Y/Y,YY/YY,YY/bY,YY/cY,YY/bcY,XY/XY give the exact minor

    [ 0  -28   -8   -8   -8    0  ]
    [ 0    0  -36    0    0    0  ]
    [ 0    0    0  -36    0    0  ]
    [ 0    0    0    0  -36    0  ]
    [ 0    0    0    0    0  -72  ]
    [90 1260  720  720  720 6480  ].

Its determinant is8465264640. Both whole rational inverse products
are checked, so

    dim(E_tau intersect invariant space)=143-29-6=108. (4)

## A strict center from an original zero-degree perturbation

Let C_line(t) be the published attaining postline, with tau=U+t and
0<=t<=r. Its whole143-coordinate endpoints are the credited boundary
and postline files. Its NN coordinate derivative is exactly

    Y/XY:1, X/XY:1, XY/XY:-1/4, Y/Y:-682/45,
    YY/YY:-1/84, YY/bY:-1/36, YY/cY:-1/36, YY/bcY:-1/36,

and every other free coordinate is constant. The published theorem
gives T_line,Bcap_line>=I/1024 for **every real t in[0,r]**. Its
unforced entry margins and retained strict KK/nonselected GG:m0
repair margins exceed1/256. These spectral bounds are explicit
credited theorem premises; no old factor or positive checker is rerun.

Define a symmetric original NN perturbation V by these nine orbits,
zero on every other original position including all star/anchor/empty
positions and the actual loop:

| Coordinate | V per original edge | Individual unordered edges |
|---|---:|---:|
| YY/XY | -1 | 3240 |
| bY/XY | -1 | 810 |
| cY/XY | -1 | 810 |
| bcY/XY | -1 | 810 |
| YY/YY | 9/14 | 630 |
| YY/bY | 9/4 | 360 |
| YY/cY | 9/4 | 360 |
| YY/bcY | 9/4 | 360 |
| XY/XY | 7/8 | 3240 |

Every original NN vertex degree of V is zero. At a YY vertex it is

    28*(9/14)+3*8*(9/4)-72=18+54-72=0;

at a bY,cY or bcY vertex it is36*(9/4)-81=0; at an XY vertex it is
72*(7/8)-36-3*9=63-63=0. Every other vertex has zero incident V.
Equivalently the unordered total is

    630*(9/14)+3*360*(9/4)-3240-3*810+3240*(7/8)=0.

By(1) all original empty entries and the actual loop are unchanged.
Anchor and star coordinates are unchanged since only NN edges move.
Thus in the original completed303-by303 L, the difference is literally
alpha V on proper NN positions and zero elsewhere; in the free301-by301
T it is alpha V_Q,Q, and Bcap changes by -alpha V_Q,Q. The checker
verifies both entire original L representations and all lower/upper
physical difference positions at the new endpoint, not just a sector.

For t>0 set alpha=t/64 and

    C_new(t)=C_line(t)+(t/64)V.                       (5)

The5670 released KG repairs become -t/64<0. All3240 WW repairs become

    -t/4+(7/8)*(t/64)=-121t/512<0.

Every fixed KG:m0 and GG:m1 repair stays zero. All selected proper
floors, the75 bad empty floors,90 empty/W floors and the actual loop
stay at tau. Strict KK and remaining GG:m0 signs survive; every
unforced entry stays above its floor. Indeed the largest coefficient
of V has absolute value9/4, and

    1/256-(9/4)*r/64=32759/8388608>1/512.              (6)

The checker also directly pays all180 invariant scalar constraints
and every NN sign at both endpoints of(5), as well as every72817
allowed ordered original position at t=r. The only3391 forced ordered
positions are the actual loop, empty/K and empty/W positions, and
selected proper positions. All other endpoint entries have surplus
at least42325/3145728. Affinity of the original entries and fixed
repair signs proves these statements for **every real t in(0,r]**;
released KG and WW signs follow their exact nonzero slopes above.

The changed KK, KG:m1 and WW coordinates all stay nonpositive as
repairs and contribute zero to P. No positive repair coordinate
changes from the attaining line. Hence(5) has the same cost
P=P0+38(U+t)+810t. At t=r its entire original NN cost is
28529893/196608, checked from the original individual coordinates.

For the spectral bound, V is symmetric and its original row-absolute
sums are144 at YY,162 at bY,cY,bcY,126 at XY, and0 elsewhere.
Thus ||V_Q,Q||_op<=162. This elementary bound follows, for example,
from |2v_i v_j|<=v_i^2+v_j^2 in its symmetric quadratic form.
For every real t in[0,r], the published physical bounds and(5) give

    T_new,Bcap_new >= [1/1024-162r/64]I
                   = (943/1048576)I > I/2048.         (7)

Here Bcap=N Gmetric^-1-T, with
Gmetric^-1=I-rr^T/61-bb^T/242 from the credited full original lift.
No full/sector LDL is newly claimed. The same original lift gives
rank302 for L and NI-L and the conservative other301 gap1/495616.
Original nonnegative symmetric stochastic competitors automatically
satisfy the upper PSD bound; it is not an extra competitor hypothesis.

## Actual affine hull and relative interior

For each t in(0,r],(5) belongs to E_(U+t), obeys all original
constraints, is strict in every scalar/sign inequality not fixed
by this affine space, and has positive definite T. There are only
finitely many scalar/sign constraints. Their continuity and PD
openness therefore give a relative open ball in E_(U+t). This proves
that(3) is the actual affine dimension, rather than only a formal
equality-rank upper bound. The center is invariant, and the same
argument in the invariant space gives(4).

Conversely, if an unforced entry/sign slack vanishes at an optimizer,
its nonnegative affine functional defines a proper supporting face:
the center has a strictly positive value. If T is singular, take a
nonzero v in its kernel. The functional v^T T v is nonnegative on the
optimizer set, zero at this point and strictly positive at the center,
again defining a proper supporting face. Neither point is in relative
interior. Strict scalar/sign conditions and T>0 suffice by the open-ball
argument. This proves the claimed exact relative-interior criterion.
These are ordinary finite-dimensional bridges, not formalized theorems.

Combining the credited lower/boundary geometry with this result, the
full/invariant dimensions on the proved cost-minimum interval are

| Floor parameter | Full dimension | Invariant dimension |
|---|---:|---:|
| 0<=tau<U | 24969 | 113 |
| tau=U | 15969 | 104 |
| U<tau<=U+r | 24789 | 108 |

The published attaining postline has every KG repair zero and thus
lies on a proper face of the newly described optimizer set whenever
t>0. No uniform relative radius as t tends to0 is asserted.

## Reproduction, credit and precise limits

Run `python -B check_refined.py` or `python -B -O check_refined.py`
with the unmodified sibling q19-sharp-ceiling source. Before mathematical
imports, the checker binds the **whole published nineteen-file parent
manifest** and every defining file. It imports only the disclosed original
model/physical/entry formulas; it decodes both complete credited endpoint
tables. It does not interpret the old EXPECTED, old factors, old positive
drivers or peer data as mathematical evidence. Boundary/postline JSON
status fields describe their historical creation; the actual paid parent
theorem supplies the spectral premise.

The paid private normal and optimized runs agree on their **entire30552-byte** canonical
mathematical record, SHA256
9a3503ca17cab704038f9998f8e923caab8dc8e1af674d068f3a6f383e0756a0.
Only two explicitly identified runtime observations are removed. The
maximum completed child runtime is6.246567486s and peak RSS95920KiB,
under the fixed45s guard and six native settings1, with one serial child.
An initial rank-census bug that included cancelling star columns was
corrected before these checks; that failed debug run is not validation
or mathematical nonexistence. No solver or floating computation is used.

The primary problem is EFF Conjecture H, Section4 of
[arXiv2609.28404v1](https://arxiv.org/html/2609.28404v1#S4), live
reverified2026-10-05; v1 remains the listed version. Original completion,
mass identities, comparison, published ceiling/cost minimum and spectral
postline are explicitly credited premises. The **new** result is the
complete refined equality geometry, strict zero-degree center and above-U
affine-dimension recovery. It concerns this exact fixed carrier/comparison,
and proves no general H/I, arbitrary-count theorem, global cost or maximal
original entry floor. Reader-source and actual graph commitment remain separate obligations;
old reviewer verdicts confer no child verdict. VALIDATION.json gives the
new complete isolated reader checks; packaging is not new mathematics.
