# The full-grid compatible mass is a strip-chain/diamond partition

Lyra / literature-researcher-2, 2026-10-06, workday6. New AUTHOR partial
uniform reduction and precisely bounded controls, awaiting Sage's ENTIRE
separate check. Full target410 remains UNSOLVED. Original567 P has now
been rejected at8 by actual whole review658 and author acknowledgment667.
That half-grid premise is retired; an eventual P is not adopted. This
document investigates the already stated full-grid K route from621/634.
It proves no all-size compatible-density or growth inequality.

## Fixed model and exact indices

Geometric band indices are ZERO BASED throughout. A permutation is written
with labels1..q. For p in S_q write pos_p(t) for the zero-based position
of label t. Its inverse is the word p_inverse(t)=pos_p(t)+1, in label
order. Write

    H(p)[t]=1{pos_p(t+1)<pos_p(t+2)}, 0<=t<q-1.

Fix r>=2. Old row inputs sigma_i and old column inputs tau_j lie in Av_r,
i,j=0..r-1. Guard row inputs alpha_h and guard column inputs beta_k lie
in Av_(r-1),h,k=0..r-2. There is one old O(i,j) in every old cell and
one guard G(h,k) in EVERY gap cell. Its coordinates are ordered keys

    O(i,j): x=(2i,pos_sigma_i(j+1)), y=(2j,tau_j[i]);
    G(h,k): x=(2h+1,pos_alpha_h(k+1)), y=(2k+1,beta_k[h]).

Brackets on tau/beta denote zero-based entries. Sort x keys and rank all
y keys to get the output permutation of length N_r=r^2+(r-1)^2. This is
exactly adaptive_full_guard_probe_v1.py's encoder. The previously wholly
checked621/634 decoder recovers ALL4r-2 input permutations from fixed
band lengths. Thus the map is injective, and a_(N_r)>=K_r, where K_r
counts its avoiding input tuples. The accepted monochrome argument is
also an explicit old dependency: every remaining occurrence is mixed.
Its premises are that BOTH old and guard component inputs avoid.

## Claim1: every occurrence is in an adjacent strip or a diamond

First observe a property of the four selected2143 points: the open
rectangle spanned by ANY two selected points contains none of the other
selected points. This follows by checking the six pairs in the rank word
2143; for the two pairs spanning three positions, the remaining point has
an exterior value, and the outermost pair has consecutive value ranks.
Every such pair rectangle is contained in the shaded open rectangle of
the whole occurrence. A grid point inside it is therefore an UNSELECTED
blocker, regardless of its color.

Two old selected points in distinct old rows AND distinct old columns
have the occupied guard G(min_row,min_column) strictly between their
bands in both coordinates. They cannot belong to a box. Consequently
each old selected pair shares a row or a column. Two guards in distinct
guard rows AND columns similarly have the old point
O(min_guard_row+1,min_guard_column+1) strictly between them. Each selected
guard pair therefore shares a row or a column. Three pairwise band-sharing
points must all share one row or all share one column: an L-shaped triple
would contain a diagonal pair.

Consider horizontal cases first; vertical cases follow by inversion.

With three old points and one guard, the old triple is in one old row i.
The guard's odd horizontal band is separate, so it must be the first or
last selected point. The selected old minimum and maximum occupy distinct
columns L<U with U-L>=2. If the guard is in a nonadjacent horizontal band,
an intermediate old row contains an unselected old point in column L+1.
It lies inside the selected position and value bounds. Hence the guard
row is i-1 or i, whichever places it before or after the selected old row.
All four points are in an adjacent old/guard strip.

With three guards and one old point, the guards share one row h. Their
minimum/maximum column gaps L<U satisfy U-L>=2. If the old row is
nonadjacent, an intermediate old row has an unselected point in column
L+1: its even value band lies strictly between the guard gaps and its
position band strictly between the endpoints. The old row must be h
or h+1. Again this is an adjacent strip. These proofs apply whether
the lone point is the first or last selected role.

With two old and two guard points sharing horizontal bands of the SAME
axis, let the old row be i and guard row h. The two points in each band
are consecutive among the four selected positions, so the first two and
last two form descent pairs.

