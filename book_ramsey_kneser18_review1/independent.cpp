// six-reviewer-1, independent reviewer. No researcher implementation imported.
// Gray-code domains; direct full-graph book tests; unquotiented 22-frontier.
#include <algorithm>
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

struct Case { const char* name; std::array<int,3> deleted; };
const std::array<Case,5> cases{{{"triangle",{0,1,6}},{"star",{0,1,2}},
    {"path",{0,6,11}},{"wedge_edge",{0,1,15}},{"matching",{0,11,18}}}};

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

template<class T> void array_json(const std::vector<T>& a) {
    std::cout<<'['; bool comma=false;
    for (const auto& v:a) { if(comma)std::cout<<',';std::cout<<v;comma=true; }
    std::cout<<']';
}
template<std::size_t N> void tuples_json(const std::vector<std::array<int,N>>& a) {
    std::cout<<'[';bool comma=false;
    for (const auto& v:a) {
        if(comma)std::cout<<',';
        std::cout<<'[';
        for (std::size_t i=0;i<N;++i) {if(i)std::cout<<',';std::cout<<v[i];}
        std::cout<<']';comma=true;
    }
    std::cout<<']';
}

int main(int argc,char** argv) try {
    controls();
    if (argc==2 && std::string(argv[1])=="--controls-only") {
        std::cout<<"{\"controls\":true,\"small_domains\":8}\n";return 0;
    }
    need(argc==1,"unexpected argument");
    std::vector<Bits> roots;
    for(int a=0;a<7;++a)for(int b=a+1;b<7;++b)roots.push_back(bit(a)|bit(b));
    Graph seed(21,0);
    for(int i=0;i<21;++i)for(int j=i+1;j<21;++j)if(!(roots[i]&roots[j])) {
        seed[i]|=bit(j);seed[j]|=bit(i);
    }
    need(valid(seed),"invalid seed");for(Bits row:seed)need(pc(row)==10,"seed degree");
    std::array<std::array<Bits,7>,5> representatives{};
    auto root_graph=[&](const std::array<int,3>& deleted) {
        std::array<Bits,7> a{};
        for (int index:deleted) for(int x=0;x<7;++x)if(roots[index]&bit(x))
            a[x]|=roots[index]^bit(x);
        return a;
    };
    for(int c=0;c<5;++c)representatives[c]=root_graph(cases[c].deleted);
    std::vector<int> cohort(5,0);int witnesses=0;
    for(int i=0;i<21;++i)for(int j=i+1;j<21;++j)for(int k=j+1;k<21;++k) {
        auto a=root_graph({i,j,k});int matches=0;
        for(int c=0;c<5;++c) {
            std::array<int,7> image;
            if(transport(a,representatives[c],image)) {
                ++matches;++cohort[c];
                std::array<int,7> sorted=image;std::sort(sorted.begin(),sorted.end());
                need(sorted==std::array<int,7>{{0,1,2,3,4,5,6}},"transport not bijective");
                for(int x=0;x<7;++x)for(int y=0;y<7;++y)
                    need(((a[x]&bit(y))!=0)==((representatives[c][image[x]]&bit(image[y]))!=0),"false transport");
            }
        }
        need(matches==1,"core classification gap/overlap");++witnesses;
    }
    std::cout<<"{\"controls\":true,\"transport_witnesses\":"<<witnesses<<",\"cohorts\":";
    array_json(cohort);std::cout<<",\"cases\":[";
    for(int c=0;c<5;++c) {
        std::vector<int> labels;
        for(int u=0;u<21;++u)if(std::find(cases[c].deleted.begin(),cases[c].deleted.end(),u)==cases[c].deleted.end())labels.push_back(u);
        Graph core(18,0);
        for(int u=0;u<18;++u)for(int v=u+1;v<18;++v)if(!(roots[labels[u]]&roots[labels[v]])) {
            core[u]|=bit(v);core[v]|=bit(u);
        }
        auto domain=gray_domain(core);int m=static_cast<int>(domain.size());
        need(m<=2000,"domain exceeds checked arithmetic range");
        std::vector<std::vector<unsigned char>> allowed(static_cast<std::size_t>(m),std::vector<unsigned char>(static_cast<std::size_t>(m),0));
        std::vector<std::array<int,3>> pairs;
        for(int i=0;i<m;++i)for(int j=i;j<m;++j)for(int color=0;color<2;++color)
            if(valid(add(core,{domain[i],domain[j]},color))) {
                need(i!=j,"repeated-pattern pair escapes distinctness");
                pairs.push_back({i,j,color});allowed[i][j]|=static_cast<unsigned char>(bit(color));allowed[j][i]=allowed[i][j];
            }
        std::uint64_t edges=0,cliques=0;
        for(int i=0;i<m;++i)for(int j=i+1;j<m;++j)edges+=allowed[i][j]!=0;
        std::vector<std::array<int,5>> frontier;
        std::array<std::uint64_t,8> violation_flags{};
        std::array<std::uint64_t,4> cross_color_flags{};
        for(int i=0;i<m;++i)for(int j=i+1;j<m;++j)if(allowed[i][j]) {
            std::vector<int> common;
            for(int k=j+1;k<m;++k)if(allowed[i][k]&&allowed[j][k])common.push_back(k);
            for(std::size_t a=0;a<common.size();++a)for(std::size_t b=a+1;b<common.size();++b) {
                int k=common[a],l=common[b];if(!allowed[k][l])continue;++cliques;
                const std::array<int,4> indices{{i,j,k,l}};
                for(int joining=0;joining<64;++joining) {
                    bool compatible=true;int position=0;
                    for(int x=0;x<4;++x)for(int y=x+1;y<4;++y,++position)
                        if(!(allowed[indices[x]][indices[y]]&bit((joining>>position)&1)))compatible=false;
                    if(!compatible)continue;
                    Graph h=add(core,{domain[i],domain[j],domain[k],domain[l]},joining);
                    need(!valid(h),"valid 22-vertex completion found");
                    int flags=0, cross_colors=0;
                    for(int u=0;u<22;++u)for(int v=u+1;v<22;++v) {
                        bool red=(h[u]&bit(v))!=0;
                        Bits pages=red?h[u]&h[v]:full(22)&~(h[u]|h[v]|bit(u)|bit(v));
                        if(pc(pages)>(red?3:6)) {
                            flags|=1<<(v<18?0:(u<18?1:2));
                            if(u<18 && v>=18)cross_colors|=red?1:2;
                        }
                    }
                    need(flags!=0,"missing direct book");++violation_flags[flags];
                    ++cross_color_flags[cross_colors];
                    frontier.push_back({i,j,k,l,joining});
                }
            }
        }
        std::sort(frontier.begin(),frontier.end());
        if(c)std::cout<<',';
        std::cout<<"{\"name\":\""<<cases[c].name<<"\",\"domain\":";array_json(domain);
        std::cout<<",\"pair_colors\":";tuples_json(pairs);
        std::cout<<",\"frontier\":";tuples_json(frontier);
        std::cout<<",\"compatibility_edges\":"<<edges<<",\"four_cliques\":"<<cliques<<",\"violation_flags\":[";
        for(int i=0;i<8;++i){if(i)std::cout<<',';std::cout<<violation_flags[i];}
        std::cout<<"],\"cross_color_flags\":[";
        for(int i=0;i<4;++i){if(i)std::cout<<',';std::cout<<cross_color_flags[i];}
        std::cout<<"]}";
    }
    std::cout<<"]}\n";
    need(std::cout.good(),"output failure");
    return 0;
} catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 1;}
