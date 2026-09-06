// Direct full-boundary DFS; no component decomposition or path-kernel code.
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <vector>

std::array<int,16> group,colour;
std::array<std::vector<int>,16> previous;
std::array<std::uint64_t,4096> count{};
std::uint64_t nodes=0;

void visit(int v) {
    ++nodes;
    if(v==16) {
        int blocked=0;
        for(int i=1;i<16;++i) if(colour[i])
            blocked |= 1 << (3*group[i]+colour[i]-1);
        ++count[4095 ^ blocked];
        return;
    }
    for(int c=0;c<4;++c) {
        bool ok=true;
        for(int u:previous[v]) if(colour[u]==c) {ok=false;break;}
        if(ok) {colour[v]=c;visit(v+1);}
    }
}

int main() {
    int n,m,origin;
    if(!(std::cin>>n>>m>>origin) || n!=16 || m!=13 || origin!=0)
        throw std::runtime_error("wrong boundary header");
    for(int i=0;i<16;++i) {
        int label;std::cin>>label>>group[i];
        if((i==0 && (label!=0 || group[i]!=-1)) || (i>0 && (group[i]<0 || group[i]>3)))
            throw std::runtime_error("wrong vertex group");
    }
    for(int k=0;k<m;++k) {
        int u,v;std::cin>>u>>v;
        if(u<0 || u>=v || v>=16 || u==0) throw std::runtime_error("wrong edge");
        previous[v].push_back(u);
    }
    if(!std::cin) throw std::runtime_error("truncated input");
    colour[0]=0;visit(1);
    std::uint64_t total=0;
    for(auto x:count) {std::cout<<x<<'\n';total+=x;}
    std::cerr<<"nodes "<<nodes<<" proper_colourings "<<total<<'\n';
}
