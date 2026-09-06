// Native execution of the documented exhaustive four-colour search.
#include <algorithm>
#include <array>
#include <cstdint>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <vector>
using Mask=unsigned;
struct Search {
    int n; std::vector<std::vector<int>> adj;
    std::uint64_t nodes=0, conflicts=0;
    std::vector<Mask> solution;
    static unsigned count(Mask m) { return unsigned(__builtin_popcount(m)); }
    static void increment(std::uint64_t& x) {
        if(x==std::numeric_limits<std::uint64_t>::max())throw std::runtime_error("Counter overflow");
        ++x;
    }
    bool dfs(std::vector<Mask> masks,std::vector<int> queue) {
        increment(nodes);
        while(!queue.empty()) {
            int v=queue.back();queue.pop_back();Mask bit=masks[v];
            if(bit==0 || (bit&(bit-1)))throw std::runtime_error("Bad propagation queue");
            for(int u:adj[v])if(masks[u]&bit) {
                Mask next=masks[u]&~bit;
                if(!next){increment(conflicts);return false;}
                masks[u]=next;
                if(!(next&(next-1)))queue.push_back(u);
            }
        }
        int best=-1;unsigned size=5;Mask used=0;
        for(int v=0;v<n;++v) {
            Mask m=masks[v];
            if(!(m&(m-1))){used|=m;continue;}
            unsigned sz=count(m);
            if(sz<size || (sz==size && (best<0 || adj[v].size()>adj[best].size()))) {
                best=v;size=sz;
            }
        }
        if(best<0){solution=std::move(masks);return true;}
        Mask candidates=masks[best]&used,unused=masks[best]&~used;
        if(unused)candidates|=unused&(~unused+1U);
        while(candidates) {
            Mask bit=candidates&(~candidates+1U);candidates-=bit;
            auto child=masks;child[best]=bit;
            if(dfs(std::move(child),{best}))return true;
        }
        return false;
    }
};
int main() {
    try {
        int n,m,p;
        if(!(std::cin>>n>>m>>p) || n<0 || n>4096 || m<0 || p<0 || p>n ||
           static_cast<long long>(m)>static_cast<long long>(n)*(n-1)/2)
            throw std::runtime_error("Bad dimensions");
        Search s{n,std::vector<std::vector<int>>(n),0,0,{}};
        for(int i=0;i<m;++i) {
            int a,b;if(!(std::cin>>a>>b)||a<0||a>=n||b<0||b>=n||a==b)
                throw std::runtime_error("Bad edge");
            s.adj[a].push_back(b);s.adj[b].push_back(a);
        }
        for(auto& row:s.adj) {
            std::sort(row.begin(),row.end());
            if(std::adjacent_find(row.begin(),row.end())!=row.end())throw std::runtime_error("Duplicate edge");
        }
        std::vector<Mask> masks(n,15);std::vector<int> queue;
        for(int i=0;i<p;++i) {
            int v,c;if(!(std::cin>>v>>c)||v<0||v>=n||c<0||c>3||masks[v]!=15)
                throw std::runtime_error("Bad pin");
            masks[v]=1U<<unsigned(c);queue.push_back(v);
        }
        std::string tail;if(std::cin>>tail)throw std::runtime_error("Trailing data");
        bool sat=s.dfs(std::move(masks),std::move(queue));
        std::cout<<"{\"satisfiable\":"<<(sat?"true":"false")<<",\"nodes\":"<<s.nodes
                 <<",\"conflicts\":"<<s.conflicts<<",\"colouring\":[";
        if(sat)for(int v=0;v<n;++v) {
            if(v)std::cout<<',';
            std::cout<<unsigned(__builtin_ctz(s.solution[v]));
        }
        std::cout<<"]}\n";
        return 0;
    }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 2;}
}
