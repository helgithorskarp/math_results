"""Independent full equality census and normalizer quotient, standard library only."""
from pathlib import Path
from collections import Counter
import argparse, json
from carrier import *

def run(instance,work):
    inp=json.loads(Path(instance).read_text())
    require(inp['permutation']==list(G),'fixture g')
    seed=tuple(sorted(inp['classical68_words']));degrees=packing(seed)
    require(degrees==tuple([20]*17+[0]),'classical support/degree')
    triples=Counter(tuple(sorted(t))for x in seed for t in __import__('itertools').combinations(bits(x),3))
    require(len(triples)==680 and set(triples.values())=={1},'literal Steiner fixture')
    U=universe(); fixed=tuple(o[0]for o in U if len(o)==1)
    full=tuple(o for o in U if len(o)==5 and admissible(o))
    root=tuple(o for o in full if o[0]&1)
    stars_ix,root_stats=exact_cliques(graph(root),4)
    stars=tuple(sorted(tuple(sorted(x for i in s for x in root[i]))for s in stars_ix))
    require(len(stars)==len(set(stars)),'star duplicates')
    seed_star=tuple(x for x in seed if x&1)
    require(seed_star in stars,'seed star in full carrier')
    prefix=tuple(sorted(seed_star+fixed))
    residual=tuple(o for o in full if not o[0]&1 and all((x&y).bit_count()<=2 for x in o for y in prefix))
    A=graph(residual); completions_ix,completion_stats=exact_cliques(A,9)
    completions=tuple(sorted(tuple(sorted(prefix+tuple(x for i in s for x in residual[i])))for s in completions_ix))
    for c in completions:packing(c)
    # Cover every enumerated star by an actual root-fixing commuting map.
    cover={}; root_multiplicities=Counter(); all_root_maps=tuple(group_maps(root=True))
    require(len(all_root_maps)==len(set(all_root_maps)),'root group distinctness')
    for p in all_root_maps:
        s=code_image(seed_star,p);root_multiplicities[s]+=1;cover.setdefault(s,p)
    require(set(cover)==set(stars),'positive complete star transitivity')
    root_codes=set(code_image(c,cover[s])for s in stars for c in completions)
    require(len(root_codes)==len(stars)*len(completions),'root transfers injective')
    labelled=set()
    for center in FIXED:
        p=list(range(18));p[0],p[center]=p[center],p[0]
        labelled.update(code_image(c,p)for c in root_codes)
    labelled=tuple(sorted(labelled)); degree_profiles=Counter(); fixed_saturation=Counter()
    for c in labelled:
        d=packing(c); degree_profiles[tuple(sorted(d))]+=1
        fixed_saturation[sum(d[p]==20 for p in FIXED)]+=1
    # Direct group-image orbits, independently chosen lexicographic representatives.
    centralizer=tuple(group_maps());require(len(centralizer)==len(set(centralizer)),'centralizer distinctness')
    remaining=set(labelled);classes=[];representatives=[];class_of={}
    while remaining:
        rep=min(remaining); C=set(code_image(rep,p)for p in centralizer)
        require(C<=remaining,'centralizer disjoint/exhaustive inventory')
        ix=len(classes)
        for c in C:class_of[c]=ix
        classes.append(tuple(sorted(C)));representatives.append(rep);remaining-=C
    # Conjugating generator to its square generates F5*, coarsening the quotient.
    square=list(range(18))
    for cyc in CYCLES:
        for i,x in enumerate(cyc):square[x]=cyc[(2*i)%5]
    square=tuple(square)
    require(all(square[G[x]]==G[G[square[x]]]for x in range(18)),'multiplier2 conjugacy')
    quotient=tuple(class_of[code_image(c,square)]for c in representatives)
    require(sorted(quotient)==list(range(len(classes))),'normalizer quotient permutation')
    merged=[]; unseen=set(range(len(classes)))
    while unseen:
        i=min(unseen);J=[];j=i
        while j not in J:J.append(j);j=quotient[j]
        require(j==i,'normalizer quotient cycle')
        unseen-=set(J);merged.append(tuple(J))
    # Explicit complete normalizer parameter coverage, with all point conjugacies.
    normalizer=set()
    for k in range(1,5): normalizer.update(group_maps(k))
    require(len(normalizer)==18000,'full normalizer distinct parameterization')
    normalizer_profiles=[]
    for J in merged:
        rep=representatives[min(J)]
        images=set(code_image(rep,p)for p in normalizer)
        union=set(c for j in J for c in classes[j])
        require(images==union,'all actual normalizer images equal quotient union')
        normalizer_profiles.append({'centralizer_classes':list(J),'size':len(images),'stabilizer':18000//len(images),'degree_profile':list(sorted(packing(rep)))})
    # Regenerate elementary replacement constructions without supplied catalogue.
    seed_orbits=tuple(o for o in U if set(o)<=set(seed))
    fixed_replace=tuple(o for o in seed_orbits if len(o)==5 and o[0]&(1<<16) and not o[0]&1)
    split_codes=set()
    for mask in range(1<<len(fixed_replace)):
        removed=set(x for i,o in enumerate(fixed_replace)if mask>>i&1 for x in o)
        new=set((x^(1<<16))|(1<<17)for x in removed)
        c=tuple(sorted((set(seed)-removed)|new));packing(c);split_codes.add(c)
    moving_codes=set();moving_rules=[]
    for o in seed_orbits:
        if len(o)!=5 or o[0]&1:continue
        for e in bits(o[0]):
            if e in FIXED:continue
            x=o[0];point=e;new=[]
            for _ in range(5):
                new.append((x^(1<<point))|(1<<17));x=image(x,G);point=G[point]
            if len(set(new))!=5 or not admissible(new):continue
            c=tuple(sorted((set(seed)-set(o))|set(new)));packing(c)
            moving_codes.add(c);moving_rules.append([o[0],e,list(sorted(new))])
    require(not split_codes&moving_codes,'construction types disjoint')
    require(split_codes|moving_codes==set(completions),'complete constructions entry equality')
    record={'universe_words':sum(len(o)for o in U),'word_orbits':len(U),'fixed_words':list(fixed),'full_admissible_orbits':len(full),'root_orbits':len(root),'root_edges':sum(x.bit_count()for x in graph(root))//2,'stars':len(stars),'star_hash':digest(stars),'root_search':root_stats,'root_group':len(all_root_maps),'star_transport_multiplicities':dict(Counter(root_multiplicities.values())),'prefix_words':len(prefix),'residual_orbits':len(residual),'residual_edges':sum(x.bit_count()for x in A)//2,'nine_cliques':len(completions),'completion_search':completion_stats,'completions_hash':digest(completions),'root_codes':len(root_codes),'labelled_codes':len(labelled),'labelled_hash':digest(labelled),'degree_profiles':[{'profile':list(p),'count':n}for p,n in sorted(degree_profiles.items())],'saturated_fixed_counts':dict(sorted(fixed_saturation.items())),'centralizer_size':len(centralizer),'centralizer_class_sizes':[len(C)for C in classes],'centralizer_stabilizers':[4500//len(C)for C in classes],'centralizer_representatives':representatives,'multiplier_two_quotient':quotient,'normalizer_size':len(normalizer),'normalizer_classes':normalizer_profiles,'split_codes':len(split_codes),'moving_codes':len(moving_codes),'moving_rules':moving_rules}
    work=Path(work);work.mkdir(parents=True,exist_ok=True)
    for name,obj in [('stars',stars),('residual',residual),('completions',completions),('root_codes',tuple(sorted(root_codes))),('labelled',labelled),('centralizer_classes',classes)]:
        (work/(name+'.json')).write_text(json.dumps(obj,separators=(',',':'))+'\n')
    (work/'RESULT.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    print(json.dumps(record,sort_keys=True,separators=(',',':')))
    return record

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--instance',required=True);p.add_argument('--work',required=True);p.add_argument('--expect')
    a=p.parse_args();z=run(a.instance,a.work)
    if a.expect:require(json.loads(json.dumps(z))==json.loads(Path(a.expect).read_text()),'complete expected output')
