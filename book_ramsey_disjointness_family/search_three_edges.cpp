// Exact three-edge classification for a fixed sixteen-vertex core.
// Candidate scans use mask capacities; no external degree cuts or solver.
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
    unsigned n, b, t;
    Bits pages;
    std::array<int, 16> allowance;
};
struct Internal {
    std::array<unsigned, 6> red{}, blue{};
    explicit Internal(std::string pattern) {
        if (pattern == "triangle") red = {0,0,0,48,40,24};
        else if (pattern == "star") red = {0,0,56,4,4,4};
        else if (pattern == "p4") red = {0,0,8,20,40,16};
        else if (pattern == "p3k2") red = {0,12,2,2,32,16};
        else if (pattern == "3k2") red = {2,1,8,4,32,16};
        else throw std::runtime_error("invalid pattern");
        for (unsigned i=0; i<6; ++i) blue[i] = 63 ^ red[i] ^ (1u<<i);
    }
};
struct Book { int color=-1; unsigned i=0, j=0; std::vector<unsigned> pages; };

int main(int argc, char** argv) try {
    if (argc != 4) throw std::runtime_error("arguments: core16.edges trace.txt pattern");
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
    std::string pattern=argv[3]; Internal J(pattern);
    std::ofstream trace(argv[2]); if(!trace) throw std::runtime_error("cannot write trace");
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
    auto record = [&](char tag,Context const& ctx,std::vector<unsigned> const& dom) {
        trace<<tag<<' '<<ctx.size();for(auto v:ctx)trace<<' '<<v[0]<<' '<<rows[v[1]].n;
        trace<<' '<<dom.size();for(auto id:dom)trace<<' '<<rows[id].n;trace<<'\n';
    };
    auto ordered_after = [&](std::vector<unsigned> const& ids,unsigned after){std::vector<unsigned> z;for(auto id:ids)if(id>after)z.push_back(id);return z;};
    std::vector<unsigned> all,not_ten;for(unsigned id=0;id<rows.size();++id){all.push_back(id);if(rows[id].t!=10)not_ten.push_back(id);}
    uint64_t ordinary_pairs=0,ordinary_triples=0,domain_sum=0,second_sum=0,qualifying=0,prefix3=0,prefix4=0,prefix5=0,full=0,case_checks=0;
    unsigned max_domain=0,max_second=0;
    // Exactly two ordinary vertices in star/P4, three in triangle.
    if(pattern=="star" || pattern=="p4" || pattern=="triangle") {
        for(unsigned e=0;e<rows.size();++e) {
            auto ordinary_second=ordered_after(domain({{0,e}},1,all),e);
            for(auto f:ordinary_second) {
                ++ordinary_pairs;Context os{{0,e},{1,f}};
                if(pattern=="triangle") {
                    auto third=ordered_after(domain(os,2,all),f);
                    for(auto g:third) {
                        ++ordinary_triples;Context ordinary=os;ordinary.push_back({2,g});
                        auto ends=domain(ordinary,3,not_ten);record('T',ordinary,ends);
                        domain_sum+=ends.size();max_domain=std::max(max_domain,unsigned(ends.size()));
                        if(ends.size()<3)continue;
                        ++qualifying;
                        for(unsigned i=0;i<ends.size();++i)for(unsigned j=i+1;j<ends.size();++j)for(unsigned k=j+1;k<ends.size();++k){
                            Context ctx=ordinary;ctx.push_back({3,ends[i]});ctx.push_back({4,ends[j]});ctx.push_back({5,ends[k]});++case_checks;
                            Book b=book(ctx);if(b.color<0){++full;record('W',ctx,{});}else{trace<<"B";for(auto v:ctx)trace<<' '<<rows[v[1]].n;trace<<' '<<b.color<<' '<<b.i<<' '<<b.j;for(auto p:b.pages)trace<<' '<<p;trace<<'\n';}
                        }
                    }
                } else {
                    auto first=domain(os,2,pattern=="star"?not_ten:all);
                    auto second=domain(os,3,pattern=="p4"?not_ten:all);
                    domain_sum+=first.size();second_sum+=second.size();max_domain=std::max(max_domain,unsigned(first.size()));max_second=std::max(max_second,unsigned(second.size()));
                    record('A',os,first);record('D',os,second);
                    if(pattern=="star" && second.size()<3)continue;
                    if(pattern=="star" && !first.empty())++qualifying;
                    for(auto a:first) {
                        Context c3=os;c3.push_back({2,a});
                        auto dom3=domain(c3,3,second);++prefix3;
                        record('E',c3,dom3);
                        if(pattern=="star" && dom3.size()<3)continue;
                        for(auto b:dom3) {
                            Context c4=c3;c4.push_back({3,b});
                            auto dom4=domain(c4,4,pattern=="star"?ordered_after(dom3,b):second);++prefix4;
                            record('F',c4,dom4);
                            for(auto c:dom4) {
                                Context c5=c4;c5.push_back({4,c});
                                auto dom5=domain(c5,5,pattern=="star"?ordered_after(dom4,c):ordered_after(first,a));++prefix5;
                                record('G',c5,dom5);
                                for(auto d:dom5){Context c6=c5;c6.push_back({5,d});if(book(c6).color>=0)throw std::runtime_error("domain/full-book mismatch");++full;record('W',c6,{});}
                            }
                        }
                    }
                }
            }
        }
    } else if(pattern=="p3k2") {
        for(unsigned e=0;e<rows.size();++e) {
            Context os{{0,e}};
            auto leaves=domain(os,2,all);domain_sum+=leaves.size();max_domain=std::max(max_domain,unsigned(leaves.size()));
            for(auto a:leaves) {
                Context c2=os;c2.push_back({2,a});
                auto seconds=ordered_after(domain(c2,3,leaves),a);++prefix3;second_sum+=seconds.size();
                for(auto b:seconds) {
                    Context c3=c2;c3.push_back({3,b});
                    auto centers=domain(c3,1,not_ten);record('F',c3,centers);++prefix4;
                    for(auto c:centers) {
                        Context c4=c3;c4.push_back({1,c});
                        auto endpoints=domain(c4,4,all);++prefix5;
                        for(auto d:endpoints) {
                            Context c5=c4;c5.push_back({4,d});
                            auto partners=ordered_after(domain(c5,5,endpoints),d);++case_checks;
                            for(auto f:partners){Context c6=c5;c6.push_back({5,f});if(book(c6).color>=0)throw std::runtime_error("domain/full-book mismatch");++full;record('W',c6,{});}
                        }
                    }
                }
            }
        }
    } else if(pattern=="3k2") {
        for(unsigned e=0;e<rows.size();++e) {
            Context one{{0,e}};
            auto partners=ordered_after(domain(one,1,all),e);domain_sum+=partners.size();max_domain=std::max(max_domain,unsigned(partners.size()));
            for(auto f:partners) {
                Context c2=one;c2.push_back({1,f});
                auto seconds=ordered_after(domain(c2,2,all),e);++prefix3;second_sum+=seconds.size();
                for(auto a:seconds) {
                    Context c3=c2;c3.push_back({2,a});
                    auto thirds=ordered_after(domain(c3,3,seconds),a);record('F',c3,thirds);++prefix4;
                    for(auto b:thirds) {
                        Context c4=c3;c4.push_back({3,b});
                        auto last=ordered_after(domain(c4,4,seconds),a);++prefix5;
                        for(auto c:last) {
                            Context c5=c4;c5.push_back({4,c});
                            auto finals=ordered_after(domain(c5,5,last),c);++case_checks;
                            for(auto d:finals){Context c6=c5;c6.push_back({5,d});if(book(c6).color>=0)throw std::runtime_error("domain/full-book mismatch");++full;record('W',c6,{});}
                        }
                    }
                }
            }
        }
    } else throw std::runtime_error("pattern search not implemented");
    trace.close();if(!trace)throw std::runtime_error("trace write failed");
    std::cout<<"{\"complete\":true,\"pattern\":\""<<pattern<<"\",\"rows\":"<<rows.size()<<",\"ordinary_pairs\":"<<ordinary_pairs<<",\"ordinary_triples\":"<<ordinary_triples<<",\"first_domain_sum\":"<<domain_sum<<",\"second_domain_sum\":"<<second_sum<<",\"max_first_domain\":"<<max_domain<<",\"max_second_domain\":"<<max_second<<",\"qualifying_contexts\":"<<qualifying<<",\"prefix3_domains\":"<<prefix3<<",\"prefix4_domains\":"<<prefix4<<",\"prefix5_domains\":"<<prefix5<<",\"case_checks\":"<<case_checks<<",\"full_valid\":"<<full<<"}\n";
    return 0;
} catch(std::exception const&e){std::cerr<<e.what()<<'\n';return 2;}
