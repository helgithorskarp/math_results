# Independent GAP group/power checker; imports no Rowan implementation.
# Fixed spaces and norm ranks come from group centralizers/image sizes.
LoadPackage("smallgrp","1.5.1");
Reset(GlobalMersenneTwister,20261005);
Reset(GlobalRandomSource,20261005);

NovaOmega := function(n)
    if n=1 then return 0; fi;
    return Length(Set(FactorsInt(n)));
end;

NovaGroupData := function(g)
    local elements,subgroups,x,e,powers,c;
    elements:=Elements(g); subgroups:=[];
    for x in elements do
        e:=Order(x);
        powers:=Set(List([0..e-1],i->x^i));
        AddSet(subgroups,powers);
    od;
    c:=Length(subgroups);
    if Sum(elements,x->1/Phi(Order(x)))<>c then Error("literal cyclic sets mismatch"); fi;
    return rec(order:=Size(g),cyclic_subgroups:=c,
        eta:=String(c/2^NovaOmega(Size(g))),
        element_order_histogram:=Collected(List(elements,Order)),
        cyclic_subgroup_order_histogram:=Collected(List(subgroups,Length)));
end;

NovaAudit := function(label,g,v,p,d)
    local q,pi,vs,h,x,e,lifts,orders,f,norms,r,s,a,weight,defect,
          ap,bp,dc,db,ct,long,lower,data,qd,signatures,norm,element;
    if not IsPrimeInt(p) or d<1 then Error("invalid characteristic/dimension"); fi;
    if not IsNormal(g,v) or not IsElementaryAbelian(v) or Size(v)<>p^d then
        Error("invalid elementary normal kernel");
    fi;
    pi:=NaturalHomomorphismByNormalSubgroup(g,v); q:=Image(pi);
    vs:=Elements(v); ap:=0; bp:=0; dc:=0; db:=0; ct:=true; long:=true;
    signatures:=[];
    for h in Elements(q) do
        x:=PreImagesRepresentative(pi,h); e:=Order(h); a:=x^e;
        if not a in v then Error("lift power not in kernel"); fi;
        lifts:=List(vs,u->u*x); orders:=List(lifts,Order);
        if not ForAll(orders,o->o=e or o=p*e) then Error("bad lift order"); fi;
        f:=LogInt(Size(Centralizer(v,x)),p);
        norms:=[];
        for element in vs do
            norm:=Product(List([0..e-1],j->element^(x^(-j))));
            if (element*x)^e<>norm*a then Error("group affine norm identity failed"); fi;
            Add(norms,norm);
        od;
        r:=LogInt(Length(Set(norms)),p);
        if p^r<>Length(Set(norms)) then Error("norm image is not a p-power"); fi;
        s:=Number(norms,u->u=a^-1);
        if s<>Number(orders,o->o=e) then Error("short lift/norm count mismatch"); fi;
        if s<>0 and s<>p^(d-r) then Error("norm fiber size failed"); fi;
        weight:=Sum(orders,o->1/Phi(o));
        if e mod p<>0 then
            ap:=ap+1/Phi(e);
            if s<>p^(d-f) then Error("fixed-space fiber count failed"); fi;
            defect:=(p-2)*(p^(d-f)-1)/((p-1)*Phi(e));
            dc:=dc+defect; ct:=ct and f=d;
        else
            bp:=bp+1/Phi(e); defect:=(p-1)*s/(p*Phi(e));
            db:=db+defect; long:=long and s=0;
        fi;
        Add(signatures,[e,f,r,s,Collected(orders),String(weight),String(defect)]);
    od;
    data:=NovaGroupData(g); qd:=NovaGroupData(q);
    lower:=(1+(p^d-1)/(p-1))*ap+p^(d-1)*bp;
    if data.cyclic_subgroups<>lower+dc+db then Error("total defect formula failed"); fi;
    if (data.cyclic_subgroups=lower)<>((p=2 or ct) and long) then
        Error("equality predicate failed");
    fi;
    return rec(name:=label,p:=p,dimension:=d,group:=data,quotient:=qd,
        A_p:=String(ap),B_p:=String(bp),lower_bound:=String(lower),
        coprime_defect:=String(dc),divisible_defect:=String(db),
        equality:=data.cyclic_subgroups=lower,coprime_actions_all_trivial:=ct,
        divisible_cosets_all_long:=long,coset_invariants:=Collected(signatures));
