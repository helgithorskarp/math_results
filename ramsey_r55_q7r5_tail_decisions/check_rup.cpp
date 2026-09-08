// Strict forward multiset RUP checker. No solver code imported.
// Adapted from the repository catalog-switch checker; RAT is disabled.
#include <algorithm>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

using Clause=std::vector<int>;
void demand(bool test,const std::string& message) {if(!test) throw std::runtime_error(message);}
struct Entry {Clause literals;std::uint64_t copies=0;};
struct Database {
    std::vector<Entry> entries;
    std::map<Clause,std::size_t> positions;
    int variables=0;
    void add(Clause row) {
        std::sort(row.begin(),row.end());
        auto found=positions.find(row);
        if(found==positions.end()) {
            positions.emplace(row,entries.size());entries.push_back({row,1});
        } else ++entries[found->second].copies;
        for(int x:row) variables=std::max(variables,std::abs(x));
    }
    bool remove(Clause row) {
        std::sort(row.begin(),row.end());
        auto found=positions.find(row);
        if(found==positions.end() || entries[found->second].copies==0) return false;
        --entries[found->second].copies;return true;
    }
    bool rup(const Clause& candidate) const {
        int n=variables;
        for(int x:candidate) n=std::max(n,std::abs(x));
        std::vector<signed char> values(static_cast<std::size_t>(n)+1,0);
        for(int x:candidate) {
            int v=std::abs(x);signed char bit=static_cast<signed char>(x>0 ? -1:1);
            if(values[v] && values[v]!=bit) return true;
            values[v]=bit;
        }
        bool changed=true;
        while(changed) {
            changed=false;
            for(const auto& entry:entries) {
                if(!entry.copies) continue;
                bool satisfied=false;int remaining=0,last=0;
                for(int x:entry.literals) {
                    auto value=values[std::abs(x)];
                    if(value==0) {++remaining;last=x;}
                    else if((value>0)==(x>0)) {satisfied=true;break;}
                }
                if(satisfied) continue;
                if(!remaining) return true;
                if(remaining==1) {values[std::abs(last)]=static_cast<signed char>(last>0?1:-1);changed=true;}
            }
        }
        return false;
    }

};

Clause parse(const std::string& text) {
    std::istringstream input(text);long long value=0;Clause row;bool ended=false;
    while(input>>value) {
        demand(!ended,"Text after clause terminator");
        if(value==0) {ended=true;continue;}
        demand(value>=-1000000 && value<=1000000,"Literal out of supported bound");
        row.push_back(static_cast<int>(value));
    }
    demand(input.eof() && ended,"Malformed clause");
    Clause sorted=row;std::sort(sorted.begin(),sorted.end());
    demand(std::adjacent_find(sorted.begin(),sorted.end())==sorted.end(),"Duplicate literal");
    for(int x:row) demand(!std::binary_search(sorted.begin(),sorted.end(),-x),"Tautological clause");
    return row;
}

std::map<std::string,std::uint64_t> proof(Database db,const std::vector<std::string>& lines) {
    std::map<std::string,std::uint64_t> counts;bool empty=false;
    std::size_t number=0;
    for(const auto& line:lines) {
        ++number;demand(!empty,"Proof continues after empty clause");
        bool deleted=line.rfind("d ",0)==0;
        Clause row=parse(deleted?line.substr(2):line);
        if(deleted) {++counts["deletions"];if(!db.remove(row)) ++counts["absent_deletions"];continue;}
        ++counts["additions"];
        demand(db.rup(row),"RUP failed at line "+std::to_string(number));
        ++counts["rup_additions"];
        db.add(row);empty=row.empty();
    }
    demand(empty,"No checked empty clause");return counts;
}

bool sat(const Database& db,int mask) {
    for(const auto& entry:db.entries) if(entry.copies) {
        bool good=false;
        for(int x:entry.literals) if(((mask>>(std::abs(x)-1))&1)==(x>0)) good=true;
        if(!good) return false;
    }
    return true;
}

void controls() {
    std::vector<Clause> possible;
    for(int a=-1;a<=1;++a) for(int b=-1;b<=1;++b) {
        Clause row;if(a)row.push_back(a);if(b)row.push_back(2*b);possible.push_back(row);
    }
    std::uint64_t checks=0,accepted=0;
    for(int mask=0;mask<512;++mask) {
        Database db;for(int i=0;i<9;++i)if(mask&(1<<i))db.add(possible[i]);
        for(const auto& row:possible) {
            bool r=db.rup(row);++checks;if(r)++accepted;
            for(int model=0;model<4;++model)if(sat(db,model)) {
                bool holds=false;for(int x:row)if(((model>>(std::abs(x)-1))&1)==(x>0))holds=true;
                demand(!r||holds,"Unsound RUP control");
            }
        }
    }
    Database square;for(int a:{-1,1})for(int b:{-2,2})square.add({a,b});
    auto result=proof(square,{"1 0","1 0","d 1 0","0"});
    demand(result["additions"]==3,"Multiplicity control");
    Database free;bool rejected=false;
    try{proof(free,{"1 0","0"});}catch(const std::runtime_error&){rejected=true;}
    demand(rejected,"Unproved unit accepted");
    std::cout<<"{\"status\":\"PASS\",\"formulas\":512,\"checks\":"<<checks<<",\"accepted\":"<<accepted<<"}\n";
}

int main(int argc,char** argv) {
    try {
        if(argc==2 && std::string(argv[1])=="--controls") {controls();return 0;}
        demand(argc==3,"Usage: check-drat core.cnf proof.drat, or --controls");
        std::ifstream core(argv[1]),trace(argv[2]);demand(core.good() && trace.good(),"Cannot read inputs");
        std::string line,p,cnf,extra;int variables=0;std::size_t count=0;
        demand(static_cast<bool>(std::getline(core,line)),"Missing header");
        std::istringstream header(line);
        bool dimensions=static_cast<bool>(header>>p>>cnf>>variables>>count);
        demand(dimensions && p=="p" && cnf=="cnf" && variables>0 && variables<=1000000 && !(header>>extra),"Bad DIMACS header");
        Database db;std::size_t actual=0;
        while(std::getline(core,line)) {
            Clause row=parse(line);for(int x:row) demand(std::abs(x)<=variables,"Input literal exceeds header");
            db.add(row);++actual;
        }
        demand(actual==count,"DIMACS count mismatch");
        std::vector<std::string> lines;while(std::getline(trace,line)) lines.push_back(line);
        auto result=proof(db,lines);
        std::cout<<'{';bool first=true;
        for(const auto& item:result) {if(!first) std::cout<<',';first=false;std::cout<<'"'<<item.first<<"\":"<<item.second;}
        std::cout<<"}\n";
    } catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 1;}
}
