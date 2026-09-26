// Matching certificates for partial affine line-free constructions.
// All masks have25 bits; counts and complete-domain counters fit in uint64_t.
#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

using U=std::uint32_t;
constexpr U ALL=(1U<<25)-1;
using Rows=std::array<U,25>;
struct Edge { int left,right; };
using Groups=std::array<std::vector<Edge>,25>;

int plus(int a,int b,int t) {
    return 5*((a/5+t*(b/5))%5)+(a%5+t*(b%5))%5;
}

Groups prepare(U small,U a) {
    Groups groups;
    for(int u=0;u<25;++u)if((small>>u)&1U)
    for(int v=0;v<25;++v)if((a>>plus(u,v,1))&1U)
        groups[static_cast<std::size_t>(plus(u,v,4))].push_back({plus(u,v,2),plus(u,v,3)});
    return groups;
}

Rows graph(const Groups&groups,U b) {
    Rows rows{};
    while(b) {
        const int i=std::countr_zero(b);b&=b-1;
        for(const auto&e:groups[static_cast<std::size_t>(i)])
            rows[static_cast<std::size_t>(e.left)]|=1U<<e.right;
    }
    return rows;
}

struct Match {
    const Rows&rows;
    std::array<int,25> right{};
    int size=0;
    explicit Match(const Rows&r):rows(r) {right.fill(-1);}
    bool augment(int left,U&seen) {
        U options=rows[static_cast<std::size_t>(left)]&~seen;
        while(options) {
            int j=std::countr_zero(options);options&=options-1;
            if((seen>>j)&1U)continue;
            seen|=1U<<j;
            if(right[static_cast<std::size_t>(j)]<0 || augment(right[static_cast<std::size_t>(j)],seen)) {
                right[static_cast<std::size_t>(j)]=left;return true;
            }
        }
        return false;
    }
    void solve(int stop=19) {
        U used=0,matched_left=0;
        for(int i=0;i<25;++i) {
            U choices=rows[static_cast<std::size_t>(i)]&~used;
            if(choices) {
                int j=std::countr_zero(choices);
                right[static_cast<std::size_t>(j)]=i;
                used|=1U<<j;matched_left|=1U<<i;
                if(++size==stop)return;
            }
        }
        for(int i=0;i<25;++i)if(!((matched_left>>i)&1U)) {
            U seen=0;
            if(augment(i,seen) && ++size==stop)return;
        }
    }
};

bool balanced18(const Rows&rows,const Match&m) {
    if(m.size!=18)throw std::runtime_error("balanced18 matching size");
    std::array<int,25> left_id{},right_id{};
    left_id.fill(-1);right_id.fill(-1);
    int n=0;
    for(int j=0;j<25;++j)if(m.right[static_cast<std::size_t>(j)]>=0) {
        right_id[static_cast<std::size_t>(j)]=n;
        left_id[static_cast<std::size_t>(m.right[static_cast<std::size_t>(j)])]=n++;
    }
    if(n!=18)throw std::runtime_error("matching cardinality");
    std::array<U,18> imply{},reverse{};
    for(int i=0;i<18;++i)imply[static_cast<std::size_t>(i)]=1U<<i;
    U on=0,off=0;
    for(int i=0;i<25;++i) {
        U row=rows[static_cast<std::size_t>(i)];
        while(row) {
            int j=std::countr_zero(row);row&=row-1;
            int a=left_id[static_cast<std::size_t>(i)],b=right_id[static_cast<std::size_t>(j)];
            if(a<0 && b<0)throw std::runtime_error("nonmaximum matching");
            if(a<0)off|=1U<<b;
            else if(b<0)on|=1U<<a;
            else imply[static_cast<std::size_t>(b)]|=1U<<a;
        }
    }
    for(int k=0;k<18;++k)for(int i=0;i<18;++i)
        if((imply[static_cast<std::size_t>(i)]>>k)&1U)
            imply[static_cast<std::size_t>(i)]|=imply[static_cast<std::size_t>(k)];
    for(int j=0;j<18;++j)for(int i=0;i<18;++i)
        if((imply[static_cast<std::size_t>(i)]>>j)&1U)
            reverse[static_cast<std::size_t>(j)]|=1U<<i;
    for(int i=0;i<18;++i) {
        if((on>>i)&1U)on|=imply[static_cast<std::size_t>(i)];
        if((off>>i)&1U)off|=reverse[static_cast<std::size_t>(i)];
    }
    auto search=[&](auto&&self,U yes,U no)->bool {
        if((yes&no) || std::popcount(yes)>9 || std::popcount(no)>9)return false;
        U free=((1U<<18)-1)&~(yes|no);
        if(!free)return true;
        auto i=static_cast<std::size_t>(std::countr_zero(free));
        return self(self,yes|imply[i],no) || self(self,yes,no|reverse[i]);
    };
    return search(search,on,off);
}

