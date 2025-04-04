#include <iostream>
#include <string>

using namespace std;

char encriptarChar(char c) {
    // aplica '^' XOR com hexadecimal (11111111 em binário) e adiciona 5
    return (c ^ 0xFF) + 5;
}

char decriptarChar(char c) {
    // reverte a operação)
    return (c - 5) ^ 0xFF;
}

string encriptarString(const string& s) { //& -> referência
    string result;
    for (char c : s) {
        result += encriptarChar(c);
    }
    return result;
}

string decriptarString(const string& s) {
    string result;
    for (char c : s) {
        result += decriptarChar(c);
    }
    return result;
}

int main() {
    string mensagem;
    cout << "Digite a mensagem: ";
    getline(cin, mensagem); //cin -> console input = lê tudo até confirmar.
    
    // criptografa a mensagem
    string encriptar = encriptarString(mensagem);
    cout << "Mensagem criptografada: " << encriptar << endl;
    
    // descriptografa a mensagem
    string decriptar = decriptarString(encriptar);
    cout << "Mensagem descriptografada: " << decriptar << endl;
    
    return 0;
}

//https://learn.microsoft.com/pt-br/cpp/cpp/bitwise-exclusive-or-operator-hat?view=msvc-170
//https://tecdicas.com/bitwise-em-cpp/