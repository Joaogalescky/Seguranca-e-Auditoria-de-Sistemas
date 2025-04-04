#include <iostream>
#include <cstdlib> //malloc/free
#include <cctype> //isalpha, isdigit
#include <vector>
#include <string>

using namespace std;

bool verificadorDigitoAlfa(string senha) { // A-Z, a-z
    for (char c : senha) {
        if (!(isdigit(c)) && !(isalpha(c))) {
            return false;
        }
    }
    return true;
}

bool verificacaoNull(string senha) {
    return !senha.empty();
}

bool verificacaoLength(string senha) {
    return senha.length() >= 8;
}

void tracejar() {
    cout << "---------------------\n";
}

char *preencherVetorSenha(string senha, int tam) {
    //malloc -> aloca memória em tempo de execução
    char *vet = (char *)malloc(tam * sizeof(char)); // criar vetor de char

    if (!vet) {
        cout << "[Alert] - Erro ao alocar memoria!" << endl;
        return nullptr; // ponteiro nulo, verifica se alocação de memória falhou
    }

    for (int i = 0; i < tam; i++) {
        vet[i] = senha[i];
    }

    return vet;
}

vector<long long> criptografar(char *vet, int tam) { //long long -> inteiros grandes, armz o deslocamento na criptografia
    vector<long long> deslocamentos;
    char *endereco = vet;
    int chave = 2;
    int chave_soma = 5;

    for (int i = 0; i < tam; i++) {
        long long deslocamento = (vet + i) - endereco; //posição relativa do char no vetor
        deslocamento = (deslocamento ^ chave) + chave_soma;
        deslocamentos.push_back(deslocamento);
    }
    return deslocamentos;
}

string descriptografar(int tam, char *vet, vector<long long> deslocamentos) {
    char *vetor_descript = (char *) malloc(tam * sizeof(char));
    char *endereco = vet;
    int chave = 2;
    int chave_soma = 5;

    if (vetor_descript == nullptr) {
        cout << "[Alert] - Erro ao alocar memoria" << endl;
        return "";
    }

    for (int i = 0; i < tam; i++) {
        long long deslocamento = (deslocamentos[i] - chave_soma) ^ chave;
        vetor_descript[i] = *(endereco + deslocamento);
    }
    string senha_descriptografada(vetor_descript, tam);
    free(vetor_descript); //free -> libera a memória do malloc
    return senha_descriptografada;
}

void exibir_cripto(vector<long long> deslocamentos) {
    cout << "Senha Criptografada: ";
    for (long long deslocamento : deslocamentos) {
        cout << deslocamento << " ";
    }
    cout << endl;
}

void exibir_descript(string senha_descriptografada) {
    cout << "Senha Descriptografada: " << senha_descriptografada << endl;
}

int main() {
    string senha;
    int opcao;


        tracejar();
        cout << "- Digite sua senha: -\n";
        tracejar();
        cin >> senha;
        tracejar();

        if (!verificacaoNull(senha)) {
            cout << "[Alert] - Sua senha nao pode ser vazia!" << endl;
        } else if (!verificacaoLength(senha)) {
            cout << "[Alert] - Sua senha deve ter mais que oito caracteres" << endl;
        } else if (verificadorDigitoAlfa(senha)) {
            int tam = senha.length();
            char *vet = preencherVetorSenha(senha, tam);

            if (vet != nullptr) {
                cout << "Enderecos de memoria do vetor:" << endl;
                for (int i = 0; i < tam; i++) {
                    cout << "vet[" << i << "] = " << (void *)&vet[i] << " Valor = " << vet[i] << endl;
                }

                vector<long long> deslocamentos = criptografar(vet, tam);
                string senha_descriptografada = descriptografar(tam, vet, deslocamentos);

                free(vet);

                do{
                    tracejar();
                    cout << "- 1 - Para verificar sua senha criptografada\n";
                    cout << "- 2 - Para ver sua senha descriptografada\n";
                    cout << "- 3 - Para sair\n";
                    cin >> opcao;

                    if (opcao < 1 || opcao > 3) {
                        cout << "Digite um numero valido" << endl;
                    } else if (opcao == 1) {
                        exibir_cripto(deslocamentos);
                    } else if (opcao == 2) {
                        exibir_descript(senha_descriptografada);
                    }
                }while (opcao != 3);
            }
        } else {
            cout << "[Alert] - A senha deve conter somente caracteres e numeros." << endl;
        }

    return 0;
}
