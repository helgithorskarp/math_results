#include <algorithm>
#include <chrono>
#include <cstdint>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using Bits=unsigned __int128;
using Clock=std::chrono::steady_clock;
void require(bool value,const std::string& message) { if(!value)throw std::runtime_error(message); }
int count(Bits x) { return __builtin_popcountll(static_cast<uint64_t>(x))+__builtin_popcountll(static_cast<uint64_t>(x>>64)); }
int first(Bits x) { require(x!=0,"zero bit input");uint64_t low=static_cast<uint64_t>(x);
    return low?__builtin_ctzll(low):64+__builtin_ctzll(static_cast<uint64_t>(x>>64)); }
Bits parse(const std::string& text) {
    require(!text.empty()&&text.size()<=32,"invalid mask length");Bits x=0;
    for(char c:text){int digit=c>='0'&&c<='9'?c-'0':c>='a'&&c<='f'?c-'a'+10:-1;
        require(digit>=0,"invalid mask digit");x=(x<<4)|static_cast<unsigned>(digit);}
    return x;
}
struct Incomplete:std::runtime_error {using std::runtime_error::runtime_error;};
struct Search {
    std::vector<Bits> neighbor;
    int target;
    uint64_t nodes=0,limit;
    double seconds;
    Clock::time_point began=Clock::now();
    std::vector<int> chosen,witness;
    Search(std::vector<Bits> graph,int goal,uint64_t cap,double timeout):neighbor(std::move(graph)),target(goal),limit(cap),seconds(timeout) {}
    bool visit(Bits vertices) {
        ++nodes;
        if(nodes>limit||(nodes%128==0&&std::chrono::duration<double>(Clock::now()-began).count()>seconds))
            throw Incomplete("clique guard reached");
        if(static_cast<int>(chosen.size())==target){witness=chosen;return true;}
        if(static_cast<int>(chosen.size())+count(vertices)<target)return false;
        // Greedy independent color classes, choosing largest residual degree.
        // Every prefix of the resulting order is colored by its stored bound.
        std::vector<int> order,bound;
        Bits uncolored=vertices;int color=0;
        while(uncolored) {
            ++color;Bits usable=uncolored;
            while(usable) {
                int vertex=-1,degree=-1;Bits scan=usable;
                while(scan){int v=first(scan);scan&=scan-1;int d=count(neighbor[v]&vertices);
                    if(d>degree){degree=d;vertex=v;}}
                require(vertex>=0,"color made no progress");
                order.push_back(vertex);bound.push_back(color);
                uncolored&=~(Bits(1)<<vertex);
                usable&=~((Bits(1)<<vertex)|neighbor[vertex]);
            }
        }
        for(int i=static_cast<int>(order.size())-1;i>=0;--i) {
            if(static_cast<int>(chosen.size())+bound[i]<target)return false;
            int v=order[i];require((vertices&(Bits(1)<<v))!=0,"branch vertex absent");
            chosen.push_back(v);
            if(visit(vertices&neighbor[v]))return true;
            chosen.pop_back();vertices&=~(Bits(1)<<v);
        }
        return false;
    }
};
int main(int argc,char** argv) {
    try {
        require(argc==1||argc==3,"optional node and time guard arguments");
        uint64_t limit=argc==3?std::stoull(argv[1]):200000;
        double seconds=argc==3?std::stod(argv[2]):10;
        require(limit<=200000&&seconds>0&&seconds<=10,"invalid guards");
        std::string line;
        while(std::getline(std::cin,line)) {
            std::istringstream input(line);std::string id;int n,target;
            require(bool(input>>id>>n>>target)&&n>=0&&n<=128&&target>0&&target<=129,"invalid header");
            Bits full=n==128?~Bits(0):(Bits(1)<<n)-1;
            std::vector<Bits> graph;
            for(int i=0;i<n;++i){std::string text;require(bool(input>>text),"missing adjacency");
                Bits mask=parse(text);require((mask&~full)==0&&(mask&(Bits(1)<<i))==0,"invalid graph bits");graph.push_back(mask);}
            std::string extra;require(!(input>>extra),"surplus fields");
            for(int i=0;i<n;++i)for(int j=0;j<n;++j)
                require(bool(graph[i]&(Bits(1)<<j))==bool(graph[j]&(Bits(1)<<i)),"asymmetric graph");
            Search search(std::move(graph),target,limit,seconds);
            bool found=search.visit(full);
            std::cout<<id<<' '<<(found?"WITNESS":"EMPTY")<<' '<<search.nodes;
            for(int v:search.witness)std::cout<<' '<<v;
            std::cout<<'\n';
        }
        require(std::cin.eof(),"input stream error");
    }catch(const Incomplete& e){std::cerr<<"INCOMPLETE: "<<e.what()<<'\n';return 2;}
     catch(const std::exception& e){std::cerr<<"ERROR: "<<e.what()<<'\n';return 1;}
}
