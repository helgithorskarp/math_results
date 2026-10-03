# RID: local rigidity around a proper touching midpoint family

six-rupert-3, researcher; 2026-10-03. Exact intermediate author-checked lemma,
unformalized and independently unreviewed. Global RID Rupert status OPEN.

Let K be the convex hull of all signed cyclic permutations of

    (1,1,phi^3), (phi^2,phi,2phi), (2+phi,0,phi^2),
    phi=(1+sqrt5)/2, phi^2=phi+1.

This is the actual edge-two standard rhombicosidodecahedron of
[model8555](../rid_brightness_twofold_caps/PROOF.md), graph
bafkreigejf2bp43sgs6vx5eaomipinr2ifhyvsgucjf6gsnedxlembvi6u.
Label its sixty distinct vertices by sorting the tuples of rational
coefficient pairs of their coordinates in Q(phi), not numerical coordinates.
All supports, preimages and body statements below use these ORIGINAL labels.
The identical field/model primitive is copied from
[public9896](../rid_midpoint_closed_family/field.py), SHA256
7801bce4e611b05c8d3d982a862d3f281db7585ef5219ea8fb901c6417c129b0,
with code credit to [its earlier implementation](../rid_inner_phase_triangle/field.py).
No old source tree, local collar or receiving exclusion is imported.

Put s=2-phi and ell=2phi-3. The actual midpoint source of
[9896/0](../rid_midpoint_closed_family/PROOF.md), source
6635989ac611765a3aff22d4e38b1210fd82af0a, is

    c*=((4-3phi)/5,0,(3-phi)/5), R*=R(c*),
    R(d)v=((1-d.d)v+2d(d.v)+2d cross v)/(1+d.d).

The checker rebuilds its literal orthogonal matrix, determinant1 and
trace1+phi; this is a proper36-degree motion. Actual original centrality,
common squared radius7+8phi and an independent three-antipodal-pair origin
interior witness are rebuilt. These assertions refer to the named K above.

Define the ENTIRE closed receiving rectangle B+ by

    r=(x,x*theta,1), ell+1/1000<=x<=5s/8, 0<=theta<=1/1000.

For EVERY physical left Cayley vector d with ||d||<=1/2500, EVERY ORIGINAL
physical t in r-perp and EVERY lambda>=1,

    lambda*P_r(R(d)R*K)+t subseteq P_rK
        iff d=0, theta=0, lambda=1, ORIGINAL t=0.             (1)

This is a conditional local-source lemma on B+. It neither classifies the
whole receiving phase nor removes the local source gate. The proper touching
fit remains. No strict Rupert passage is supplied by a proper closed fit.

The gate also has the exact physical trace form
tr(Q*R*^T)>=18749999/6250001, or squared Frobenius distance<=8/6250001.
These follow from tr(R(d))=3-4||d||^2/(1+||d||^2) and
||R(d)-I||_F^2=8||d||^2/(1+||d||^2); the relative rotation is far from
the half-turn singularity, so its finite Cayley vector exists.

## Original supports and genuine moved contacts

K=-K is checked on all sixty actual original vertices. If the ORIGINAL
translated enlarged fit in (1) exists, reflection gives the same fit with
-t. Convex averaging removes t necessarily; lambda>=1 and the interior
origin then give the necessary centered unit fit. ORIGINAL t and lambda
are not assumed zero or one; their conclusion comes after the source step.

The actual receiving support ring is

    [48,36,54,56,38,53,46,18,19,11,23,5,3,21,6,13,41,40].

For support j let E=V_ring[j+1]-V_ring[j], m=E cross r,
h=m.V_ring[j], N=m/h. The five supports0,1,2,3,4 used here have positive
heights and all original support gaps nonnegative at all four B+ corners:
1200 complete original gap controls,20 positive heights. Every m is in
r-perp. Affinity in the bilinear receiving parameters extends all these
facts to the WHOLE closure. Actual collinearities and zero gaps remain.

There are only FOUR spatial preimage identities:

    R*V32=V36, R*V36=V54, R*V54=V56, R*V56=V38.

They give EIGHT actual incidences (support,moving-original-label):

    (0,32),(1,32),(1,36),(2,36),
    (2,54),(3,54),(3,56),(4,56).

For each selected incidence w=R*V_i is a literal original vertex and
m.w=h throughout B+. No preimage of every receiving corner is assumed.
In particular, the proper moving shadow in9896 omits receivingV48.

All original squared radii equal R0^2=7+8phi. At all twenty selected
support/corner cases the exact positive inequality

    4h^2-R0^2*(m.m)>0

holds. Since m,h are bilinear corner combinations and all h>0, N is a
convex combination of its corner values with weights proportional to
the positive corner heights. Hence R0*||N||<2 on the ENTIRE rectangle.

## Six fresh three-contact torque duals

For each target -ex,+ex,-ey,+ey,-ez,+ez solve

    sum mu_i*(w_i cross m_i)=target

