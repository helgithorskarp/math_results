#include <algorithm>
#include <array>
#include <bitset>
#include <cstdint>
#include <iostream>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

using T = std::bitset<180>;
using X = std::bitset<720>;
using Y = std::bitset<144>;
using Group = std::vector<int>;
const std::vector<Group> pairs = {{10,18},{12,15},{16,20},{24,30},{36,40},{45,48},{60,72}};
const Group core = {10,12,15,16,18,20};
const std::array<std::array<int,3>,5> patterns = {{{0,0,0},{0,0,1},{0,1,0},{0,1,1},{0,1,2}}};
const std::array<int,5> multiplicities = {5,20,20,20,60};

void need(bool ok, const std::string& message) {
    if (!ok) throw std::runtime_error(message);
}
bool inS(int t) { return t%9!=6; }
bool inR0(int x) { return x%8!=5 && x%9!=6 && x%18!=3; }
T shape(int id) {
    T result;
    for (int t=0;t<180;++t)
        if (inS(t) && (id==4 ? t%3!=0 : (t%2==id/2 || t%3==id%2+1))) result.set(t);
    return result;
}
std::string hex(const T& mask) {
    std::string result;
    for (int block=44;block>=0;--block) {
        int value=0;
        for (int bit=0;bit<4;++bit) value+=static_cast<int>(mask.test(4*block+bit))<<bit;
        result.push_back("0123456789abcdef"[value]);
    }
    return result;
}
int normalized_phase(int a, int d) {
    const int g=std::gcd(d,4), e=d/g;
    need(a%g==0,"nonproductive raw phase decoded");
    for (int r=0;r<e;++r) if (4*r%d==a) return r;
    throw std::runtime_error("raw ORIGINAL phase lacks normalized phase");
}

// A genuinely different core audit: modulo144 geometry and canonical
// partitions of THREE labeled modulo5 fibers, rather than raw720 unions.
int core_maximum(bool controls) {
    Y base;
    for (int y=0;y<144;++y)
        if (inR0(y) && !(y%4==0 && y%3!=0)) base.set(y);
    need(base.count()==82,"modulo144 compulsory fiber size");
    for (int x=0;x<720;++x)
        need(base.test(x%144)==(inR0(x) && !(x%4==0 && x%3!=0)),"physical5-fiber decomposition");
    std::array<std::vector<Y>,19> phase;
    for (int m : {12,16,18}) {
        phase[m].resize(m);
        for (int a=0;a<m;++a)
            for (int y=0;y<144;++y)
                if (base.test(y) && y%m==a) phase[m][a].set(y);
    }
    struct Profile { std::array<Y,3> masks; int multiplicity; };
    std::vector<Profile> profiles;
    for (std::size_t k=0;k<patterns.size();++k)
        for (int r2=0;r2<2;++r2) for (int r3=0;r3<3;++r3) for (int r4=0;r4<4;++r4) {
            Profile record{};
            record.multiplicity=multiplicities[k];
            const std::array<int,3> residues={r2,r3,r4};
            const std::array<int,3> moduli={2,3,4};
            for (int i=0;i<3;++i) for (int y=0;y<144;++y)
                if (base.test(y) && y%moduli[i]==residues[i]) record.masks[patterns[k][i]].set(y);
            profiles.push_back(record);
        }
    need(profiles.size()==120,"complete left profile domain");
    std::uint64_t raw=0;
    for (const auto& p:profiles) raw+=static_cast<std::uint64_t>(p.multiplicity)*12U*16U*18U;
    need(raw==10368000,"profile orbit weights do not cover full ORIGINAL phase product");
    if (controls) {
        std::array<int,120> occurrences{};
        std::uint64_t points=0;
        for (int a=0;a<10;++a) for (int b=0;b<15;++b) for (int c=0;c<20;++c) {
            const std::array<int,3> fibers={a%5,b%5,c%5};
            std::array<int,3> canon{};
            std::vector<int> labels;
            for (int i=0;i<3;++i) {
                auto at=std::find(labels.begin(),labels.end(),fibers[i]);
                if (at==labels.end()) { labels.push_back(fibers[i]); at=labels.end()-1; }
                canon[i]=static_cast<int>(at-labels.begin());
            }
            auto found=std::find(patterns.begin(),patterns.end(),canon);
            need(found!=patterns.end(),"uncatalogued5-fiber partition");
            const int index=static_cast<int>(found-patterns.begin())*24+(a%2)*12+(b%3)*4+c%4;
            ++occurrences[index];
            for (int x=0;x<720;++x) {
                const bool reduced=(x%5==a%5 && x%2==a%2) || (x%5==b%5 && x%3==b%3) ||
                                   (x%5==c%5 && x%4==c%4);
                need(reduced==(x%10==a || x%15==b || x%20==c),"literal ORIGINAL10/15/20 CRT incidence");
                ++points;
            }
        }
        for (std::size_t i=0;i<profiles.size();++i)
            need(occurrences[i]==profiles[i].multiplicity,"wrong canonical orbit multiplicity");
        std::uint64_t right_points=0;
        for (int a=0;a<12;++a) for (int b=0;b<16;++b) for (int c=0;c<18;++c) {
            const auto covered=phase[12][a]|phase[16][b]|phase[18][c];
            for (int y=0;y<144;++y) {
                need(covered.test(y)==(base.test(y) && (y%12==a || y%16==b || y%18==c)),
                     "literal ORIGINAL12/16/18 fiber union");
                ++right_points;
            }
        }
        std::cout<<"CONTROLS "<<points<<' '<<right_points<<' '<<profiles.size()<<' '<<raw<<'\n';
        return 0;
    }
    int maximum=0;
    std::uint64_t visits=0;
    for (int a=0;a<12;++a) for (int b=0;b<16;++b) for (int c=0;c<18;++c) {
        const auto covered=phase[12][a]|phase[16][b]|phase[18][c];
        const auto remaining=base&~covered;
        for (const auto& p:profiles) {
            int value=5*static_cast<int>(covered.count());
            for (const auto& mask:p.masks) value+=static_cast<int>((mask&remaining).count());
            maximum=std::max(maximum,value);
            ++visits;
        }
    }
    need(visits==414720,"incomplete core profile enumeration");
    return maximum;
}

