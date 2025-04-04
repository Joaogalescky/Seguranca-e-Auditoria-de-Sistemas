/* Intuito
    Manipulação bit a bit - manipular os bits de números inteiros a partir da entrada do usuário (string)
*/
#include <iostream>
#include <cctype> //
#include <vector>

using namespace std;

vector<char> extrairNumerosInt(string senha_str){
    int i;
    vector<char> senha_int;

    for (i = 0; i < senha_str.length(); i++){
        if(isdigit(senha_str[i])){
          senha_int.push_back(senha_str[i]); //push_back - adiciona um elemento ao final do vetor
        }
    }
    return senha_int;
}

void exibir(vector<char> senha_int){
    for(char c : senha_int){
        cout << c; // << - operador de inserção, cout é saída de texto, onde c é essa saída
    }
    cout << endl; // endl - fim da linha
}

vector<char> transporSenhaBitABit( vector<char>& senha_int){
    vector<char> senha_transp;
    char transposto;

    for(char c: senha_int){
        /* Explicação...
        O operador << desloca os bits do número para a esquerda, multiplicando por 4 (2^2 = 4). 
        Por exemplo, se c = '5' (ASCII 53 em decimal), ao aplicar 53 << 2, o valor vira 212.
        */
        transposto = (c - '0') << 2; //Converte 'char' para 'int'
        /* Ou
        int transposto = ((c - '0') << 2) % 10; // Garante que fique entre 0-9
        */
        // transpondo os bits 2 casas para esquerda (mult por 4)

        senha_transp.push_back(transposto + '0'); //Converte de volta para 'char'
    }
    return senha_transp;
}

int main(){
    string senha_str;

    cout << "Digite sua senha: ", cin >> senha_str;

    cout << "A sua senha eh: " << endl;

    vector<char> senha_int = extrairNumerosInt(senha_str);
    vector<char> senha_transp = transporSenhaBitABit(senha_int);

    exibir(senha_int);
    exibir(senha_transp);

    return 0;
}
