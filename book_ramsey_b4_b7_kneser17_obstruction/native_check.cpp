// Author: six-books-3, researcher. Exact induced17 prefix checker.
// Generic direct-book, Gray-domain and point-transport helpers adapted with
// attribution from six-reviewer-1 source 0b527dd00c913e5148b473d8e0d2bc556d11bf75,
// book_ramsey_kneser18_review1/independent.cpp. New four-deletion census,
// hereditary five-prefix traversal and book-location records are by this author.
#include <algorithm>
#include <chrono>
#include <filesystem>
#include <fstream>
#include <set>
#include <array>
#include <cstdint>
#include <functional>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using Bits = std::uint32_t;
using Graph = std::vector<Bits>;
void need(bool b, const char* message) { if (!b) throw std::runtime_error(message); }
int pc(Bits x) { return __builtin_popcount(x); }
Bits bit(int x) { need(x >= 0 && x < 31, "shift range"); return Bits{1} << x; }
Bits full(int n) { return bit(n)-1U; }

// All pairs are tested, including spine endpoints in blue complements.
bool valid(const Graph& g) {
    int n = static_cast<int>(g.size());
    need(n <= 22, "graph range");
    for (int u=n-1;u>=0;--u) for (int v=u-1;v>=0;--v) {
        bool red = (g[u] & bit(v)) != 0;
        Bits pages = red ? g[u]&g[v] : full(n)&~(g[u]|g[v]|bit(u)|bit(v));
        if (pc(pages) > (red?3:6)) return false;
    }
    return true;
}

Graph add(const Graph& g, const std::vector<Bits>& patterns, int joining) {
    int n = static_cast<int>(g.size()), k = static_cast<int>(patterns.size());
    need(n+k<=22 && joining>=0, "augmentation range");
    Graph h=g; h.resize(static_cast<std::size_t>(n+k),0);
    for (int i=0;i<k;++i) {
        need((patterns[i]&~full(n))==0, "pattern range");
        for (int u=0;u<n;++u) if ((patterns[i]&bit(u))!=0) {
            h[u]|=bit(n+i); h[n+i]|=bit(u);
        }
    }
    int b=0;
    for (int i=0;i<k;++i) for (int j=i+1;j<k;++j,++b)
        if ((static_cast<Bits>(joining)&bit(b))!=0) {
            h[n+i]|=bit(n+j); h[n+j]|=bit(n+i);
        }
    need(static_cast<Bits>(joining)<bit(b), "joining range");
    return h;
}

std::vector<Bits> gray_domain(const Graph& g) {
    need(valid(g), "invalid core");
    int n=static_cast<int>(g.size());
    std::vector<int> red_degree(n,0), blue_degree(n,0), color(n,0);
    std::vector<std::vector<std::pair<int,int>>> saturated(n);
    int bad_new=0, bad_old=0;
    for (int u=0;u<n;++u) {
        blue_degree[u]=n-1-pc(g[u]);
        bad_new += blue_degree[u]>6;
        for (int v=u+1;v<n;++v) {
            int c=(g[u]&bit(v))!=0;
            Bits pages=c?g[u]&g[v]:full(n)&~(g[u]|g[v]|bit(u)|bit(v));
            if (pc(pages)==(c?3:6)) {
                saturated[u].emplace_back(v,c); saturated[v].emplace_back(u,c);
                bad_old += c==0;
            }
        }
    }
    auto bad=[&](int u) { return color[u] ? red_degree[u]>3 : blue_degree[u]>6; };
    std::vector<Bits> out;
    Bits p=0;
    if (bad_new==0 && bad_old==0) out.push_back(p);
    for (Bits step=1;step<bit(n);++step) {
        int x=__builtin_ctz(step), old=color[x], delta=old?-1:1;
        bad_new -= bad(x);
        for (const auto& item:saturated[x]) {
            int y=item.first,c=item.second;
            bad_old -= old==c && color[y]==c;
            bad_old += (1-old)==c && color[y]==c;
        }
        for (int y=0;y<n;++y) if (y!=x) {
            bad_new -= bad(y);
            if ((g[x]&bit(y))!=0) red_degree[y]+=delta;
            else blue_degree[y]-=delta;
            bad_new += bad(y);
        }
        color[x]=1-old; p^=bit(x); bad_new+=bad(x);
        need(p==(step^(step>>1U)), "Gray traversal");
        need(bad_old>=0 && bad_new>=0, "negative violation counter");
        if (bad_old==0 && bad_new==0) out.push_back(p);
    }
    std::sort(out.begin(),out.end());
    need(std::adjacent_find(out.begin(),out.end())==out.end(), "duplicate pattern");
    for (Bits p0:out) need(valid(add(g,{p0},0)), "Gray accepted invalid pattern");
    return out;
}

