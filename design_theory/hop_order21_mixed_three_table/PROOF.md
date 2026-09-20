# Proof certificate

Let the 21 couples be labelled `0,...,20`.  Couple `20` is fixed and the
first 20 labels are acted on by addition modulo 20.  A person is `(v,b)`,
where `v` is the couple and `b` is the spouse bit.

For each target `[a,b,2]`, `certificates.jsonl` stores two external perfect
matchings `F1` and `F3`.  The second matching is determined from `F1`: rotate
by 10, remove the two same-bit edges between couples 0 and 10, and insert the
two crossed edges between those couples.  Call the resulting matching `F2`.

Develop `F1` and `F2` by shifts `0,...,9`, and develop `F3` by shifts
`0,...,19`.  The verifier establishes directly that:

1. each of the 40 developed factors is a perfect matching of the 42 people;
2. adjoining the 21 spouse edges gives cycle lengths `(2a,2b,4)`;
3. the 40 factors are distinct; and
4. across them, each of the 840 edges joining people from different couples
   occurs exactly once.

Consequently, in every meal each participant sits beside their spouse, and
over all meals every pair of non-spouses sits together exactly once.  This is
precisely a solution of `HOP(2a,2b,4)`.

The integer solutions of `a+b=19`, `a>=b>=3`, are

```text
[16,3,2], [15,4,2], [14,5,2], [13,6,2],
[12,7,2], [11,8,2], [10,9,2].
```

The seven certificates therefore prove the full stated classification.
This argument checks the schedule definition itself; it does not require the
search to be exhaustive and does not rely on the implementation of the
starter search.

The cyclic organization is the odd-order three-starter framework of Jerade
and Šajna.  Its role here is conceptual and compresses each 40-meal schedule
to 42 stored edges.  Correctness is independently established by expanding
the schedule.
