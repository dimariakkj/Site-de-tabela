import streamlit as st
import pandas as pd
import openpyxl as op
from io import BytesIO


st.title("Cadastro de Produtos")


st.info("Chaves esperadas: Produto, semana 1, semana 2, semana 3, semana 4")

# inicializa o session state para guardar os dados
if 'tabela' not in st.session_state:
    st.session_state.tabela = {}

with st.form("Cadastro"):
    chave = st.text_input("Chave: categoria do item (ex: 'Produto', 'semana 1', 'semana 2'...)")
    valor = st.text_input("Valor: valor correspondente à chave (ex: 'arroz', '10.5')")
    adicionar = st.form_submit_button("Adicionar")
    if adicionar:
        if chave not in st.session_state.tabela:
            st.session_state.tabela[chave] = []
        if chave == 'Produto':
            st.session_state.tabela[chave].append(valor)
            st.success('Produto adicionado')
        else:
            st.session_state.tabela[chave].append(float(valor))
            st.success('Valor adicionado')
if st.session_state.tabela:
    st.dataframe(st.session_state.tabela)
else:
    st.warning('Nenhum produto cadastrado ')
excluir = st.button('Reniciar')
if excluir:
    del(st.session_state.tabela)
    st.rerun()
finalizar = st.button('finalizar')
if finalizar:
        max_len = max(len(v) for v in st.session_state.tabela.values())

        for chave in st.session_state.tabela:
            while len(st.session_state.tabela[chave]) < max_len:
                st.session_state.tabela[chave].append(None)
        
        tabeladf = pd.DataFrame(st.session_state.tabela)

        # DataFrame dos produtos
        produtosdf = tabeladf[['Produto', 'semana 1', 'semana 2', 'semana 3', 'semana 4']]

# Linha de totais
        totais = {
        'produto': 'Total',
        'semana 1': tabeladf['semana 1'].sum(skipna=True),
        'semana 2': tabeladf['semana 2'].sum(skipna=True),
        'semana 3': tabeladf['semana 3'].sum(skipna=True),
        'semana 4': tabeladf['semana 4'].sum(skipna=True),
        }





        variacaot1 = (totais['semana 2'] - totais['semana 1']) / totais['semana 1'] * 100
        variacaot2 = (totais['semana 4'] - totais['semana 3']) / totais['semana 3'] * 100


        produtosdf['variacao1'] = (tabeladf['semana 2'] - tabeladf['semana 1']) / tabeladf['semana 1'] * 100
        produtosdf['variacao2'] = (tabeladf['semana 4'] - tabeladf['semana 3']) / tabeladf['semana 3'] * 100


        salario1 = (1621.00 - totais['semana 1'])
        salario2 = (1621.00 - totais['semana 2'])
        salario3 = (1621.00 - totais['semana 3'])
        salario4 = (1621.00 - totais['semana 4'])

        totais['variacaot1'] = variacaot1
        totais['variacaot2'] = variacaot2

        totais['salario0'] = 1621.00
        totais['salario1'] = salario1
        totais['salario2'] = salario2
        totais['salario3'] = salario3
        totais['salario4'] = salario4


        totaisdf = pd.DataFrame([totais])

# Junta tudo
        finaldf = pd.concat([produtosdf, totaisdf], ignore_index=True)
        tabelafinal = finaldf.to_csv(index=False)
        st.download_button(
        label= 'Baixar csv',
        data=tabelafinal,
        file_name="financas.csv",
        mime='text/csv',
        key= 'csv'
        )
        buffer = BytesIO()
        finaldf.to_excel(buffer, index=False, engine='openpyxl')
        buffer.seek(0)

        st.download_button(
        label='Baixar excel',
        data=buffer,
        file_name='financas.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        key= 'excel'
        )

      