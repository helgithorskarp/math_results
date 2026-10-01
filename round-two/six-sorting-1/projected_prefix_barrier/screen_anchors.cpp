// Complete screening of the literal canonical projected-seed prefix family.
#define SEMANTIC_PROFILE_LIBRARY
#include "filter_frontier.cpp"
#include <chrono>

int main(int argc,char** argv) {
 try {
  if(argc!=3)throw std::runtime_error("usage: screen_anchors SEEDS_TXT OUTPUT_JSON");
  std::ifstream in(argv[1]);std::size_t number=0;
  if(!(in>>number) || number==0)throw std::runtime_error("missing seeds");
  std::ofstream out(argv[2]);if(!out)throw std::runtime_error("cannot open output");
  const std::array<unsigned,5> cuts{{8,12,16,20,24}};
  std::array<unsigned,5> counts{};
  State base=initial();
  const auto started=std::chrono::steady_clock::now();
  out<<"{\"n\":13,\"budget\":44,\"cuts\":[8,12,16,20,24],\"records\":[";
  for(std::size_t r=0;r<number;++r) {
    unsigned n=0,m=0;if(!(in>>n>>m) || n!=N || (m!=45 && m!=46))throw std::runtime_error("bad seed dimensions");
    State state=base;std::size_t cut_index=0;
    out<<(r?",":"")<<"{\"seed_index\":"<<r<<",\"units\":[";
    for(unsigned j=0;j<m;++j) {
      int a=0,b=0;if(!(in>>a>>b) || a<0 || a>=b || b>=N)throw std::runtime_error("invalid comparator");
      if(j<cuts.back())apply(state,{a,b});
      if(cut_index<cuts.size() && j+1==cuts[cut_index]) {
        auto units=anchor_units(state);
        out<<(cut_index?",":"")<<'['<<units[0]<<','<<units[1]<<']';
        if(units[0]<=512 && units[1]<=512)++counts[cut_index];
        ++cut_index;
      }
    }
    if(cut_index!=cuts.size())throw std::runtime_error("missing cut");
    out<<"]}";
    if((r+1)%100==0)std::cout<<"screened="<<(r+1)<<std::endl;
  }
  std::string extra;if(in>>extra)throw std::runtime_error("trailing input");
  out<<"],\"passing_counts\":[";
  for(std::size_t j=0;j<counts.size();++j)out<<(j?",":"")<<counts[j];
  out<<"],\"status\":\"COMPLETE_NECESSARY_ANCHOR_SCREEN\",\"seconds\":"
     <<std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count()<<"}\n";
  out.close();if(!out)throw std::runtime_error("output failed");
  std::cout<<"COMPLETE passing_counts=";
  for(auto count:counts)std::cout<<count<<' ';
  std::cout<<std::endl;
 }catch(const std::exception& e){std::cerr<<"ERROR "<<e.what()<<'\n';return 2;}
}
