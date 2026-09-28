# Affine normal forms for independent-column Schur constructions

For a reflected cyclic construction with two independent short columns,
all invertible affine relations between the columns admit explicit normal
forms. At modulus 545, the 11772 pairs of affine parameters form 110 orbits
under multiplication by units. One orbit has an exact largest endpoint 214,
with a complete attaining word supplied. A separate 234-point word lies
outside every affine relation, including all its unit images.

These are results about specified construction families. **There is no
new numerical bound for S(6)** and no exclusion of the full independent-column
family. Both 545 target pilots and four additional affine target pilots are
UNKNOWN. We use the greatest-colourable-endpoint convention and include
repeated summands throughout. No historical-priority claim is made for
these elementary coordinate arguments.

## Independent columns and their exact criterion

Let a be odd and n=5a. Symmetric E0,...,E5 partition Z_a minus {0}.
Independently partition Z_a into R1,A2,A3,A4,A5 and into R2,B2,B3,B4,B5.
For 0<=q<a, colour 5q+1 by 0 on R1 and by i on Ai; colour 5q+2 by 1 on R2
and by i on Bi. Give each reflected point n-(5q+b) the same colour.
Colour 5q by i on Ei for q!=0. Empty classes are allowed.

The full word is sum-free modulo n if and only if:

1. Each Ei is sum-free modulo a.
2. E0 avoids R1-R1, and E1 avoids R2-R2.
3. Ei avoids (Ai-Ai) union (Bi-Bi), for i=2,...,5.
4. (Ai+Ai) is disjoint from Bi.
5. -1 is absent from Ai+Bi+Bi.

For the proof, an axis sum gives condition 1. Equal opposite short residues
cancel onto the axis and give conditions 2 and 3; adding an axis point to
another point gives the same difference exclusions. Among positive short
coordinates,1+1=2 gives condition 4. Both 1+2=3=-2 and 2+2=4=-1 give condition 5,
including the carry 1 in their long-coordinate sum. Other signs rearrange
or negate one of these equations. The special short pairs {1,-1} and {2,-2}
are themselves sum-free modulo 5. These cases exhaust the possible sums,
proving necessity and sufficiency, including doublings.

Ai and Bi individually need not be sum-free. In particular Q1(0) and Q2(0)
need not be residual. Here Q1,Q2 denote their state maps, with state R
encoded by 0, and common states 2,...,5 unchanged. Permuting the common
names simultaneously is sound. An independent exchange of E0 and E1
alone is generally not sound: their difference sets can differ.

The [shared shifted family](../schur6_shifted_fibre_interval_obstruction/README.md)
is the special case Q1=Q2. The earlier
[reflected CRT family](../schur6_reflected_fibres/README.md)
will appear as another affine normal form below. Coprimality with 5 is
not needed for the independent-column criterion.

## All unit dilations preserve the independent family

For any unit u modulo 5a, send every point x to ux. If u is 2 or 3 modulo 5,
also exchange special colours 0 and 1 globally. If u is 1 or 4 modulo 5, keep
those colours. Keep every common colour unchanged. This preserves the
family: units permute the two short residue pairs, and multiples of 5
remain on the axis. It preserves every modular sum and global reflection.

This is a symmetry of the full family, not of a fixed specified class.
For a prime a>45 in the six-colour model, it justifies E(1)=0 as an
existence normalization. Otherwise, if both special axis classes were
empty, the axis would four-colour [1,a-1], contradicting the established
S(4)=44. Choose a nonzero q in one special axis class. CRT gives a unit u
with uq=1 modulo a and with u=1 modulo 5 if that class is 0, or u=2 modulo 5
if it is 1. The transformed axis has colour 0 at 1. No such normalization
is used for the fixed 158-point target or for arbitrary fixed affine parameters.

