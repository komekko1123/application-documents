#include <stdlib.h>
#include <time.h>

#include <iostream>
#include <vector>

using namespace std;

class Coord {
   public:
    int x, y;
    Coord() {
        x = rand() % 1000;
        y = rand() % 1000;
    }
};

int main() {
    srand(time(NULL));
    vector<Coord> array;
    for (int i = 0; i < 100; i++) {
        Coord coord;
        array.push_back(coord);
    }
    
    
    cout << "find element " << endl;
    return 0;
}