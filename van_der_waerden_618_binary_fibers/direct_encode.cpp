// Independent full CRT-pair enumeration; no field-support or first-zero reduction.
// 381306 pairs, <=7 literals each; all counters fit32 bits and offsets fit ints.
#include <algorithm>
#include <array>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>

using Edge=std::vector<int>;
void require(bool b,const char *text){if(!b)throw std::runtime_error(text);}

int main(int argc,char **argv){
    try{
        require(argc==2,"choose cnf or weighted");
        const std::string kind(argv[1]);require(kind=="cnf" || kind=="weighted","unknown output kind");
        int n=0;std::cin>>n;require(bool(std::cin) && n==103,"tau header must be103");
        std::array<int,103> tau{};
        for(int &v:tau)require(bool(std::cin>>v) && v>=0 && v<3,"invalid/truncated tau");
        std::string trailing;require(!(std::cin>>trailing),"trailing tau data");
        // Literal six-bit columns in y-bit order; these are f(y),f(y-1),f(y-2).
        constexpr std::array<unsigned,3> columns={56U,49U,35U};
        std::map<Edge,unsigned> counts;
        unsigned tautologies=0;
        for(int a=0;a<618;++a)for(int d=1;d<618;++d){
            Edge e;
            for(int j=0;j<7;++j){
                const int t=(a+j*d)%618,x=t%103,y=t%6;
                const unsigned bit=(columns[static_cast<std::size_t>(tau[static_cast<std::size_t>(x)])]>>y)&1U;
                e.push_back((x+1)*(bit? -1:1));
            }
            std::sort(e.begin(),e.end());e.erase(std::unique(e.begin(),e.end()),e.end());
            bool taut=false;for(int v:e)if(std::binary_search(e.begin(),e.end(),-v))taut=true;
            if(taut){++tautologies;continue;}
            require(e.size()==7,"unexpected collapsed non-tautological AP");
            Edge opposite;for(int v:e)opposite.push_back(-v);std::sort(opposite.begin(),opposite.end());
            if(opposite<e)e=opposite;
            ++counts[e];
        }
        require(tautologies==3090,"local cyclic pair count changed");
        unsigned weight_sum=0;
        for(auto &[edge,count]:counts){
            (void)edge;require(count%4==0 && count>=4 && count<=12,"invalid cyclic multiplicity");
            count/=4;weight_sum+=count;
        }
        require(weight_sum==94554,"weight sum changed");
        if(kind=="weighted"){
            std::cout<<"103 "<<counts.size()<<'\n';
            for(const auto &[edge,weight]:counts){
                for(int v:edge)std::cout<<v<<' ';
                std::cout<<"0 "<<weight<<'\n';
            }
        }else{
            std::set<Edge> clauses;clauses.insert({-1});
            for(const auto &[edge,weight]:counts){
                (void)weight;clauses.insert(edge);Edge opposite;
                for(int v:edge){opposite.push_back(-v);}
                std::sort(opposite.begin(),opposite.end());clauses.insert(opposite);
            }
            std::cout<<"p cnf 103 "<<clauses.size()<<'\n';
            for(const auto &clause:clauses){for(int v:clause)std::cout<<v<<' ';std::cout<<"0\n";}
        }
        require(std::cout.good(),"output failure");return 0;
    }catch(const std::exception &e){std::cerr<<"ERROR: "<<e.what()<<'\n';return 2;}
}