void controls() {
    Graph red5(5,full(5)); for (int u=0;u<5;++u) red5[u]^=bit(u);
    Graph red6(6,full(6)); for (int u=0;u<6;++u) red6[u]^=bit(u);
    need(valid(red5) && !valid(red6), "red book boundary");
    need(valid(Graph(8,0)) && !valid(Graph(9,0)), "blue book boundary");
    for (int n=1;n<=8;++n) {
        Graph g(n,0);
        if (n>=3) for (int u=0;u<n;++u) {
            int v=(u+1)%n; g[u]|=bit(v);g[v]|=bit(u);
        }
        std::vector<Bits> direct;
        for (Bits p=0;p<bit(n);++p) if (valid(add(g,{p},0))) direct.push_back(p);
        need(gray_domain(g)==direct, "small direct/Gray mismatch");
    }
}

// Construct an actual point isomorphism by degree-constrained backtracking.
bool transport(const std::array<Bits,7>& a,const std::array<Bits,7>& b,
               std::array<int,7>& image) {
    std::array<int,7> order{{0,1,2,3,4,5,6}};
    std::stable_sort(order.begin(),order.end(),[&](int x,int y){return pc(a[x])>pc(a[y]);});
    image.fill(-1);
    std::function<bool(int,Bits)> solve=[&](int d,Bits used) {
        if (d==7) return true;
        int x=order[d];
        for (int y=0;y<7;++y) if (!(used&bit(y)) && pc(a[x])==pc(b[y])) {
            bool good=true;
            for (int j=0;j<d;++j) {
                int z=order[j];
                if (((a[x]&bit(z))!=0)!=((b[y]&bit(image[z]))!=0)) good=false;
            }
            if (good) { image[x]=y;if (solve(d+1,used|bit(y))) return true;image[x]=-1; }
        }
        return false;
    };
    return solve(0,0);
}


