import os
import streamlit as st

def main():
    st.title('Análise de Frequência de Caracteres')

    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_dir = os.path.abspath(os.path.join(base_dir, '..', 'textos'))

    arquivos = {
        'Português': 'portugues.txt',
        'Inglês': 'ingles.txt',
        'Alemão': 'alemao.txt',
        'Japonês': 'japones.txt'
    }

    erros = []

    for idioma, nome_arquivo in arquivos.items():
        caminho = os.path.join(db_dir, nome_arquivo)
        if not os.path.exists(caminho):
            erros.append(f"{idioma}: '{nome_arquivo}' não encontrado")

    if erros:
        st.error("Erro ao localizar os arquivos:")
        for erro in erros:
            st.write(f"- {erro}")
        return

    st.success("Todos os arquivos foram encontrados com sucesso!")

if __name__ == '__main__':
    main()