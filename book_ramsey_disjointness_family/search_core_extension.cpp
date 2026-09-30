// Complete-domain exclusion of all 22-vertex extensions of the fixed core.
// Author: six-books-2, role researcher; exact integer computation.
// Candidate scans use mask capacities; no external degree cuts or solver.
#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>
using Bits = __uint128_t;
unsigned pop(unsigned x) { return __builtin_popcount(x); }
struct Row {
    unsigned n, b, t;
    Bits pages;
    std::array<int, 16> allowance;
};
struct Internal {
    std::array<unsigned, 6> red{}, blue{};
    explicit Internal(unsigned mask) {
        unsigned k=0;
        for(unsigned a=0;a<6;++a)for(unsigned b=a+1;b<6;++b,++k)
            if(mask>>k&1){red[a]|=1u<<b;red[b]|=1u<<a;}
        for (unsigned i=0; i<6; ++i) blue[i] = 63 ^ red[i] ^ (1u<<i);
    }
};
struct Book { int color=-1; unsigned i=0, j=0; std::vector<unsigned> pages; };

int main(int argc, char** argv) try {
    if (argc != 4) throw std::runtime_error("arguments: core16.edges trace.txt internal_red_mask");
    std::ifstream input(argv[1]); unsigned n; input>>n;
    if (!input || n != 16) throw std::runtime_error("invalid core order");
    std::array<unsigned,16> core{}; unsigned i,j, edge_count=0;
    while (input>>i) {
        if (!(input>>j)) throw std::runtime_error("incomplete core edge");
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
    std::string mask_text(argv[3]);
    if (mask_text.empty() || mask_text.find_first_not_of("0123456789") != std::string::npos)
        throw std::runtime_error("invalid internal mask");
    std::size_t consumed = 0;
    unsigned long mask_value = std::stoul(mask_text, &consumed);
    if (consumed != mask_text.size() || mask_value >= 32768)
        throw std::runtime_error("invalid internal mask");
    unsigned internal_mask = static_cast<unsigned>(mask_value);
    Internal J(internal_mask);
    std::ofstream trace(argv[2]); if(!trace) throw std::runtime_error("cannot write trace");
    for(unsigned a=0;a<6;++a)for(unsigned b=0;b<a;++b)if(J.red[a]>>b&1) {
        unsigned pages=J.red[a]&J.red[b];
        if(pop(pages)>3) {
            trace<<"I "<<b<<' '<<a;
            for(unsigned count=0;count<4;++count){unsigned p=__builtin_ctz(pages);pages&=pages-1;trace<<' '<<p;}
            trace<<'\n';trace.close();if(!trace)throw std::runtime_error("trace write failed");
            std::cout<<"{\"complete\":true,\"internal_red_mask\":"<<internal_mask<<",\"rows\":0,\"internal_book\":true,\"full_valid\":0}\n";
            return 0;
        }
    }
    std::vector<Row> rows; std::vector<unsigned> ten;
    for(unsigned mask=0;mask<65536;++mask) {
        bool eligible=true;
        for(unsigned y=0;y<16;++y) if(mask>>y&1) {
            unsigned d=pop(core[y]&mask);
            if(d>3) eligible=false;
        }
        if(!eligible) continue;
        if(pop(mask)>10) throw std::runtime_error("row lemma failed");
        Row r{}; r.n=mask; r.b=65535^mask; r.t=pop(mask);
        for(unsigned k=0;k<spines.size();++k) {
            unsigned a=spines[k][0],b=spines[k][1],s=k<48?r.n:r.b;
            if(s>>a&s>>b&1) r.pages|=Bits(1)<<k;
        }
        if(r.pages&capmask[0]) continue;
        for(unsigned y=0;y<16;++y) {
            r.allowance[y]=7-int(pop(r.b))+int(pop(core[y]&r.b));
            if(r.b>>y&1) {
                if(r.allowance[y]<0) eligible=false;
            }
        }
        if(!eligible) continue;
        if(r.t==10) ten.push_back(rows.size());
        trace<<"R "<<r.n<<'\n'; rows.push_back(r);
    }
    if(ten.size()!=4) throw std::runtime_error("unexpected ten-row domain");
    for(auto id:ten) for(unsigned y=0;y<16;++y) if(rows[id].n>>y&1)
        if(pop(core[y]&rows[id].n)!=3) throw std::runtime_error("ten-row is not cubic");
    using Context = std::vector<std::array<unsigned,2>>;
    // Exact domain after any valid prefix. A candidate is rejected only
    // for an exhausted core spine, pair spine, or old/new cross spine.
    auto domain = [&](Context const& context, unsigned role, std::vector<unsigned> const& base) {
        Bits used1=0,used2=0,used3=0;
        for(auto item:context){auto&p=rows[item[1]].pages;used3|=used2&p;used2|=used1&p;used1|=p;}
        Bits saturated=(used1&capmask[1])|(used2&capmask[2])|(used3&capmask[3]);
        unsigned must_red=0,must_blue=0;
        for(auto item:context) {
            unsigned oldrole=item[0]; auto&r=rows[item[1]];
            unsigned color=(J.red[role]>>oldrole&1)?0:1;
            for(unsigned y=0;y<16;++y) {
                unsigned oldcolor=(r.n>>y&1)?0:1;
                if(oldcolor!=color)continue;
                int pages=oldcolor==0?int(pop(core[y]&r.n)):0;
                for(auto other:context)if((oldcolor==0?J.red[oldrole]:J.blue[oldrole])>>other[0]&1)
                    pages+=(oldcolor==0?rows[other[1]].n:rows[other[1]].b)>>y&1;
                int cap=oldcolor==0?3:r.allowance[y];
                if(pages>cap)throw std::runtime_error("invalid input prefix");
                if(pages==cap) {if(oldcolor==0)must_blue|=1u<<y;else must_red|=1u<<y;}
            }
        }
        std::array<unsigned,16> redcols{},bluecols{};
        for(auto item:context)for(unsigned y=0;y<16;++y){
            if(J.red[role]>>item[0]&1)redcols[y]+=rows[item[1]].n>>y&1;
            else bluecols[y]+=rows[item[1]].b>>y&1;
        }
        std::vector<unsigned> result;
        for(auto id:base) {
            auto&r=rows[id];
            if((r.n&must_red)!=must_red || (r.b&must_blue)!=must_blue || (r.pages&saturated))continue;
            bool good=true;
            for(auto item:context) {
                unsigned oldrole=item[0];auto&s=rows[item[1]];
                unsigned color=(J.red[role]>>oldrole&1)?0:1;
                unsigned pages=pop((color==0?r.n:r.b)&(color==0?s.n:s.b));
                pages+=pop((color==0?J.red[role]:J.blue[role])&(color==0?J.red[oldrole]:J.blue[oldrole]));
                if(pages>(color==0?3u:6u)){good=false;break;}
            }
            if(!good)continue;
            for(unsigned y=0;y<16;++y) {
                if(r.n>>y&1){if(pop(core[y]&r.n)+redcols[y]>3){good=false;break;}}
                else if(int(bluecols[y])>r.allowance[y]){good=false;break;}
            }
            if(good)result.push_back(id);
        }
        return result;
    };
    // Literal graph certificate check: an unknown cross edge has no color.
    auto book = [&](Context const& context) {
        std::array<std::array<unsigned,22>,2> adjacency{};
        for(unsigned a=0;a<16;++a){adjacency[0][a]=core[a];adjacency[1][a]=65535^core[a]^(1u<<a);}
        for(unsigned role=0;role<6;++role){adjacency[0][16+role]=J.red[role]<<16;adjacency[1][16+role]=J.blue[role]<<16;}
        for(auto item:context)for(unsigned y=0;y<16;++y){unsigned color=(rows[item[1]].n>>y&1)?0:1;adjacency[color][16+item[0]]|=1u<<y;adjacency[color][y]|=1u<<(16+item[0]);}
        for(unsigned color=0;color<2;++color)for(unsigned a=0;a<22;++a)for(unsigned b=0;b<a;++b)if(adjacency[color][a]>>b&1){
            unsigned pages=adjacency[color][a]&adjacency[color][b],cap=color==0?3:6;
            if(pop(pages)>cap){Book z;z.color=color;z.i=b;z.j=a;while(z.pages.size()<cap+1){unsigned p=__builtin_ctz(pages);pages&=pages-1;z.pages.push_back(p);}return z;}
        }
        return Book{};
    };
    // Isolates and low-degree vertices first. Variable order changes no domain.
    std::array<unsigned,6> order{0,1,2,3,4,5};
    std::stable_sort(order.begin(),order.end(),[&](unsigned a,unsigned b){return pop(J.red[a])<pop(J.red[b]);});
    std::array<unsigned,6> permutation{0,1,2,3,4,5};
    std::vector<std::array<unsigned,6>> automorphisms;
    do {
        bool good=true;
        for(unsigned a=0;a<6;++a)for(unsigned b=a+1;b<6;++b)
            if(bool(J.red[a]>>b&1)!=bool(J.red[permutation[a]]>>permutation[b]&1))good=false;
        if(good)automorphisms.push_back(permutation);
    } while(std::next_permutation(permutation.begin(),permutation.end()));
    unsigned automorphism_count=automorphisms.size();
    // At each step, the next role has the smallest row in its orbit under
    // automorphisms fixing all earlier roles. Every distinct-row labeling
    // has exactly one such representative in its automorphism orbit.
    std::vector<std::array<unsigned,2>> inequalities;
    for(unsigned role:order) {
        unsigned orbit=0;for(auto const& p:automorphisms)orbit|=1u<<p[role];
        for(unsigned other=0;other<6;++other)if(other!=role && (orbit>>other&1))inequalities.push_back({role,other});
        std::vector<std::array<unsigned,6>> stabilizer;
        for(auto const& p:automorphisms)if(p[role]==role)stabilizer.push_back(p);
        automorphisms=std::move(stabilizer);
    }
    if(automorphisms.size()!=1)throw std::runtime_error("incomplete stabilizer chain");
    using Domains=std::array<std::vector<unsigned>,6>;
    Domains initial;
    for(unsigned role=0;role<6;++role)for(unsigned id=0;id<rows.size();++id)
        if(pop(J.red[role])<2 || rows[id].t<10)initial[role].push_back(id);
    for(unsigned color=0;color<2;++color)for(unsigned a=0;a<6;++a)for(unsigned b=0;b<a;++b)
        if((color==0?J.red[a]:J.blue[a])>>b&1 && pop((color==0?J.red[a]:J.blue[a])&(color==0?J.red[b]:J.blue[b]))>(color==0?3u:6u))
            throw std::runtime_error("internal pattern already contains a book");
    std::array<uint64_t,7> nodes{},branches{},empty{};
    std::array<uint64_t,6> calls{};
    uint64_t full=0;
    std::function<void(Context const&,Domains const&)> dfs;
    dfs=[&](Context const& context,Domains const& parent) {
        unsigned depth=context.size();++nodes[depth];
        if(depth==6){if(book(context).color>=0)throw std::runtime_error("complete domain/book disagreement");++full;trace<<"W";for(auto v:context)trace<<' '<<v[0]<<' '<<rows[v[1]].n;trace<<'\n';return;}
        std::array<int,6> assigned{};assigned.fill(-1);for(auto v:context)assigned[v[0]]=int(v[1]);
        Domains ready=parent;int selected=-1;
        for(unsigned role:order)if(assigned[role]<0) {
            ++calls[depth];auto candidate=domain(context,role,parent[role]);
            std::vector<unsigned> filtered;
            for(auto id:candidate) {
                bool good=true;
                for(auto v:context)if(id==v[1]){good=false;break;}
                if(!good)continue;
                for(auto pair:inequalities) {
                    if(pair[0]==role && assigned[pair[1]]>=0 && id>=unsigned(assigned[pair[1]]))good=false;
                    if(pair[1]==role && assigned[pair[0]]>=0 && id<=unsigned(assigned[pair[0]]))good=false;
                }
                if(good)filtered.push_back(id);
            }
            ready[role]=std::move(filtered);
            if(selected<0)selected=int(role);
            if(ready[role].empty()){selected=int(role);break;}
        }
        if(selected<0)throw std::runtime_error("no next role");
        unsigned role=unsigned(selected);auto const& dom=ready[role];
        trace<<"D "<<depth;for(auto v:context)trace<<' '<<v[0]<<' '<<rows[v[1]].n;
        trace<<' '<<role<<' '<<dom.size();for(auto id:dom)trace<<' '<<rows[id].n;trace<<'\n';
        if(dom.empty()){++empty[depth];return;}
        branches[depth]+=dom.size();
        for(auto id:dom){Context child=context;child.push_back({role,id});dfs(child,ready);}
    };
    dfs({},initial);
    trace.close();if(!trace)throw std::runtime_error("trace write failed");
    auto print_array=[&](auto const& array){std::cout<<'[';for(unsigned k=0;k<array.size();++k){if(k)std::cout<<',';std::cout<<array[k];}std::cout<<']';};
    std::cout<<"{\"complete\":true,\"internal_red_mask\":"<<internal_mask<<",\"rows\":"<<rows.size()<<",\"automorphism_count\":"<<automorphism_count<<",\"internal_book\":false,\"full_valid\":"<<full<<",\"records_by_depth\":";print_array(nodes);
    std::cout<<",\"branches_by_depth\":";print_array(branches);std::cout<<",\"empty_domains_by_depth\":";print_array(empty);
    std::cout<<",\"candidate_domain_calls_by_depth\":";print_array(calls);std::cout<<"}\n";
    return 0;
} catch(std::exception const&e){std::cerr<<e.what()<<'\n';return 2;}
