// Complete queue-based 4-core propagation and explicit colouring restoration.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

void need(bool ok,const char* why) {if(!ok) throw std::runtime_error(why);}
struct Graph {int n;std::vector<std::vector<int>> adj;std::vector<std::pair<int,int>> edges;};
struct Witness {std::vector<int> omitted;std::string colour;};
struct Result {std::vector<bool> core;std::vector<int> peeled;int certificate;};

Graph graph(int n,std::vector<std::pair<int,int>> edges) {
    Graph g{n,std::vector<std::vector<int>>(n),edges};
    for(auto [u,v]:edges) {need(0<=u && u<v && v<n,"edge range");g.adj[u].push_back(v);g.adj[v].push_back(u);}
    return g;
}

void check(const Graph& g,const Witness& w) {
    need(int(w.colour.size())==g.n,"witness length");std::vector<int> ds;
    for(int i=0;i<g.n;++i) {char c=w.colour[i];need(c=='.' || (c>='0' && c<='3'),"colour range");if(c=='.')ds.push_back(i);}
    need(ds==w.omitted,"exact witness omissions");
    for(auto [u,v]:g.edges) need(w.colour[u]=='.' || w.colour[v]=='.' || w.colour[u]!=w.colour[v],"witness unit edge");
}

Result decide(const Graph& g,const std::vector<int>& omitted,const std::vector<Witness>& ws) {
    Result r{std::vector<bool>(g.n,true),{},-1};std::vector<int> degree(g.n),queue;
    for(int v:omitted) {need(v>=0 && v<g.n && r.core[v],"original omission");r.core[v]=false;}
    for(int v=0;v<g.n;++v) if(r.core[v]) {
        for(int u:g.adj[v]) if(r.core[u]) ++degree[v];
        if(degree[v]<4)queue.push_back(v);
    }
    for(std::size_t head=0;head<queue.size();++head) {
        int v=queue[head];if(!r.core[v])continue;
        need(degree[v]<4,"queued degree");r.core[v]=false;r.peeled.push_back(v);
        for(int u:g.adj[v]) if(r.core[u] && --degree[u]==3)queue.push_back(u);
    }
    for(int v=0;v<g.n;++v) if(r.core[v]) need(degree[v]>=4,"remaining core degree");
    for(std::size_t i=0;i<ws.size();++i) {
        bool missing=true;for(int v:ws[i].omitted)if(r.core[v]) {missing=false;break;}
        if(missing) {r.certificate=int(i);break;}
    }
    if(r.certificate>=0) {
        std::string c(g.n,'.');const auto& seed=ws[r.certificate].colour;
        for(int v=0;v<g.n;++v) if(r.core[v]) {need(seed[v]!='.',"seed covers core");c[v]=seed[v];}
        for(auto it=r.peeled.rbegin();it!=r.peeled.rend();++it) {
            int v=*it,mask=0,neighbours=0;
            for(int u:g.adj[v]) if(c[u]!='.') {mask|=1<<(c[u]-'0');++neighbours;}
            need(neighbours<=3,"reverse peeling bound");int colour=0;while(mask&(1<<colour))++colour;
            need(colour<4,"available restoration colour");c[v]=char('0'+colour);
        }
        check(g,Witness{omitted,c});
    }
    return r;
}

void controls() {
    std::vector<std::pair<int,int>> clique;for(int i=0;i<5;++i)for(int j=i+1;j<5;++j)clique.emplace_back(i,j);
    int tests=0;
    auto test=[&](Graph g,std::vector<int> O,Witness w,std::vector<int> expected,int certificate) {
        check(g,w);auto r=decide(g,O,{w});std::vector<int> actual;
        for(int i=0;i<g.n;++i)if(r.core[i])actual.push_back(i);
        need(actual==expected && r.certificate==certificate,"control outcome");++tests;
    };
    test(graph(5,clique),{},{{0},".0123"},{0,1,2,3,4},-1);
    test(graph(5,clique),{1},{{0},".0123"},{},0);
    auto path=clique;path.emplace_back(0,5);path.emplace_back(5,6);path.emplace_back(6,7);
    test(graph(8,path),{},{{0},".0123010"},{0,1,2,3,4},-1);
    test(graph(8,path),{1},{{0},".0123010"},{},0);
    test(graph(8,path),{5},{{0},".0123010"},{0,1,2,3,4},-1);
    test(graph(8,path),{0},{{0},".0123010"},{},0);
    auto two=clique;for(auto [u,v]:clique)two.emplace_back(u+5,v+5);
    test(graph(10,two),{},{{0,5},".0123.0123"},{0,1,2,3,4,5,6,7,8,9},-1);
    test(graph(10,two),{1},{{0,5},".0123.0123"},{5,6,7,8,9},-1);
    test(graph(10,two),{1,6},{{0,5},".0123.0123"},{},0);
    test(graph(4,{}),{},{{0},".012"},{},0);
    std::cout<<"{\"controls\":"<<tests<<",\"status\":\"PASSED\"}\n";
}

