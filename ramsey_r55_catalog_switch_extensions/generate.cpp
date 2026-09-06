// Exact anchored-pattern CNF for Seidel switches of a graph plus one free vertex.
#include <array>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

struct Clause { std::array<int,8> literals{}; int size=0; };
struct Formula {
    int n;
    std::array<std::array<int,42>,42> edges{};
    std::vector<Clause> clauses;
    std::array<int,5> vertices{};
    explicit Formula(const std::string& graph) : n(0) {
        if (graph.empty()) throw std::runtime_error("Empty graph6 record");
        n=static_cast<unsigned char>(graph[0])-63;
        if(n<4 || n>42) throw std::runtime_error("Supported core order is4..42");
        const int pairs=n*(n-1)/2;
        if(graph.size()!=static_cast<std::size_t>(1+(pairs+5)/6))
            throw std::runtime_error("graph6 record length");
        for(char ch: graph) if(ch<63 || ch>126) throw std::runtime_error("graph6 character");
        int index=0;
        for(int v=1;v<n;++v) for(int u=0;u<v;++u,++index) {
            int bit=((static_cast<unsigned char>(graph[1+index/6])-63)>>(5-index%6))&1;
            edges[u][v]=edges[v][u]=bit;
        }
        for(int i=pairs;i<((pairs+5)/6)*6;++i)
            if(((static_cast<unsigned char>(graph[1+i/6])-63)>>(5-i%6))&1)
                throw std::runtime_error("Nonzero graph6 padding");
    }
    void event(int k) {
        std::array<int,5> spin{};
        for(int color=0;color<2;++color) {
            spin[0]=0;
            for(int j=1;j<k;++j) spin[j]=edges[vertices[0]][vertices[j]]^color;
            bool good=true;
            for(int i=0;i<k;++i) for(int j=i+1;j<k;++j)
                if((edges[vertices[i]][vertices[j]]^spin[i]^spin[j])!=color) good=false;
            if(!good) continue;
            for(int flip=0;flip<2;++flip) {
                if(vertices[0]==0 && flip==1) continue;
                Clause clause;
                for(int j=0;j<k;++j) if(vertices[j]!=0)
                    clause.literals[clause.size++]=(spin[j]^flip) ? -vertices[j] : vertices[j];
                if(k==4) for(int j=0;j<k;++j)
                    clause.literals[clause.size++]=color ? -(n+vertices[j]) : n+vertices[j];
                clauses.push_back(clause);
            }
        }
    }
    void subsets(int k,int depth=0,int start=0) {
        if(depth==k) {event(k);return;}
        for(int v=start;v<=n-(k-depth);++v) {vertices[depth]=v;subsets(k,depth+1,v+1);}
    }
};

int main(int argc,char** argv) {
    try {
        if(argc!=4) throw std::runtime_error("Usage: generate catalog.g6 index output.cnf");
        std::size_t end=0;
        const int index=std::stoi(argv[2],&end);
        if(index<0 || std::string(argv[2]).size()!=end) throw std::runtime_error("Bad parent index");
        std::ifstream input(argv[1]);
        if(!input) throw std::runtime_error("Cannot open catalog");
        std::string record;
        for(int j=0;j<=index;++j) if(!std::getline(input,record)) throw std::runtime_error("Parent index absent");
        Formula f(record);
        f.subsets(5);f.subsets(4);
        std::ofstream output(argv[3]);
        if(!output) throw std::runtime_error("Cannot open output");
        output<<"p cnf "<<2*f.n-1<<' '<<f.clauses.size()<<'\n';
        for(const auto& c:f.clauses) {
            for(int j=0;j<c.size;++j) output<<c.literals[j]<<' ';
            output<<"0\n";
        }
        output.close();
        if(!output) throw std::runtime_error("Formula write failed");
        std::cout<<"variables="<<2*f.n-1<<" clauses="<<f.clauses.size()<<'\n';
    } catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 1;}
}
