# Finite family and certificate argument

Author and executing agent: **six-sorting-1, researcher**.

Wire i is bit i of an original Boolean integer, wire 0 being least significant.
A standard comparator (a,b), a<b, places the minimum on a and maximum on b.
The precise objects are the eight ordered comparator words in `parents.json`.
Their layer labels identify the table entries; layering is not used in the proof.

## 1. Extreme projection and normalization

Choose n-13 input positions, each tagged low or high. All other values lie
between these extremes. Their original relative order is unrestricted. At an
original comparator, two unmarked values give a retained oriented comparator.
If at least one value is marked, delete the comparator and connect its unmarked
input, if present, to its unmarked output. The marker follows the appropriate
minimum or maximum output, including stationary passages. Two marked inputs
still delete just one comparator. Thus all tags and bypasses are independent
of the actual unmarked values.

Initially give unmarked inputs consecutive labels 0..12 in original input
order. Let t associate a current physical wire with its unmarked label or low/high
tag. For a retained original comparator with unmarked labels a,b, append oriented
comparator (a,b). At a deleted comparator, move the tag and unmarked label
according to low < unmarked < high. This produces an oriented comparator word
Q and a final physical wire frame t.

Normalize Q using a permutation p initially equal to the identity. For each
oriented gate (a,b), append standard gate (min(p[a],p[b]),max(p[a],p[b])). If
p[a]>p[b], exchange p[a] and p[b]. The frame update accounts exactly for the
reversed output orientation of that gate. By induction, the standard word has
the same values as Q after applying this changing frame. At the end, read
p[t[i]] along the unmarked physical output wires. The supplied parents are
sorters, so this trailing frame is the identity: otherwise the standard word,
which fixes every canonical sorted Boolean vector, could not be followed by
that permutation and still sort them all. Both implementations require the
identity explicitly and reject a failure of it. No trailing permutation is
silently dropped.

The positive-parent scalar check and the two projection implementations check
this bridge on the actual fixture. Standardization and extreme pruning are
established methods; [Harder](https://arxiv.org/abs/2012.04400v3), Sections 2–3,
provides primary context. No lower-bound certificate from that paper is needed
for the present negative finite-family argument.

Keep only the fully normalized words with at most 46 gates. The complete
projection enumeration in the README has 9,858 assignments and 1,227 qualifying
assignments. Sort and deduplicate complete gate words, without a wire-isomorphism
quotient. The canonical text has the SHA256 recorded in the README and
certificate. One word has length45 and 868 have length46. The generator enumerates
deleted positions and low/high choices and normalizes in two phases; the checker
enumerates surviving positions and normalizes during the bypass construction.
They agree entry by entry through the complete canonical text hash.

## 2. Deletion coverage

For each length46 word, choose one labelled gate to delete for a size45 candidate,
or an unordered pair of distinct gates for a size44 candidate. For the length45
incumbent control, delete one gate for a size44 candidate. Thus there are

    868 * 46 = 39,928 size45 choices,
    868 * binomial(46,2) + 45 = 898,425 size44 choices.

The counts are parameter counts: different choices may yield the same word.
Every choice is tested; no symmetry, no-op pruning, depth restriction or search
cutoff reduces this domain. Gates not deleted retain their order on each wire.
Equivalently, they form a fixed directed acyclic circuit. Any topological
schedule evaluates its pure min/max nodes with the same input ports and hence
has the same outputs. Consequently serializing the retained gates does not
omit any possible depth or legal schedule in this fixed-circuit family.

Normalization precedes deletion by definition. This argument does not cover
editing the oriented projection before normalization, deleting three or more
gates from longer projections, adding gates, or altering retained wire endpoints.

## 3. The Boolean obstruction certificate

`certificate.json` contains 487 distinct integers in [0,8191], one per Boolean
input. For every deletion choice, at least one certificate input has an adjacent
output inversion. Such a candidate is not a sorting network: sorting all totally
ordered inputs would necessarily sort these Boolean inputs.

The generator evaluates the edited sequential word on all 8192 inputs at once,
using 128 unsigned 64-bit words per wire. Each comparator uses Boolean AND/OR
for minimum/maximum. It accumulates adjacent-inversion masks and greedily adds
an input when the current certificate has no failure for a candidate. The
independent checker does not trust the generator's edited word or its full-input
failure masks. It reconstructs original per-wire paths, bypasses deleted gate
ports, and recursively evaluates all output ports of this circuit on the supplied
witnesses. Gate visitation detects cycles or references to deleted ports.
Witness positions in its packed truth vectors are certificate-row positions,
rather than original input integers as in the generator.

The checker rejects if any candidate has no witnessed inversion. It completes
all 938,353 size44/size45 choices. A planted positive size45 deletion is made by
adding a redundant final comparator to the known size45 sorter and deleting
that extra gate. The checker finds no inversion for this control, demonstrating
that its exclusion test does not reject every circuit indiscriminately.

The full mode substitutes all 8192 original inputs in the same independent
circuit evaluator. It again rejects every enumerated candidate and finds minimum
size44 failure count11, agreeing with the sequential generator. This additional
count is not necessary for the certificate's exclusion theorem. Address and
undefined-behavior sanitizer execution covers the complete 487-input check.

Bit shifts are unsigned with exponents0..63. A per-candidate failure count is
at most8192 and fits int; total family counts fit uint64. Circuit port indices
are less than13+2*46=105. Unused truth-vector bits start at zero and remain zero,
so complementing one input while testing a&~b cannot create a false inversion
on padding positions. There is no floating point, solver status or incomplete
enumeration in this proof.

The theorem is exactly this pinned finite-family exclusion. It leaves the
unrestricted size44 construction problem open and does not establish a global
minimum of45.
