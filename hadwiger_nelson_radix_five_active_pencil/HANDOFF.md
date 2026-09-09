# Exact five-active interface for team-hn-2

The exactly-five-active branch now has one necessary signature form: five
distinct projective directions forming a full affine pencil. The alternative
five-cover form contains a four-section partition and is excluded by h4165.

After h4139 and h4167, the 131,356 global h4117 pair representatives split as:

- 128,616 realized-pencil compatible, allowance 7,585,472;
- 2,096 parallel-signature pairs, allowance 129,952;
- 644 pairs whose unique pencil contains an unrealized type, allowance 39,104.

The last two classes cannot support an exactly-five-active counterexample and
therefore require at least six active curves. Do not delete them from a
six-or-more search.

At curve level, the 5,382 realized pencils have 136,094,976 raw lifts. The
accepted h4151 constraints remove none because all 3,006 lie within one
parallel class. H4167 pairs also remove none; h4167 triples leave 132,232,896
lifts. Every pencil and every one of the 128,616 compatible pair orbits has a
constraint-avoiding extension. Thus the current incidence constraints do not
justify further pair deletion within the exact-five mode.

Generate the explicit interface from the repository root:

```sh
python3 -B hadwiger_nelson_radix_five_active_pencil/verify.py \
  --export-interface /tmp/hn-five-pencil-interface.json
```

The output path must not exist. It is 6,200,577 bytes. Canonical JSON digest
(without terminal newline):
`eb03a45aa30f2ce0bd1b4989f72413001522b6eedbc329f0273427f94bdf3e20`.
File SHA-256 (with newline):
`fc12122b45703c2cd04a0f064a7f225081ac065c917118888679723106a97b7d`.

The interface contains curve signatures, all 5,382 realized pencil patterns,
the three exact pair-mode lists, and one constraint-avoiding five-curve witness
per compatible pair. IDs are the original h4105 curve IDs; circle ID 342 is
absent from the classified pairs. Global representatives must be solved over
the whole plane and cannot be combined with a chamber restriction.

This closes only the residue-cover classification of exactly five active
curves. Algebraic concurrence of its 132,232,896 surviving quintets and every
six-or-more-active case remain open. HN2 retains physical realization and
chromatic search ownership. No record graph is claimed.
