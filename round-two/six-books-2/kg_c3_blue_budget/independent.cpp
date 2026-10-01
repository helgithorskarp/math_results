// Exact independent ground-pair census: no centralizer, clique, or pair pruning.
// Every single-admissible q-subset is physically built and literally checked.
// C++17, unsigned22-bit adjacency, one process/thread, bounded case phases.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Edge = std::pair<int,int>;
using Orbit = std::array<Edge,3>;
using Rows = std::array<std::uint32_t,22>;
constexpr std::uint32_t FULL = (std::uint32_t(1)<<22)-1;

void need(bool value, const std::string& message) {
    if (!value) throw std::runtime_error(message);
}
int count(std::uint32_t x) { return __builtin_popcount(x); }
Edge ordered(int u, int v) { return std::minmax(u,v); }

struct Input {
    std::vector<unsigned> labels;
    std::array<int,21> action;
    std::vector<Orbit> red, blue;
    Rows baseline{};
    Input() {
        std::array<int,7> ground{1,2,0,4,5,3,6};
        std::set<Edge> unused;
        for (int u=0;u<7;++u) for (int v=u+1;v<7;++v) unused.insert({u,v});
        while (!unused.empty()) {
            Edge start=*unused.begin(), step=start;
            for (int k=0;k<3;++k) {
                need(unused.erase(step)==1,"ground vertex orbit coverage");
                labels.push_back((1u<<step.first)|(1u<<step.second));
                step=ordered(ground[step.first],ground[step.second]);
            }
            need(step==start,"ground vertex orbit length");
        }
        need(labels.size()==21,"ground labels");
        for (int u=0;u<21;++u) {
            unsigned image=0;
            for (int i=0;i<7;++i) if (labels[u]>>i&1u) image|=1u<<ground[i];
            auto position=std::find(labels.begin(),labels.end(),image);
            need(position!=labels.end(),"vertex action image");
            action[u]=int(position-labels.begin());
        }
        unused.clear();
        for (int u=0;u<21;++u) for (int v=u+1;v<21;++v) unused.insert({u,v});
        while (!unused.empty()) {
            Edge start=*unused.begin(), step=start;
            Orbit orbit;
            bool disjoint=(labels[start.first]&labels[start.second])==0;
            for (int k=0;k<3;++k) {
                need(unused.erase(step)==1,"ground edge orbit coverage");
                need(((labels[step.first]&labels[step.second])==0)==disjoint,"edge orbit color");
                orbit[k]=step;
                step=ordered(action[step.first],action[step.second]);
            }
            need(step==start,"ground edge orbit length");
            (disjoint?red:blue).push_back(orbit);
        }
        need(red.size()==35 && blue.size()==35,"edge orbit counts");
        for (int u=0;u<21;++u) for (int v=0;v<21;++v)
            if (!(labels[u]&labels[v])) baseline[u]|=1u<<v;
        for (int u=0;u<21;++u) {
            need(count(baseline[u])==10,"KG degree control");
            for (int v=u+1;v<21;++v) {
                bool r=baseline[u]>>v&1u;
                std::uint32_t pages=r?(baseline[u]&baseline[v]):
                    ((1u<<21)-1)&~(baseline[u]|baseline[v]|(1u<<u)|(1u<<v));
                int literal=0;
                for (int w=0;w<21;++w) if (w!=u && w!=v)
                    literal+=r?((baseline[u]>>w&1u)&&(baseline[v]>>w&1u)):
                        (!(baseline[u]>>w&1u)&&!(baseline[v]>>w&1u));
                need(count(pages)==literal && literal==(r?3:5),"KG page control");
            }
        }
    }
};

void add(Rows& rows, const Orbit& orbit) {
    for (auto [u,v]:orbit) { rows[u]|=1u<<v; rows[v]|=1u<<u; }
}
void toggle(Rows& rows, const Orbit& orbit) {
    for (auto [u,v]:orbit) { rows[u]^=1u<<v; rows[v]^=1u<<u; }
}
bool blue_valid(const Rows& rows) {
    // Endpoints are explicitly excluded; no degree or red-book premise.
    for (int u=0;u<22;++u) {
        std::uint32_t blue_u=FULL&~(rows[u]|(1u<<u));
        std::uint32_t later=blue_u&~((1u<<(u+1))-1);
        while (later) {
            int v=__builtin_ctz(later); later&=later-1;
            if (count(blue_u&~(rows[v]|(1u<<v)))>6) return false;
        }
    }
    return true;
}