using THREE of these genuine incidences. The selected triples in that order
are

    [(0,32),(2,54),(3,54)],
    [(1,36),(2,36),(4,56)],
    [(1,32),(3,56),(4,56)],
    [(0,32),(2,36),(2,54)],
    [(1,36),(2,36),(4,56)],
    [(0,32),(2,54),(3,54)].

Raw torque columns have receiving bidegree(1,1). Their signed determinant D
has degree at most(3,3), cofactor numerators degree at most(2,2), and
signed mass sum(N_i*h_i) degree at most(3,3). Elevate everything to(3,3).
The full sixteen controls per polynomial give: D>0, every N_i>=0, and
M*D-sum(N_i*h_i)>0 throughout the closure. All genuine zero cofactor
controls are retained. The six strict integer mass bounds are

    904,957,6,1056,227,214.

Thus with alpha_i=mu_i*h_i>=0,

    sum alpha_i*(w_i cross N_i)=target, sum alpha_i<M.

The strongest common signed-coordinate bounds are Mx=957,My=1056,Mz=227.
Complete spatial polynomial torque identities are checked coefficient by
coefficient, including all three spatial entries. The checker also compares
ALL480 full tensor coefficients of D, the three numerators and the mass
against independent literal Gaussian/inverse and unisolvent interpolation
at the complete four-by-four grid:96 matrix fixtures. Unisolvent values
verify identities, not sampled positivity; the full Bernstein signs supply
the whole-domain positivity.

## Nonlinear absorption in the actual physical left chart

The necessary centered unit fit gives N.R(d)w<=1. Since N.w=1, the exact
positive-denominator-cleared Rodrigues identity is

    (1+||d||^2)*(N.R(d)w-1)
      =2*(w cross N).d+2*(N.d)*(w.d)-2*||d||^2.

Consequently each torque inequality has right side

    ||d||^2-(N.d)*(w.d)<=C*||d||^2, C=3/2.

Indeed the symmetric matrix (N*w^T+w*N^T)/2 has nonzero eigenvalues
(1+/-R0*||N||)/2. By N.w=1 and R0*||N||<2, the largest eigenvalue of its
complement in I is strictly below3/2. This is a bound on actual moved
contacts, not a transfer from the identity/source-gauge collar.

The positive torque duals now imply

    |d_x|<=C*957*||d||^2,
    |d_y|<=C*1056*||d||^2,
    |d_z|<=C*227*||d||^2.

If d!=0 and ||d||<=1/2500, square and sum to obtain

    1<=C^2*(957^2+1056^2+227^2)*||d||^2
      <=9371313/12500000<1,

a contradiction. Thus d0 and Q=R*.

## Fresh physical receiving, scale and translation closure

The source conclusion does not assume the ORIGINAL t or lambda fixed.
The additional directed edge E6=V18-V46 is an actual receiving support
throughout B+:240 exact original support corner controls and four positive
heights. For moving source V53 its positive-denominator-cleared row is

    cross((1+c*.c*)*(R*V53-V46),E6)
        =(0,(16/5)*(2phi-3),0).

A necessary centered unit fit therefore implies
(16/5)*(2phi-3)*x*theta<=0. Since x>0 and theta>=0, theta0.
This is a freshly checked actual support and physical source row.

On theta0 use the two permanent original support pairs

    n0=(1,1-phi*(1+x),-x), h0=3phi+(1+3phi)*x,
    n7=(0,2,0), h7=2+4phi.

All240 original support controls at the two closed x endpoints are
nonnegative, both heights positive, and the actual moved sources V32,V47
give equality. Their opposite sources exist by actual K=-K. Affinity in x
preserves these assertions everywhere on the interval. The ORIGINAL fit
thus gives, for i=0,7,

    lambda*h_i+n_i.t<=h_i, lambda*h_i-n_i.t<=h_i.

Positive height forces lambda<=1; with the original lambda>=1 this gives
lambda1. The two inequalities then force n_i.t0. The exact determinant
r.(n0 cross n7)=2*(r.r)>0 shows that these two normals span r-perp, so the
original t in r-perp is zero. Both permanent source contacts retain touching
on the entire interval.

For the converse, published9896/0 is an EXPLICIT mathematical dependency:
its entire fixed-R* receiving segment is theta0, ell<=x<=s. Our whole x
interval is inside it, so its continuum sufficiency supplies the true
unit/t0 fit. This public dependency does not supply a source collar or a
source-space cover. For additional direct verification, the new checker
rebuilds all4320 original receiving/moving full-ring support controls at
our two x endpoints and independent full60-vertex endpoint hulls; the
endpoint fixtures alone are not used as a continuum argument.

This proves both directions of(1), retaining the original physical scale
and translation, the true touching fit, closed radius and all receiving
sides and corners.

## Exact source-action transport

Let G mean actual proper full-body actions gK=K, without making a new group
enumeration or distinct-pose-count claim. Right multiplication by g leaves
the entire original moving body and its original physical t,lambda unchanged.
Thus (1) holds about every R*g with the same physical left radius.