std::vector<U> read(const std::string&path) {
    std::ifstream input(path);if(!input)throw std::runtime_error("input open failed");
    std::vector<U> words;std::uint64_t w=0;
    while(input>>w) {
        if(w>ALL)throw std::runtime_error("invalid mask");
        words.push_back(static_cast<U>(w));
    }
    if(!input.eof())throw std::runtime_error("input parse failed");
    return words;
}

bool centered(U mask) {
    int y=0,z=0;
    for(int i=0;i<25;++i)if((mask>>i)&1U){y+=i/5;z+=i%5;}
    return y%5==0 && z%5==0;
}

void emit(std::ostream&out,U small,U a,U b,const Rows&rows,const Match&m) {
    out<<"{\"small\":"<<small<<",\"a\":"<<a<<",\"b\":"<<b
       <<",\"matching_size_capped19\":"<<m.size<<",\"rows\":[";
    for(int i=0;i<25;++i){if(i)out<<',';out<<rows[static_cast<std::size_t>(i)];}
    out<<"],\"matching\":[";bool first=true;
    for(int j=0;j<25;++j)if(m.right[static_cast<std::size_t>(j)]>=0) {
        if(!first)out<<',';
        first=false;
        out<<'['<<m.right[static_cast<std::size_t>(j)]<<','<<j<<']';
    }
    out<<"]}\n";
}