If guards come first, let their lower gap be L and higher gap K>L. Both
selected old values lie above the higher guard; the selected old maximum
is in a column U>=K+2. If i>=h+2, the old point O(h+1,L+1) is an
unselected interior blocker. Thus i=h+1. If olds come first, let the
old minimum column be L and maximum column A>L. Both guards are above
the old maximum; the selected guard maximum gap U is at least A+1.
If h>=i+1, O(i+1,L+1) is an unselected interior blocker. Thus h=i.
This covers every same-axis horizontal2+2 case, including boundaries.
Inversion covers the same-axis vertical2+2 cases.

The only remaining case is a CROSS of axes. Suppose the old pair lies
in old row i and the guard pair in guard column j. Their distinct odd
position bands mean the old pair is either the first two, middle two
or last two selected positions.

If the old pair comes first (roles a,b), its old minimum column L and
old maximum A obey A>L. Both guards are above A, so j>=A>=L+1. Let
their rows be u<v. The unselected old point O(u+1,j) is between the
first and last selected positions and has value strictly above old
minimum b and below guard maximum c. This is impossible. If olds come
last (roles c,d), both are above the guards. The old maximum column
U is at least j+2. With guard rows u<v, O(u+1,j+1) is an unselected
interior blocker, also impossible.

Thus the old pair must be the MIDDLE roles b,c, and the guards the
outer roles a,d. Write their old columns L<U and guard rows u<v.
We have u<i<=v and L<=j<U. Any old column strictly between L and U
would give an unselected point in row i inside the whole horizontal
interval. Hence U=L+1 and j=L. Every intervening guard row at gap j
would likewise give an unselected blocker. Therefore v=u+1, and
u=i-1,v=i. All four selected tags are exactly

    G(i-1,j), O(i,j), O(i,j+1), G(i,j),
    1<=i<=r-2, 0<=j<=r-2.

The transpose is the other orthogonal diamond:

    O(i,j), G(i,j-1), G(i,j), O(i+1,j),
    0<=i<=r-2, 1<=j<=r-2,

where the middle two tags are sorted by their actual positions. Together
with the adjacent horizontal/vertical strips these cover EVERY remaining
box, not just a selected pattern type or a fixed finite domain.

## Claim2: the strip occurrence sets are literal two-block sets

For old pi in Av_r and guard eta in Av_(r-1), define the TWO complete
strip words, of length2r-1,

    Splus(pi,eta)=(2*pi_1-1,...,2*pi_r-1,2*eta_1,...,2*eta_(r-1));
    Sminus(pi,eta)=(2*eta_1,...,2*eta_(r-1),2*pi_1-1,...,2*pi_r-1).

An adjacent strip has one point per involved vertical band. These words
therefore give exactly its relative values, regardless of within-band
ranks of other full-grid points. They also give its entire position
order. Every point in the whole horizontal interval of a selected strip
quadruple is in those two adjacent bands. Thus its full-grid rectangle
is empty iff its strip-word rectangle is empty. Mapping ALL literal
strip occurrence quadruples back to full-grid tags gives the ENTIRE
horizontal-strip occurrence set.

For h=0..r-2 the relevant strips are

    Splus(sigma_h,alpha_h), Sminus(sigma_(h+1),alpha_h).

Reflection about the diagonal preserves boxed2143: its inverse is2143
and the strict open rectangle reflects to the strict open rectangle.
In the inverted grid the horizontal row inputs are

    rho_j=inverse(tau_j), gamma_k=inverse(beta_k).

Thus the complete vertical-strip sets are given by the identical two
words Splus(rho_k,gamma_k),Sminus(rho_(k+1),gamma_k), k=0..r-2.
No tests using tau itself in place of inverse(tau) are substituted.
Monochrome component avoidance and Claim1 exclude all other strip-free
boxes except the two diamonds.

## Claim3: exact two-bit diamond equivalences

For the old-row/guard-column diamond, the selected position order is
as displayed iff H(sigma_i)[j]=1. Its low old point has value in band
2j, its high old point in band2j+2, and both guards in band2j+1.
The guards have roles a,d iff beta_j[i-1]<beta_j[i]. Consequently this
diamond is a2143 precisely when

    H(sigma_i)[j] AND H(gamma_j)[i-1].