The external value S(4)=44 is recorded, together with the convention,
in [Heule's primary paper](https://arxiv.org/html/1711.08076).

## Classification of all affine column parameters

Assume now a>=3 is odd and coprime to 5. Impose the specified relation

    Q2(q) = Q1(lambda*q + delta),

where lambda is a unit modulo a and delta is arbitrary. Define

    gamma = 5*delta + 1 - 2*lambda  (mod a),
    d = gcd(gamma,a),
    L = {lambda, -lambda^(-1)}.

**Theorem.** The parameter orbits under the unit dilations above are
classified exactly by the pair (L,d). Every divisor d of a occurs for
every slope orbit L. Consequently the number of parameter orbits is

    ((phi(a)+r(a))/2) * tau(a),

where r(a) counts the roots of lambda^2=-1 modulo a, and tau(a) counts
the positive divisors of a.

These are orbits of a specified affine relation, not disjoint sets of
words. For example a constant state map may satisfy multiple relations.
The theorem neither asserts existence in each orbit nor classifies every
possible equivalence between individual colourings.

### Proof

Let H be the units u=1 modulo 5. Write t=(u-1)/5. Sending x to ux sends
the positive coordinate 5q+b to 5(uq+bt)+b. Substitution in the relation
therefore gives

    lambda' = lambda,
    delta' = u*delta + (1-2*lambda)*t,
    gamma' = u*gamma  (mod a).

CRT makes the reduction H -> (Z_a)^* surjective. The orbits of gamma
under all units of Z_a are precisely its gcd classes. One elementary
way to see transitivity is prime-power decomposition: two residues with
the same valuation differ by a unit after their common prime power is
removed; lift that unit to the full prime power and combine the lifts
by CRT. This includes gamma=0.

The unit 2, with the required global exchange of special colours, acts by

    lambda' = -lambda^(-1),
    delta' = 2*lambda^(-1)*delta - 1,
    gamma' = 2*lambda^(-1)*gamma.

For example its first new column is the old second column at (-q-1)/2,
and its second new column is the old first at q/2, giving these formulas
directly. The group of all units modulo 5a is generated by H and 2, since
2 generates the units modulo 5. Thus L and d are invariant, and the
preceding transformations reach every parameter with the same L,d.
Finally lambda -> -lambda^(-1) is an involution, with exactly r(a) fixed
points. Its number of orbits is (phi(a)+r(a))/2. As 5 is invertible modulo a,
varying delta makes gamma arbitrary, so each of tau(a) gcd classes occurs.
This proves all assertions.

At a=109, phi(a)=108 and the roots of -1 are 33 and 76. The 11772 parameter
pairs have 110 orbits:53 of size 216,2 of size 108,53 of size 2 and 2 of size 1.
The four fixed-slope representatives tested here are

    (lambda,delta) = (33,13),(33,100),(76,52),(76,30).

The first and third have gamma=0; the others have gamma=-1.

## Why signed shifts do not provide new prime-factor families

The signed shifts Q2(q)=Q1(epsilon*q+delta), epsilon=+1 or -1, constitute
the single slope orbit {1,-1}. At a prime a!=5 they have just two orbits.

For epsilon=+1, write Gamma=5*delta-1 modulo 5a. If gcd(Gamma,a)=1,
the unit u=-Gamma^(-1) modulo 5a automatically satisfies u=1 modulo 5
and sends delta to 0. Thus the primitive orbit is the shared shifted
family. The other orbit has delta=5^(-1) modulo a. Setting
F(t)=Q1(t-delta), the common state at 5q+b is F(q+b*delta)=F(delta*x).
The CRT coordinates (delta*x modulo a, x modulo 5) give exactly the older
reflected product rule. In a valid word F(0) is necessarily residual.
For epsilon=-1, multiplication by 2 first sends the offset to -2*delta-1
and makes epsilon positive.

At 109 the exceptional signed pairs are (+1,22) and (-1,43); the other 216
signed parameter pairs belong to the shared shifted orbit. Changing only
a shift or reflection therefore does not escape those two older families.

There is also an all-odd-a signed version, even when 5 divides a. Its
parameter orbits are indexed by divisors of a coprime to 5, with invariant
gcd(5*delta-1,a) for epsilon=+1 and gcd(5*delta+3,a) for epsilon=-1.
Indeed the positive offsets correspond bijectively to residues Gamma=-1
modulo 5 in Z_(5a). Unit orbits there are gcd classes. Any unit taking one
such Gamma to another must be 1 modulo 5, so restriction to H does not
split a class. Multiplication by 2 handles the negative sign as above.

## An affine orbit with exact endpoint 214

For any odd a, consider Q2(q)=Q1(q/2), where division is modulo a.
If Q1(q) is a common colour, the points 5q+1 and its double modulo 5a,
whose positive short coordinate is 5(2q mod a)+2, have that same colour.
Thus every Q1(q) must be residual; Q2 is also residual everywhere.
The difference exclusions force E0=E1=empty. Conversely any symmetric
four-colouring of Z_a minus {0}, using the common colours on the axis,
completes this all-residual pair of columns.

The external S(4)=44 theorem implies a-1<=44. Oddness gives a<=45;
a=45 is impossible because global reflection gives the same colour to
15 and 30 on the axis, contradicting 15+15=30. Hence a<=43 and the endpoint
is at most 5*43-1=214. The supplied complete 214-point word has a=43,
lambda=22,delta=0 and class sizes 86,86,10,10,10,12, so the cap is attained.
Its 214 entries and all doublings are checked independently.

The entire unit orbit shares this obstruction. At 109 its two parameters
are (55,0) and (107,108). This is one excluded parameter orbit among 110;
the other 109 are not excluded by this result.

## A complete example outside every affine relation

The supplied 234-point word has a=47 and class sizes 74,28,32,32,36,32.
Its first residual set has 37 coordinates and its second has 9. Every
invertible affine relation between the state maps would preserve these
cardinalities, so none exists. Every unit image keeps these two sizes or
exchanges them. Each common colour occurs in both short column pairs,
so choosing a different common colour as a special one cannot restore
the required residue support. This obstruction persists under global
palette relabelling as well. The verifier checks the residue supports
and cardinalities; all 184 unit images have also passed the full-word
checker locally. This is a strictness example, not a record Schur partition.

## Exact audits and unresolved target searches

The independent auditor fills symbolic cells by point reflection and
projects modular sums enumerated by their output. These clauses equal
the reduced criterion exactly. At 545 it checks 147968 unordered nonzero
modular pairs, giving 112756 distinct Schur clauses and 1414 indicators.
The four affine target projections are independently compared as well.

All 944784 assignments of the a=5,four-colour toy instance are evaluated.
7394 satisfy the clauses, including 7368 with unequal columns. Every
surviving word and its common-palette-normalized image is checked against
all integer and modular sums. The smallest a=1 case has 21 of 25 assignments
valid. These are finite audits supplementing the all-parameter proofs.

The affine parameter audit at 109 covers every parameter orbit and every
unit, with 5179680 independent symbolic point checks. It also checks 7,13,
47,61 and 77. The signed audit includes long factors divisible by 5.

The package supplies complete controls through 64,214,234 and 304. The 304
word is a unit image of the previous shared-family control. Seven previous
shared words were pinned into the split encoder with identical decoding
and zero conflicts before the target searches. None of these controls
improves the known lower bound.

The six 545 pilots each used a 100000-conflict budget, CaDiCaL 1.9.5 through
python-sat 1.9.dev15, one process and default solver settings. All were
UNKNOWN, at 100000 to 100003 actual conflicts. They were the free normalized
model, a fixed 158-point class, and the four fixed-slope affine cases above.
The fixed class is explicitly labelled as one class only in scaffold.json;
386 positions remain uncoloured there. Its axis is saturated without loss
for its fixed two column supports, but no completion is known.

The exact CNF sizes and hashes, finite audit counts and search statuses
are recorded in expected.json. No UNSAT claim rests on a timeout or an
unchecked solver report. The exact 214 cap uses the elementary argument
and external S(4), not a fresh large solver proof. The primary
[July 2026 shifted-template paper](https://arxiv.org/abs/2607.15034)
still uses S(6)>=536; its base-colouring expansion rule is distinct.

## Reproduction

From this directory, standard-library Python 3.11 or later suffices:

    sha256sum -c SHA256SUMS
    python3 -B verify.py
    python3 -B audit.py --output /tmp/split-audit.json
    python3 -B symmetry.py --output /tmp/signed-orbits.json
    python3 -B affine.py --output /tmp/affine-orbits.json
    python3 -B model.py --axis-factor 109 --normalize-axis --export-cnf /tmp/split545.cnf
    python3 -B affine.py --axis-factor 109 --lam 33 --delta 13 --export-cnf /tmp/affine545.cnf

The three audit outputs can be compared with the corresponding fields in
expected.json. verify.py imports no encoder, solver or orbit code. It
checks full coverage, all sums and doublings, stated affine relations,
the exact 214 attainment, and the 234-point cardinality obstruction.
The orbit audits compare literal point preimages with the formulas;
they do not merely compare two copies of the action formula.

Optional bounded searches require python-sat==1.9.dev15:

    python model.py --axis-factor 109 --normalize-axis --budget 100000 --output /tmp/split-search.json
    python model.py --axis-factor 109 --fixed-scaffold --budget 100000 --output /tmp/fixed-search.json
    python affine.py --axis-factor 109 --lam 33 --delta 13 --budget 100000 --output /tmp/affine-search.json

No generated CNFs, proofs, solver installations, private state or large
logs are committed. The proofs, external S(4) value and finite checkers
are the stated trust boundary; separate peer review is pending.
