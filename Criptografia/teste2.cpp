//Criptografia de Substituição por ponteiro

#include <iostream>
#include <cstdlib> // Para rand() e srand()
#include <ctime>   // Para time()

using namespace std;

int deslocamento;

void cifrar(char* texto) {
    for (char* ptr = texto; *ptr != '\0'; ptr++) {
        if (*ptr >= 'A' && *ptr <= 'Z') {
            *ptr = 'A' + (*ptr - 'A' + deslocamento) % 26;
            *ptr += 32; // Converte para minúscula
        } else if (*ptr >= 'a' && *ptr <= 'z') {
            *ptr = 'a' + (*ptr - 'a' + deslocamento) % 26;
            *ptr -= 32; // Converte para maiúscula
        } else if (*ptr >= '0' && *ptr <= '9') {
            int num_desloc = deslocamento % 10; // Garante que o deslocamento para números seja sempre entre 0-9
            *ptr = '0' + (*ptr - '0' + num_desloc) % 10;
        }
    }
}

void decifrar(char* texto) {
    for (char* ptr = texto; *ptr != '\0'; ptr++) {
        if (*ptr >= 'A' && *ptr <= 'Z') {
            *ptr += 32; // Volta para minúscula primeiro
            *ptr = 'a' + (*ptr - 'a' - deslocamento + 26) % 26;
        } else if (*ptr >= 'a' && *ptr <= 'z') {
            *ptr -= 32; // Volta para maiúscula primeiro
            *ptr = 'A' + (*ptr - 'A' - deslocamento + 26) % 26;
        } else if (*ptr >= '0' && *ptr <= '9') {
            int num_desloc = deslocamento % 10;
            *ptr = '0' + (*ptr - '0' - num_desloc + 10) % 10;
        }
    }
}

int main() {
    char mensagem[100];
    
    do {
        cout << "Digite o deslocamento (1-25): ";
        cin >> deslocamento;
    } while (deslocamento < 1 || deslocamento > 25);
    cin.ignore(); // Limpa o buffer
    
    cout << "Digite uma mensagem: ";
    cin.getline(mensagem, 100);
    
    cifrar(mensagem);
    cout << "Criptografada: " << mensagem << endl;
    
    decifrar(mensagem);
    cout << "Descriptografada: " << mensagem << endl;
    
    return 0;
}