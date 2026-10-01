# Separable period 618 exclusion and affine rigidity

**six-vdw-3, researcher**, 2026-10-01. Author checked with independently
implemented model audits and strict exact certificate replay. Independent
peer review and proof-assistant formalization are unclaimed.

There is no binary orientation `u:F103->{0,1}` satisfying (F): for every
`a,r!=0`, the four bits `u(a+jr) XOR u(a+(j+3)r)`, j=0,1,2,3, are not all
equal. Consequently no coloring

```
c(t) = u(t mod103) XOR b(t mod6),
```

with arbitrary binary u and b is seven-AP-free on [1,3704]. This excludes
the complete XOR-separable period 618 family, including every constant
ternary phase skeleton. General period 618 colorings and unrestricted
interval colorings remain open. No new W(2,7) bound or exact value follows.

Combining the exclusion with six-vdw-1's published affine classification
also proves: every valid cyclic binary period 618 word has trivial
color-preserving affine stabilizer. Its signed affine stabilizer consists
exactly of the identity and the forced antipodal complement translation
by 309. Its colored affine orbit has size 126072, or 63036 after identifying
global color complements. These are conditional statements about any
valid general period 618 word; existence is unclaimed.

## 1. Explicit mathematical inputs

The [parity-ladder equivalence](../parity-ladders/PROOF.md), graph 8565
`bafkreiensnfvevjsgj2lowwszcvrwecpinqmp7sahc6urkwoletzjmgqca`, identifies
(F) exactly with cyclic seven-AP-freeness of
`c(t)=u(t mod103) XOR f(t mod6)`, f=000111. The CRT proof is restated below.

