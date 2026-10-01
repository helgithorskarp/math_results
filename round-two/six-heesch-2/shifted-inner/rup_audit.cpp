// Exact deletion-free RUP reader. No solver library is linked.
// Literals/indices are bounded by checked DIMACS headers and vector sizes.
#include <algorithm>
#include <array>
#include <chrono>
#include <fstream>
#include <iostream>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
#include <sys/resource.h>

using Clause = std::vector<int>;
void require(bool condition, const std::string &message) {
    if (!condition) throw std::runtime_error(message);
}

struct Reader {
    int variables, original=0, head=0, root_conflict=-1, stamp=0;
    std::vector<Clause> clauses;
    std::vector<std::array<int,2>> positions;
    std::vector<std::vector<int>> watches;
    std::vector<int> values, reasons, trail, seen_variables, seen_clauses;
    std::vector<std::set<int>> dependencies;

    explicit Reader(int n):variables(n),watches(2*n),values(n+1,0),reasons(n+1,-1),
        seen_variables(n+1,0) { require(n>0 && n<10000000,"Invalid variable count"); }
    int wi(int literal) const { return 2*(std::abs(literal)-1)+(literal<0); }
    int value(int literal) const { return literal>0 ? values[literal] : -values[-literal]; }
    bool assign(int literal, int reason) {
        int v=value(literal);
        if (v) return v==1;
        values[std::abs(literal)]=literal>0 ? 1 : -1;
        reasons[std::abs(literal)]=reason;
        trail.push_back(literal); return true;
    }
    void validate(const Clause &clause) const {
        std::set<int> unique;
        for(int literal:clause) {
            require(literal!=0 && literal>=-variables && literal<=variables,"Invalid literal");
            require(unique.insert(literal).second,"Duplicate literal");
        }
    }
    int propagate() {
        while (head<int(trail.size())) {
            int false_literal=-trail[head++];
            auto &row=watches[wi(false_literal)];
            size_t i=0;
            while (i<row.size()) {
                int number=row[i]; auto &p=positions[number]; const auto &c=clauses[number];
                int side=c[p[0]]==false_literal ? 0 : 1;
                require(c[p[side]]==false_literal,"Watch invariant failed");
                int other=c[p[1-side]];
                if(value(other)==1) {++i;continue;}
                int replacement=-1;
                for(int j=0;j<int(c.size());++j)
                    if(j!=p[0] && j!=p[1] && value(c[j])!=-1) {replacement=j;break;}
                if(replacement>=0) {
                    p[side]=replacement; row[i]=row.back();row.pop_back();
                    watches[wi(c[replacement])].push_back(number);
                } else if(!assign(other,number)) return number;
                else ++i;
            }
        }
        return -1;
    }
    int install(const Clause &c, bool run=true) {
        validate(c); int number=int(clauses.size());clauses.push_back(c);
        seen_clauses.push_back(0);
        if(c.empty()) {positions.push_back({0,0});return number;}
        int a=-1,b=-1;
        for(int i=0;i<int(c.size());++i) if(value(c[i])!=-1) {
            if(a<0)a=i;else if(b<0)b=i;
        }
        bool all_false=a<0;
        if(a<0)a=0;
        bool unit=b<0;
        if(b<0)b=c.size()>1 ? (a==0 ? 1 : 0) : a;
        positions.push_back({a,b});
        if(c.size()>1) {
            watches[wi(c[a])].push_back(number);watches[wi(c[b])].push_back(number);
        }
        if(all_false)return number;
        if(unit && !assign(c[a],number))return number;
        return run ? propagate() : -1;
    }
    void undo(size_t length) {
        for(size_t i=length;i<trail.size();++i) {
            int v=std::abs(trail[i]);values[v]=0;reasons[v]=-1;
        }
        trail.resize(length);head=int(length);
    }
    std::set<int> support(int conflict, int fact=0) {
        ++stamp;std::vector<int> todo;
        if(conflict>=0)todo.push_back(conflict);
        if(fact && reasons[fact]>=0)todo.push_back(reasons[fact]);
        std::set<int> used;
        while(!todo.empty()) {
            int number=todo.back();todo.pop_back();
            if(seen_clauses[number]==stamp)continue;
            seen_clauses[number]=stamp;
            if(number>=original)used.insert(number-original);
            for(int literal:clauses[number]) if(value(literal)==-1) {
                int v=std::abs(literal);
                if(seen_variables[v]==stamp)continue;
                seen_variables[v]=stamp;
                if(reasons[v]>=0)todo.push_back(reasons[v]);
            }
        }
        return used;
    }
    bool addition(const Clause &c,std::set<int> &used) {
        validate(c);
        if(root_conflict>=0) {used=support(root_conflict);return true;}
        size_t length=trail.size(); int conflict=-1,fact=0;
        for(int literal:c) if(!assign(-literal,-1)) {fact=std::abs(literal);break;}
        if(!fact)conflict=propagate();
        bool rup=fact || conflict>=0;
        if(rup)used=support(conflict,fact);
        undo(length);require(rup,"Addition is not RUP");
        if(c.empty())return true;
        dependencies.push_back(used);root_conflict=install(c);return false;
    }
};

Clause parse_clause(const std::string &line) {
    std::istringstream s(line);Clause c;long long value;bool end=false;
    while(s>>value) {
        require(value>=-10000000 && value<=10000000,"Literal outside parser bounds");
        if(value==0){end=true;break;}c.push_back(int(value));
    }
    require(end,"Missing clause terminator");std::string extra;
    require(!(s>>extra),"Data after clause terminator");return c;
}

