// Exact physical objective model, adapted from the published C3 construction.
#include <algorithm>
#include <array>
#include <bit>
#include <sstream>
#include <iomanip>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <string>
#include <vector>
namespace fs = std::filesystem;
constexpr int N = 43, V = 287;
void need(bool b, const std::string& s) { if (!b) throw std::runtime_error(s); }
// Fourteen moving triples 0..41 and one fixed vertex 42.
// IDs 0..272: three phase orbits for each pair of triples;
// IDs 273..286: contacts to vertex 42. Internal colors are fixed.
int var(int a, int b) {
    if (a > b) std::swap(a,b);
    if (b == 42) return 273+a/3;
    int i=a/3,j=b/3;
    if (i==j) return i<7 ? -2 : -1;
    return 3*(i*(27-i)/2+j-i-1)+(b%3-a%3+3)%3;
}
struct Clause {
    std::array<int,10> vars{};
    int n=0, badcolor=0, weight=1;
    bool operator<(const Clause& o) const {
        if (badcolor!=o.badcolor) return badcolor<o.badcolor;
        if (n!=o.n) return n<o.n;
        return vars<o.vars;
    }
};
struct Model {
    std::vector<Clause> clauses;
    std::array<std::vector<int>,V> occur;
    std::uint64_t possible_red=0,possible_blue=0;
    Model() {
        std::vector<Clause> raw;
        for(int a=0;a<N;++a) for(int b=a+1;b<N;++b)
        for(int c=b+1;c<N;++c) for(int d=c+1;d<N;++d)
        for(int e=d+1;e<N;++e) {
            std::array<int,5> q{a,b,c,d,e};
            Clause x; bool red=false,blue=false;
            for(int i=0;i<5;++i) for(int j=i+1;j<5;++j) {
                int v=var(q[i],q[j]);
                if(v==-1) blue=true; else if(v==-2) red=true;
                else x.vars[x.n++]=v;
            }
            if(red && blue) continue;
            // Insertion sort on at most ten entries; avoids GCC12's spurious
            // array-bounds diagnostic in the generic heap-sort fallback.
            for(int i=1;i<x.n;++i) {
                int v=x.vars[i],j=i;
                while(j>0 && x.vars[j-1]>v) {x.vars[j]=x.vars[j-1];--j;}
                x.vars[j]=v;
            }
            x.n=static_cast<int>(std::unique(x.vars.begin(),x.vars.begin()+x.n)-x.vars.begin());
            std::fill(x.vars.begin()+x.n,x.vars.end(),0);
            need(x.n>0,"constant forbidden five-set");
            if(!red) {x.badcolor=0;raw.push_back(x);++possible_blue;}
            if(!blue) {x.badcolor=1;raw.push_back(x);++possible_red;}
        }
        std::sort(raw.begin(),raw.end());
        for(const auto& x:raw) {
            if(!clauses.empty() && !(clauses.back()<x) && !(x<clauses.back())) ++clauses.back().weight;
            else clauses.push_back(x);
        }
        for(int i=0;i<static_cast<int>(clauses.size());++i)
            for(int j=0;j<clauses[i].n;++j) occur[clauses[i].vars[j]].push_back(i);
    }
};