It is then ALWAYS boxed. Only old row i lies between the two guard
position bands, and its only points in the selected value interval are
the two selected olds. In the two endpoint guard rows only guard column
j lies in the selected value interval; both of its points are selected.
All other old rows are outside the horizontal interval, and all other
guard columns outside the vertical interval. This proves sufficiency
as well as necessity without a numerical boundary approximation.

By inversion, the old-column/guard-row diamond exists exactly when

    H(alpha_i)[j-1] AND H(rho_j)[i]
    (=pos_alpha_i(j)<pos_alpha_i(j+1) AND tau_j[i]<tau_j[i+1]).

The ranges are those displayed in Claim1. At r2 both diamond families
are empty. At r>=3 every internal index/gap is included. No artificial
boundary diamond or absent guard is added.

Hence the FULL literal occurrence set equals the union of all mapped
adjacent horizontal-strip sets, all mapped vertical-strip sets, and all
present diamonds. Sets are united, so overlap between horizontal and
vertical descriptions never counts an occurrence twice. In particular
the full output avoids iff every adjacent strip avoids and every diamond
conjunction is zero.

## Claim4: exact full-chain multiplicities, not independent components

Let T_r be the family of ALL tuples

    u=(sigma_0,alpha_0,sigma_1,...,alpha_(r-2),sigma_(r-1))

with the specified Av inputs and with both strips at every h avoiding.
Its raw input domain has size a_r^r*a_(r-1)^(r-1). A vertical chain is
the same family on rho/gamma, since inversion preserves their Av domains.
The full strip-filtered tuple domain has size |T_r|^2. Conditioning the
original independent input law on the separate horizontal and vertical
strip tests gives TWO independent uniform WHOLE chains in T_r. It does
NOT give independent components inside either chain: adjacent strips
share the whole old/guard permutations.

The identity old/guard chain belongs to T_r for every r>=2. Each identity
strip is a concatenation of two increasing blocks; two disjoint descents
cannot both cross its single block boundary. It contains no classical
2143, and therefore no boxed2143. Thus |T_r|>0 and the conditioning is
defined without deleting any dead old-core repair fibers from K_r.

For a chain u retain its full tuple of comparison words

    x_i=H(sigma_i), z_h=H(alpha_h).

Define m_r(x,z) as the number of ACTUAL full tuples in T_r giving that
word tuple. Every permutation and every multiplicity is retained. In
particular sum_(x,z)m_r(x,z)=|T_r|. For a vertical chain write y_j,w_k
for the words of rho_j,gamma_k. Claim3 gives the compatibility indicator

    F_r((x,z),(y,w))
      = product_(i=1..r-2,j=0..r-2) (1-x_i[j]*w_j[i-1])
        *product_(h=0..r-2,j=1..r-2) (1-z_h[j-1]*y_j[h]).

The products are Boolean zero/one, with empty products equal to one.
The exact full-grid compatible count is

    K_r=sum_(x,z),(y,w) m_r(x,z)*m_r(y,w)*F_r((x,z),(y,w)).

This equality is uniform in r and retains the actual original Av
population. One cannot replace m_r by one per attained state, by products
of marginal component weights, or by independent comparison bits. The
chain constraints and cross clauses retain their shared inputs.

The two independent chains need not be compatible. For r>=3 pairing
the identity chain with itself gives every available diamond bit equal
to one, hence compatibility zero. Therefore a positive lower-density
claim for arbitrary chain weights is false: with chain law
(1-epsilon)*delta_identity+epsilon*uniform(T_r), full support remains,
but compatible probability is at most1-(1-epsilon)^2<=2epsilon. This
does NOT refute the actual uniform law on T_r or any proposed bound for
that law. It prevents silently replacing the mathematical population by
an arbitrary positive-weight model.

Write theta_r=K_r/|T_r|^2. The actual unresolved sufficient hypothesis
from621/634 is fixed r0>=2,delta>0 with

    theta_r >= 2^(delta*N_r)*a_r^(2r)/|T_r|^2 for EVERY r>=r0.

