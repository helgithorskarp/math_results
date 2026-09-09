// Independent exhaustive CSP: seven labelled columns, literal B3/B2 tests.
#include <algorithm>
#include <array>
#include <bit>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>
void check(bool ok,const char* m){if(!ok)throw std::runtime_error(m);}
using Graph=std::array<std::array<int,7>,7>;
Graph read_graph(const std::string& line){
    check(line.size()==5 && line.front()=='F',"graph6 length/order");
    std::vector<int> bits;
    for(std::size_t i=1;i<line.size();++i){int v=static_cast<unsigned char>(line[i])-63;check(0<=v && v<64,"graph6 character");for(int b=5;b>=0;--b)bits.push_back((v>>b)&1);}
    check(bits[21]==0 && bits[22]==0 && bits[23]==0,"padding");
    Graph g{};int pos=0;
    for(int v=1;v<7;++v)for(int u=0;u<v;++u)g[u][v]=g[v][u]=bits[pos++];
    for(int subset=0;subset<128;++subset)if(std::popcount(static_cast<unsigned>(subset))==4){
        int colors=0;for(int v=0;v<7;++v)for(int u=0;u<v;++u)if((subset&(1<<u)) && (subset&(1<<v)))colors|=1<<g[u][v];
        check(colors==3,"not R44");
    }
    return g;
}
struct Search {
    Graph g;std::array<int,7> order{},values{};
    std::array<std::vector<int>,7> prior_edges;
    std::array<std::vector<std::pair<int,int>>,7> prior_triangles;
    std::array<unsigned,16> edge_allowed{},triangle_allowed{};
    std::array<std::array<bool,16>,16> bad{};
    std::array<std::array<unsigned,16>,16> bad_last{};
    std::array<std::pair<int,int>,2> matching{};
    std::uint64_t plain=0,joint=0,nodes=0;
    explicit Search(Graph input):g(input){
        for(int i=0;i<7;++i)order[i]=i;
        auto degree=[&](int u){int d=0;for(int v=0;v<7;++v)d+=g[u][v];return d;};
        std::stable_sort(order.begin(),order.end(),[&](int u,int v){return degree(u)>degree(v);});
        for(int k=0;k<7;++k){int v=order[k];for(int i=0;i<k;++i)if(g[v][order[i]]){
            prior_edges[k].push_back(order[i]);
            for(int j=i+1;j<k;++j)if(g[v][order[j]] && g[order[i]][order[j]])prior_triangles[k].emplace_back(order[i],order[j]);
        }}
        // Build admissibility masks by checking all literal subsets of block rows.
        for(int p=0;p<16;++p)for(int t=0;t<15;++t){
            bool e=true,tr=true;
            for(int s=0;s<16;++s)if((s&p)==s && (s&t)==s){
                if(std::popcount(static_cast<unsigned>(s))==3)e=false;
                if(std::popcount(static_cast<unsigned>(s))==2)tr=false;
            }
            if(e)edge_allowed[p]|=1u<<t;
            if(tr)triangle_allowed[p]|=1u<<t;
        }
        for(int e=0;e<16;++e)for(int f=0;f<16;++f){
            for(int s=0;s<16;++s)if(std::popcount(static_cast<unsigned>(s))==2 && (s&e)==s && (((15^s)&f)==(15^s)))bad[e][f]=true;
        }
        for(int partner=0;partner<16;++partner)for(int complete=0;complete<16;++complete)
            for(int t=0;t<15;++t)if(bad[partner&t][complete])bad_last[partner][complete]|=1u<<t;
        unsigned used=0;int found=0;
        for(int u=0;u<7;++u)for(int v=u+1;v<7;++v)if(g[u][v] && !(used&(1u<<u)) && !(used&(1u<<v))){
            used|=(1u<<u)|(1u<<v);if(found<2)matching[found]={u,v};++found;
        }
        check(found>=2,"matching");
    }
    unsigned allowed(int depth) const {
        unsigned a=(1u<<15)-1;
        for(int u:prior_edges[depth])a&=edge_allowed[values[u]];
        for(auto [u,v]:prior_triangles[depth])a&=triangle_allowed[values[u]&values[v]];
        return a;
    }
    void visit(int depth){
        ++nodes;unsigned a=allowed(depth);int v=order[depth];
        if(depth==6){
            plain+=std::popcount(a);auto [e0,e1]=matching[0];auto [f0,f1]=matching[1];unsigned forbidden=0;
            if(v==e0 || v==e1)forbidden=bad_last[values[v==e0?e1:e0]][values[f0]&values[f1]];
            else if(v==f0 || v==f1)forbidden=bad_last[values[v==f0?f1:f0]][values[e0]&values[e1]];
            else if(bad[values[e0]&values[e1]][values[f0]&values[f1]])forbidden=(1u<<15)-1;
            joint+=std::popcount(a&~forbidden);return;
        }
        while(a){int t=std::countr_zero(a);a&=a-1;values[v]=t;visit(depth+1);}
    }
};
int main(int argc,char** argv){try{
    check(argc==3 || argc==4,"usage: column_check catalogue.g6 output.tsv [limit]");
    std::ifstream in(argv[1]);check(static_cast<bool>(in),"input open");std::vector<Graph> graphs;std::string line;
    while(std::getline(in,line))graphs.push_back(read_graph(line));
    check(graphs.size()==362,"catalogue size");
    unsigned limit=argc==4 ? static_cast<unsigned>(std::stoul(argv[3])) : 362;check(limit>0 && limit<=362,"limit");
    std::ofstream out(argv[2]);check(static_cast<bool>(out),"output open");std::uint64_t nodes=0;
    auto start=std::chrono::steady_clock::now();
    for(unsigned i=0;i<limit;++i){Search s(graphs[i]);s.visit(0);nodes+=s.nodes;check(s.joint<=s.plain && s.plain<=170859375,"count bounds");out<<i<<'\t'<<s.plain<<'\t'<<s.joint<<'\n';}
    check(static_cast<bool>(out),"output write");
    std::cout<<"{\"method\":\"labelled_columns\",\"complete\":"<<(limit==362?"true":"false")<<",\"records\":"<<limit<<",\"nodes\":"<<nodes<<",\"seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<"}\n";
    return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}}