end;

NovaJson := function(stream,obj)
    local names,i,s;
    if IsString(obj) then
        s:=ReplacedString(obj,"\\","\\\\"); s:=ReplacedString(s,"\"","\\\"");
        PrintTo(stream,"\"",s,"\"");
    elif IsBool(obj) or IsInt(obj) then PrintTo(stream,obj);
    elif IsRecord(obj) then
        names:=SortedList(RecNames(obj)); PrintTo(stream,"{");
        for i in [1..Length(names)] do
            if i>1 then PrintTo(stream,","); fi;
            NovaJson(stream,names[i]); PrintTo(stream,":"); NovaJson(stream,obj.(names[i]));
        od;
        PrintTo(stream,"}");
    elif IsList(obj) then
        PrintTo(stream,"[");
        for i in [1..Length(obj)] do
            if i>1 then PrintTo(stream,","); fi; NovaJson(stream,obj[i]);
        od;
        PrintTo(stream,"]");
    else Error("unsupported JSON object"); fi;
end;

NovaSemi := function(p,d,m,images)
    local v,c,vg,cg,aut,ag,action,g;
    v:=AbelianGroup(IsPcGroup,List([1..d],i->p)); vg:=GeneratorsOfGroup(v);
    aut:=GroupHomomorphismByImages(v,v,vg,images(vg));
    if aut=fail or not IsBijective(aut) then Error("invalid automorphism"); fi;
    ag:=Group([aut]); c:=CyclicGroup(IsPcGroup,m);
    # PC presentations of C4 may list a generator and its square. Specify
    # one generator of the whole cyclic complement for this one-image map.
    cg:=[First(Elements(c),x->Order(x)=m)];
    action:=GroupHomomorphismByImages(c,ag,cg,[aut]);
    if action=fail then Error("invalid complement action"); fi;
    g:=SemidirectProduct(c,action,v);
    return [g,Image(Embedding(g,2))];
end;

NovaHeisenberg := function(p)
    local a,b,g;
    a:=IdentityMat(3,GF(p)); b:=IdentityMat(3,GF(p));
    a[1][2]:=One(GF(p)); b[2][3]:=One(GF(p));
    g:=Group(a,b); return [g,Centre(g)];
end;

results:=[];; extras:=[];;
for params in [[2,2],[3,2],[5,2],[7,2],[3,3],[7,3]] do
    p:=params[1]; n:=p^params[2]; g:=CyclicGroup(IsPermGroup,n);
    v:=Subgroup(g,[GeneratorsOfGroup(g)[1]^(n/p)]);
    Add(results,NovaAudit(Concatenation("C",String(n),"_over_C",String(n/p)),g,v,p,1));
od;
g:=AbelianGroup(IsPcGroup,[2,2]);;
Add(results,NovaAudit("C2_x_C2_over_C2",g,Subgroup(g,[GeneratorsOfGroup(g)[1]]),2,1));
g:=DihedralGroup(IsPermGroup,8);; Add(results,NovaAudit("D8_central_C2",g,Centre(g),2,1));
g:=QuaternionGroup(8);; Add(results,NovaAudit("Q8_central_C2",g,Centre(g),2,1));
g:=AlternatingGroup(4);; Add(results,NovaAudit("A4_V4_over_C3",g,DerivedSubgroup(g),2,2));
g:=SymmetricGroup(3);; Add(results,NovaAudit("S3_C3_over_C2",g,DerivedSubgroup(g),3,1));
gv:=NovaSemi(5,2,4,x->[x[1],x[2]^-1]);;
Add(results,NovaAudit("F5_squared_nonfaithful_C4",gv[1],gv[2],5,2));
gv:=NovaSemi(3,2,3,x->[x[1],x[1]*x[2]]);;
Add(results,NovaAudit("F3_squared_unipotent_C3",gv[1],gv[2],3,2));
for p in [3,5] do
    gv:=NovaHeisenberg(p);
    Add(results,NovaAudit(Concatenation("Heisenberg_F",String(p),"_central_C",String(p)),gv[1],gv[2],p,1));