std::uint64_t choose(int n,int q) {
    if (q>n) return 0;
    std::uint64_t result=1;
    for (int i=1;i<=q;++i) result=result*std::uint64_t(n-q+i)/std::uint64_t(i);
    return result;
}
struct Census {
    const Input& input;
    const std::vector<int>& pool;
    int target;
    std::uint64_t leaves=0,valid=0;
    std::vector<int> prefix;
    std::vector<std::vector<int>> witnesses;
    Census(const Input& in,const std::vector<int>& p,int q):input(in),pool(p),target(q) {}
    void visit(Rows& rows,int start,int need_more) {
        if (!need_more) {
            ++leaves;
            if (blue_valid(rows)) { ++valid; witnesses.push_back(prefix); }
            return;
        }
        for (int i=start;i<=int(pool.size())-need_more;++i) {
            toggle(rows,input.red[pool[i]]);
            prefix.push_back(pool[i]);
            visit(rows,i+1,need_more-1);
            prefix.pop_back();
            toggle(rows,input.red[pool[i]]);
        }
    }
};
template<class T> void print_vector(const std::vector<T>& v) {
    std::cout<<'[';
    for (std::size_t i=0;i<v.size();++i) { if(i) std::cout<<','; std::cout<<v[i]; }
    std::cout<<']';
}

int main(int argc,char** argv) {
    try {
        int promotions=2, first=0;
        double seconds=30;
        for(int i=1;i<argc;++i) {
            std::string option=argv[i];
            need(i+1<argc,"option value missing");
            std::string value=argv[++i];
            if(option=="--promotions") promotions=std::stoi(value);
            else if(option=="--first") first=std::stoi(value);
            else if(option=="--seconds") seconds=std::stod(value);
            else throw std::runtime_error("unknown option");
        }
        need((promotions==1 || promotions==2) && first>=0 && seconds>0 && seconds<=30,"bounded options");
        auto started=std::chrono::steady_clock::now();
        Input input;
        std::vector<std::array<int,3>> joins;
        for(int a=0;a<7;++a) for(int b=a+1;b<7;++b) for(int c=b+1;c<7;++c) joins.push_back({a,b,c});
        std::vector<std::vector<int>> additions;
        for(int a=0;a<35;++a) {
            if(promotions==1) additions.push_back({a});
            else for(int b=a+1;b<35;++b) additions.push_back({a,b});
        }
        const int total=int(joins.size()*additions.size()), target=2*promotions+2;
        need(first<=total,"first case range");
        int index=first;
        for(;index<total;++index) {
            if(index>first && std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count()>=seconds) break;
            auto J=joins[index/int(additions.size())];
            auto P=additions[index%int(additions.size())];
            Rows rows=input.baseline;
            for(int p:P) add(rows,input.blue[p]);
            for(int j:J) for(int t=0;t<3;++t) { int u=3*j+t; rows[u]|=1u<<21; rows[21]|=1u<<u; }
            need(count(rows[21])==9,"fixed root control");
            bool base_good=blue_valid(rows);
            std::vector<int> pool;
            if(base_good) for(int d=0;d<35;++d) {
                toggle(rows,input.red[d]);
                bool good=blue_valid(rows);
                toggle(rows,input.red[d]);
                if(good) pool.push_back(d);
            }
            // Record pair domains for transport validation ONLY. The raw census
            // below does not use them to prune any subset.
            std::vector<std::uint64_t> compatibility(pool.size(),0);
            for(int i=0;i<int(pool.size());++i) for(int j=i+1;j<int(pool.size());++j) {
                toggle(rows,input.red[pool[i]]); toggle(rows,input.red[pool[j]]);
                bool good=blue_valid(rows);
                toggle(rows,input.red[pool[j]]); toggle(rows,input.red[pool[i]]);
                if(good) { compatibility[i]|=std::uint64_t(1)<<j; compatibility[j]|=std::uint64_t(1)<<i; }
            }
            Census census{input,pool,target};
            census.visit(rows,0,target);
            need(census.leaves==choose(int(pool.size()),target),"complete raw subset count");
            std::cout<<"{\"index\":"<<index<<",\"joins\":["<<J[0]<<','<<J[1]<<','<<J[2]<<"],\"promotions\":";
            print_vector(P);
            std::cout<<",\"base_blue_valid\":"<<(base_good?"true":"false")<<",\"pool\":";
            print_vector(pool);
            std::cout<<",\"compatibility\":";
            print_vector(compatibility);
            std::cout<<",\"subsets\":"<<census.leaves<<",\"blue_valid_subsets\":"<<census.valid<<",\"witnesses\":[";
            for(std::size_t i=0;i<census.witnesses.size();++i) { if(i)std::cout<<',';print_vector(census.witnesses[i]); }
            std::cout<<"]}\n";
        }
        std::cout<<"{\"segment\":true,\"first\":"<<first<<",\"next\":"<<index<<",\"total\":"<<total
                 <<",\"complete\":"<<(index==total?"true":"false")<<",\"seconds\":"
                 <<std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count()<<"}\n";
        return 0;
    } catch(const std::exception& e) { std::cerr<<e.what()<<'\n'; return 1; }
}
