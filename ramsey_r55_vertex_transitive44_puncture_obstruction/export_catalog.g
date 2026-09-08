# Export GAP's complete degree-44 transitive-action catalog in a small,
# language-neutral format.  Run with GAP 4.12.1 and TransGrp 3.6.3:
#   gap -q export_catalog.g

out := "catalog.generated.txt";;
PrintTo(out, "");;
for k in [1..NrTransitiveGroups(44)] do
    g := TransitiveGroup(44, k);;
    gens := GeneratorsOfGroup(g);;
    AppendTo(out, k, "|", Size(g), "|");
    for j in [1..Length(gens)] do
        p := gens[j];;
        for i in [1..44] do
            AppendTo(out, i^p);
            if i < 44 then AppendTo(out, ","); fi;
        od;
        if j < Length(gens) then AppendTo(out, ";"); fi;
    od;
    AppendTo(out, "\n");
od;
QUIT;
