// Definition-level census of physical supports, and a separate queue consumer.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>
using V = std::vector<int>;
using U = std::uint64_t;
void need(bool b, const char* s) { if (!b) throw std::runtime_error(s); }
U choose(int n,int k) {
    if(k<0||n<k)return 0;
    U a=1;for(int i=1;i<=k;++i)a=a*static_cast<U>(n-i+1)/static_cast<U>(i);return a;
}
U rank_set(const V& s) { U a=0;for(std::size_t i=0;i<s.size();++i)a+=choose(s[i],static_cast<int>(i)+1);return a; }
V canonical(V a) {std::sort(a.begin(),a.end());return a;}
std::array<std::array<int,43>,43> var{};
std::vector<std::pair<int,int>> edge(857,{-1,-1});
void indexing() {
    int k=2;
    for(int i=0;i<43;++i)for(int j=i+1;j<43;++j)
        if(!(i<32&&j<32&&i/4==j/4)){var[i][j]=var[j][i]=k;edge[k++]={i,j};}
    need(k==857&&var[32][33]==802&&var[41][42]==856,"physical numbering");
}
U five_count(int r,int color) {
    // Count selections by occupied fixed blocks, with an unrestricted 11-core.
    std::array<U,6> a{};for(int k=0;k<=5;++k)a[k]=choose(11,k);
    for(int b=0;b<8;++b){std::array<U,6> out{};
        for(int k=0;k<=5;++k)for(int j=0;j<=4&&j<=k;++j)
            if((b<r)==(color==1)||j<=1)out[k]+=a[k-j]*choose(4,j);
        a=out;
    }return a[5];
}
struct Reader {
    std::ifstream f; U read=0, nc=0;int nv=0;
    explicit Reader(const char* path):f(path){
        std::string p,c,extra,line;need(bool(std::getline(f,line)),"missing header");
        std::istringstream s(line);need(bool(s>>p>>c>>nv>>nc)&&p=="p"&&c=="cnf"&&!(s>>extra),"header");
    }
    V next(){
        std::string line,extra;need(bool(std::getline(f,line)),"truncated CNF");
        std::istringstream s(line);int x;V out;bool zero=false;
        while(s>>x){if(x==0){zero=true;break;}need(x>=-nv&&x<=nv,"literal range");out.push_back(x);}
        need(zero&&!(s>>extra),"clause syntax");++read;return out;
    }
    void finish(){std::string line;need(read==nc&&!std::getline(f,line),"clause count/trailing data");}
};
void master(int r,const char* path) {
    need(r>=5&&r<=8,"q8 r range");indexing();Reader rd(path);
    std::vector<std::pair<int,int>> pairs;
    for(int b=1;b<7;++b)if((b<r)==(b+1<r))pairs.emplace_back(b,b+1);
    need(rd.nv==856+15*static_cast<int>(pairs.size()),"auxiliary count");
    need(rd.next()==V{1},"constant");
    std::set<V> roots;
    for(int k=0;k<2520;++k){V c=rd.next();need(c.size()==8,"root width");
        int block=-1;std::map<int,int> values;std::set<std::pair<int,int>> seen;
        for(int l:c){int v=std::abs(l);need(v>=2&&v<=856,"root physical variable");auto [a,b]=edge[v];
            need(a<4&&b>=4&&b<32,"root support");if(block<0)block=b/4;need(block==b/4,"root block");
            need(seen.insert({a,b%4}).second,"root repeated edge");values[b%4]|=(l<0?1:0)<<a;
        }
        need(values.size()==2,"root columns");auto x=values.begin(),y=std::next(x);
        need(y->first==x->first+1&&x->second<y->second,"root forbidden word pair");
        need(roots.insert(canonical(c)).second,"duplicate root clause");
    }
    std::array<std::vector<bool>,2> covered={std::vector<bool>(962598),std::vector<bool>(962598)};
    U red=five_count(r,1),blue=five_count(r,0);std::array<U,2> actual{};
    for(U k=0;k<red+blue;++k){V c=rd.next();need(!c.empty(),"empty five clause");
        int color=c[0]<0?1:0;std::set<int> vertices;std::set<int> vars;
        for(int l:c){int v=std::abs(l);need(v>=2&&v<=856&&((l<0)?1:0)==color,"five literal type");
            auto [a,b]=edge[v];vertices.insert(a);vertices.insert(b);need(vars.insert(v).second,"repeated five literal");}
        need(vertices.size()==5,"five physical support");V s(vertices.begin(),vertices.end());std::set<int> required;
        for(int i=0;i<5;++i)for(int j=i+1;j<5;++j){int a=s[i],b=s[j];
            if(var[a][b])required.insert(var[a][b]);else need(int(a/4<r)==color,"incompatible fixed edge");}
        need(required==vars,"missing physical five edge");U rank=rank_set(s);
        need(!covered[color][rank],"duplicate physical five");covered[color][rank]=true;++actual[color];
    }
    need(actual[1]==red&&actual[0]==blue,"complete five support counts");
    U closure=0;for(int k=0;k<=4;++k)closure+=(U(1)<<(2*k))*choose(8-r,k)*choose(11,4-k);
    std::set<U> fours;
    for(U k=0;k<closure;++k){V c=rd.next();need(c.size()==6,"red4 width");std::set<int> vertices,vs;
        for(int l:c){need(l<=-2&&l>=-856,"red4 sign/range");auto [a,b]=edge[-l];need(a>=4*r,"red4 tail");vertices.insert(a);vertices.insert(b);need(vs.insert(-l).second,"red4 duplicate");}
        need(vertices.size()==4,"red4 support");V s(vertices.begin(),vertices.end());
        for(int i=0;i<4;++i)for(int j=i+1;j<4;++j)need(var[s[i]][s[j]]&&vs.count(var[s[i]][s[j]]),"red4 all pairs");
        need(fours.insert(rank_set(s)).second,"duplicate red4");
    }
    int first=857;U truth=0;
    for(auto [a,b]:pairs){int prefix=1;
        for(int bit=15;bit>=0;--bit){int x=var[bit/4][4*a+bit%4],y=var[bit/4][4*b+bit%4];
            need(canonical(rd.next())==canonical(V{-prefix,x,-y}),"order first difference");
            if(bit){int z=first++;std::vector<V> gates;for(int k=0;k<5;++k)gates.push_back(rd.next());
                std::set<int> allowed={prefix,x,y,z};
                for(const V& c:gates){need(!c.empty(),"empty prefix gate");for(int l:c)need(allowed.count(std::abs(l)),"prefix gate variable");}
                for(int assignment=0;assignment<16;++assignment){std::map<int,bool> v={{prefix,bool(assignment&1)},{x,bool(assignment&2)},{y,bool(assignment&4)},{z,bool(assignment&8)}};
                    bool sat=true;for(const V& c:gates){bool ok=false;for(int l:c)ok|=v[std::abs(l)]==(l>0);sat&=ok;}
                    need(sat==(v[z]==(v[prefix]&&(v[x]==v[y]))),"prefix gate semantics");++truth;
                }prefix=z;
            }
        }
    }
    rd.finish();need(first-1==rd.nv,"last auxiliary");
    std::cout<<"{\"r\":"<<r<<",\"clauses\":"<<rd.read<<",\"red5\":"<<red<<",\"blue5\":"<<blue
        <<",\"red4\":"<<closure<<",\"root_clauses\":2520,\"prefix_truth_assignments\":"<<truth<<",\"status\":\"VERIFIED\"}\n";
}
U read_le(std::istream& f,int bytes){U a=0;for(int i=0;i<bytes;++i){int c=f.get();need(c>=0,"truncated binary stream");a|=U(c)<<(8*i);}return a;}
void magic(std::istream& f,const std::string& s){for(unsigned char c:s)need(f.get()==c,"binary magic");}
void queue_audit(const char* catpath,const char* corepath,const char* jobpath){
    std::ifstream cat(catpath,std::ios::binary),core(corepath,std::ios::binary),jobs(jobpath,std::ios::binary);
    magic(core,"Q8CORE1\n");need(read_le(core,4)==546356,"core count");
    std::vector<U> words;std::set<U> unique;U four_checks=0;
    std::array<std::array<int,11>,11> lex{};int ei=0;
    for(int i=0;i<11;++i)for(int j=i+1;j<11;++j)lex[i][j]=lex[j][i]=ei++;
    for(int c=0;c<546356;++c){std::string line;need(bool(std::getline(cat,line))&&line.size()==11&&line[0]=='J',"graph6 record");
        for(unsigned char x:line)need(x>=63&&x<=126,"graph6 byte");
        need(((line[10]-63)&31)==0,"graph6 padding");
        std::array<std::array<bool,11>,11> adj{};int k=0;
        for(int j=1;j<11;++j)for(int i=0;i<j;++i){bool b=((line[1+k/6]-63)>>(5-k%6))&1;adj[i][j]=adj[j][i]=b;++k;}
        U word=read_le(core,8);need(word<(U(1)<<55)&&unique.insert(word).second,"core word/uniqueness");
        for(int i=0;i<11;++i)for(int j=i+1;j<11;++j)need(bool((word>>lex[i][j])&1)==adj[i][j],"core physical edge mismatch");
        for(int a=0;a<11;++a)for(int b=a+1;b<11;++b)for(int d=b+1;d<11;++d)for(int e=d+1;e<11;++e){
            int sum=adj[a][b]+adj[a][d]+adj[a][e]+adj[b][d]+adj[b][e]+adj[d][e];need(sum>0&&sum<6,"catalog is not Ramsey(4,4)");++four_checks;}
        words.push_back(word);
    }
    need(cat.peek()==EOF&&core.peek()==EOF,"catalog/core trailing bytes");
    magic(jobs,std::string("Q8JOB1\n\0",8));need(read_le(jobs,4)==2185424,"job count");U checked=0;
    for(int r=5;r<=8;++r)for(int c=0;c<546356;++c){
        need(read_le(jobs,1)==U(r)&&read_le(jobs,4)==U(c),"queue gap, duplicate or foreign task");
        U word=read_le(jobs,8);need(word==words[c],"queue core routing");U back=0;
        for(int i=0;i<11;++i)for(int j=i+1;j<11;++j){int physical=802+lex[i][j];int literal=(word>>lex[i][j]&1)?physical:-physical;
            need(std::abs(literal)>=802&&std::abs(literal)<=856,"worker core variable");if(literal>0)back|=U(1)<<(std::abs(literal)-802);++checked;}
        need(back==word,"worker assumption round trip");
    }
    need(jobs.peek()==EOF,"job trailing bytes");
    std::cout<<"{\"catalog_records\":546356,\"catalog_four_sets_checked\":"<<four_checks
        <<",\"queue_tasks\":2185424,\"worker_assumption_literals\":"<<checked
        <<",\"status\":\"VERIFIED\",\"task_decisions\":0,\"target_solver_calls\":0}\n";
}
int main(int argc,char** argv){try{
    if(argc==4&&std::string(argv[1])=="base")master(std::stoi(argv[2]),argv[3]);
    else if(argc==5&&std::string(argv[1])=="queue")queue_audit(argv[2],argv[3],argv[4]);
    else throw std::runtime_error("audit base R CNF | audit queue CATALOG CORES JOBS");
    return 0;
}catch(const std::exception& e){std::cerr<<e.what()<<'\n';return 1;}}
