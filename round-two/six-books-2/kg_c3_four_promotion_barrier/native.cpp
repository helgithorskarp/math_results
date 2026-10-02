// Four-promotion frontier: independent blue-adjacency prefix DFS.
// A partial completed-case prefix is NOT an all-family negative result.
// No manifest, centralizer, compatibility graph, or clique pruning is read.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Matrix=std::array<std::uint32_t,22>;
using Edge=std::pair<int,int>;
using Orbit=std::array<Edge,3>;
void require(bool p,const std::string& why){if(!p)throw std::runtime_error(why);}
int population(std::uint32_t x){return __builtin_popcount(x);}
Edge order(int a,int b){return a<b?Edge{a,b}:Edge{b,a};}

struct Ground {
    std::vector<unsigned> labels;
    std::vector<Orbit> reds,blues;
    Matrix initial{};
    Ground() {
        const int sigma[7]={1,2,0,4,5,3,6};
        std::set<unsigned> visited;
        for(int a=0;a<7;++a)for(int b=a+1;b<7;++b) {
            unsigned mask=(1u<<a)|(1u<<b);
            if(visited.count(mask))continue;
            for(int step=0;step<3;++step) {
                require(visited.insert(mask).second,"ground vertex coverage");
                labels.push_back(mask);
                unsigned image=0;
                for(int x=0;x<7;++x)if(mask>>x&1u)image|=1u<<sigma[x];
                mask=image;
            }
            require(mask==((1u<<a)|(1u<<b)),"vertex orbit closure");
        }
        require(labels.size()==21,"twenty-one two-subsets");
        std::array<int,21> vertex_action{};
        for(int u=0;u<21;++u) {
            unsigned image=0;
            for(int x=0;x<7;++x)if(labels[u]>>x&1u)image|=1u<<sigma[x];
            auto it=std::find(labels.begin(),labels.end(),image);
            require(it!=labels.end(),"native action image");
            vertex_action[u]=int(it-labels.begin());
        }
        std::set<Edge> done;
        for(int u=0;u<21;++u)for(int v=u+1;v<21;++v) {
            Edge first{u,v};
            if(done.count(first))continue;
            Orbit orbit{};Edge current=first;
            bool disjoint=!(labels[u]&labels[v]);
            for(int t=0;t<3;++t) {
                require(done.insert(current).second,"native edge coverage");
                require((!(labels[current.first]&labels[current.second]))==disjoint,"native orbit color");
                orbit[t]=current;
                current=order(vertex_action[current.first],vertex_action[current.second]);
            }
            require(current==first,"edge orbit closure");
            (disjoint?reds:blues).push_back(orbit);
        }
        require(reds.size()==35 && blues.size()==35 && done.size()==210,"native edge domain");
        for(int u=0;u<21;++u)for(int v=0;v<21;++v)
            if(u!=v && (labels[u]&labels[v]))initial[u]|=1u<<v;
        for(int u=0;u<21;++u)require(population(initial[u])==10,"KG blue degree");
        for(int u=0;u<21;++u)for(int v=u+1;v<21;++v) {
            int literal=0;
            for(int w=0;w<21;++w)if(w!=u && w!=v)
                literal+=bool(labels[u]&labels[w]) && bool(labels[v]&labels[w]);
            if(initial[u]>>v&1u)require(literal==5,"KG blue page control");
        }
    }
};

bool avoids_blue_book(const Matrix& blue) {
    for(int u=0;u<22;++u)for(int v=u+1;v<22;++v)
        if((blue[u]>>v&1u) && population(blue[u]&blue[v])>=7)return false;
    return true;
}
void make_blue(Matrix& blue,const Orbit& orbit) {
    for(auto [u,v]:orbit){blue[u]|=1u<<v;blue[v]|=1u<<u;}
}
void make_red(Matrix& blue,const Orbit& orbit) {
    for(auto [u,v]:orbit){blue[u]&=~(1u<<v);blue[v]&=~(1u<<u);}
}
// The caller enters with a B7-free blue graph. For a new edge uv, only
// its spine and existing edges uw,vw for common blue neighbors w can
// acquire a forbidden seventh page. This is an exact local condition.
// On failure, a proper prefix of the three-edge orbit may be inserted;
// the caller always clears the entire original-red orbit on return.
bool try_blue_orbit(Matrix& blue,const Orbit& orbit) {
    for(auto [u,v]:orbit)
        require(!(blue[u]>>v&1u) && !(blue[v]>>u&1u),"orbit initially red");
    for(auto [u,v]:orbit) {
        std::uint32_t common=blue[u]&blue[v];
        if(population(common)>=7)return false;
        while(common) {
            int w=__builtin_ctz(common);
            common&=common-1u;
            if(population(blue[u]&blue[w])>=6 ||
               population(blue[v]&blue[w])>=6)return false;
        }
        blue[u]|=1u<<v;blue[v]|=1u<<u;
    }
    return true;
}
int bad_red_spines(const Matrix& blue) {
    int bad=0;
    for(int u=0;u<22;++u)for(int v=u+1;v<22;++v)if(!(blue[u]>>v&1u)) {
        int pages=0;
        for(int w=0;w<22;++w)if(w!=u && w!=v)
            pages+=!(blue[u]>>w&1u) && !(blue[v]>>w&1u);
        if(pages>=4)++bad;
    }
    return bad;
}

