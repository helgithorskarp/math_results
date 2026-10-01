# Exact single-interval obstruction

Let N=3704 and let b be the literal binary word in `base3704.bits`, equivalently
the formula in the README. For every integer pair0<=L<R<=N, define
c[L,R](t)=b(t) XOR1{L<t<=R}. Then c[L,R] has a monochromatic seven-term AP with
positive integer difference. The pair domain has N(N+1)/2=6,861,660 elements.

For an actual AP p[k]=a+k*d, k=0,...,6, set
h=(0,p[0],...,p[6],N+1). If L belongs to the integer gap
[h[i],h[i+1]-1] and R to [h[j],h[j+1]-1], then exactly the term indices
i,...,j-1 flip. Since L<R, it suffices to consider0<=i<=j<=7. If the seven
resulting bits are equal, the entire Cartesian gap box is obstructed after
intersecting it with the cut domain. This is an exact identity, including
empty term segments, first/last gaps, and equality at AP positions.

`verify_interval_cover.py` derives all36 gap cells per selected AP by actual
seven-bit flips. Its row union merges all active R intervals, clipped to
L<R<=N. `export_interval_cover_bitset.py` independently encodes the actual
seven colors as an integer, XORs contiguous term masks, and ORs active
R masks for each L. Neither checker imports the constructor. They derive525
rectangles from the289 APs in `AP-cover.json`. Their complements agree for
every L in both normal and optimized interpreter modes. The union covers
6,858,761 cuts; the exact2,899-point complement equals `residual-cuts.json`.
No absent AP or failed search is used as an obstruction.

Each [L,R,a,d] in `point-obstructions.json` corresponds to exactly the next
mandatory residual cut in sorted order. `check_residual_interval_points.py`
requires positive integer d,1<=a and a+6d<=N, then reads and flips all seven
actual colors. All2,899 submitted APs are monochromatic. The checker rejects
missing, duplicate, reordered, malformed, out-of-range and bichromatic
obstructions, along with scope/hash mismatches. Thus every residual point
also fails. The rectangle-covered points and the exact residual points
partition the full domain, proving the assertion.

If an AP-free word disagreed with b on one maximal nonempty contiguous run,
it would equal some c[L,R], contradicting the assertion. If it disagreed on
zero runs, it would equal b, which has the explicit AP a=2,d=617. Therefore
every AP-free word on this interval has at least two disagreement runs.
This corollary counts runs relative to this specific base word; no edit-count,
other pole-assignment, all-coloring nonexistence or W-bound conclusion follows.

The method of finding the certificate does not affect its sufficiency. The
289-AP rectangle list resulted from12 full invalid candidate checks and at
most24 positive APs selected per check, plus the original AP. The list is
supplied compactly and rechecked from definitions. Fresh bounded small-step
search regenerates all residual positive APs exactly. The search neither
exhausts arbitrary colorings nor certifies negative solver outcomes.

No external numerical certificate is needed for this proof. The baseline
prefix and primary bounds supply motivation, not an unverified premise.
