// Independent reconstruction from actual unordered-pair permutation orbits.
// Also reconstructs every gate, counter and normalizing clause, and compares
// the complete canonical DIMACS stream, not just counts or a selected core.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <sstream>
#include <stdexcept>
#include <vector>
using Clause = std::vector<int>;
using Pair = std::pair<int,int>;
constexpr int T = 100000;
int nv = 372;
std::set<Clause> formula;
void require(bool yes, const char* message) {
    if (!yes) throw std::runtime_error(message);
}
void add(Clause c) {
    std::sort(c.begin(),c.end());
    c.erase(std::unique(c.begin(),c.end()),c.end());
    for (int x:c) if (std::binary_search(c.begin(),c.end(),-x)) return;
    formula.insert(c);
}
int main(int argc,char** argv) {
  try {
    require(argc==3,"usage: check_formula RED_CYCLES CNF");
    int r=std::stoi(argv[1]); require(0<=r && r<=4,"red-cycle range");
    std::array<int,43> permutation{};
    for (int a=0;a<43;++a) permutation[a]=a<27 ? 3*(a/3)+(a+1)%3 : a;
    std::vector<Pair> pairs;
    int index[43][43]{};
    for (int a=0;a<43;++a) for (int b=a+1;b<43;++b) {
        index[a][b]=index[b][a]=int(pairs.size()); pairs.emplace_back(a,b);
    }
    std::vector<int> parent(pairs.size()); std::iota(parent.begin(),parent.end(),0);
    auto root=[&parent](int a) {while(parent[a]!=a) a=parent[a]; return a;};
    for (int t=0;t<int(pairs.size());++t) {
        auto [a,b]=pairs[t]; int other=index[permutation[a]][permutation[b]];
        parent[root(other)]=root(t);
    }
    std::map<int,std::vector<Pair>> groups;
    for (int t=0;t<int(pairs.size());++t) groups[root(t)].push_back(pairs[t]);
    require(groups.size()==381,"edge-orbit count");
    std::vector<Pair> cross,fixed,links;
    for (auto const& entry:groups) {
        const auto& group=entry.second;
        Pair representative=*std::min_element(group.begin(),group.end());
        auto [a,b]=representative;
        require(group.size()==size_t(a>=27 ? 1 : 3),"edge-orbit length");
        if (a>=27) fixed.push_back(representative);
        else if (b>=27) links.push_back(representative);
        else if (a/3!=b/3) cross.push_back(representative);
    }
    std::sort(cross.begin(),cross.end()); std::sort(fixed.begin(),fixed.end());
    std::sort(links.begin(),links.end(),[](Pair a,Pair b) {
        return std::make_pair(a.second,a.first)<std::make_pair(b.second,b.first);
    });
    require(cross.size()==108 && fixed.size()==120 && links.size()==144,"orbit categories");
    std::map<Pair,int> name; int base=0;
    for (auto const& list:{cross,fixed,links}) for (Pair rep:list) name[rep]=++base;
    require(base==372,"base variables");
    int edge[43][43]{};
    for (auto const& entry:groups) {
        Pair rep=*std::min_element(entry.second.begin(),entry.second.end());
        int value=name.count(rep) ? name.at(rep) : (rep.first/3<r ? T : -T);
        for (auto [a,b]:entry.second) edge[a][b]=edge[b][a]=value;
    }
    int five_sets=0;
    for (int a=0;a<43;++a) for (int b=a+1;b<43;++b)
    for (int c=b+1;c<43;++c) for (int d=c+1;d<43;++d)
    for (int e=d+1;e<43;++e) {
        ++five_sets; std::array<int,5> vertices{a,b,c,d,e};
        for (int sign:{-1,1}) {
            Clause clause; bool satisfied=false;
            for (int i=0;i<5;++i) for (int j=i+1;j<5;++j) {
                int lit=sign*edge[vertices[i]][vertices[j]];
                if (lit==T) satisfied=true;
                else if (lit!=-T) clause.push_back(lit);
            }
            if (!satisfied) add(clause);
        }
    }
    require(five_sets==962598,"five-set coverage");
    size_t ramsey_clauses=formula.size();
    std::array<Clause,9> cost_tokens,full_tokens;
    int gate_rows=0;
    for (int i=0;i<9;++i) for (int j=i+1;j<9;++j) {
        std::array<int,3> bits{edge[3*i][3*j],edge[3*i][3*j+1],edge[3*i][3*j+2]};
        std::set<int> colors{int(i<r),int(j<r)};
        for (int color:colors) {
            int one=++nv,two=++nv,full=++nv;
            for (int valuation=0;valuation<8;++valuation) {
                std::map<int,bool> assignment;
                Clause antecedent;
                for (int k=0;k<3;++k) {
                    bool value=(valuation>>k)&1;
                    assignment[bits[k]]=value;
                    antecedent.push_back(value ? -bits[k] : bits[k]);
                }
                int weight=0;
                // Read the three actual edges of a representative vertex.
                for (int vertex=3*j;vertex<3*j+3;++vertex)
                    weight+=assignment.at(edge[3*i][vertex])==bool(color);
                int deficit=2-weight+(weight==3 ? 3 : 0);
                for (auto [variable,value]:std::array<Pair,3>{Pair{one,deficit>=1},
                      Pair{two,deficit>=2},Pair{full,weight==3}}) {
                    Clause clause=antecedent;
                    clause.push_back(value ? variable : -variable); add(clause);
                }
                ++gate_rows;
            }
            for (int endpoint:{i,j}) if (int(endpoint<r)==color) {
                cost_tokens[endpoint].push_back(one); cost_tokens[endpoint].push_back(two);
                full_tokens[endpoint].push_back(full);
            }
        }
        if (i==0) {add({-bits[1],bits[0]});add({-bits[2],bits[1]});}
    }
    for (const Clause& row:cost_tokens) {
        require(row.size()==16,"cost tokens");
        for (int i=0;i<16;++i) for (int j=i+1;j<16;++j)
        for (int k=j+1;k<16;++k) for (int l=k+1;l<16;++l)
        for (int m=l+1;m<16;++m) add({-row[i],-row[j],-row[k],-row[l],-row[m]});
    }
    // Prefix-threshold variables: first allocate the full triangular array,
    // then derive its implications. This is separate from generator allocation.
    auto atmost=[&](const Clause& input,int bound) {
        std::vector<Clause> cells(input.size()+1);
        for (size_t i=1;i<=input.size();++i) {
            cells[i].push_back(0);
            for (int j=1;j<=std::min(int(i),bound+1);++j) cells[i].push_back(++nv);
        }
        for (size_t i=1;i<=input.size();++i) for (size_t j=1;j<cells[i].size();++j) {
            int s=cells[i][j],x=input[i-1];
            if (j==1) add({-x,s});
            if (j<cells[i-1].size()) add({-cells[i-1][j],s});
            if (j>1 && j-1<cells[i-1].size()) add({-x,-cells[i-1][j-1],s});
        }
        if (int(cells.back().size())>bound+1) add({-cells.back()[bound+1]});
    };
    for (int i=0;i<9;++i) {
        int sign=i<r ? 1 : -1;
        Clause common,own;
        for (int f=27;f<43;++f) {common.push_back(sign*edge[3*i][f]);own.push_back(sign*edge[3*i][f]);}
        for (int full:full_tokens[i]) for (int repeat=0;repeat<3;++repeat) common.push_back(full);
        atmost(common,4);
        for (int a=0;a<9;++a) for (int b=a+1;b<9;++b) if (a==i || b==i)
            for (int position=0;position<3;++position) own.push_back(sign*edge[3*a][3*b+position]);
        for (int& x:own) x=-x;
        require(own.size()==40 && common.size()==40,"counter length");
        atmost(own,24);
    }
    for (int f=27;f<42;++f) for (int position=0;position<9;++position) {
        for (int prefix=0;prefix<(1<<position);++prefix) {
            Clause clause;
            for (int k=0;k<position;++k) {
                int sign=((prefix>>k)&1) ? -1 : 1;
                clause.push_back(sign*edge[3*k][f]);clause.push_back(sign*edge[3*k][f+1]);
            }
            clause.push_back(-edge[3*position][f]);clause.push_back(edge[3*position][f+1]);
            add(clause);
        }
    }
    std::vector<Clause> canonical(formula.begin(),formula.end());
    std::sort(canonical.begin(),canonical.end(),[](const Clause& a,const Clause& b) {
        return a.size()==b.size() ? a<b : a.size()<b.size();
    });
    std::ifstream input(argv[2]); require(bool(input),"cannot read formula");
    std::string line;
    require(bool(std::getline(input,line)),"missing header");
    require(line=="p cnf "+std::to_string(nv)+" "+std::to_string(canonical.size()),"header mismatch");
    for (const Clause& c:canonical) {
        std::ostringstream expected;
        for (size_t j=0;j<c.size();++j) {if (j) expected<<' ';expected<<c[j];}
        expected<<" 0";
        require(bool(std::getline(input,line)) && line==expected.str(),"complete clause mismatch");
    }
    require(!std::getline(input,line),"unexpected trailing content");
    std::cout<<"FORMULA_AUDIT r="<<r<<" variables="<<nv<<" clauses="<<canonical.size()
             <<" ramsey_clauses="<<ramsey_clauses<<" edge_orbits=381 five_sets="<<five_sets
             <<" gate_rows="<<gate_rows<<" PASS\n";
  } catch (const std::exception& e) {std::cerr<<e.what()<<'\n';return 1;}
}