od;
g:=SL(2,5);; Add(results,NovaAudit("SL2_F5_central_C2",g,Centre(g),2,1));
for p in [2,3,5,7] do
    g:=DirectProduct(AlternatingGroup(5),CyclicGroup(IsPermGroup,p));
    v:=Image(Embedding(g,2));
    Add(results,NovaAudit(Concatenation("A5_x_C",String(p),"_over_A5"),g,v,p,1));
od;
g:=DirectProduct(AlternatingGroup(5),AbelianGroup(IsPcGroup,[2,2]));;
Add(results,NovaAudit("A5_x_C2xC2_over_A5",g,Image(Embedding(g,2)),2,2));
c:=CyclicGroup(IsPermGroup,49);; g:=DirectProduct(AlternatingGroup(5),c);;
v:=Subgroup(g,[Image(Embedding(g,2),GeneratorsOfGroup(c)[1]^7)]);;
Add(results,NovaAudit("A5_x_C49_over_A5_x_C7",g,v,7,1));

# Changed inputs exercise nonzero norm rank, a faithful odd action and a
# nontrivial characteristic-two action, beyond the author's exact fixtures.
gv:=NovaSemi(3,3,3,x->[x[1],x[1]*x[2],x[2]*x[3]]);;
Add(extras,NovaAudit("F3_cubed_Jordan_C3",gv[1],gv[2],3,3));
gv:=NovaSemi(5,2,4,x->[x[1]^2,x[2]^2]);;
Add(extras,NovaAudit("F5_squared_faithful_scalar_C4",gv[1],gv[2],5,2));
gv:=NovaSemi(2,3,7,x->[x[2],x[3],x[1]*x[2]]);;
Add(extras,NovaAudit("F2_cubed_faithful_C7",gv[1],gv[2],2,3));
g:=CyclicGroup(IsPermGroup,121);; v:=Subgroup(g,[GeneratorsOfGroup(g)[1]^11]);;
Add(extras,NovaAudit("C121_over_C11",g,v,11,1));

# Malformed data rejected via different guards from Rowan's vector parser.
g:=CyclicGroup(IsPermGroup,4);; gen:=GeneratorsOfGroup(g)[1];;
bad_kernel_rejected:=not IsElementaryAbelian(g);;
q:=CyclicGroup(IsPermGroup,2);; qgen:=GeneratorsOfGroup(q)[1];;
badmap:=function(x) local i; i:=Position([One(g),gen,gen^2,gen^3],x)-1;
    return qgen^QuoInt(i,2); end;;
bad_projection_rejected:=ForAny(Elements(g),x->badmap(x*gen)<>badmap(x)*badmap(gen));;
negative:=rec(invalid_C4_as_F2_squared:=bad_kernel_rejected,
    invalid_C4_projection:=bad_projection_rejected,
    invalid_composite_characteristic:=not IsPrimeInt(4));;
if not ForAll(RecNames(negative),n->negative.(n)) then Error("negative guard failed"); fi;

stream:=OutputTextFile("RESULT.json",false);; SetPrintFormattingStatus(stream,false);
NovaJson(stream,rec(status:="INDEPENDENT_EXTENSION_CONTROLS_PASS",gap_version:=GAPInfo.Version,
    fixtures:=results,changed_inputs:=extras,negative_controls:=negative));
PrintTo(stream,"\n"); CloseStream(stream);
Print("INDEPENDENT_EXTENSION_CONTROLS_PASS 22 fixtures, 4 changed inputs, 3 rejections\n");
QUIT;