No such estimate is proved. If it were, the checked decoder would give
t_(N_r)>=t_r+delta, where t_r=(log_2 a_r)/r; iteration would solve the
full negative alternative. The reduction is neither an adoption of that
unproved premise nor a replacement target. In particular the two-block
boundary at r2 gives |T_2|=4,K_2=16=a_2^4, so positive delta could not
hold starting at2; an existential r0 was already part of the original
full-grid hypothesis. No starting size or delta is fitted from finite data.

## Exact controls fixed before execution

FULL_GRID_STRIP_DIAMOND_PLAN_V1.md was pinned before the controls and
posted662. Its historical pending642/646 status is immutable; actual
657/658 author acknowledgment667 supplies the current checked status.
New full_grid_strip_diamond_probe_v1.py imports the exact pinned encoder
and literal checker. It tests the new reduction, not its own output
count through a second copy of that kernel. These are SAME-AUTHOR
controls, awaiting a different researcher's uniform argument and ENTIRE
finite-field check. Executed source/report bytes are unchanged.

All avoiding strip-component pairs through5 are checked in BOTH directions.
The complete domain sizes are2,12,138,2438; safe counts per direction
are2,11,103,1423. Size4 uses Av_4 of size23, not all24 permutations.
All full strip sets, mixed-type totals and first representatives are
retained or streamed. At4 each direction has27 one-guard,4 two-guard and
12 three-guard occurrences; at5 the totals are799,208,490. These establish
nonvacuous coverage of all mixed color counts, not an all-size estimate.

The full literal-grid control domain has exactly1694 cases:

* r3:96 precisely generated old cores (single-component changes around
  identity/reverse and constant row/column choices), with ALL16 guard
  profiles each,1536 full literal scans;
* r4:both axes/every internal index and gap/ALL four diamond bit states,
  48 full literal scans, retaining unrelated boxes as well;
* r5:110 distinct fixed identity/reverse profiles with one-component
  changes among four prescribed old/guard choices,110 full literal scans.

EVERY full box set equals the strip/diamond union. Total mixed occurrence
counts with1/2/3 guards are536/5672/24; none of those types is vacuous.
All1694 full input/output records and decomposition fields are retained.
The ordered complete full-box-set stream is
1e0a9c6c7f74d2526bbfff06643d97fe68aed0b451a1a510f8642511facd06d0.
This is not a larger tuple census or a count of selected boxes only.

Only after these controls passed, the COMPLETE small raw chain domain at3
was enumerated:864 tuples,616 strip-safe chains,256 attained full-chain
comparison-word states with EVERY multiplicity retained. All65536 ordered
word-state pairs give the exact weighted kernel count K_3=88456. The
full raw grid domain is746496 tuples and strip-filtered domain379456.
Neither domain was wholly scanned by the literal full-grid oracle. K_3
is computed by the uniform kernel theorem plus its exact finite partition,
not claimed as a complete746496 literal-grid census.

All616 chains and all256 word weights are retained. Their ordered streams:

    chains 2857b46eeba38c0fe33db1785314d32fff494f468463d9ab0364bab7ce6b1f5b;
    partition 39f385e8e6adc4be5f2e852802be448349760dd091da86b64b3d8d0cfba2b292.

The ratio88456/a_3^6, where a_3^6=46656, supplies NO all-size delta.
Runtime7.155845216s/27216KiB, Python3.11.2, one job/thread. Source SHA
506ffef0783f2c20d8b3341a8044c42741377e12ed716b4a656cb21e981bff05.
The complete JSON pins its own source and all three executable/plan
dependencies. The review packet also pins this uniform proof and the
actual earlier whole decoder/monochrome review634 with its manifest.

Reproduce using fresh output, CPython3.11+/standard library/thread1:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 python3 -B full_grid_strip_diamond_probe_v1.py --output /tmp/lyra-full-grid-strip-diamond-new.json

Requested new ENTIRE check: all-size Claims1--4, actual boundary indices,
full occurrence-set equivalence, multiplicity-retaining K identity and
positivity, the arbitrary-chain-weight limitation and r2 boundary, ALL
specified deterministic strip/grid/chain/partition fields and streams.
Excluded: the positive delta inequality, larger grid censuses, novelty,
full410, source publication and graph originals. The next mathematical
obligation is an actual uniform weighted population estimate or a precise
failure of it, rather than an unweighted state count or a bigger favorable
table. No source/graph scope or team target changes through this reduction.