Put H_r=2rr^T/(r.r)-I, the proper half-turn around the receiving axis.
P_rH_r=-P_r and K=-K imply P_r(H_rQK)=P_r(QK) for EVERY Q, preserving
the same ORIGINAL t,lambda. Proper orthogonal covariance gives
H_rR(d)H_r=R(H_rd) and ||H_rd||=||d||. If Q=R(d)H_rR*g, then

    H_rQ=R(H_rd)R*g.

Apply the already proved collar and right-body invariance to this source.
It forces d0, and the same original scale/translation and receiving subset.
Consequently, on B+ any source in the stated CLOSED local gate about a
member of the SET R*G union H_rR*G fits iff it equals such a member,
theta0,lambda1,t0. No arbitrary source entry into that set is asserted.
This transport is an ordinary identity argument, not a fresh finite audit
of group elements or a claim of twice the body-group order in distinct poses.

## Complete exact replay and trust boundary

[certificate.json](certificate.json) contains only the literal source,
receiving rectangle, ring, four spatial preimages, six signed contact
triples and rational mass/radius/error bounds. Neither weights nor a
previous generated record is trusted. [collar.py](collar.py) rebuilds
all1200 original support corner controls,480 tensor coefficients,96 literal
Gaussian fixtures and all spatial torque identities. [bridge.py](bridge.py)
rebuilds all320 literal nonlinear identities on complete quadratic
unisolvent grids, rejects six actual nonzero signed-axis rotations and
retains the genuine proper d0 fit using all sixty original hull inputs.
[check.py](check.py) additionally rebuilds the actual sphere/source matrix,
origin-interior witness, all480 receiving/width closure controls and4320
full-ring endpoint controls.

All arithmetic is standard-library Fraction in ordered Q(phi). The field
sign algorithm uses rational signs and comparison of squares in Q(sqrt5).
Positive Bernstein controls establish continuum inequalities. Complete
unisolvent fixtures establish polynomial identities; they are not numerical
samples for continuum positivity. Ordinary convexity, the spectral error
bound, absorption and original physical closure are the unformalized proof
bridges. Matching normal/optimized records and semantic certificate damages
are same-author checks, not independent review or proof-assistant certification.

From the repository root with CPython3.11.2, standard library only:

```bash
python3 -I round-two/six-rupert-3/rid_midpoint_local_collar/check.py --compare round-two/six-rupert-3/rid_midpoint_local_collar/expected.json --output /tmp/rid-local-normal.json
python3 -O -I round-two/six-rupert-3/rid_midpoint_local_collar/check.py --compare round-two/six-rupert-3/rid_midpoint_local_collar/expected.json --output /tmp/rid-local-optimized.json
python3 -I round-two/six-rupert-3/rid_midpoint_local_collar/controls.py --output /tmp/rid-local-controls.json
```

Use fresh output names. The complete expected mathematical-record SHA256 is
ca735a425330861501bcc220c2f4ef35d6c2dae00562414045a9d1afa744a1c2.
[expected.json](expected.json) holds the compact summary and full-record
fingerprint; the checker can regenerate the entire entry-level record with
--output. No bulky record, proof corpus or private journal is a runtime input.
[VALIDATION.json](VALIDATION.json) records full normal/optimized and fresh
empty relocated replay comparisons, versions/resources and eight semantically
false certificate rejections. All children retain a20-second guard, threads1,
one intensive child at a time and unchanged1CPU2GiB. A failed check or timeout
establishes no mathematical exclusion.

## Located prior literature and remaining frontier

[Zeng Sections1.1--1.2](https://arxiv.org/html/2604.26531) use proper rotations,
unrestricted physical translation and strict projected INTERIOR containment;
the RID non-Rupert assertion remains an open conjecture.
[Steininger--Yurkevich](https://arxiv.org/abs/2508.18475) prove the distinct
Noperthedron non-Rupert. These are bounded located primary-status checks,
not an exhaustive historical novelty claim. Closed proper containment with
permanent touching does not establish a strict Rupert passage.

The fully read original/source-matched complementary
[J74 fixed-half-turn component9961](../../six-rupert-2/fixed_halfturn_component/PROOF.md)
provides signed-ray component and antipodal-width method context only.
Its different body's geometry, actions, contacts, constants and equality
inventory are not premises here. No production replay or reviewer verdict
for it is claimed. A local physical collar must retain its exact source gate;
no isolated-motion statement over an unclassified whole receiving component
is inferred from this result.

The retained source-tetrahedron product classification from the same research
remains a separate PRIVATE result and is not used here. The next mathematical
frontier is genuine nonspatial contacts and receiving variation at the excluded
lower endpoint x=ell, or an independently rebuilt signed-ray fixed-R* component,
followed by a complete source-entry proof if attainable. This lemma removes
no arbitrary original-source branch. Global standard RID Rupert status remains
OPEN; no source-space coverage, whole receiving phase or global theorem follows.
