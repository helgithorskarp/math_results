# A three-deletion barrier for the Albertson `r=27` sampling route

This note determines how far the current recursive crossing tables can go on
the sole surviving Albertson frontier row

```text
|V(G)|=53,  |E(G)|=713,  chi(G)=27.
```

It is a method-limit theorem, not a proof of Albertson's conjecture.  Even if
one knew the complete distribution of the edge counts of all subgraphs
obtained by deleting at most three vertices, summing the current local bounds
could not reach `Z(27)=6084`.  Deleting four vertices is the first depth with
enough numerical headroom.

## Setting

Let `G` be a hypothetical counterexample, put

```text
x_v=d_G(v)-26,  h=|{v:x_v>0}|,
```

and let `F_s(q)` be the exact recursive convex-sampling lower bound from the
preceding certificate, including the current simple 5-planar slope-6 line.
The committed frontier now gives

```text
sum_v x_v=48,  h>=13,  0<=x_v<=25.                 (1)
```

The last inequality uses connectedness of the complement: `G` has no
universal vertex.

For a `t`-set `T`, write `q_T=|E(G-T)|`.  Restrict a crossing-minimal good
drawing to every `G-T`.  Each crossing survives for exactly
`C(49,t)` choices of `T`, and hence

```text
C(49,t) cr(G) >= sum_{|T|=t} F_{53-t}(q_T).         (2)
```

The question here is deliberately generous to this method: how large could
the right side of (2) possibly be, subject only to the proved numerical
constraints?

## Forced edge-count ranges

For every `T`,

```text
q_T = 713 - 26t - sum_{v in T}x_v + e_G(T).         (3)
```

At least `13-t` positive excesses remain outside `T` when `t<=4`, so (1)
gives

```text
sum_{v in T}x_v <= min(25t,48-(13-t)).
```

Together with `0<=e_G(T)<=C(t,2)`, this forces the following intervals:

| deleted vertices `t` | local order | forced interval for `q_T` |
|---:|---:|---:|
| 1 | 52 | `[662,687]` |
| 2 | 51 | `[624,662]` |
| 3 | 50 | `[597,638]` |
| 4 | 49 | `[570,615]` |

Independently of the degree distribution,

```text
sum_{|T|=t} q_T = 713 C(51,t),                       (4)
```

because every edge survives exactly `C(51,t)` deletions.

## Exact concave caps

On each forced interval, the endpoint chord is an upper majorant of the
entire current local table.  Exact exhaustive checking gives:

| `t` | endpoint chord majorizing `F_{53-t}(q)` | chord-relaxation ceiling from (2) |
|---:|---|---:|
| 1 | `(661q-313157)/25` | `6073` |
| 2 | `(943q-425032)/38` | `6077` |
| 3 | `(974q-421250)/41` | `6082` |
| 4 | `(114q)/5-9467` | `6090` |

Indeed, sum the appropriate chord using (4), take the integer floor because
the sum of the `F` values is integral, divide by `C(49,t)`, and take the final
ceiling.  For `t=2,3`, even these deliberately optimistic caps miss the
minimum integer sum needed to certify `6084` by respectively `7198` and
`25178`.  The `t=4` cap exceeds the threshold; this does not prove that it is
attainable, only that the same numerical obstruction no longer rules it out.

The one-deletion case admits a sharper audit.  Exact dynamic programming over
all 53 integral excesses satisfying (1) gives

```text
min sum_v F_52(687-x_v) = 297470, at 0^37,3^16;
max sum_v F_52(687-x_v) = 297517, at 0^40,1^11,12,25.
```

Thus the now-proved `h>=13` condition still permits the old `6071` floor,
while even the most favorable allowed degree multiset can make the
one-deletion certificate yield only `6072`.  Learning the exact degree
sequence cannot by itself close the gap through this inequality.

Consequently, any successful use of the existing recursive tables must begin
at four-vertex deletion (the order-49 table), add a genuinely stronger local
crossing bound, or exploit information beyond the edge-count marginals in
(2).  This is the precise resumable frontier supplied by the note.

## Reproduction and trust boundary

Run with CPython 3.9 or later; there are no third-party dependencies:

```sh
python3 verify.py
```

Expected first line:

```text
PASS Albertson r=27 low-depth deletion barrier audit
```

The verifier reconstructs the complete recursive table through order 53 with
exact rational arithmetic, checks its published SHA-256 digest, optimizes the
one-deletion degree relaxation, proves every displayed edge-count interval,
checks every integer point under all four chord majorants, and recomputes the
integer target shortfalls.  It uses no solver, randomness, floating point,
external data, or project import.

SHA-256 of `verify.py`:
`c51635bf5601973a37accd9d468ab0ef725fc476d89efe17d75dfd3458ed6a2b`.
The reconstructed recursive-table digest is
`55da0a3d413620951dba0ac52618fa24f09d59de43a0c7e8a0f3927283036f43`.

The mathematical trust boundary is good-drawing normalization; the universal
linear crossing bounds used by the recursive certificate; the September 2026
order-53 frontier; and the committed structural theorem `h>=13`.  The present
deletion identities, support-conditioned ranges, concave caps, and arithmetic
are elementary or exhaustively checked.

## Sources and novelty scope

- A. Sadhu, [*Albertson's Conjecture Holds for `r` at Most
  26*](https://arxiv.org/abs/2609.01682v1), for the connected-complement
  order-53 frontier.
- A. Büngener and M. Kaufmann, [*Improving the Crossing Lemma by
  Characterizing Dense 2-Planar and 3-Planar
  Graphs*](https://doi.org/10.7155/jgaa.v29i3.3000), for the strongest two
  universal lines underlying the recursive table.
- A. Büngener, J. Franz, M. Kaufmann, and M. Pfister, [*A First View on the
  Density of 5-Planar Graphs*](https://arxiv.org/abs/2505.24364v3), for the
  simple 5-planar density input.
- The preceding [recursive convex-sampling
  certificate](../albertson_r27_recursive_convex_sampling/README.md),
  [degree-support audit](../albertson_r27_degree_support_limit/README.md), and
  [`h>=13` structural closure](../albertson_r27_order53_h11_h12_closure/README.md).

Targeted primary-literature and committed-graph searches found no prior
statement of these support-conditioned concave caps or the three-deletion
barrier.  This is a search-relative novelty assessment, not a claim of
historical priority.
