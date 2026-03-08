import streamlit as st
import pandas as pd
import plotly.express as px


# onde colocaro o arquivo
file_upload = st.file_uploader("faca o upload do arquivo aqui", type=["csv"])


# se tiver arquivo
if file_upload:
    #espaco onde fica so a tabela que colocaram
    exp0 = st.expander("Tabela")
    # aqui le o arquivo que foi colocado e coloca ele no lugar que e pra ficar so a tabela
    df = pd.read_csv(file_upload)
    exp0.dataframe(df, hide_index=True)
    
# aqui cria o lugar dos graficos
    exp1 = st.expander("graficos")
    #aqui e a onde cada um dos graficos vai ficar para organizar melhor o site
    tab_variacao, tab_salario, tab_preco = exp1.tabs(["variacao", "salario", "preco"])

   
    #aqui fica o primeiro grafico de preços
    with tab_preco:
        #o grafico é uma trasposiçao do dataframe criado de semanas por produtos que vira produtos por semana
        grafico = df.set_index('produto')[['sem1', 'sem2', 'sem3', 'sem4']].T
        
        #aqui é criado o grafico onde se usa o plotly express para criar o grafico de linha
        fig = px.line(grafico,title="Grafico em relacao a o preco", labels={'index': 'semanas', 'value': 'Valor(R$)'})
        
        # aqui é como se faz para colocar o grafico no site
        st.plotly_chart(fig, use_container_width=True)

    
    
    with tab_variacao:
        # a trasposiçao de variaçao por produto para produto por variaçao
        grafico_var = df.set_index('produto')[['variacao1', 'variacao2']].T

        fig_var = px.line(grafico_var,title='Grafico em relacao a variacao', labels={'index':'variacao', 'value': 'valor'})

        fig_var.add_hline(
            y=0,
            line_dash='dash',
            line_color='red'
        )

        st.plotly_chart(fig_var, use_container_width=True)

    
    
    with tab_salario:
    
    # Filtra a linha de totais do DataFrame e converte para Series
    # para permitir acesso direto pelos nomes das colunas
        linha_total = df[df['produto'] == 'Total'].iloc[0]
    
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
    
    # Cria o gráfico de linha com semanas no eixo X e valores no eixo Y
        fig_sal = px.line(salario_df, x='semana', y='valor', title='Evolução do Salário')
    
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

#não tem arquivo...