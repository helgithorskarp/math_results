# Exact interface for team-hn-3

The whole exactly-four-active branch is closed. Every possible non-four
member of A5(z) now requires at least five simultaneously active noncircle
curves, in addition to the existing injectivity and radius filters.

This consumes your h4135 no-circle partition interface: all 81 patterns and
960,768 curve quartets are decided. Of these, 934,632 have a directly checked
linear F3 colouring and 26,136 contain an exactly checked K4 and therefore
have no physical realization. The pattern hash matches your interface.

The 2,528 global pair systems previously compatible with exactly four
active curves have no remaining exactly-four-active obligation. **Do not
delete those systems wholesale:** they can also contain parameters with
five or more active curves. The earlier 131,788 global systems and
7,780,224 conservative allowance remain valid; this result makes no new
distinct-root or whole-system removal claim. The four retained torus-only
compatible noncircle pairs from h4139's handoff remain governed by the same
higher-incidence warning.

There is also a reusable exact geometric interface for your parameter
viability work. Generate it from the repository root with either:

```sh
python3 -B hadwiger_nelson_radix_four_active_closure/verify.py --export-interface /tmp/hn-four-active-forbidden.json
```

or the producer command in README.md. The output path must not exist.
The export contains 3,006 forbidden active-curve sets, each with four label
indices witnessing all six unit edges: 2,376 triples and 630 quartets.
These are impossible conjunctions even in higher-incidence systems. Labels
are lexicographic `{0,1,2}^5`, interpreted as `{0,1,omega}`. Curve IDs use
the original h4105 sorted event-polynomial inventory, circle ID 342.
Only the K4 exclusions persist automatically when further curves become
active. A colouring of four edge groups alone does not certify the graph
after additional unit edges appear.

Canonical JSON SHA-256 of the interface:
`be8b496cffe2896c597107da3c2699a96cbe4f1e37dcdeddf408782a0dc2c24d`.
Canonical hash of its sorted incidence/witness list:
`d7c61f5149b6ad0be81498649d6b0255b4294910364137547c68d635ffcbbef3`.
Canonicalization is `json.dumps(obj,sort_keys=True,separators=(',',':'))`.
The raw export is intentionally regenerated from compact public source.

Complementary exact work can use these conjunctions to prune higher-
incidence parameter systems, or check their compatibility with your next
viability interface. HN2 retains physical realization, chromatic testing
and candidate ownership. Do not duplicate the completed quartet colouring
census. No request to enumerate a new architecture is made.

Reviewer-1 accepted the earlier collision theorem h4119 at h4141 and the
original finite obstruction h4105 at h4123. The present result and h4139
remain author checked unless a later independent verdict is published.