bool naive_rup(const std::vector<Clause>& formula,const Clause &candidate) {
    std::vector<int> values(3,0);
    for(int literal:candidate) {
        int v=std::abs(literal),wanted=literal>0 ? -1 : 1;
        if(values[v] && values[v]!=wanted)return true;
        values[v]=wanted;
    }
    bool changed=true;
    while(changed) {
        changed=false;
        for(const Clause &c:formula) {
            bool satisfied=false;int free=0,last=0;
            for(int literal:c) {
                int value=literal>0 ? values[literal] : -values[-literal];
                if(value==1)satisfied=true;
                if(value==0){++free;last=literal;}
            }
            if(satisfied)continue;
            if(free==0)return true;
            if(free==1){values[std::abs(last)]=last>0 ? 1 : -1;changed=true;}
        }
    }
    return false;
}

void controls() {
    Reader r(3);r.install({1,2},false);r.install({-1,3},false);r.install({-2,3},false);
    r.original=int(r.clauses.size());r.root_conflict=r.propagate();std::set<int> used;
    require(!r.addition({3},used),"Control finished prematurely");
    for(Clause c:std::vector<Clause>{{},{-3},{4},{0}}) {
        bool rejected=false;try{r.addition(c,used);}catch(const std::runtime_error&){rejected=true;}
        require(rejected,"False/malformed control accepted");
    }
    Reader bad(1);int conflict=bad.install({1},false);require(conflict<0,"Bad control setup");
    conflict=bad.install({-1},false);require(conflict>=0,"Input contradiction missed");
    const std::vector<Clause> possibilities={{1},{-1},{2},{-2},{1,2},{1,-2},{-1,2},{-1,-2}};
    std::vector<Clause> candidates=possibilities;candidates.push_back({});
    for(int mask=0;mask<256;++mask)for(const Clause &candidate:candidates) {
        std::vector<Clause> formula;
        for(int j=0;j<8;++j)if(mask&(1<<j))formula.push_back(possibilities[j]);
        Reader test(2);
        for(const Clause &clause:formula) {
            int found=test.install(clause,false);
            if(found>=0 && test.root_conflict<0)test.root_conflict=found;
        }
        test.original=int(test.clauses.size());
        if(test.root_conflict<0)test.root_conflict=test.propagate();
        bool accepted=true;
        try{test.addition(candidate,used);}catch(const std::runtime_error&){accepted=false;}
        require(accepted==naive_rup(formula,candidate),"Exhaustive two-variable RUP disagreement");
    }
}

int main(int argc,char **argv) {
    try {
        controls();
        if(argc==2 && std::string(argv[1])=="--self-test") {
            std::cout<<"{\"exhaustive_controls\":2304,\"malformed_or_false_controls\":4}\n";return 0;
        }
        require(argc==4,"Usage: rup_audit INPUT.cnf ADDITIONS.rup CORE.rup");
        auto start=std::chrono::steady_clock::now();
        std::ifstream input(argv[1]);require(bool(input),"Cannot open CNF");std::string line;
        int n=0,count=0;
        while(std::getline(input,line)) {
            if(line.empty() || line[0]=='c')continue;
            std::istringstream header(line);std::string p,cnf;
            require(bool(header>>p>>cnf>>n>>count) && p=="p" && cnf=="cnf","Invalid CNF header");break;
        }
        require(count>0 && count<10000000,"Invalid clause count");Reader reader(n);
        while(std::getline(input,line)) {
            if(line.empty() || line[0]=='c')continue;
            int conflict=reader.install(parse_clause(line),false);
            if(conflict>=0 && reader.root_conflict<0)reader.root_conflict=conflict;
        }
        reader.original=int(reader.clauses.size());require(reader.original==count,"CNF count mismatch");
        if(reader.root_conflict<0)reader.root_conflict=reader.propagate();
        std::ifstream proof(argv[2]);require(bool(proof),"Cannot open proof");
        std::vector<Clause> additions;std::set<int> goal;bool complete=false;int checked=0;
        while(std::getline(proof,line)) {
            require(!line.empty() && line[0]!='d',"Proof must contain additions only");
            Clause clause=parse_clause(line);++checked;
            if(reader.addition(clause,goal)){complete=true;break;}
            additions.push_back(clause);
            double elapsed=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
            require(elapsed<=120,"120-second native audit bound");
        }
        require(complete,"Proof did not derive a contradiction");
        std::vector<int> pending(goal.begin(),goal.end());std::set<int> required(goal);
        while(!pending.empty()) {
            int i=pending.back();pending.pop_back();require(i>=0 && i<int(additions.size()),"Invalid dependency");
            for(int p:reader.dependencies[i]) {
                require(p<i,"Nonprior proof dependency");
                if(required.insert(p).second)pending.push_back(p);
            }
        }
        std::ofstream core(argv[3]);require(bool(core),"Cannot write core");
        for(int i:required) {for(int literal:additions[i])core<<literal<<' ';core<<"0\n";}
        core<<"0\n";core.close();
        struct rusage usage;require(getrusage(RUSAGE_SELF,&usage)==0,"Cannot read resource usage");
        double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
        std::cout<<"{\"complete\":true,\"input_variables\":"<<n<<",\"input_clauses\":"<<count
                 <<",\"checked_additions\":"<<checked<<",\"core_additions\":"<<required.size()+1
                 <<",\"seconds\":"<<seconds<<",\"max_rss_kib\":"<<usage.ru_maxrss<<"}\n";
        return 0;
    } catch(const std::exception &e) {std::cerr<<e.what()<<'\n';return 1;}
}
