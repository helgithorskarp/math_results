// six-reviewer-3: generic signed-CNF audit kernel, not an NAE-mask search.
// C++17 standard library. Exact Boolean computation; time is a stop budget.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using Clock = std::chrono::steady_clock;
using Clauses = std::vector<std::vector<int>>;

void require(bool condition, const char* message) {
    if (!condition) throw std::runtime_error(message);
}
struct Incomplete {};

struct Search {
    Clauses clauses;
    std::vector<int> values, trail;
    std::vector<std::pair<int,int>> positions;
    std::vector<std::vector<int>> watches;
    std::size_t processed = 0;
    std::uint64_t nodes = 0, conflicts = 0, units = 0, limit;
    Clock::time_point began = Clock::now();
    double seconds;
    bool empty = false;

    Search(Clauses cs, int n, std::uint64_t budget, double time_budget):
        clauses(std::move(cs)), values(static_cast<std::size_t>(n+1),0),
        watches(static_cast<std::size_t>(2*n+2)), limit(budget),
        seconds(time_budget) {
        std::sort(clauses.begin(),clauses.end(),[](const auto& a,const auto& b) {
            if (a.size()!=b.size()) return a.size()<b.size();
            return a<b;
        });
        for (std::size_t i=0; i<clauses.size(); ++i) {
            const auto& clause=clauses[i];
            positions.emplace_back(0,clause.size()>1 ? 1 : 0);
            if (clause.empty()) { empty=true; continue; }
            watches[key(clause[0])].push_back(static_cast<int>(i));
            if (clause.size()>1)
                watches[key(clause[1])].push_back(static_cast<int>(i));
        }
    }
    static std::size_t key(int literal) {
        return static_cast<std::size_t>(2*std::abs(literal)+(literal<0 ? 1 : 0));
    }
    int value(int literal) const {
        const int v=values[static_cast<std::size_t>(std::abs(literal))];
        return literal>0 ? v : -v;
    }
    bool assign(int literal) {
        const int v=value(literal);
        if (v) return v==1;
        values[static_cast<std::size_t>(std::abs(literal))]=literal>0 ? 1 : -1;
        trail.push_back(literal);
        return true;
    }
    void restore(std::size_t checkpoint) {
        for (std::size_t i=checkpoint; i<trail.size(); ++i)
            values[static_cast<std::size_t>(std::abs(trail[i]))]=0;
        trail.resize(checkpoint);
        processed=std::min(processed,checkpoint);
    }
    bool propagate() {
        while (processed<trail.size()) {
            const int false_literal=-trail[processed++];
            auto& pending=watches[key(false_literal)];
            std::size_t index=0;
            while (index<pending.size()) {
                const auto ci=static_cast<std::size_t>(pending[index]);
                const auto& clause=clauses[ci];
                auto& pair=positions[ci];
                int& position=clause[static_cast<std::size_t>(pair.first)]==
                    false_literal ? pair.first : pair.second;
                const int other=(&position==&pair.first) ? pair.second : pair.first;
                require(clause[static_cast<std::size_t>(position)]==false_literal,
                        "stale watch");
                if (value(clause[static_cast<std::size_t>(other)])==1) {
                    ++index; continue;
                }
                int replacement=-1;
                for (std::size_t j=0; j<clause.size(); ++j)
                    if (static_cast<int>(j)!=other && value(clause[j])!=-1) {
                        replacement=static_cast<int>(j); break;
                    }
                if (replacement>=0) {
                    position=replacement;
                    const int clause_id=pending[index];
                    pending[index]=pending.back();
                    pending.pop_back();
                    watches[key(clause[static_cast<std::size_t>(replacement)])]
                        .push_back(clause_id);
                    continue;
                }
                const int unit=clause[static_cast<std::size_t>(other)];
                if (value(unit)==-1) { ++conflicts; return false; }
                require(assign(unit),"inconsistent unit");
                ++units; ++index;
            }
        }
        return true;
    }
    bool visit() {
        ++nodes;
        if (nodes>limit ||
            std::chrono::duration<double>(Clock::now()-began).count()>=seconds)
            throw Incomplete{};
        if (!propagate()) return false;
        std::vector<int> scores(values.size(),0), signs(values.size(),0);
        int considered=0;
        for (const auto& clause:clauses) {
            if (std::any_of(clause.begin(),clause.end(),
                            [this](int lit){return value(lit)==1;})) continue;
            int count=0;
            for (int lit:clause) if (value(lit)==0) ++count;
            require(count>0,"missed conflict");
            const int weight=1<<std::max(0,7-count);
            for (int lit:clause) if (value(lit)==0) {
                const auto variable=static_cast<std::size_t>(std::abs(lit));
                scores[variable]+=weight;
                signs[variable]+=lit>0 ? weight : -weight;
            }
            if (++considered==24) break;
        }
        std::size_t choice=0;
        for (std::size_t i=1; i<scores.size(); ++i)
            if (scores[i]>scores[choice]) choice=i;
        if (choice==0) {
            for (std::size_t i=1; i<values.size(); ++i)
                if (!values[i]) values[i]=-1;
            for (const auto& clause:clauses)
                require(std::any_of(clause.begin(),clause.end(),
                        [this](int lit){return value(lit)==1;}),"bad SAT witness");
            return true;
        }
        const int preferred=signs[choice]>=0 ?
            static_cast<int>(choice) : -static_cast<int>(choice);
        const auto checkpoint=trail.size();
        for (int literal:{preferred,-preferred}) {
            require(assign(literal),"branch variable already assigned");
            if (visit()) return true;
            restore(checkpoint);
        }
        return false;
    }
    bool solve() {
        if (empty) { ++conflicts; return false; }
        for (const auto& clause:clauses)
            if (clause.size()==1 && !assign(clause[0])) {
                ++conflicts; return false;
            }
        return visit();
    }
};

