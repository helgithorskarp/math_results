# A 1668-word binary constant-weight `(32,8,8)` code

## Result

[`code_32_8_8_1668.txt`](code_32_8_8_1668.txt) contains 1668 distinct binary
words of length 32 and weight 8.  Every two words have Hamming distance at
least 8.  Therefore

```text
A(32,8,8) >= 1668.
```

This improves the lower bound 1667 reported by William Echols in
[*New lower bounds for constant-weight codes via seeded bit-swap tabu
search*](https://arxiv.org/abs/2608.13906) and listed in Andries Brouwer's
maintained [constant-weight-code table](https://aeb.win.tue.nl/codes/Andw.html)
when checked on 12 September 2026.  The upstream certificate repository still
contained `32_8_8_1667.txt` and no 1668-word certificate at that check.  These
checks establish the public comparison used here; they cannot exclude
unpublished concurrent work.

The result is a constructive lower bound, not an exact determination of
`A(32,8,8)`.

## Five-for-six exchange

The new code is obtained from Echols's 1667-word incumbent by deleting the
following five zero-based rows:

```text
index   word as a 32-bit hexadecimal integer
142     24042807
267     84422884
348     24414244
452     0422b802
1520    060c00c5
```

and adjoining these six words:

```text
04444047
060c0035
24242822
24e14200
8402b802
84472004
```

The hexadecimal convention identifies character `i` in each displayed binary
word with bit `i` of the integer.  [`exchange.json`](exchange.json) records both
representations, the deleted rows, and the exact upstream source hash.
[`construct.py`](construct.py) checks these data and deterministically rebuilds
the checked-in 1668-word certificate.

For an outsider `x`, let its *blocker set* be the incumbent rows at distance
less than 8 from `x`.  In the order above, the six added words have blocker
sets

```text
{142,348,1520}, {1520}, {142,452}, {348}, {267,452}, {267}.
```

Their union is exactly the five deleted rows, while the added words are
pairwise at distance at least 8.  Every surviving incumbent word is therefore
compatible with every added word, and all old-old distances are inherited.
This directly proves the construction.

The blocker incidence is especially tight: every deleted row occurs in
exactly two blocker sets.  The minimum union sizes among subfamilies of `k`
added words, for `k=1,...,6`, are

```text
1, 2, 3, 4, 5, 5.
```

Thus the six blocker sets form a Hall circuit on five deleted rows.  This
explains why no proper subexchange improves the incumbent even though the full
five-for-six exchange does.

## Hall-circuit search reduction

The construction was found using the following reusable reduction.  Let `C`
be any incumbent code, let `B(x)` be the incumbent words conflicting with an
outsider `x`, and suppose `C` admits no improving exchange after deleting at
most `r-1` words.  If `r+1` pairwise compatible outsiders improve `C` with at
most `r` deletions, then:

1. their blocker union has size exactly `r`;
2. every proper subfamily `Y` has `|union B(Y)| >= |Y|`;
3. the full blocker family is a circuit of the transversal matroid; and
4. every blocker occurs in at least two of the `r+1` blocker sets.

Indeed, a blocker union of size below `r`, or a proper subfamily with fewer
blockers than words, would already give a smaller improving exchange.  The
last assertion follows by deleting the unique word containing a hypothetical
degree-one blocker, which would leave `r` outsiders on at most `r-1` blockers.

If `m` is the largest blocker-set size in the circuit, start with such a set
and add a selected outsider whenever it covers a new blocker.  At most `r-m`
further outsiders are needed.  Hence every improving radius-`r` circuit has a
pairwise compatible cover seed of length at most `r-m+1`.  For `r=5`, the
maximum-support strata therefore require seed depths only `1,2,3,4` for
`m=5,4,3,2`.  Applying this reduction to the previously certified
four-exchange-maximal incumbent exposed the circuit above in the `m=3` stratum.

The general reduction guided discovery, but the claimed lower bound depends
only on the explicit code certificate and its direct verification.

## Kissing-number consequence

Echols applies the construction of Edel, Rains, and Sloane from
[*On kissing numbers in dimensions 32 to 128*](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v5i1r22)
to obtain

```text
tau_n >= 2^17 + A(n,8,8) * 2^7 + 2n(n-1),  n >= 32.
```

The new code therefore gives

```text
tau_32 >= 2^17 + 1668 * 2^7 + 2 * 32 * 31 = 346560,
```

improving the previously reported 346432 by 128.

## Reproduction

Requirements are Python 3, GNU Make, and a C++20 compiler.  The recorded run
used Python 3.11 and GCC 12.2.0.  Run

```bash
make check
```

This reconstructs the certificate from the five-for-six exchange and compares
it byte for byte with the checked-in code.  The Python verifier then checks the
exchange, all blocker sets, the Hall-circuit profile, and all 1,390,278 pairs
of final codewords directly as character strings.  A separate C++ verifier
parses the final certificate into 32-bit integers and independently checks its
cardinality, distinctness, weights, and complete distance distribution.

The expected output is

```text
constructed_size=1668
distinct_words=1668
constant_weight=8
pairs_checked=1390278
minimum_distance=8
distance_histogram=8:174317,10:193839,12:595643,14:315460,16:111019
verification=PASS
```

As an external implementation cross-check, the final certificate was also
placed in an otherwise unmodified clone of Echols's verifier at upstream commit
`4f0bf18b094fb15c3634001ea8aed847e8353d1c`.  Its documented
`make && ./bin/sbst --verify-all` command returned `All files in ./codes are
valid codes.`

For an AddressSanitizer/UndefinedBehaviorSanitizer replay of the C++ verifier:

```bash
make sanitize
```

All arithmetic is exact.  Codewords use 32 bits; the pair counter is unsigned
64-bit and reaches only 1,390,278.  The only external input is the adjacent
CC0 incumbent, pinned by SHA-256 and upstream commit in
[`NOTICE.md`](NOTICE.md).  The final certificate can also be verified on its
own: the new lower bound does not rely on trusting the search, blocker
reduction, or upstream incumbent once the 1668 rows are present.
