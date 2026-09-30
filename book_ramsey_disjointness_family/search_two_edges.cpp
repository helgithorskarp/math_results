// Complete fixed-core two-edge classification. One thread, exact integers.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <vector>
using Bits = __uint128_t;
unsigned pop(unsigned x) { return __builtin_popcount(x); }
struct Row {
    unsigned n, b, t, zero, one, low;
    Bits pages;
    std::array<int, 16> allowance;
};
struct Internal {
    std::array<unsigned, 6> red{}, blue{};
    explicit Internal(bool path) {
        if (path) red = {0, 0, 0, 48, 8, 8};
        else red = {0, 0, 8, 4, 32, 16};
        for (unsigned i=0; i<6; ++i) blue[i] = 63 ^ red[i] ^ (1u<<i);
    }
};
struct Book { int color=-1; unsigned i=0, j=0; std::vector<unsigned> pages; };

int main(int argc, char** argv) try {
    if (argc != 3) throw std::runtime_error("arguments: core16.edges trace.txt");
    std::ifstream input(argv[1]); unsigned n; input>>n;
    if (!input || n != 16) throw std::runtime_error("invalid core order");
    std::array<unsigned,16> core{}; unsigned i,j, edge_count=0;
    while (input>>i>>j) {
        if (i>=16 || j>=i || (core[i]>>j&1)) throw std::runtime_error("invalid core edge");
        core[i]|=1u<<j; core[j]|=1u<<i; ++edge_count;
    }
    if (!input.eof() || edge_count!=48) throw std::runtime_error("invalid core fixture");
    for (auto a:core) if(pop(a)!=6) throw std::runtime_error("core is not six-regular");
    std::vector<std::array<unsigned,2>> spines;
    std::vector<unsigned> caps;
    std::array<Bits,4> capmask{};
    for (unsigned color=0;color<2;++color)
        for(unsigned i=0;i<16;++i) for(unsigned j=0;j<i;++j) {
            if (bool(core[i]>>j&1) != (color==0)) continue;
            unsigned codeg = color==0 ? pop(core[i]&core[j]) :
                pop((65535^core[i]^(1u<<i))&(65535^core[j]^(1u<<j)));
            unsigned cap=(color==0?3:6)-codeg;
            if(cap>3) throw std::runtime_error("unexpected residual capacity");
            capmask[cap]|=Bits(1)<<spines.size();
            spines.push_back({i,j}); caps.push_back(cap);
        }
    if(spines.size()!=120) throw std::runtime_error("incomplete spine list");
    std::ofstream trace(argv[2]); if(!trace) throw std::runtime_error("cannot write trace");
    std::vector<Row> rows; std::vector<unsigned> ten;
    for(unsigned mask=0;mask<65536;++mask) {
        bool eligible=true; unsigned low=0;
        for(unsigned y=0;y<16;++y) if(mask>>y&1) {
            unsigned d=pop(core[y]&mask);
            if(d>3) eligible=false;
            if(d<=2) low|=1u<<y;
        }
        if(!eligible) continue;
        if(pop(mask)>10) throw std::runtime_error("row lemma failed");
        Row r{}; r.n=mask; r.b=65535^mask; r.t=pop(mask); r.low=low;
        for(unsigned k=0;k<spines.size();++k) {
            unsigned a=spines[k][0],b=spines[k][1],s=k<48?r.n:r.b;
            if(s>>a&s>>b&1) r.pages|=Bits(1)<<k;
        }
        if(r.pages&capmask[0]) continue;
        for(unsigned y=0;y<16;++y) {
            r.allowance[y]=7-int(pop(r.b))+int(pop(core[y]&r.b));
            if(r.b>>y&1) {
                if(r.allowance[y]<0) eligible=false;
                if(r.allowance[y]==0) r.zero|=1u<<y;
                if(r.allowance[y]<=1) r.one|=1u<<y;
            }
        }
        if(!eligible) continue;
        if(r.t==10) ten.push_back(rows.size());
        trace<<"R "<<r.n<<'\n'; rows.push_back(r);
    }
    if(ten.size()!=4) throw std::runtime_error("unexpected ten-row domain");
    for(auto id:ten) for(unsigned y=0;y<16;++y) if(rows[id].n>>y&1)
        if(pop(core[y]&rows[id].n)!=3) throw std::runtime_error("ten-row is not cubic");
    Internal matching(false), path(true);
    // roles 0,1 are ordinary in both patterns; role 2 is also ordinary for P3.
    auto valid = [&](std::vector<unsigned> const& ids, Internal const& J) {
        Bits used1=0,used2=0,used3=0;
        for(unsigned a=0;a<ids.size();++a) {
            Row const&r=rows[ids[a]];
            if(r.pages&((used1&capmask[1])|(used2&capmask[2])|(used3&capmask[3]))) return false;
            used3|=used2&r.pages; used2|=used1&r.pages; used1|=r.pages;
            for(unsigned b=0;b<a;++b) {
                Row const&s=rows[ids[b]];
                if(J.red[a]>>b&1) {
                    if(pop(r.n&s.n)+pop(J.red[a]&J.red[b])>3) return false;
                } else if(pop(r.b&s.b)+pop(J.blue[a]&J.blue[b])>6) return false;
            }
        }
        for(unsigned a=0;a<ids.size();++a) {
            Row const&r=rows[ids[a]];
            for(unsigned y=0;y<16;++y) {
                if(r.n>>y&1) {
                    unsigned pages=pop(core[y]&r.n);
                    for(unsigned b=0;b<ids.size();++b) if(J.red[a]>>b&1) pages+=rows[ids[b]].n>>y&1;
                    if(pages>3) return false;
                } else {
                    int pages=0;
                    for(unsigned b=0;b<ids.size();++b) if(J.blue[a]>>b&1) pages+=rows[ids[b]].b>>y&1;
                    if(pages>r.allowance[y]) return false;
                }
            }
        }
        return true;
    };
    // A literal known-edge book finder also handles unassigned cross edges.
    auto book = [&](std::array<int,6> const& masks, Internal const& J) {
        std::array<std::array<unsigned,22>,2> adjacency{};
        for(unsigned a=0;a<16;++a) {
            adjacency[0][a]=core[a]; adjacency[1][a]=65535^core[a]^(1u<<a);
        }
        for(unsigned a=0;a<6;++a) {
            adjacency[0][16+a]=J.red[a]<<16; adjacency[1][16+a]=J.blue[a]<<16;
            if(masks[a]<0) continue;
            for(unsigned y=0;y<16;++y) {
                unsigned color=(unsigned(masks[a])>>y&1)?0:1;
                adjacency[color][16+a]|=1u<<y; adjacency[color][y]|=1u<<(16+a);
            }
        }
        for(unsigned color=0;color<2;++color) for(unsigned a=0;a<22;++a) for(unsigned b=0;b<a;++b)
            if(adjacency[color][a]>>b&1) {
                unsigned pages=adjacency[color][a]&adjacency[color][b],cap=color==0?3:6;
                if(pop(pages)>cap) {
                    Book result;result.color=color;result.i=b;result.j=a;
                    while(result.pages.size()<cap+1) {unsigned p=__builtin_ctz(pages);pages&=pages-1;result.pages.push_back(p);}
                    return result;
                }
            }
        return Book{};
    };
    unsigned ten_cases=0;
    // Without a degree assumption, enumerate every disjoint partner subset.
    for(auto a:ten) for(unsigned ei=0;ei<ten.size();++ei) for(unsigned fi=ei+1;fi<ten.size();++fi) {
        unsigned e=ten[ei],f=ten[fi]; if(e==a||f==a) continue;
        unsigned b=rows[a].b;
        while(true) {
            std::array<int,6> masks{int(rows[e].n),int(rows[f].n),int(rows[a].n),int(b),-1,-1};
            Book witness=book(masks,matching);
            if(witness.color<0) throw std::runtime_error("ten-endpoint case survives");
            trace<<"H "<<rows[e].n<<' '<<rows[f].n<<' '<<rows[a].n<<' '<<b<<' '<<witness.color<<' '<<witness.i<<' '<<witness.j;
            for(auto p:witness.pages) trace<<' '<<p;
            trace<<'\n'; ++ten_cases;
            if(b==0) break;
            b=(b-1)&rows[a].b;
        }
    }
    auto ordinary_pair = [&](unsigned a,unsigned b) {
        Row const&r=rows[a],&s=rows[b];
        return pop(r.b&s.b)<=2 && !(r.pages&s.pages&capmask[1]) && !(r.b&s.zero) && !(s.b&r.zero);
    };
    std::vector<std::array<unsigned,2>> ordinary_pairs;
    std::vector<std::vector<unsigned>> neighbors(rows.size());
    for(unsigned e=0;e<rows.size();++e) for(unsigned f=e+1;f<rows.size();++f)
        if(ordinary_pair(e,f)) {
            ordinary_pairs.push_back({e,f}); neighbors[e].push_back(f);
            trace<<"O "<<rows[e].n<<' '<<rows[f].n<<'\n';
        }
    // Exact one-row domains after an all-blue ordinary prefix, obtained by
    // core capacities, saturated old cross spines, and new cross spines.
    auto domain = [&](std::vector<unsigned> const& os,unsigned overlap_cap,bool exclude_ten) {
        Bits used1=0,used2=0,used3=0;
        std::array<unsigned,16> blue_columns{};
        for(auto id:os) {
            auto&r=rows[id]; used3|=used2&r.pages;used2|=used1&r.pages;used1|=r.pages;
            for(unsigned y=0;y<16;++y)blue_columns[y]+=r.b>>y&1;
        }
        Bits exhausted=(used1&capmask[1])|(used2&capmask[2])|(used3&capmask[3]);
        unsigned forced=0;
        for(auto id:os) for(unsigned y=0;y<16;++y) if(rows[id].b>>y&1)
            if(int(blue_columns[y]-1)==rows[id].allowance[y]) forced|=1u<<y;
        std::vector<unsigned> result;
        for(unsigned k=0;k<rows.size();++k) {
            auto&r=rows[k];if((exclude_ten&&r.t==10)||(r.n&forced)!=forced||(r.pages&exhausted))continue;
            bool good=true;
            for(auto id:os)if(pop(r.b&rows[id].b)>overlap_cap){good=false;break;}
            if(!good)continue;
            for(unsigned y=0;y<16;++y)if(r.b>>y&1 && int(blue_columns[y])>r.allowance[y]){good=false;break;}
            if(good)result.push_back(k);
        }
        return result;
    };
    uint64_t matching_domains4=0,matching_checks=0,matching_pairs=0,matching_full_checks=0,matching_full=0;
    unsigned matching_max_domain=0,matching_max_pairs=0;
    for(auto ef:ordinary_pairs) {
        auto dom=domain({ef[0],ef[1]},3,true);
        matching_max_domain=std::max(matching_max_domain,unsigned(dom.size()));
        trace<<"M "<<rows[ef[0]].n<<' '<<rows[ef[1]].n<<' '<<dom.size();for(auto id:dom)trace<<' '<<rows[id].n;trace<<'\n';
        if(dom.size()<4) continue;
        ++matching_domains4;
        std::vector<std::array<unsigned,2>> pairs;
        for(unsigned a=0;a<dom.size();++a)for(unsigned b=a+1;b<dom.size();++b) {
            ++matching_checks;
            if(valid({ef[0],ef[1],dom[a],dom[b]},matching)) {
                pairs.push_back({dom[a],dom[b]});++matching_pairs;
                trace<<"P "<<rows[ef[0]].n<<' '<<rows[ef[1]].n<<' '<<rows[dom[a]].n<<' '<<rows[dom[b]].n<<'\n';
            }
        }
        matching_max_pairs=std::max(matching_max_pairs,unsigned(pairs.size()));
        for(unsigned a=0;a<pairs.size();++a)for(unsigned b=a+1;b<pairs.size();++b) {
            ++matching_full_checks;
            if(valid({ef[0],ef[1],pairs[a][0],pairs[a][1],pairs[b][0],pairs[b][1]},matching))++matching_full;
        }
    }
    uint64_t triangles=0,ordinary_triples=0,center_domains=0,leaf_domains=0,center_leaf_checks=0,center_leaf=0,path_full_checks=0,path_full=0;
    unsigned max_center=0,max_leaf=0;
    for(unsigned e=0;e<rows.size();++e)for(auto f:neighbors[e]) {
        std::vector<unsigned> common;
        std::set_intersection(neighbors[e].begin(),neighbors[e].end(),neighbors[f].begin(),neighbors[f].end(),std::back_inserter(common));
        for(auto g:common) {
            ++triangles;std::vector<unsigned> os{e,f,g};if(!valid(os,path))continue;++ordinary_triples;
            auto centers=domain(os,4,true),leaves=domain(os,3,false);
            center_domains+=centers.size();leaf_domains+=leaves.size();
            max_center=std::max(max_center,unsigned(centers.size()));max_leaf=std::max(max_leaf,unsigned(leaves.size()));
            trace<<"T "<<rows[e].n<<' '<<rows[f].n<<' '<<rows[g].n<<' '<<centers.size();for(auto id:centers)trace<<' '<<rows[id].n;
            trace<<' '<<leaves.size();for(auto id:leaves)trace<<' '<<rows[id].n;trace<<'\n';
            for(auto c:centers) {
                std::vector<unsigned> compatible;
                for(auto a:leaves) {
                    ++center_leaf_checks;
                    if(valid({e,f,g,c,a},path)){compatible.push_back(a);++center_leaf;}
                }
                for(unsigned a=0;a<compatible.size();++a)for(unsigned b=a+1;b<compatible.size();++b) {
                    ++path_full_checks;
                    if(valid({e,f,g,c,compatible[a],compatible[b]},path))++path_full;
                }
            }
        }
    }
    trace.close();if(!trace)throw std::runtime_error("trace write failed");
    std::cout<<"{\"complete\":true,\"rows\":"<<rows.size()<<",\"ten_endpoint_cases\":"<<ten_cases
        <<",\"ordinary_pairs\":"<<ordinary_pairs.size()<<",\"matching_domains_at_least_four\":"<<matching_domains4
        <<",\"matching_max_domain\":"<<matching_max_domain<<",\"matching_pair_checks\":"<<matching_checks
        <<",\"matching_pairs\":"<<matching_pairs<<",\"matching_max_pairs_per_context\":"<<matching_max_pairs
        <<",\"matching_full_checks\":"<<matching_full_checks<<",\"matching_full\":"<<matching_full
        <<",\"ordinary_pair_triangles\":"<<triangles<<",\"ordinary_triples\":"<<ordinary_triples
        <<",\"center_domain_sum\":"<<center_domains<<",\"leaf_domain_sum\":"<<leaf_domains
        <<",\"max_center_domain\":"<<max_center<<",\"max_leaf_domain\":"<<max_leaf
        <<",\"center_leaf_checks\":"<<center_leaf_checks<<",\"center_leaf_pairs\":"<<center_leaf
        <<",\"path_full_checks\":"<<path_full_checks<<",\"path_full\":"<<path_full<<"}\n";
    return 0;
} catch(std::exception const& e) { std::cerr<<e.what()<<'\n';return 2; }
