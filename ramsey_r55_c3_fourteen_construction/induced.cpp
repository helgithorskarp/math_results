// Complete induced-subgraph search for the fixed candidate comparison.
// Status 0=exhausted, 1=witness, 2=node cap (never an exclusion).
#include <array>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
using Bits = std::uint64_t;
void need(bool ok, const char* why) { if (!ok) throw std::runtime_error(why); }
struct Search {
    int n=0,m=0;
    std::array<Bits,63> host{},pattern{};
    std::array<int,63> mapping{};
    std::uint64_t nodes=0,limit=0;
    int dfs(Bits remaining, const std::array<Bits,63>& domains) {
        if (++nodes>limit) return 2;
        if (!remaining) return 1;
        int chosen=-1,smallest=64;
        for(int u=0;u<m;++u) if(remaining & (Bits{1}<<u)) {
            int size=std::popcount(domains[u]);
            if(!size) return 0;
            if(size<smallest) {smallest=size;chosen=u;}
        }
        need(chosen>=0,"unassigned vertex");
        Bits candidates=domains[chosen], rest=remaining ^ (Bits{1}<<chosen);
        while(candidates) {
            int v=std::countr_zero(candidates);
            Bits bit=Bits{1}<<v;candidates^=bit;
            auto next=domains;bool possible=true;
            for(int u=0;u<m;++u) if(rest & (Bits{1}<<u)) {
                next[u] &= (pattern[chosen] & (Bits{1}<<u)) ? host[v] : ~host[v];
                next[u] &= ~bit;
                if(!next[u]) {possible=false;break;}
            }
            if(!possible) continue;
            mapping[chosen]=v;
            int status=dfs(rest,next);
            if(status) return status;
        }
        return 0;
    }
    int run() {
        std::array<Bits,63> domains{};
        for(int u=0;u<m;++u) {
            int degree=std::popcount(pattern[u]);
            for(int v=0;v<n;++v) {
                int hd=std::popcount(host[v]);
                if(hd>=degree && n-1-hd>=m-1-degree) domains[u]|=Bits{1}<<v;
            }
        }
        return dfs((Bits{1}<<m)-1,domains);
    }
};
void graph(std::istream& in,std::array<Bits,63>& rows,int n) {
    for(int u=0;u<n;++u) {
        need(static_cast<bool>(in>>rows[u]),"graph rows");
        need(!(rows[u]>>n) && !(rows[u] & (Bits{1}<<u)),"graph range/loop");
    }
    for(int u=0;u<n;++u)for(int v=0;v<n;++v)
        need(((rows[u]>>v)&1)==((rows[v]>>u)&1),"asymmetric graph");
}
int main(int argc,char** argv) {
    try {
        need(argc==4,"usage: induced CASES OUTPUT NODE_LIMIT");
        std::ifstream in(argv[1]);std::ofstream out(argv[2]);
        need(static_cast<bool>(in)&&static_cast<bool>(out),"input/output");
        auto cap=std::stoull(argv[3]);need(cap>0,"positive node cap");
        int id=0;
        while(in>>id) {
            Search s;s.limit=cap;
            need(static_cast<bool>(in>>s.n>>s.m),"case header");
            need(1<=s.m && s.m<=s.n && s.n<=63,"case order");
            graph(in,s.host,s.n);graph(in,s.pattern,s.m);
            int status=s.run();
            out<<id<<' '<<status<<' '<<s.nodes;
            if(status==1)for(int u=0;u<s.m;++u)out<<' '<<s.mapping[u];
            out<<'\n';out.flush();need(static_cast<bool>(out),"output write");
        }
        need(in.eof(),"input parse");
    } catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 1;}
}
