// Exhaust every second alternating switch after every minimum-height first
// switch from each of the 238 saved q12 states.
#define main primary_analyzer_main
#include "analyze_switches.cpp"
#undef main
#include <atomic>
#include <mutex>

template<class F> void switches(const Input& in,const std::array<uint8_t,M>& color,F visit){
  for(int a=0;a<N;++a)for(int b=a+1;b<N;++b)for(int c=b+1;c<N;++c)for(int d=c+1;d<N;++d){
    std::array<std::array<int,2>,3> m{{{{in.eid[a][b],in.eid[c][d]}},{{in.eid[a][c],in.eid[b][d]}},{{in.eid[a][d],in.eid[b][c]}}}};
    for(int i=0;i<3;++i)for(int j=i+1;j<3;++j){bool x=color[m[i][0]],y=color[m[j][0]];if(color[m[i][1]]!=x||color[m[j][1]]!=y||x==y)continue;visit(std::array<int,4>{m[i][0],m[i][1],m[j][0],m[j][1]});}}
}
int after(const Input& in,const Adj& a,int q,const std::array<int,4>& move,Adj* endpoint=nullptr){Adj work=a;for(int e:move){auto[u,v]=in.endpoints[e];q+=flip_delta(work,u,v);}if(endpoint)*endpoint=work;return q;}
struct Two{int first_q=0,first_count=0,second_min=100000;uint64_t second_total=0,below12=0,equal12=0,descending=0;};

int main(int argc,char**argv){if(argc!=4){std::cerr<<"usage: analyze INPUT.json FIRST.tsv OUTPUT.tsv\n";return 2;}Input in(argv[1]);std::ifstream f(argv[2]);std::string line;std::getline(f,line);std::vector<int> claimed_min;while(std::getline(f,line)){std::replace(line.begin(),line.end(),'\t',' ');std::istringstream s(line);int idx,tog;uint64_t sw,de,ne,mul;int q;s>>idx>>tog>>sw>>de>>ne>>q>>mul;claimed_min.push_back(q);}if(claimed_min.size()!=238)throw std::runtime_error("claim");
  std::vector<Two> result(238);std::atomic<int>next{0};std::vector<std::thread>threads;int workers=std::max(1u,std::thread::hardware_concurrency());
  for(int w=0;w<workers;++w)threads.emplace_back([&]{for(;;){int z=next.fetch_add(1);if(z>=238)break;auto color=in.base;for(int e:in.rows[z])color[e]^=1;Adj root{};for(int e=0;e<M;++e)if(color[e]){auto[u,v]=in.endpoints[e];root[u]|=UINT64_C(1)<<v;root[v]|=UINT64_C(1)<<u;}if(direct_q(root)!=12)throw std::runtime_error("root");Two r;r.first_q=claimed_min[z];std::vector<std::array<int,4>> first;
    switches(in,color,[&](auto move){if(after(in,root,12,move)==r.first_q)first.push_back(move);});r.first_count=first.size();
    for(auto one:first){Adj middle;int mq=after(in,root,12,one,&middle);auto middle_color=color;for(int e:one)middle_color[e]^=1;switches(in,middle_color,[&](auto two){int q=after(in,middle,mq,two);++r.second_total;r.below12+=(q<12);r.equal12+=(q==12);r.descending+=(q<mq);r.second_min=std::min(r.second_min,q);});}
    result[z]=r;}});for(auto&t:threads)t.join();
  std::ofstream out(argv[3]);out<<"index\tfirst_minimum_q\tfirst_minimum_multiplicity\tsecond_switches\tsecond_descending\tsecond_equal_12\tsecond_below_12\tsecond_minimum_q\n";uint64_t endpoints=0,total=0,desc=0,equal=0,below=0;int global=100000;
  for(int i=0;i<238;++i){auto&r=result[i];endpoints+=r.first_count;total+=r.second_total;desc+=r.descending;equal+=r.equal12;below+=r.below12;global=std::min(global,r.second_min);out<<i<<'\t'<<r.first_q<<'\t'<<r.first_count<<'\t'<<r.second_total<<'\t'<<r.descending<<'\t'<<r.equal12<<'\t'<<r.below12<<'\t'<<r.second_min<<'\n';}
  std::cout<<"seeds=238 minimum_first_endpoints="<<endpoints<<" second_switches="<<total<<" second_descending="<<desc<<" second_equal12="<<equal<<" second_below12="<<below<<" global_second_minimum_q="<<global<<'\n';
  return 0;
}
