import streamlit as st
import pandas as pd
import plotly.express as px
import io

# onde colocar o arquivo
file_upload = st.file_uploader("faca o upload do arquivo aqui", type=["csv"])

# se tiver arquivo
if file_upload:
    # espaco onde fica so a tabela que colocaram
    exp0 = st.expander("Tabela")
    
    # aqui le o arquivo que foi colocado e coloca ele no lugar que e pra ficar so a tabela
    bytes_data = file_upload.read()
    try:
        df = pd.read_csv(io.BytesIO(bytes_data), encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(io.BytesIO(bytes_data), encoding='latin-1')

    exp0.dataframe(df, hide_index=True)
    
    # aqui cria o lugar dos graficos
    exp1 = st.expander("graficos")
    # aqui e a onde cada um dos graficos vai ficar para organizar melhor o site
    tab_variacao, tab_variacao_total, tab_salario, tab_preco= exp1.tabs(["variacao", "variacao total","salario", "preco"])

    # aqui fica o primeiro grafico de precos
    with tab_preco:
        grafico = df[df['Produto'] != 'Total'].set_index('Produto')[['semana 1', 'semana 2', 'semana 3', 'semana 4']].T
        fig = px.line(grafico, title="Grafico em relacao a o preco", labels={'index': 'semanas', 'value': 'Valor(R$)'})
        st.plotly_chart(fig, use_container_width=True)

    with tab_variacao_total:
    # a transposicao de variacao total das semanas para usar no grafico
        linha_total1 = df[df['Produto'] == 'Total'].iloc[0]

    # cria um DataFrame com as duas variacoes totais para plotar
        variacao_total = pd.DataFrame({
        'variacao': ['variacao1', 'variacao2'],
        'valor': [round(linha_total1['variacaot1'], 2), round(linha_total1['variacaot2'], 2)]  # arredonda para 2 casas decimais
        })

        fig_var = px.bar(variacao_total, x='variacao', y='valor',
                     title='Variacao Total por Semana',
                     labels={'variacao': 'Periodo', 'valor': 'Variacao (%)'})
        fig_var.add_hline(y=0, line_dash='dash', line_color='red')
        st.plotly_chart(fig_var, use_container_width=True)

    with tab_variacao:
    # a transposicao de variacao por produto para produto por variacao
        grafico_var = df[df['Produto'] != 'Total'].set_index('Produto')[['variacao1', 'variacao2']].T
        grafico_var = grafico_var.round(2)  # arredonda para 2 casas decimais
        fig_var = px.line(grafico_var, title='Grafico em relacao a variacao', labels={'index':'variacao', 'value': 'valor'})
        fig_var.add_hline(y=0, line_dash='dash', line_color='red')
        st.plotly_chart(fig_var, use_container_width=True)

    with tab_salario:
        # Filtra a linha de totais do DataFrame e converte para Series
        # para permitir acesso direto pelos nomes das colunas
        linha_total = df[df['Produto'] == 'Total'].iloc[0]
        
        # Cria um dicionário com os dados de salário organizados em duas colunas:
        # 'semana': identificador de cada período
        # 'valor': salário restante após os gastos de cada semana
        salarios = {
            'semana': ['semana 0', 'semana 1', 'semana 2', 'semana 3', 'semana 4'],
            'valor': [
                linha_total['salario0'],  # salário base (sem gastos)
                linha_total['salario1'],  # salário restante após semana 1
                linha_total['salario2'],  # salário restante após semana 2
                linha_total['salario3'],  # salário restante após semana 3
                linha_total['salario4'],  # salário restante após semana 4
            ]
        }
        
        # Converte o dicionário em DataFrame para uso no plotly
        salario_df = pd.DataFrame(salarios)
        
        # Salva o salário base como referência para a linha horizontal
        base = linha_total['salario0']
        
        # Cria o gráfico de barras com semanas no eixo X e valores no eixo Y
        fig_sal = px.bar(salario_df, x='semana', y='valor', title='Evolução do Salário')
        
        # Adiciona linha horizontal tracejada vermelha no valor do salário base
        # para facilitar a visualização de quanto o salário subiu ou desceu
        fig_sal.add_hline(
            y=base,
            line_dash='dash',       # estilo tracejado
            line_color='red',       # cor vermelha para destacar
            annotation_text=f'Base: R${base:.2f}'  # exibe o valor com 2 casas decimais
        )
        
        # Renderiza o gráfico na tela do Streamlit
        st.plotly_chart(fig_sal, use_container_width=True)

# não tem arquivo...