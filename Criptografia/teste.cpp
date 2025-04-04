/* Criptografia de Substituição por ponteiro
 
*/

#include <iostream>
using namespace std;

void cifrar(char* texto) {
    for (char* ptr = texto; *ptr != '\0'; ptr++) { // Percorre cada caractere até o final da string = \0
        if (*ptr >= 'A' && *ptr <= 'Z') { // Maiúsculo
            *ptr = (*ptr + 3); // Avança 3 letras
            if (*ptr > 'Z') { // Caso passe de Z, volte a A
                *ptr = 'A' + (*ptr - 'Z' - 1);
            }
            *ptr += 32; // Converte para minúscula
        } else if (*ptr >= 'a' && *ptr <= 'z') { // Minúscula
            *ptr = (*ptr + 3);
            if (*ptr > 'z') {
                *ptr = 'a' + (*ptr - 'z' - 1);
            }
            *ptr -= 32;
        } else if (*ptr >= '0' && *ptr <= '9') {
            *ptr = '0' + (*ptr - '0' + 3) % 10;
        }
    }
}

void decifrar(char* texto) {
    for (char* ptr = texto; *ptr != '\0'; ptr++) {
        if (*ptr >= 'A' && *ptr <= 'Z') {
            *ptr += 32;
            *ptr = (*ptr - 3);
            if (*ptr < 'a') {
                *ptr = 'z' - ('a' - *ptr - 1);
            }
        } else if (*ptr >= 'a' && *ptr <= 'z') {
            *ptr -= 32;
            *ptr = (*ptr - 3);
            if (*ptr < 'A') {
                *ptr = 'Z' - ('A' - *ptr - 1);
            }
        } else if (*ptr >= '0' && *ptr <= '9') {
            *ptr = '0' + (*ptr - '0' - 3 + 10) % 10;
        }
    }
}

int main() {
    char mensagem[100];
    
    cout << "Digite uma mensagem: ";
    cin.getline(mensagem, 100);
    
    cout << "\nOriginal: " << mensagem << endl;
    
    cifrar(mensagem);
    cout << "Criptografada: " << mensagem << endl;
    
    decifrar(mensagem);
    cout << "Descriptografada: " << mensagem << endl;
    
    return 0;
}

/*Criptografia:
0 → 3

1 → 4

2 → 5

3 → 6

4 → 7

5 → 8

6 → 9

7 → 0 (7+3=10, 10%10=0)

8 → 1

9 → 2
*/

/*Descriptografia:

3 → 0

4 → 1

5 → 2

6 → 3

7 → 4

8 → 5

9 → 6

0 → 7 (0-3=-3, (-3+10)%10=7)

1 → 8

2 → 9

*/