struct ValidSet {std::vector<int> D;int red_bad;bool degrees;};
struct NativeDFS {
    const Ground& ground;
    const std::vector<int>& pool;
    std::vector<int> prefix;
    std::array<std::uint64_t,10> attempted{},good{};
    std::array<std::vector<ValidSet>,10> terminal;
    NativeDFS(const Ground& g,const std::vector<int>& p):ground(g),pool(p){}
    void visit(Matrix& blue,int start,int depth) {
        for(int i=start;i<int(pool.size());++i) {
            // At depth<8, a prefix needs at least8-depth remaining choices
            // including this candidate to reach either target8 or9.
            // This cardinality test cannot discard any valid target.
            if(depth<8 && int(pool.size())-i<8-depth)break;
            ++attempted[depth+1];
            if(try_blue_orbit(blue,ground.reds[pool[i]])) {
                ++good[depth+1];prefix.push_back(pool[i]);
                if(depth+1>=8) {
                    bool degree_ok=true;
                    for(auto row:blue) {
                        int d=21-population(row);
                        if(d<7 || d>10)degree_ok=false;
                    }
                    terminal[depth+1].push_back({prefix,bad_red_spines(blue),degree_ok});
                }
                if(depth+1<9)visit(blue,i+1,depth+1);
                prefix.pop_back();
            }
            make_red(blue,ground.reds[pool[i]]);
        }
    }
};
template<class T>void array_out(const T& value) {
    std::cout<<'[';
    bool comma=false;
    for(const auto& x:value){if(comma)std::cout<<',';comma=true;std::cout<<x;}
    std::cout<<']';
}

int main(int argc,char** argv) {
    try {
        int first=0,limit=1832600;double seconds=25;
        for(int i=1;i<argc;++i) {
            std::string key=argv[i];require(i+1<argc,"missing option value");
            std::string value=argv[++i];
            if(key=="--first")first=std::stoi(value);
            else if(key=="--limit")limit=std::stoi(value);
            else if(key=="--seconds")seconds=std::stod(value);
            else throw std::runtime_error("unknown option");
        }
        require(first>=0 && first<=1832600 && limit>0 && seconds>0 && seconds<=25,"bounded options");
        Ground ground;
        std::vector<std::array<int,3>> joins;
        std::vector<std::array<int,4>> promotions;
        for(int a=0;a<7;++a)for(int b=a+1;b<7;++b)for(int c=b+1;c<7;++c)joins.push_back({a,b,c});
        for(int a=0;a<35;++a)for(int b=a+1;b<35;++b)for(int c=b+1;c<35;++c)for(int d=c+1;d<35;++d)promotions.push_back({a,b,c,d});
        require(joins.size()==35 && promotions.size()==52360,"labeled product domain");
        auto started=std::chrono::steady_clock::now();int index=first;
        for(;index<1832600 && index-first<limit;++index) {
            if(index>first && std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count()>=seconds)break;
            auto J=joins[index/52360]; auto P=promotions[index%52360];
            Matrix blue=ground.initial;
            for(int p:P)make_red(blue,ground.blues[p]);
            for(int u=0;u<21;++u)if(std::find(J.begin(),J.end(),u/3)==J.end()) {
                blue[u]|=1u<<21;blue[21]|=1u<<u;
            }
            bool base=avoids_blue_book(blue);
            std::vector<int> pool;
            if(base)for(int d=0;d<35;++d) {
                bool valid=try_blue_orbit(blue,ground.reds[d]);
                make_red(blue,ground.reds[d]);
                if(valid)pool.push_back(d);
            }
            NativeDFS search(ground,pool);
            search.visit(blue,0,0);
            std::cout<<"{\"index\":"<<index<<",\"joins\":";array_out(J);
            std::cout<<",\"promotions\":";array_out(P);
            std::cout<<",\"base_blue_valid\":"<<(base?"true":"false")<<",\"pool\":";array_out(pool);
            std::cout<<",\"attempted\":";array_out(search.attempted);
            std::cout<<",\"good\":";array_out(search.good);
            std::cout<<",\"targets\":{";
            bool comma=false;
            for(int q:{8,9}) {
                if(comma)std::cout<<',';
                comma=true;
                std::cout<<'\"'<<q<<"\":[";
                bool sep=false;
                for(const auto& c:search.terminal[q]) {
                    if(sep)std::cout<<',';
                    sep=true;
                    std::cout<<"{\"D\":";array_out(c.D);
                    std::cout<<",\"red_bad\":"<<c.red_bad<<",\"degrees\":"<<(c.degrees?"true":"false")<<'}';
                }
                std::cout<<']';
            }
            std::cout<<"}}\n";
        }
        std::cout<<"{\"segment\":true,\"first\":"<<first<<",\"next\":"<<index<<",\"total\":1832600,\"complete\":"
                 <<(index==1832600?"true":"false")<<",\"seconds\":"
                 <<std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count()<<"}\n";
        return 0;
    }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}
}
