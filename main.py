import streamlit as st
import pandas as pd
import subprocess

lista_encoding = ['ascii',
 'cp500',
 'cp858',
 'cp1140',
 'latin_1',
 'utf_8',
 'utf_8_sig']

def definir_separador(valor):
    if valor == 'Virgula':
        return ','
    elif valor == 'Ponto-e-virgula':
        return ';'
    elif valor == 'Espaço':
        return ' '




# Título do aplicativo
st.title("GERADOR DE MAPAS")
with st.container():
    st.subheader('Subir arquivo CSV')
    # Elemento para fazer o upload do arquivo CSV
    uploaded_file = st.file_uploader("", type=["csv"])


# Verifica se um arquivo foi carregado
if uploaded_file is not None:
    with st.container():



        separador = st.radio('Separador', ['Virgula','Ponto-e-virgula', 'Espaço',])

        encod_index = lista_encoding.index('utf_8')
        encod = st.selectbox('Conjunto de caracteres', lista_encoding, index=encod_index)
        df = pd.read_csv(uploaded_file, sep=definir_separador(separador), encoding=encod)
        try:

            st.write(df.head())

        except:

            st.write('CONFIGURAÇÂO ERRADA')




        lista_colunas = list(df.columns)
        lista_colunas.append('-')

        st.subheader('Configurar Colunas')

        if 'Endereco' in lista_colunas:
            index_endereco = list(df.columns).index('Endereco')
            rua = st.selectbox('Rua', lista_colunas, index=index_endereco)
        else:
            rua = st.selectbox('Rua', lista_colunas, index=(len(lista_colunas)-1))

        if 'Numero' in lista_colunas:
            index_Numero = list(df.columns).index('Numero')
            numero = st.selectbox('Numero', lista_colunas, index=index_Numero)
        else:
            # Lê o arquivo CSV em um DataFrame pandas
            numero = st.selectbox('Numero', lista_colunas, index=(len(lista_colunas)-1))

        if 'Bairro' in lista_colunas:
            index_bairro = list(df.columns).index('Bairro')
            bairro = st.selectbox('Bairro', lista_colunas, index=index_bairro)
        else:
            bairro = st.selectbox('Bairro', lista_colunas, index=(len(lista_colunas)-1))

        if 'Cidade' in lista_colunas:
            index_Cidade = list(df.columns).index('Cidade')
            cidade = st.selectbox('Cidade', lista_colunas, index=index_Cidade)
        else:
            cidade = st.selectbox('Cidade', lista_colunas, index=(len(lista_colunas)-1))

        if 'UF' in lista_colunas:
            index_uf = list(df.columns).index('UF')
            uf = st.selectbox('UF', lista_colunas, index=index_uf)
        else:
            uf = st.selectbox('UF', lista_colunas, index=(len(lista_colunas)-1))

        cor = st.selectbox('Cor', lista_colunas, index=(len(lista_colunas)-1))

        if cor != '-':

            st.subheader('Configurar Cores')
            lista_cores = list(df[cor].value_counts().index)
            lista_cores.append('-')

            if len(lista_cores) > 0:
                vermelho = st.selectbox('Vermelho', lista_cores, index=0)
            else:
                vermelho = st.selectbox('Vermelho', lista_cores, index=(len(lista_cores)-1))

            if len(lista_cores) > 1:
                azul = st.selectbox('Azul', lista_cores, index=1)
            else:
                azul = st.selectbox('Azul', lista_cores, index=(len(lista_cores)-1))


            if len(lista_cores) > 2:
                verde = st.selectbox('Verde', lista_cores, index=2)
            else:
                verde = st.selectbox('Verde', lista_cores, index=(len(lista_cores)-1))


            if len(lista_cores) > 3:
                roxo = st.selectbox('Roxo', lista_cores, index=3)
            else:
                roxo = st.selectbox('Roxo', lista_cores, index=(len(lista_cores)-1))


            if len(lista_cores) > 4:
                laranja = st.selectbox('Laranja', lista_cores, index=4)
            else:
                laranja = st.selectbox('Laranja', lista_cores, index=(len(lista_cores)-1))



            if len(lista_cores) > 5:
                vinho = st.selectbox('Vinho', lista_cores, index=5)
            else:
                vinho = st.selectbox('Vinho', lista_cores, index=(len(lista_cores)-1))

            st.subheader('Colocar E-mail')
            email = st.text_input('Colocar e-mail', '')

            gerar_mapa = st.button('Gerar Mapa')

            temp_csv = 'df_configurado.csv'
            df.to_csv(temp_csv, index=False)


            ### GERAR MAPA ###
            if gerar_mapa:


                if email == '':
                    st.write(f'Email não configurado')
                else:
                    st.write(f'O mapa será enviado para {email}')
                    subprocess.Popen(["python", "enviar_anexo.py"])
                    st.write('Execução iniciada. Você pode fechar esta janela.')

                    cmd = ["python", "enviar_anexo.py", "--datafile", temp_csv, "--email", email, "--rua", rua,
                           "--numero", numero, "--bairro", bairro, "--cidade", cidade, "--uf", uf,"--cor", cor,
                           "--vermelho", vermelho, "--azul", azul, "--verde", verde, "--roxo", roxo, "--laranja", laranja, "--vinho", vinho
                           ]
                    subprocess.Popen(cmd)
