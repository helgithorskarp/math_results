# Every XOR-separable period-620 coloring has a seven-term progression

**six-vdw-1, researcher**, 2026-10-01. Exact restricted-family result,
checked by separate author implementations. Independent peer review and
proof-assistant formalization are unclaimed.

Let f:F31->{0,1} and g:Z20->{0,1} be completely arbitrary. Define, at
zero-based integer positions,

```
C(x) = f(x mod31) XOR g(x mod20).
```

**Theorem.** C contains a monochromatic nonconstant seven-term integer
arithmetic progression in [0,2479]. Consequently every such coloring of
[1,3704] fails, already within its first 2480 positions. All affine images
under a unit multiplier modulo620, translations and color exchange are
included in the same family. The cutoff2480 is certified, not asserted
optimal.

This covers all 2^51=2251799813685248 labeled (f,g) parameter pairs and
2^50=1125899906842624 distinct period words. It supplies no exclusion of
general period620 or unrestricted interval colorings, no new W(2,7) bound
and no exact value. The desired progression-free coloring on3704 points
remains open.

For the distinct-word count, equality of two product words says
f(r) XOR f'(r)=g(s) XOR g'(s) for every r,s. Both sides must be the
same constant. Exactly two parameter pairs represent any product word,
related by simultaneously complementing both factors.

## CRT and the interval bridge

The Chinese remainder map identifies Z620 with F31 x Z20. A convenient
representative is

```
crt(r,s) = s + 20*((r-s)*14 mod31),
```

since20*14=1 mod31. A nonzero modular step D has a representative1..619.
If D>310, reverse its seven terms, replacing the start A by A+6D mod620
and the step by620-D. Choose the new start in0..619. The last lifted
integer position is at most619+6*310=2479. Colors are preserved by
periodicity. Repeated row residues are retained; a nonzero modular step
is not required to have seven distinct residues.

Thus every modular obstruction proved below gives an actual integer AP
within the certified prefix. Shifting f and g by one handles the
alternative convention C(i)=f(i mod31) XOR g(i mod20) on one-based inputs.
Every target interval AP has step at most617, nonzero modulo620, so
cyclic and target-interval progression freedom are equivalent for all
period620 words. Only the separable family is excluded here.

## Complete row reduction

Step310 fixes the field coordinate and advances the row coordinate by10.
If g(s)=g(s+10), the seven product colors at step310 are equal, whatever
the value of f. Therefore a putatively valid product must satisfy

```
g(s+10)=1-g(s),  0<=s<10.
```

Only1024 opposite-half rows remain. All other1047552 of the2^20 rows
are excluded by this explicit obstruction. The separate Python auditor
actually visits every arbitrary row and checks its equal-pair witness.

If an opposite-half row has a monochromatic row AP with nonzero step
modulo20, choose field step zero and that row step in the CRT. The product
AP is monochromatic for every f. Exactly444 of the1024 rows are excluded
this way; the other580 have no such row AP, including those with repeated
row points.

Translations and the eight units modulo20 act on these580 rows. Their
complete orbits have seven representatives, listed below by their low
ten-bit masks. Bit i gives g(i); the upper ten bits are their complements.
The group has160 elements; complement is translation by10. The producer
forms pullback images. The helper-free auditor instead pushes each of
the20 actual points forward and compares every orbit member, signature
and the complete1024-row partition.

A row affine map can be implemented by a unit/translation modulo620
whose field component is the identity. This preserves cyclic APs and
leaves every f free. Row normalization therefore loses no product.
No field seed, root transition, weight or orientation-invariance cut is
used.

## Forbidden field patterns

For a surviving row g, let P_g be the set of all seven-bit strings

```
(g(b),g(b+s),...,g(b+6s)),  b,s in Z20.
```

Step zero is included. P_g contains both constant strings and is closed
under complement, since replacing b by b+10 flips all seven bits.

For a nonzero field step r, a monochromatic product AP has field string
equal to a row string or its complement. Both belong to P_g. Conversely,
if the field string belongs to P_g, match the row start and step, and
apply CRT to get a monochromatic product AP of color zero. The CRT step
is nonzero because r is nonzero. Field step zero and row step nonzero
are already mixed by the row reduction. This proves the exact equivalence:
a product is cyclically seven-AP-free if and only if its field string
avoids P_g at every field start and every nonzero field step.

In fact only field steps1,2,3 are needed for the following complete
exclusion. These are necessary constraints, not a claimed replacement
of the full progression definition for arbitrary inputs.

| Low-ten-bit row mask | Row orbit size | Forbidden patterns | Field words passing step1 | Passing steps1,2 | Passing steps1,2,3 |
|---|---:|---:|---:|---:|---:|
|8|160|124|0|0|0|
|10|40|88|22072|558|0|
|12|80|76|992|0|0|
|16|160|104|0|0|0|
|20|40|72|22072|558|0|
|34|80|92|0|0|0|
|72|20|48|1066214|2046|0|

The step1 domains total1111350 actual31-bit words. They are distinct
within each row case, but different row cases are not combined as unique
original words. Every such word has an explicit literal product AP record
at field step2 or3, or its reversal. Every other one of the2^31 field
words already violates step1 and yields the matching CRT obstruction.

## Enumeration and independent exact coverage

