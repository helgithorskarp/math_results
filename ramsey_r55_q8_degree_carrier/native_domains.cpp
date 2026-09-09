// Independent literal eight-vertex enumeration; emits only to the given file.
#include <array>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

int main(int argc, char** argv) {
  if (argc != 2) return 2;
  std::ifstream prior(argv[1]);
  if (prior.good()) { std::cerr << "refuse existing output\n"; return 2; }
  std::ofstream out(argv[1]);
  if (!out) return 2;
  std::vector<std::array<int,5>> fives;
  for(int a=0;a<8;a++) for(int b=a+1;b<8;b++) for(int c=b+1;c<8;c++)
    for(int d=c+1;d<8;d++) for(int e=d+1;e<8;e++) fives.push_back({a,b,c,d,e});
  out << "[\n";
  bool first=true;
  for (int left=0;left<2;left++) for(int right=0;right<2;right++)
    for(int root=0;root<=left;root++) {
      std::string flags(65536,'0');
      std::array<std::array<int,25>,12> hist{};
      int total=0;
      for(int word=0;word<65536;word++) {
        bool graph[8][8]{};
        for(int u=0;u<8;u++) for(int v=u+1;v<8;v++) {
          bool edge=(v<4) ? left : ((u>=4) ? right : ((word>>(4*u+v-4))&1));
          graph[u][v]=graph[v][u]=edge;
        }
        bool allowed=true;
        for(const auto& set:fives) {
          int red=0;
          for(int u=0;u<5;u++) for(int v=u+1;v<5;v++) red+=graph[set[u]][set[v]];
          if(red==0 || red==10) { allowed=false; break; }
        }
        if(!allowed) continue;
        if(root) {
          int previous=16;
          for(int col=0;col<4;col++) {
            int sig=0;
            for(int row=0;row<4;row++) if(graph[row][4+col]) sig+=1<<row;
            if(sig>previous) allowed=false;
            previous=sig;
          }
        }
        if(!allowed) continue;
        flags[word]='1'; ++total;
        int index=0;
        for(int side=0;side<2;side++) for(int u=0;u<4;u++) for(int v=u+1;v<4;v++) {
          int a=0,b=0;
          for(int w=0;w<4;w++) {
            a+=graph[4*side+u][4*(1-side)+w];
            b+=graph[4*side+v][4*(1-side)+w];
          }
          hist[index++][5*a+b]++;
        }
      }
      if(!first) out << ",\n";
      first=false;
      out << "{\"left\":" << left << ",\"right\":" << right << ",\"root\":" << root
          << ",\"total\":" << total << ",\"allowed_flags\":\"" << flags << "\",\"hist\":[";
      for(int i=0;i<12;i++) {
        if(i) out << ',';
        out << '[';
        for(int j=0;j<25;j++) { if(j) out << ','; out << hist[i][j]; }
        out << ']';
      }
      out << "]}";
    }
  out << "\n]\n";
  if(!out.good()) return 2;
  return 0;
}