int main(int argc,char** argv) {
    try {
        std::uint64_t limit=1000000;
        double seconds=120;
        for (int i=1; i<argc; i+=2) {
            require(i+1<argc,"option lacks value");
            const std::string option=argv[i];
            if (option=="--nodes") limit=std::stoull(argv[i+1]);
            else if (option=="--seconds") seconds=std::stod(argv[i+1]);
            else throw std::runtime_error("unknown option");
        }
        require(seconds>=0 && seconds<=120 && limit<=1000000,
                "unsupported budget");
        int variables=0, count=0;
        while (std::cin>>variables) {
            require(static_cast<bool>(std::cin>>count),"truncated header");
            require(variables>=1 && variables<=62 && count>=0 && count<=100000,
                    "unsupported dimensions");
            Clauses clauses;
            for (int i=0; i<count; ++i) {
                std::vector<int> clause;
                int literal=0;
                do {
                    require(static_cast<bool>(std::cin>>literal),"truncated clause");
                    require(literal>=-variables && literal<=variables,"bad literal");
                    if (literal) clause.push_back(literal);
                } while (literal);
                for (std::size_t j=0; j<clause.size(); ++j)
                    require(std::find(clause.begin(),clause.begin()+
                            static_cast<std::ptrdiff_t>(j),clause[j])==
                            clause.begin()+static_cast<std::ptrdiff_t>(j),
                            "duplicate literal");
                clauses.push_back(std::move(clause));
            }
            Search search(std::move(clauses),variables,limit,seconds);
            const bool sat=search.solve();
            std::cout<<"{\"status\":\""<<(sat ? "SAT" : "UNSAT")
                     <<"\",\"nodes\":"<<search.nodes
                     <<",\"conflicts\":"<<search.conflicts
                     <<",\"propagated_units\":"<<search.units;
            if (sat) {
                std::cout<<",\"witness\":[";
                for (int i=1; i<=variables; ++i) {
                    if (i>1) std::cout<<',';
                    std::cout<<(search.values[static_cast<std::size_t>(i)]==1 ? 1:0);
                }
                std::cout<<']';
            }
            std::cout<<"}\n";
        }
        require(std::cin.eof(),"bad input stream");
        return 0;
    } catch (const Incomplete&) {
        std::cout<<"{\"status\":\"INCOMPLETE\"}\n";
        return 2;
    } catch (const std::exception& error) {
        std::cerr<<error.what()<<'\n';
        return 3;
    }
}
