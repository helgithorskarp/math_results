#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

using U = std::uint64_t;
using Wide = unsigned __int128;
void require(bool c, const char* m) { if (!c) throw std::runtime_error(m); }
int count(U x) { return __builtin_popcountll(x); }
int first(U x) { require(x != 0, "zero bit scan"); return __builtin_ctzll(x); }
std::string decimal(Wide x) {
    std::string s;
    do { s.push_back(char('0' + x % 10)); x /= 10; } while (x);
    std::reverse(s.begin(), s.end()); return s;
}
bool downset(U f, int n) {
    for (int a = 0; a < (1 << n); ++a) if ((f >> a) & 1)
        for (int i = 0; i < n; ++i) if ((a >> i) & 1)
            if (!((f >> (a ^ (1 << i))) & 1)) return false;
    return true;
}
std::vector<U> labelled(int n) {
    std::vector<U> old{0,1};
    for (int k = 1; k <= n; ++k) {
        std::vector<U> next;
        for (U l : old) for (U u : old) if ((u & ~l) == 0)
            next.push_back(l | (u << (1 << (k-1))));
        old.swap(next);
    }
    std::sort(old.begin(), old.end());
    require(std::adjacent_find(old.begin(),old.end()) == old.end(), "duplicate labeled family");
    return old;
}
struct Permutation {
    std::array<std::array<U,256>,8> table{};
    int chunks;
    Permutation(const std::vector<int>& p) : chunks(((1 << p.size())+7)/8) {
        std::array<int,64> image{};
        for (int a=0; a < (1 << p.size()); ++a)
            for (std::size_t i=0; i<p.size(); ++i)
                if ((a >> i) & 1) image[a] |= 1 << p[i];
        for (int b=0; b<chunks; ++b) for (int v=1; v<256; ++v) {
            int t=__builtin_ctz(unsigned(v));
            table[b][v] = table[b][v & (v-1)];
            if (b*8+t < (1 << p.size())) table[b][v] |= U(1) << image[b*8+t];
        }
    }
    U operator()(U f) const {
        U g=0;
        for (int b=0;b<chunks;++b) g |= table[b][(f >> (8*b)) & 255];
        return g;
    }
};
std::vector<Permutation> transformations(int n) {
    std::vector<int> p(n); std::iota(p.begin(),p.end(),0);
    std::vector<Permutation> result;
    do { result.emplace_back(p); } while (std::next_permutation(p.begin(),p.end()));
    return result;
}
struct Coloring {
    std::vector<int> sets, colors;
    std::vector<U> neighbors;
    int s=0;
    std::uint64_t nodes=0;
    explicit Coloring(U f,int n) {
        for (int a=1; a<(1 << n); ++a) if ((f >> a)&1) sets.push_back(a);
        colors.assign(sets.size(),-1); neighbors.resize(sets.size());
        for (std::size_t i=0;i<sets.size();++i) for (std::size_t j=0;j<sets.size();++j)
            if (i!=j && (sets[i]&sets[j])) neighbors[i] |= U(1)<<j;
        int root=0;
        for (int a=0;a<n;++a) {
            int size=0; for (int x:sets) size += (x>>a)&1;
            if (size>s) { s=size;root=a; }
        }
        int c=0;
        for (std::size_t i=0;i<sets.size();++i) if ((sets[i]>>root)&1) colors[i]=c++;
    }
    bool search(U remaining) {
        if (++nodes>2000000) throw std::runtime_error("INCOMPLETE: coloring node limit");
        if (!remaining) return true;
        int selected=-1,saturation=-1,degree=-1;U banned=0;
        for (U todo=remaining;todo;todo&=todo-1) {
            int i=first(todo);U used=0;
            for (U adj=neighbors[i];adj;adj&=adj-1) {
                int j=first(adj); if (colors[j]>=0) used |= U(1)<<colors[j];
            }
            int sat=count(used),deg=count(neighbors[i]);
            if (sat>saturation || (sat==saturation && deg>degree)) {
                selected=i;saturation=sat;degree=deg;banned=used;
            }
        }
        if (saturation==s) return false;
        for (int c=0;c<s;++c) if (!((banned>>c)&1)) {
            colors[selected]=c;
            if (search(remaining & ~(U(1)<<selected))) return true;
        }
        colors[selected]=-1;return false;
    }
    std::vector<U> partition() {
        U todo=0;
        for (std::size_t i=0;i<sets.size();++i) if (colors[i]<0) todo |= U(1)<<i;
        require(search(todo),"unhandled coloring failure; no theorem is concluded");
        std::vector<U> bins(s);
        for (std::size_t i=0;i<sets.size();++i) {
            require(colors[i]>=0 && colors[i]<s,"bad color");
            bins[colors[i]] |= U(1)<<sets[i];
        }
        return bins;
    }
};
void check_partition(U f,const std::vector<U>& bins,int n,int s) {
    require(downset(f,n),"certificate family not downward closed");
    require(int(bins.size())==s,"wrong number of bins");
    U included=0;
    for (U bin:bins) {
        require(bin!=0 && (bin&1)==0 && (included&bin)==0,"invalid or repeated bin member");
        unsigned used=0;
        for (U row=bin;row;row&=row-1) {
            unsigned a=unsigned(first(row));require((used&a)==0,"intersecting bin members");used|=a;
        }
        included |= bin;
    }
    require(included==(f & ~U(1)),"partition coverage mismatch");
}
void map_json(const std::map<int,std::uint64_t>& m) {
    bool first_item=true;std::cout<<'{';
    for (auto [k,v]:m) { if (!first_item)std::cout<<','; first_item=false;std::cout<<'"'<<k<<"\":"<<v; }
    std::cout<<'}';
}
int main(int argc,char**argv) try {
    require(argc>=2 && argc<=4,"usage: audit n [private-witness-file] [private-map-file]");
    int n=std::stoi(argv[1]);require(n>=0 && n<=6,"supported ground size is 0..6");
    auto all=labelled(n);auto perms=transformations(n);
    std::vector<unsigned char> seen(all.size(),0);
    std::ofstream witnesses;
    if (argc>=3) { witnesses.open(argv[2]);require(bool(witnesses),"cannot open witness file"); }
    if (argc==4) {
        std::ofstream maps(argv[3],std::ios::binary);require(bool(maps),"cannot open map file");
        for (const auto& p:perms) for (int a=0;a<(1<<n);++a) {
            U image=p(U(1)<<a);require(count(image)==1,"basis image is not a basis vector");
            maps.put(char(first(image)));
        }
        maps.flush();require(bool(maps),"permutation map write failed");
    }
    U exceptional=1991589575991295ULL;
    if (n==6) for (const auto& p:perms) exceptional=std::min(exceptional,p(1991589575991295ULL));
    Wide mask_sum=0;std::map<int,std::uint64_t> sizes,orbit_sizes;
    for (U f:all) { require(downset(f,n),"enumeration is not a downset");mask_sum+=f;++sizes[count(f)]; }
    std::uint64_t classes=0,partitions=0,trivial=0,exceptions=0,max_nodes=0;
    for (std::size_t index=0;index<all.size();++index) if (!seen[index]) {
        U f=all[index];std::vector<U> orbit;orbit.reserve(perms.size());
        for (const auto& p:perms) orbit.push_back(p(f));
        std::sort(orbit.begin(),orbit.end());orbit.erase(std::unique(orbit.begin(),orbit.end()),orbit.end());
        require(orbit.front()==f,"full permutation canonical representative differs");
        for (U image:orbit) {
            auto at=std::lower_bound(all.begin(),all.end(),image);
            require(at!=all.end() && *at==image,"orbit contains an unenumerated family");
            std::size_t j=at-all.begin();require(!seen[j],"overlapping orbits");seen[j]=1;
        }
        ++classes;++orbit_sizes[int(orbit.size())];
        if (f<=1) { ++trivial;if(witnesses.is_open())witnesses<<f<<' '<<orbit.size()<<" 0 0\n";continue; }
        Coloring coloring(f,n);
        if (n==6 && f==exceptional) { ++exceptions;require(orbit.size()==12 && coloring.s==11,"exception parameters");if(witnesses.is_open())witnesses<<f<<" 12 11 -1\n";continue; }
        auto bins=coloring.partition();check_partition(f,bins,n,coloring.s);
        ++partitions;max_nodes=std::max(max_nodes,coloring.nodes);
        if(witnesses.is_open()) { witnesses<<f<<' '<<orbit.size()<<' '<<coloring.s<<' '<<coloring.nodes;for(U bin:bins)witnesses<<' '<<bin;witnesses<<'\n'; }
    }
    require(std::all_of(seen.begin(),seen.end(),[](unsigned char x){return x==1;}),"incomplete orbit coverage");
    if (witnesses.is_open()) { witnesses.flush();require(bool(witnesses),"witness write failed"); }
    std::cout<<"{\"reviewer\":\"six-reviewer-5\",\"n\":"<<n<<",\"labeled\":"<<all.size()<<",\"classes\":"<<classes
             <<",\"partition_certified\":"<<partitions<<",\"trivial\":"<<trivial<<",\"exception_classes\":"<<exceptions
             <<",\"exception_canonical_mask\":"<<(n==6?exceptional:0)<<",\"max_coloring_nodes\":"<<max_nodes
             <<",\"labeled_mask_sum\":\""<<decimal(mask_sum)<<"\",\"labeled_size_histogram\":";
    map_json(sizes);std::cout<<",\"orbit_size_histogram\":";map_json(orbit_sizes);std::cout<<"}\n";
    return 0;
} catch (const std::exception& e) { std::cerr<<e.what()<<'\n';return 1; }