int main(int argc,char** argv) {
    if(argc==2 && std::string(argv[1])=="--controls") {controls();return 0;}
    need(argc==7,"usage: graph witnesses frontier core_records survivors summary");
    const auto start=std::chrono::steady_clock::now();
    std::ifstream gin(argv[1]),win(argv[2]),frontier(argv[3]);std::ofstream out(argv[4],std::ios::binary),survivors(argv[5]),summary(argv[6]);
    need(gin.good() && win.good() && frontier.good() && out.good() && survivors.good() && summary.good(),"file open");
    int n,m;gin>>n>>m;need(n==514 && m==2526,"target graph counts");std::vector<std::pair<int,int>> edges;
    for(int i=0;i<m;++i) {int u,v;gin>>u>>v;edges.emplace_back(u,v);}need(bool(gin),"graph input");Graph g=graph(n,edges);
    int count;win>>count;need(count==516,"library count");std::vector<Witness> ws;
    for(int i=0;i<count;++i) {int k;win>>k;need(k>0 && k<=3,"cut size");Witness w;for(int j=0;j<k;++j){int v;win>>v;w.omitted.push_back(v);}win>>w.colour;check(g,w);ws.push_back(w);}need(bool(win),"witness input");
    std::uint64_t rows=0,covered=0,peeled=0;std::map<int,std::uint64_t> histogram,cut_histogram;
    std::string line;
    while(std::getline(frontier,line)) {
        std::string text=line;std::replace(text.begin(),text.end(),',',' ');std::istringstream parse(text);std::vector<int> O;int v;
        while(parse>>v) {O.push_back(v);}
        need(O.size()==6 && std::is_sorted(O.begin(),O.end()),"six sorted omissions");
        auto r=decide(g,O,ws);++rows;peeled+=r.peeled.size();++histogram[int(r.peeled.size())];
        if(r.certificate>=0) {++covered;++cut_histogram[r.certificate];}else survivors<<line<<'\n';
        unsigned int tag=r.certificate<0?65535:unsigned(r.certificate);
        out.put(char(tag&255));out.put(char((tag>>8)&255));
        std::array<unsigned char,65> bits{};for(int i=0;i<514;++i)if(r.core[i])bits[i/8]|=1<<(i%8);
        for(auto byte:bits)out.put(char(byte));
        if(rows%32768==0)std::cerr<<"rows "<<rows<<" covered "<<covered<<" peeled "<<peeled<<'\n';
    }
    need(rows==258914 && out.good() && survivors.good(),"complete output");
    double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
    summary<<"{\"rows\":"<<rows<<",\"covered\":"<<covered<<",\"survivors\":"<<rows-covered<<",\"peeled_vertices_total\":"<<peeled<<",\"peel_histogram\":{";
    bool comma=false;for(auto [k,c]:histogram){if(comma)summary<<',';summary<<'\"'<<k<<"\":"<<c;comma=true;}
    summary<<"},\"cut_histogram\":{";comma=false;for(auto [k,c]:cut_histogram){if(comma)summary<<',';summary<<'\"'<<k<<"\":"<<c;comma=true;}
    summary<<"},\"seconds\":"<<seconds<<",\"native_colouring_queries\":0}\n";
    std::cerr<<"complete "<<rows<<" covered "<<covered<<" seconds "<<seconds<<'\n';
}