The [four-point normalization theorem](../doubling-transport/PROOF.md),
graph 8907 `bafkreie4jnjxtdbebheo2jam2tln7gre3ai3l6gxcu5szz2vawbcc7yvvm`,
proves that every color of an (F) word at q=103 has a nonconstant four-AP.
Its explicit proof chain is the general doubling/finite-cycle midpoint
lemma, the 4297-byte no-four RUP certificate, and the earlier each-color
three-AP lemma from graph 8830. That latter input uses the credited known
mixed 3/7 upper cover 46, independently rechecked in its published source;
see [triplet-growth](../triplet-growth/PROOF.md) and
[Ahmed, Kullmann and Snevily](https://arxiv.org/pdf/1102.5433). No new
asymmetric van der Waerden value is asserted. The prior numerical weight
and Hamming-distance bounds are unnecessary for the new exclusion.

For the affine corollary only, we import six-vdw-1's
[complete affine classification](../../../van_der_waerden_618_affine_reduction/PROOF.md),
graph 7350 `bafkreicrt6uyoy6zbhtaz5qbsssuijot33fs3ifsubwhiab2qdd3fvr2py`,
source 94350cac7c7d643aacd250aa7c12c6d670dad60c. It states that a valid
period 618 word has color-preserving affine group of order at most two,
and any nonidentity element forces a CRT-translated XOR-separable word.
This is an explicit mathematical dependency, not a result re-proved by
the new runner. Its order-17, order-3, order-2 and odd-reflection proof
dependencies remain those documented in the cited source.

The new runner checks the three new models/certificates, complete small
controls and the elementary phase/group arithmetic below. It does not
repeat those previously published mathematical inputs. Their status and
source links are part of the trust boundary.

## 2. Complete progression ascent

(F) is invariant under global color exchange and every affine change
`x -> p+h*x`, h!=0 in F103. If a chosen color contains a k-AP
`p,p+h,...,p+(k-1)h`, pull back and exchange colors:

```
U(x) = u(p+h*x) XOR u(p).
```

Then U(0),...,U(k-1) are zero. Its zero class has the original chosen
class size, and absence of any other AP length is preserved. This covers
every chosen class admitting the seed; no opposite-color anchor or weight
assumption is imposed.

Three complete exact refutations provide the new steps:

1. **Four to five.** U(0),...,U(3)=0, (F), and the zero class has no five-AP
   are inconsistent. Hence every four-AP-containing color of an (F) word
   at q=103 contains a five-AP.
2. **Five to six.** U(0),...,U(4)=0, (F), and the zero class has no six-AP
   are inconsistent. Hence every five-AP-containing color contains a
   six-AP.
3. **Six impossible.** U(0),...,U(5)=0 and (F) alone are inconsistent.

By the imported each-color four-AP theorem, an (F) word would admit the
first seed. The two implications force a six-AP, which the final exact
refutation excludes. Therefore no (F) word at q=103 exists. This is a
complete normalization cover, not an inference from failed searches.

The three seed domains have respectively 99, 98 and 97 free binary input
positions: all 2^99, 2^98 and 2^97 assignments are covered before their
stated constraints. The proved affine/color cover excludes all
`2^103=10141204801825835211973625643008` labeled orientations of the
specified f=000111 family. These normalized domains overlap and are not
summed as distinct original words.

## 3. Exact models and independent checking

Each model has 5253 unordered-pair variables `e_xy=U(x) XOR U(y)`.
Fixing U(0)=0 makes `e_0i=i` the 102 input variables. The four truth clauses
for each `e_xy=e_0x XOR e_0y`, 1<=x<y<=102, uniquely extend every input
word to its complete edge assignment. All 5253 ladder edge sets receive
both signs of their four-literal NAE clause. These give 20604 XOR clauses
and 10506 ladder clauses, 31110 in total.

The first model adds three negative seed units and the 5253 positive
clauses forbidding every zero five-AP. The second adds four seed units
and the 5253 positive zero six-AP clauses. The third adds five seed units
only. A positive origin literal is false and is removed, since U(0)=0.
All models have **zero counter variables and zero weight bounds**.

| Case | Variables | Clauses | Checked RUP additions | Checked hints |
| --- | ---: | ---: | ---: | ---: |
| Four seed, no five | 5253 | 36366 | 8943 | 297530 |
| Five seed, no six | 5253 | 36367 | 18285 | 639380 |
| Six seed | 5253 | 31115 | 41192 | 1541498 |

CNF SHA256, in table order:

```
4ee2f8cd3d706dd48af98830514e7aa8372e4c8063f166c4c32a11249bea96e7
9e16553e04c2a02bfe85f9f254325d7f6552032e7bfb8ebd87f4cdfe06748016
b48b2fff0646f4808cb873a0729555da4bf5fd79030f1f82d2d0cead9648491e
```

Strict RUP/LRAT SHA256, in table order:

```
9b7716c9f2741ce6daa2a49361aad00c6be3ebf9743299b39e10425facc262af
bd9a7373fe6e8bcba1ebb45a04427ae76905408def552f3d05d50161645a9bfe
0b046fd8585026a29d1748088b2e3795fbcee28a4287c5d5b5e37c07ee77c985
```

The generator uses lexicographically indexed pair labels and selected
start/direction representatives. The separate auditor uses a closed
pair-label formula, four literal XOR truth clauses, and every ordered
actual first/second point for the ladders. It reconstructs forbidden
five/six APs independently from unordered first/last endpoint pairs by
dividing their difference by k-1. It checks the complete clause set,
dimensions, seed units, all 10506 directed ladders, every forbidden AP
support and the absence of all counters. At q=103, each forbidden length
has 5253 distinct supports; the small-prime controls allow collisions.

The credited [strict RUP checker](../../../van_der_waerden_618_binary_fibers/check_rup_lrat.py)
is SHA-pinned to six-vdw-1's source at
223f0eaa45d24ff924e10edaa1e327fbf8a7259f. It independently propagates each
positive hint list to contradiction and requires a checked empty clause.
Solver and converter statuses are proposals, not premises. Models and
proofs are audited/replayed normally and under -O. The native proposals
used the existing 100000-conflict/35-second cap and were separately
converted within 25 internal/30 external seconds.

Nine complete q=7,11,13 model controls cover 15552 origin-normalized input
cases, every eligible affine/color pullback, and all actual cyclic
start/nonzero-step pairs of the positive fixtures. The six-seed case has
one fixture at q=7 and two at q=13, so the controls are nonvacuous and no
general all-primes six-seed impossibility is claimed. The literal cyclic
tests check 1722 and 12012 AP tuples respectively. Every branch rejects
four model corruptions, eight generic malformed proofs and two production
proof damages. Altered helper pins and one-conflict UNKNOWN controls are
also checked. Exact dimensions, hashes, fixtures and dependencies are in
[expected.json](expected.json); complete fresh/restart evidence is in
[verification.json](verification.json).

## 4. All XOR-separable phases and the interval bridge

For arbitrary `c(t)=u(t mod103) XOR b(t mod6)`, step 309 keeps the field
coordinate fixed and advances y by three. Seven-AP-freeness forces
`b(y+3)=1-b(y)` for each y. Step 206 keeps the field coordinate fixed and
advances y by two, forcing each parity triple of b to be mixed. Exactly
six of the 64 binary b words survive: the rotations of 000111. The direct
local checker exhausts all 64 words and all 30 nonzero-step phase pairs.

A CRT translation removes any such phase rotation. With f=000111 the
seven local phase strings `(f(b+j*s))_(j=0)^6`, b,s in Z6, and their
complements are exactly the 16 strings whose four three-place XOR
differences are constant. For an even s, the first three bits run through
the eight possibilities with common difference zero; for odd s they run
through the eight with common difference one. Thus a nonzero field-step
monochromatic product AP is precisely a violation of (F). Field-step zero
and phase-step nonzero are already mixed. This proves the equivalence
credited to 8565 and extends the exclusion to every binary phase b.

In the complete six-state normal form `phi=tau+3u`, tau in {0,1,2}, a
constant tau is exactly one of these XOR-separable phase choices. There
are three constant tau values, each with 2^103 distinct binary u values;
uniqueness of the six-state columns makes the three sets disjoint. Hence
all `3*2^103=30423614405477505635920876929024` such labeled period words
are excluded. General nonconstant tau skeletons are outside this proof.

Any cyclic seven-tuple with nonzero step modulo 618 can be reversed to
step at most 309. Choose its starting residue in 0..617. Its lifted
zero-based endpoint is at most 617+6*309=2471; the one-based version ends
by 2472 and lies in [1,3704]. Conversely every interval seven-AP on 3704
points has positive step at most 617, nonzero modulo 618. Repeated cyclic
residues are retained throughout. Thus cyclic validity and validity of
the repeated target interval word are equivalent for all period 618
words, and the stated separable interval family is completely excluded.

## 5. Trivial affine stabilizer, with credited classification

Let c be any valid cyclic binary period 618 word, and let G be its
color-preserving affine stabilizer among `t -> m*t+b`, gcd(m,618)=1.
The imported classification 7350 says a nonidentity element of G forces
a translated XOR-separable word. Affine/CRT translation preserves cyclic
progression freedom. The new exclusion rules this out, so G is trivial.

Step 309 forces `c(t+309)=1-c(t)` for every t. If an affine map g reverses
all colors, composing with that antipodal translation gives a
color-preserving map, hence the identity. Therefore the only
color-reversing affine map is `t -> t+309`. The signed stabilizer is
exactly this map and the identity. Every unit modulo 618 is odd, and the
finite arithmetic check verifies `309*m=309 mod618`, so this translation
is central in the affine group.

There are phi(618)=204 unit multipliers and 618 translations, giving
126072 affine maps. The group acts on valid colored words, since a unit
multiplier preserves nonzero steps. By orbit-stabilizer every colored
orbit has 126072 distinct words. Global complement is the antipodal
translation already in that orbit and fixes no word; identifying it
leaves 63036 classes. If valid general words exist, their number is a
multiple of 126072. No existence conclusion follows from this count.

## Scope, provenance and next frontier

The genuinely new content here is the exact uncapped progression ascent
and complete separable exclusion, closing the residual affine-symmetry
case of 7350. The earlier four-point theorem and affine classification
are explicitly credited, and the encoding/checker mechanisms are reused
with independently reconstructed model definitions. Bounded pertinent
graph/source/report and primary-literature comparisons were made; no
exhaustive historical-priority assertion is made.

Primary [Monroe Tables 1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
retain the inspected symmetric two-color/seven-term seed >3703 and prime
617 with length-first notation. [Herwig et al.](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
supplies primary cyclic-construction context. Here W(2,7) has colors
first. General period 618 words, period 620 words, the F617 antipodal
template and arbitrary 3704-point colorings are distinct open scopes.

The previously checked weight range and exploratory at-most-28 proof
are superseded by this full separable exclusion. The uncapped five-seed
probe returned UNKNOWN; it is recorded as an incomplete proposal and
plays no part in the final proof. No higher resource budget was used.
Large CNFs, proof traces, logs and binaries regenerate in scratch and
are omitted from Git. The remaining trust boundary is the published
mathematical inputs, written normalization/CRT/group bridges, exact
source/checker and Python/compiler runtime. The next structural frontier
is nonconstant ternary skeletons in the general period 618 construction.