struct Case { const char* name; std::array<int,4> deleted; int multiplicity; };
const std::array<Case,10> cases{{
    {"star4",{0,1,2,3},105}, {"path4",{0,6,11,15},1260},
    {"fork",{0,1,2,15},1260}, {"cycle4",{0,2,6,11},105},
    {"paw",{0,1,2,6},420}, {"triangle_edge",{0,1,6,15},210},
    {"star_edge",{0,1,2,18},420}, {"path_edge",{0,6,11,18},1260},
    {"two_wedges",{0,1,15,16},630}, {"wedge_two_edges",{0,1,15,20},315}
}};
using Positions = std::array<std::array<int,5>,5>;
Positions positions() {
    Positions result{}; int b=0;
    for(int i=0;i<5;++i)for(int j=i+1;j<5;++j)result[i][j]=b++;
    need(b==10,"joining layout");return result;
}
struct Record { std::array<int,5> indices{}; int mask=0; };
bool less_record(const Record& a,const Record& b) {
    return a.indices<b.indices || (a.indices==b.indices && a.mask<b.mask);
}
bool equal_record(const Record& a,const Record& b) {
    return a.indices==b.indices && a.mask==b.mask;
}
Graph decode(const Graph& core,const std::vector<Bits>& domain,
             const Record& r,int k,const Positions& pos) {
    std::vector<Bits> patterns;int joining=0,b=0;
    for(int i=0;i<k;++i) {
        need(r.indices[i]>=0 && static_cast<std::size_t>(r.indices[i])<domain.size(),"index range");
        if(i)need(r.indices[i-1]<r.indices[i],"nondistinct pattern ordering");
        patterns.push_back(domain[r.indices[i]]);
    }
    for(int i=0;i<k;++i)for(int j=i+1;j<k;++j,++b)
        if((r.mask>>pos[i][j])&1)joining|=1<<b;
    return add(core,patterns,joining);
}
int location_flags(const Graph& g) {
    need(g.size()==22,"location graph size");int flags=0;
    for(int u=0;u<22;++u)for(int v=u+1;v<22;++v) {
        bool red=(g[u]&bit(v))!=0;
        Bits pages=red?g[u]&g[v]:full(22)&~(g[u]|g[v]|bit(u)|bit(v));
        if(pc(pages)>(red?3:6))flags|=1<<((red?0:3)+(v<17?0:(u<17?1:2)));
    }
    return flags;
}
template<class T> void numbers(std::ostream& out,const std::vector<T>& xs) {
    out<<'[';for(std::size_t i=0;i<xs.size();++i){if(i)out<<',';out<<xs[i];}out<<']';
}
void records(std::ostream& out,const std::vector<Record>& xs,int k) {
    out<<'[';bool comma=false;
    for(const auto& r:xs) {
        if(comma)out<<',';
        comma=true;out<<"[[";
        for(int i=0;i<k;++i){if(i)out<<',';out<<r.indices[i];}
        out<<"],"<<r.mask<<']';
    }
    out<<']';
}
std::vector<int> census(const std::vector<Bits>& roots) {
    auto root_graph=[&](const std::array<int,4>& removed) {
        std::array<Bits,7> a{};
        for(int index:removed)for(int x=0;x<7;++x)if(roots[index]&bit(x))a[x]|=roots[index]^bit(x);
        return a;
    };
    std::array<std::array<Bits,7>,10> representatives{};
    for(int c=0;c<10;++c)representatives[c]=root_graph(cases[c].deleted);
    std::vector<int> counts(10,0);int total=0;
    for(int a=0;a<21;++a)for(int b=a+1;b<21;++b)
    for(int c=b+1;c<21;++c)for(int d=c+1;d<21;++d) {
        auto source=root_graph({a,b,c,d});int matches=0;
        for(int j=0;j<10;++j) {
            std::array<int,7> image;
            if(!transport(source,representatives[j],image))continue;
            auto sorted=image;std::sort(sorted.begin(),sorted.end());
            need(sorted==std::array<int,7>{{0,1,2,3,4,5,6}},"point map not bijective");
            for(int x=0;x<7;++x)for(int y=0;y<7;++y)
                need(((source[x]&bit(y))!=0)==((representatives[j][image[x]]&bit(image[y]))!=0),"false root map");
            ++matches;++counts[j];
        }
        need(matches==1,"four-deletion census gap/overlap");++total;
    }
    need(total==5985,"incomplete census");
    for(int c=0;c<10;++c)need(counts[c]==cases[c].multiplicity,"cohort mismatch");
    return counts;
}
void check_case(const Case& item,const std::vector<Bits>& roots,const std::filesystem::path& directory) {
    const auto pos=positions();std::vector<int> labels;
    for(int u=0;u<21;++u)if(std::find(item.deleted.begin(),item.deleted.end(),u)==item.deleted.end())labels.push_back(u);
    need(labels.size()==17,"core size");Graph core(17,0);
    for(int u=0;u<17;++u)for(int v=u+1;v<17;++v)if(!(roots[labels[u]]&roots[labels[v]])) {
        core[u]|=bit(v);core[v]|=bit(u);
    }
    auto domain=gray_domain(core);int m=static_cast<int>(domain.size());
    need(m>0 && m<=2000,"domain exceeds guarded arithmetic range");
    std::vector<std::vector<unsigned char>> allowed(static_cast<std::size_t>(m),std::vector<unsigned char>(static_cast<std::size_t>(m),0));
    std::vector<std::array<int,3>> pairs;std::vector<Record> previous;
    for(int i=0;i<m;++i)for(int j=i;j<m;++j)for(int color=0;color<2;++color)
        if(valid(add(core,{domain[i],domain[j]},color))) {
            need(i!=j,"repeated pattern needs multiplicity coverage");
            pairs.push_back({i,j,color});allowed[i][j]|=static_cast<unsigned char>(bit(color));allowed[j][i]=allowed[i][j];
            Record r;r.indices[0]=i;r.indices[1]=j;r.mask=color;previous.push_back(r);
        }
    std::vector<std::vector<Record>> levels{previous};
    std::array<std::uint64_t,3> candidate_counts{},joining_counts{};
    std::vector<std::array<int,7>> final_flags;
    for(int k=2;k<5;++k) {
        std::vector<Record> following;
        for(const auto& r:previous)for(int j=r.indices[k-1]+1;j<m;++j) {
            bool compatible=true;for(int i=0;i<k;++i)if(!allowed[r.indices[i]][j])compatible=false;
            if(!compatible)continue;
            ++candidate_counts[k-2];
            for(int colors=0;colors<(1<<k);++colors) {
                bool allowed_colors=true;
                for(int i=0;i<k;++i)if(!(allowed[r.indices[i]][j]&bit((colors>>i)&1)))allowed_colors=false;
                if(!allowed_colors)continue;
                ++joining_counts[k-2];
                Record next=r;next.indices[k]=j;
                for(int i=0;i<k;++i)if((colors>>i)&1)next.mask|=1<<pos[i][k];
                Graph graph=decode(core,domain,next,k+1,pos);
                if(valid(graph))following.push_back(next);
                else if(k==4) {
                    int flags=location_flags(graph);need(flags!=0,"missing book location");
                    final_flags.push_back({next.indices[0],next.indices[1],next.indices[2],next.indices[3],next.indices[4],next.mask,flags});
                }
            }
        }
        std::sort(following.begin(),following.end(),less_record);
        need(std::adjacent_find(following.begin(),following.end(),equal_record)==following.end(),"duplicate valid prefix");
        levels.push_back(following);previous=std::move(following);
        std::cout<<"native_level "<<item.name<<' '<<k+1<<" tests="<<joining_counts[k-2]<<" valid="<<previous.size()<<'\n'<<std::flush;
    }
    std::sort(final_flags.begin(),final_flags.end());
    std::ofstream out(directory/(std::string("case-")+item.name+".json"));need(out.is_open(),"output open");
    out<<"{\"name\":\""<<item.name<<"\",\"deleted\":[";
    for(int i=0;i<4;++i){if(i)out<<',';out<<item.deleted[i];}
    out<<"],\"domain\":";numbers(out,domain);out<<",\"pair_colors\":[";
    for(std::size_t i=0;i<pairs.size();++i){if(i)out<<',';out<<'['<<pairs[i][0]<<','<<pairs[i][1]<<','<<pairs[i][2]<<']';}
    out<<"],\"levels\":[";
    for(int k=2;k<=5;++k){if(k>2)out<<',';records(out,levels[static_cast<std::size_t>(k-2)],k);}
    out<<"],\"counts\":[";
    for(int k=3;k<=5;++k) {
        if(k>3)out<<',';
        out<<"{\"outside_vertices\":"<<k<<",\"candidate_index_extensions\":"<<candidate_counts[k-3]
           <<",\"joining_tests\":"<<joining_counts[k-3]<<",\"valid_prefixes\":"<<levels[static_cast<std::size_t>(k-2)].size()<<'}';
    }
    out<<"],\"final_flags\":[";
    for(std::size_t i=0;i<final_flags.size();++i) {
        if(i)out<<',';
        out<<'[';for(int j=0;j<7;++j){if(j)out<<',';out<<final_flags[i][j];}out<<']';
    }
    out<<"]}\n";out.close();need(!out.fail(),"incomplete output");
    need(previous.empty(),"valid22 completion found; inspect written case");
}
int main(int argc,char** argv) try {
    controls();
    if(argc==2 && std::string(argv[1])=="--controls-only") {std::cout<<"controls_complete\n";return 0;}
    need(argc==2 || argc==4,"usage: native_check OUTPUT_DIR [--case NAME]");
    std::string selected;
    if(argc==4){need(std::string(argv[2])=="--case","unknown option");selected=argv[3];}
    if(!selected.empty())need(std::any_of(cases.begin(),cases.end(),[&](const Case& c){return selected==c.name;}),"unknown case");
    const auto start=std::chrono::steady_clock::now();const std::filesystem::path directory(argv[1]);
    std::filesystem::create_directories(directory);
    std::filesystem::remove(directory/"completion.json");
    std::vector<Bits> roots;
    for(int a=0;a<7;++a)for(int b=a+1;b<7;++b)roots.push_back(bit(a)|bit(b));
    Graph seed(21,0);
    for(int i=0;i<21;++i)for(int j=i+1;j<21;++j)if(!(roots[i]&roots[j])){seed[i]|=bit(j);seed[j]|=bit(i);}
    need(valid(seed),"invalid known seed");for(Bits row:seed)need(pc(row)==10,"known seed degree");
    for(int u=0;u<21;++u)for(int v=u+1;v<21;++v) {
        bool red=(seed[u]&bit(v))!=0;
        Bits pages=red?seed[u]&seed[v]:full(21)&~(seed[u]|seed[v]|bit(u)|bit(v));
        need(pc(pages)==(red?3:5),"known seed codegree");
    }
    auto cohorts=census(roots);int completed=0;
    for(const auto& c:cases)if(selected.empty() || selected==c.name){check_case(c,roots,directory);++completed;}
    std::ofstream out(directory/"completion.json");need(out.is_open(),"completion open");
    out<<"{\"complete\":true,\"scope\":\""<<(selected.empty()?"all":selected)<<"\",\"cases\":"<<completed<<",\"labeled_cores\":5985,\"cohorts\":";
    numbers(out,cohorts);out<<"}\n";out.close();need(!out.fail(),"completion write");
    std::cout<<"native_complete cases="<<completed<<" scope="<<(selected.empty()?"all":selected)
             <<" seconds="<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<'\n';
    return 0;
} catch(const std::exception& error){std::cerr<<error.what()<<'\n';return 1;}
