#include <iostream>

using namespace std;

int cripto_bitwise(int n) {
    int left_bit = n << 2;
    return left_bit;
}

int descript_bitwise(int n) {
    int right_bit = n >> 2;
    return right_bit;
}

int main() {
    int a = 61;

    int left_bit = cripto_bitwise(a);

    int right_bit = descript_bitwise(left_bit);

    cout << "Deslocamento para a esquerda: " << left_bit << endl;
    cout << "Deslocamento para a direita: " << right_bit <<endl;
}