The producer builds the binary de Bruijn graph on six-bit states. Append
one bit when the resulting seven-bit string lies outside P_g. For each
initial six-bit state, a depth-first walk appends the remaining25 field
bits, then checks the six wrap-around windows. Each31-bit word passing
step1 is visited exactly once: its first six bits and subsequent25 bits
uniquely specify that walk. The producer tests literal field steps2 then3
and writes one actual CRT witness for every visited word.

The separate native checker imports no producer code. It reconstructs
P_g with the opposite bit order and computes trace(M^31), where M is
the64-state allowed-transition matrix. Integer dynamic programming counts
all closed walks. A31-bit cyclic word determines exactly one labeled
closed walk and conversely, so this trace is the exact cardinality of the
step1 word domain. No primitive-period assumption or rotation quotient
is made.

For each case the checker reads every generated record and checks:

- the word is a31-bit field input and directly passes all31 step1 windows;
- its actual start, positive step and color satisfy the integer prefix bounds;
- all seven actual colors f(x mod31) XOR g(x mod20) are the stated color;
- its field step is2 or3, up to reversal;
- a step3 record directly passes every step2 window;
- all recorded words are unique and their number equals the independent trace.

Membership, uniqueness and the exact independent cardinality prove complete
coverage of each domain. Every witness is checked entry by entry. Matching
counts or hashes alone are not the proof. The step2 column of the table
is also checked: step2 records show failure, while all step3 records are
independently verified to pass step2.

The regenerated record corpus has1111350 fixed-width nine-byte records,
10002150 bytes in total. It is omitted from Git. Each record consists of
little-endian uint32 field word, uint16 start, uint16 positive step and
one color byte. Individual file hashes, complete deterministic tool
outputs and row audit metadata are frozen in [expected.json](expected.json).
The runner requires that file to exist before replay and never writes it.

## Controls and trust boundary

The replay checks complete normal/-O row bytes and literal row audits.
Native address/undefined-sanitizer builds regenerate every record byte
and repeat full literal coverage, matching the optimized builds exactly.
The transfer trace is separately checked against all14322 small inputs
at lengths1..10 for all seven signatures;602 are positive. All-allowed
and all-forbidden31-bit controls also pass.

Nineteen concrete damages must reject: nine native record/case damages
and five row-data damages in both normal and optimized Python. They
include omitted/extra/duplicate/truncated records, zero step, wrong
literal color, outside-domain coordinates, a missing case, an omitted
row/orbit member, a wrong signature and wrong author provenance.
Arithmetic uses Python integers and unsigned C++ integers. A matrix
entry has at most2^31 paths; even the loose64*2^31 trace bound is below
2^37. Summing all possible31-bit words is below2^62. Serialization and
all shifts are explicitly bounded. No solver, floating point, downloaded
proof corpus, earlier no-go theorem or W(2,4) normalization is a premise.

Remaining trust consists of the written CRT/orbit/walk-cardinality
arguments, exact source/checkers, and the Python/compiler runtime.
Same-author algorithm independence does not assert a peer verdict.

## Prior work and remaining construction frontier

Primary [Monroe Tables1/2](https://combinatorialpress.com/jcmcc-articles/volume-128/new-lower-bounds-for-van-der-waerden-numbers-using-distributed-computing/)
retain the inspected two-color/seven-term seed >3703 and prime617.
Monroe's arguments are length first; W(2,7) here is colors first.
[Herwig et al.2007](https://www.cs.utexas.edu/~marijn/publications/waerden.pdf)
and [Rabung–Lotts2012](https://www.combinatorics.org/ojs/index.php/eljc/article/viewFile/v19i2p35/pdf/)
provide established cyclic/residue construction context. Generic CRT,
XOR products, de Bruijn graphs and transfer-matrix counting are credited
methods, not claimed new algorithms. Bounded current primary and
campaign comparisons establish scope; exhaustive historical priority
is not claimed.

The preceding [QR31-by20 obstruction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/qr31-x20-obstruction/PROOF.md),
source a02e1cdbae25cb3fe22e8d5c072abcf4194023f4, committed graph8983
`bafkreicaqkswvpg27225yjrop2gighou6pdj7ilvllarbczkqwzdpzphp4`,
excluded two prescribed QR field factors and their affine images. The
new result allows every31-bit field factor. Its cutoff2480 extends the
prior affine-image assertion; the sharper2296 QR-specific bound is
unchanged.

The published [period621 XOR obstruction](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-1/crt23x27/PROOF.md)
concerns F23 and an order-nine row group, not F31 x Z20.
The peer [separable618 exclusion](https://github.com/helgithorskarp/math_results/blob/main/round-two/six-vdw-3/separable618-exclusion/PROOF.md),
source f5985e678e95b4b122b9143cf4c8f411bc5e5232, committed graph8985
`bafkreigpyvdzpke2nyx5dwabz6twmxpx4kpcrrfudup75wvpy7lmtycalm`,
concerns F103 x Z6 and uses a different progression-ascent proof.
Those results are context, not mathematical dependencies. No617-specific
QR edit or H7 phase restriction transfers to this proof.

General period620 words must go beyond a common row and field-wise color
exchange. A concrete next construction family allows one exceptional
field column with an arbitrary opposite-half row; every other column
has a common row up to color exchange. Its reduction and feasibility
are not established by this theorem. The unrestricted310-variable
period620 proposal previously timed out and remains inconclusive.

Actual author is **six-vdw-1, researcher**; signatures share the campaign
identity. Source publication and graph commitment are separate provenance
steps and do not themselves constitute proof.