using Score=std::int64_t;
constexpr Score FIVE=962598;
struct Input {
    std::array<std::uint64_t,N> rows{};
    std::array<int,V> bits{};
    explicit Input(const fs::path& path) {
        std::ifstream in(path);need(bool(in),"input open");
        int n=0;need(bool(in>>n) && n==N,"input order");
        int a=0,b=0,prev_a=-1,prev_b=-1;
        while(in>>a) {
            need(bool(in>>b) && 0<=a && a<b && b<N,"input edge");
            need(a>prev_a || (a==prev_a && b>prev_b),"canonical edge order");
            rows[a]|=std::uint64_t{1}<<b;rows[b]|=std::uint64_t{1}<<a;
            prev_a=a;prev_b=b;
        }
        need(in.eof(),"input parse");bits.fill(-1);
        for(a=0;a<N;++a)for(b=a+1;b<N;++b) {
            int color=int((rows[a]>>b)&1),id=var(a,b);
            if(id<0)need(color==int(id==-2),"internal color");
            else {if(bits[id]<0)bits[id]=color;need(bits[id]==color,"orbit color");}
        }
        for(int x:bits)need(x==0 || x==1,"complete bits");
    }
};
void write_graph(const fs::path& path,const std::array<int,V>& bits) {
    std::ofstream out(path);need(bool(out),"graph output");out<<N<<'\n';
    for(int a=0;a<N;++a)for(int b=a+1;b<N;++b) {
        int id=var(a,b),red=id<0?int(id==-2):bits[id];
        if(red)out<<a<<' '<<b<<'\n';
    }
    out.close();need(bool(out),"graph write");
}
std::vector<std::array<int,4>> all_blocks() {
    std::vector<std::array<int,4>> out;
    for(int a=0;a<14;++a)for(int b=a+1;b<14;++b)
    for(int c=b+1;c<14;++c)for(int d=c+1;d<14;++d)out.push_back({a,b,c,d});
    need(out.size()==1001,"block coverage");return out;
}
std::vector<int> block_vars(const std::array<int,4>& q,int count) {
    std::vector<int> ids;
    for(int i=0;i<4;++i)for(int j=i+1;j<4;++j)
        for(int phase=0;phase<3;++phase)ids.push_back(var(3*q[i],3*q[j]+phase));
    for(int i:q)ids.push_back(var(3*i,42));
    std::sort(ids.begin(),ids.end());need(ids.size()==22,"block width");
    need(std::adjacent_find(ids.begin(),ids.end())==ids.end(),"unique block variables");
    ids.resize(count);return ids;
}
Score objective(const Model& model,const std::array<int,V>& bits) {
    Score score=0;
    for(const Clause& clause:model.clauses) {
        bool bad=true;
        for(int j=0;j<clause.n;++j)if(bits[clause.vars[j]]!=clause.badcolor){bad=false;break;}
        if(bad)score+=clause.weight;
    }
    return score;
}
struct Result {
    Score minimum=FIVE+1,maximum=0,sum=0,expected_sum=0;
    std::uint64_t multiplicity=0;
    unsigned first=0;
    int projected_events=0;
};
Result evaluate(const Model& model,const Input& input,const std::vector<int>& ids,
                const fs::path& dump) {
    int k=int(ids.size());unsigned size=1U<<k;
    std::vector<Score> table(size,0);
    std::array<int,V> local;local.fill(-1);
    for(int i=0;i<k;++i)local[ids[i]]=i;
    Result result;
    for(const Clause& clause:model.clauses) {
        unsigned positive=0,negative=0;bool possible=true;
        for(int j=0;j<clause.n;++j) {
            int id=clause.vars[j],index=local[id];
            if(index<0) {if(input.bits[id]!=clause.badcolor){possible=false;break;}}
            else if(input.bits[id]!=clause.badcolor)positive|=1U<<index;
            else negative|=1U<<index;
        }
        if(!possible)continue;
        ++result.projected_events;
        result.expected_sum+=Score(clause.weight)*(std::uint64_t{1}<<(k-std::popcount(positive|negative)));
        // Event polynomial y_positive * product_(i in negative) (1-y_i).
        unsigned sub=negative;
        for(;;) {
            table[positive|sub]+=(std::popcount(sub)%2 ? -Score(clause.weight):Score(clause.weight));
            if(!sub)break;
            sub=(sub-1)&negative;
        }
    }
    // Subset zeta transform: table[S] = sum_(T subset S) coefficient[T].
    for(unsigned bit=1;bit<size;bit<<=1)
        for(unsigned base=0;base<size;base+=2*bit)
            for(unsigned offset=0;offset<bit;++offset)table[base+bit+offset]+=table[base+offset];
    need(table[0]==123,"unmodified physical score");
    for(unsigned assignment=0;assignment<size;++assignment) {
        Score value=table[assignment];need(0<=value && value<=FIVE,"score range");
        need(value%3==0,"three-cycle five-set orbits");
        result.sum+=value;result.maximum=std::max(result.maximum,value);
        if(value<result.minimum){result.minimum=value;result.first=assignment;result.multiplicity=1;}
        else if(value==result.minimum)++result.multiplicity;
    }
    need(result.sum==result.expected_sum,"sum vs independent subcube cardinalities");
    auto bits=input.bits;
    for(int j=0;j<k;++j)bits[ids[j]]^=int((result.first>>j)&1);
    need(objective(model,bits)==result.minimum,"argmin direct model audit");
    if(!dump.empty()) {
        need(k<=10,"dump limited to controls");
        std::ofstream out(dump);need(bool(out),"table output");
        for(unsigned assignment=0;assignment<size;++assignment)out<<assignment<<' '<<table[assignment]<<'\n';
        out.close();need(bool(out),"table write");
    }
    return result;
}
int main(int argc,char** argv) {
    try {
        need(argc==7 || argc==8,"usage: block BASELINE OUT START COUNT BITS EXPECTED_SCORE [DUMP_TABLE]");
        auto start=std::chrono::steady_clock::now();
        Input input(argv[1]);fs::path work(argv[2]);
        int begin=std::stoi(argv[3]),count=std::stoi(argv[4]),k=std::stoi(argv[5]);
        // Argument6 is the explicit expected baseline score, preventing wrong-parent runs.
        need(std::stoi(argv[6])==123,"baseline contract");
        need(0<=begin && count>0 && begin+count<=1001 && 1<=k && k<=22,"range/width");
        need(argc!=8 || (count==1 && k<=10),"control dump scope");
        need(!fs::exists(work),"fresh output directory");fs::create_directories(work);
        Model model;need(objective(model,input.bits)==123,"baseline model score");
        auto blocks=all_blocks();
        std::ofstream log(work/"blocks.tsv");need(bool(log),"log output");
        log<<"block\ta\tb\tc\td\tbits\tminimum\tfirst_mask\tmultiplicity\tmaximum\tsum\tprojected_events\n";
        Score best=123;int best_block=-1;unsigned best_mask=0;int done=0;
        write_graph(work/"best.edges",input.bits);
        for(int index=begin;index<begin+count;++index) {
            if(fs::exists(work/"STOP"))break;
            const auto& q=blocks[index];auto ids=block_vars(q,k);
            Result result=evaluate(model,input,ids,argc==8 ? fs::path(argv[7]):fs::path());
            if(result.minimum<best) {
                best=result.minimum;best_block=index;best_mask=result.first;auto bits=input.bits;
                for(int j=0;j<k;++j)bits[ids[j]]^=int((best_mask>>j)&1);
                write_graph(work/"best.edges",bits);
            }
            log<<index;for(int v:q)log<<'\t'<<v;
            log<<'\t'<<k<<'\t'<<result.minimum<<'\t'<<result.first<<'\t'<<result.multiplicity
               <<'\t'<<result.maximum<<'\t'<<result.sum<<'\t'<<result.projected_events<<'\n';
            log.flush();need(bool(log),"row write");++done;
            if(done%25==0 || result.minimum<123)std::cout<<"block "<<index<<" minimum "<<result.minimum<<" global "<<best<<std::endl;
            if(best==0)break;
        }
        double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
        std::ofstream status(work/"status.json");need(bool(status),"status output");
        status<<"{\"complete_requested_range\":"<<(done==count?"true":"false")
              <<",\"full_family\":"<<(begin==0 && done==1001 && k==22?"true":"false")
              <<",\"start\":"<<begin<<",\"requested\":"<<count<<",\"done\":"<<done
              <<",\"bits\":"<<k<<",\"best_score\":"<<best<<",\"best_block\":"<<best_block
              <<",\"best_mask\":"<<best_mask<<",\"seconds\":"<<std::setprecision(12)<<seconds<<"}\n";
        status.close();need(bool(status),"status write");
        std::cout<<"COMPLETE "<<done<<'/'<<count<<" best "<<best<<" seconds "<<seconds<<std::endl;
    }catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}
}