int main(int argc,char** argv) {
    try {
        if (argc==2 && std::string(argv[1])=="controls") { core_maximum(true); return 0; }
        need(argc==1,"unexpected arguments");
        Group free, first;
        for (int d=2;d<=720;++d) if (720%d==0 && d!=2 && d!=4) free.push_back(d);
        for (int m=8;m<=720;++m) if (720%m==0 && m!=8 && m!=9) first.push_back(m);
        need(free.size()==27 && first.size()==22,"ORIGINAL inventories");
        std::array<std::vector<T>,721> supports;
        std::array<int,721> weights{};
        for (int d:free) {
            supports[d].resize(d);
            for (int a=0;a<d;++a) for (int t=0;t<180;++t)
                if (inS(t) && 4*t%d==a) supports[d][a].set(t);
            for (const auto& mask:supports[d]) weights[d]=std::max(weights[d],static_cast<int>(mask.count()));
            std::cout<<"WEIGHT "<<d<<' '<<weights[d]<<'\n';
        }
        std::uint64_t raw_pairs=0,effective_pairs=0;
        int large=0;
        for (std::size_t i=0;i<free.size();++i) for (std::size_t j=i+1;j<free.size();++j) {
            const int d=free[i],e=free[j];
            if (weights[d]+weights[e]<99) continue;
            std::cout<<"PAIR "<<d<<' '<<e<<'\n';
            raw_pairs+=static_cast<std::uint64_t>(d)*e;
            for (int a=0;a<d;++a) for (int b=0;b<e;++b) {
                if (supports[d][a].any() && supports[e][b].any()) ++effective_pairs;
                const auto U=supports[d][a]|supports[e][b];
                if (U.count()<99) continue;
                int capacity=0;
                for (int f:free) if (f!=d && f!=e) {
                    std::vector<int> counts(f);
                    for (int t=0;t<180;++t) if (U.test(t)) ++counts[4*t%f];
                    capacity+=*std::max_element(counts.begin(),counts.end());
                }
                const int bound=std::min(static_cast<int>(U.count()),capacity/4);
                std::cout<<"TAIL "<<d<<' '<<e<<' '<<normalized_phase(a,d)<<' '<<normalized_phase(b,e)<<' '
                         <<hex(U)<<' '<<U.count()<<' '<<capacity<<' '<<bound<<' '<<(bound>=99)<<'\n';
                ++large;
            }
        }
        std::cout<<"TAILCOUNTS "<<raw_pairs<<' '<<effective_pairs<<' '<<large<<'\n';
        std::vector<Group> singles;
        for (int m:first) {
            bool paired=false;
            for (const auto& g:pairs) if (std::find(g.begin(),g.end(),m)!=g.end()) paired=true;
            if (!paired) singles.push_back({m});
        }
        for (int id=0;id<5;++id) {
            const auto U=shape(id);
            X compulsory;
            for (int x=0;x<720;++x) if (inR0(x) && !(x%4==0 && U.test(x/4))) compulsory.set(x);
            std::array<std::vector<X>,721> phases;
            for (int m:first) {
                phases[m].resize(m);
                for (int a=0;a<m;++a) for (int x=a;x<720;x+=m)
                    if (compulsory.test(x)) phases[m][a].set(x);
            }
            std::vector<Group> groups;
            if (id==4) groups.push_back(core);
            for (const auto& g:pairs)
                if (id<4 || std::find(core.begin(),core.end(),g[0])==core.end()) groups.push_back(g);
            groups.insert(groups.end(),singles.begin(),singles.end());
            Group inventory;
            for (const auto& g:groups) inventory.insert(inventory.end(),g.begin(),g.end());
            std::sort(inventory.begin(),inventory.end());
            need(inventory==first,"disjoint full ORIGINAL first resource partition");
            int total=0;
            for (std::size_t k=0;k<groups.size();++k) {
                const auto& g=groups[k];
                int cap=0;
                std::uint64_t tuples=1;
                for (int m:g) tuples*=m;
                if (g.size()==6) cap=core_maximum(false);
                else if (g.size()==2) for (const auto& a:phases[g[0]]) for (const auto& b:phases[g[1]])
                    cap=std::max(cap,static_cast<int>((a|b).count()));
                else for (const auto& a:phases[g[0]]) cap=std::max(cap,static_cast<int>(a.count()));
                std::cout<<"CAP "<<id<<' '<<k<<' '<<g.size();
                for (int m:g) std::cout<<' '<<m;
                std::cout<<' '<<tuples<<' '<<cap<<'\n';
                total+=cap;
            }
            need(total<static_cast<int>(compulsory.count()),"first complement not excluded");
            std::cout<<"FIRST "<<id<<' '<<hex(U)<<' '<<U.count()<<' '<<compulsory.count()<<' '<<total<<'\n';
        }
        return 0;
    } catch (const std::exception& e) { std::cerr<<e.what()<<'\n'; return 1; }
}