int main(int argc,char**argv) {
    if(argc<3)throw std::runtime_error("audit INPUT or scan MENU CAPS CASE START STOP OUTPUT");
    const std::string mode=argv[1];
    if(mode=="audit" || mode=="audit-balanced") {
        if(argc!=3)throw std::runtime_error("audit arguments");
        auto words=read(argv[2]);
        if(words.size()%3)throw std::runtime_error("audit triple format");
        for(std::size_t i=0;i<words.size();i+=3) {
            auto rows=graph(prepare(words[i],words[i+1]),words[i+2]);
            Match m(rows);m.solve();
            if(mode=="audit")emit(std::cout,words[i],words[i+1],words[i+2],rows,m);
            else std::cout<<'['<<words[i]<<','<<words[i+1]<<','<<words[i+2]<<','
                          <<m.size<<','<<(m.size<18 || (m.size==18 && balanced18(rows,m)) ? 1 : 0)<<"]\n";
        }
    } else if(mode=="scan" || mode=="balanced-scan") {
        if(argc!=8)throw std::runtime_error("scan arguments");
        auto menu=read(argv[2]),caps=read(argv[3]);
        const auto which=std::stoul(argv[4]),start=std::stoul(argv[5]),stop=std::stoul(argv[6]);
        std::vector<U> centers;
        if(menu.size()!=28375)throw std::runtime_error("menu cardinality");
        for(U m:menu) {
            if(std::popcount(m)!=16)throw std::runtime_error("menu weight");
            if(centered(m))centers.push_back(m);
        }
        if(centers.size()!=1135 || which>=caps.size() || start>=stop || stop>centers.size())
            throw std::runtime_error("scan interval");
        U small=caps[which];
        if(std::popcount(small)!=6 && std::popcount(small)!=7)throw std::runtime_error("cap weight");
        std::ofstream out(argv[7]);if(!out)throw std::runtime_error("output open failed");
        std::array<std::uint64_t,20> hist{};
        auto began=std::chrono::steady_clock::now();
        for(std::size_t ai=start;ai<stop;++ai) {
            auto groups=prepare(small,centers[ai]);
            for(U b:menu) {
                auto rows=graph(groups,b);Match m(rows);m.solve();
                ++hist[static_cast<std::size_t>(m.size)];
                if(m.size<19 && (mode=="scan" || m.size<18 || balanced18(rows,m)))
                    emit(out,small,centers[ai],b,rows,m);
            }
        }
        std::cout<<"{\"cap_index\":"<<which<<",\"small\":"<<small
                 <<",\"start\":"<<start<<",\"stop\":"<<stop<<",\"histogram\":{";
        bool first=true;
        for(int i=0;i<20;++i)if(hist[static_cast<std::size_t>(i)]) {
            if(!first)std::cout<<',';
            first=false;
            std::cout<<'"'<<i<<"\":"<<hist[static_cast<std::size_t>(i)];
        }
        std::cout<<"},\"pairs\":"<<(stop-start)*menu.size()<<",\"seconds\":"
                 <<std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count()<<"}\n";
    } else if(mode=="finish") {
        if(argc!=6)throw std::runtime_error("finish MENU TRIPLES MODELS SUMMARY");
        auto menu=read(argv[2]),triples=read(argv[3]);
        if(menu.size()!=28375 || triples.size()%3)throw std::runtime_error("finish input");
        std::unordered_set<U> contains(menu.begin(),menu.end());
        if(contains.size()!=menu.size())throw std::runtime_error("duplicate planar menu");
        std::vector<std::array<unsigned char,5>> chunks;
        for(U mask:menu) {
            std::array<unsigned char,5> c{};
            for(int j=0;j<5;++j)c[static_cast<std::size_t>(j)]=static_cast<unsigned char>((mask>>(5*j))&31U);
            chunks.push_back(c);
        }
        std::ofstream models(argv[4]);if(!models)throw std::runtime_error("model output");
        std::uint64_t pairs=0,balanced=0,models_count=0,central_passes=0;
        auto began=std::chrono::steady_clock::now();
        for(std::size_t k=0;k<triples.size();k+=3) {
            ++pairs;U small=triples[k],a=triples[k+1],b=triples[k+2];
            auto rows=graph(prepare(small,a),b);Match matching(rows);matching.solve();
            if(matching.size>=19 || (matching.size==18 && !balanced18(rows,matching)))continue;
            ++balanced;
            std::array<std::array<U,32>,5> blocks{};
            for(int j=0;j<5;++j)for(U mask=1;mask<32;++mask) {
                auto z=static_cast<std::size_t>(std::countr_zero(mask));
                blocks[static_cast<std::size_t>(j)][mask]=blocks[static_cast<std::size_t>(j)][mask&(mask-1)]
                    |rows[static_cast<std::size_t>(5*j)+z];
            }
            for(std::size_t ci=0;ci<menu.size();++ci) {
                const auto&c=chunks[ci];
                U neighbors=blocks[0][c[0]]|blocks[1][c[1]];
                if(std::popcount(neighbors)>9)continue;
                neighbors|=blocks[2][c[2]];
                if(std::popcount(neighbors)>9)continue;
                neighbors|=blocks[3][c[3]];
                if(std::popcount(neighbors)>9)continue;
                neighbors|=blocks[4][c[4]];
                int count=std::popcount(neighbors);
                if(count>9)continue;
                ++central_passes;
                auto emit_model=[&](U d) {
                    ++models_count;
                    models<<'['<<small<<','<<a<<','<<menu[ci]<<','<<d<<','<<b<<"]\n";
                };
                if(count==9) {
                    U d=ALL^neighbors;
                    if(contains.contains(d))emit_model(d);
                } else for(U d:menu)if(!(d&neighbors))emit_model(d);
            }
        }
        std::ofstream summary(argv[5]);if(!summary)throw std::runtime_error("summary output");
        summary<<"{\"pairs\":"<<pairs<<",\"balanced_pass\":"<<balanced
               <<",\"candidate_c_sections\":"<<central_passes<<",\"models\":"<<models_count
               <<",\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-began).count()<<"}\n";
    } else throw std::runtime_error("unknown mode");
}
