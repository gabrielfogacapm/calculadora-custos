import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ------------------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA (Interface Profissional)
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Calculadora de Custos Industriais & PEO",
    page_icon="🏭",
    layout="wide"
)

# Título e Cabeçalho do Projeto
st.title("🏭 Calculadora de Custo de Fabricação e Ponto de Equilíbrio")
st.caption("Desenvolvido pelo Squad: Gabriel Fogaça, Caio Abreu e Julia Perez | UNESP - Gestão de Projetos")
st.markdown("---")

# ------------------------------------------------------------------------------
# BARRA LATERAL: ENTRADA DE DADOS FABRIS (EAP 1.2 / 2.1)
# ------------------------------------------------------------------------------
st.sidebar.header("⚙️ Parâmetros da Manufatura")

# Bloco 1: Custos Fixos Industriais
st.sidebar.subheader("1. Custos Fixos Totais (Mensal)")
aluguel_seguros = st.sidebar.number_input("Aluguel e Custos Administrativos (R$):", min_value=0.0, value=3000.0, step=100.0)
depreciacao_maquinas = st.sidebar.number_input("Depreciação de Equipamentos (R$):", min_value=0.0, value=1200.0, step=50.0)
cif_fixo = st.sidebar.number_input("Custos Indiretos de Fabricação Fixo - CIF (R$):", min_value=0.0, value=800.0, step=50.0)

custo_fixo_total = aluguel_seguros + depreciacao_maquinas + cif_fixo

# Bloco 2: Custos Variáveis por Unidade
st.sidebar.subheader("2. Custo Variável Unitário")
materia_prima = st.sidebar.number_input("Insumos e Matéria-Prima (R$/unidade):", min_value=0.0, value=15.0, step=1.0)
mao_de_obra_direta = st.sidebar.number_input("Mão de Obra Direta - MOD (R$/unidade):", min_value=0.0, value=8.0, step=0.5)
energia_outros_var = st.sidebar.number_input("Energia / Outros Variáveis (R$/unidade):", min_value=0.0, value=2.0, step=0.5)

custo_var_unitario = materia_prima + mao_de_obra_direta + energia_outros_var

# Bloco 3: Preço e Simulação
st.sidebar.subheader("3. Comercialização e Simulação")
preco_venda = st.sidebar.number_input("Preço de Venda Unitário (R$):", min_value=0.0, value=50.0, step=1.0)
capacidade_maxima = st.sidebar.number_input("Capacidade Máxima de Produção (Unidades):", min_value=10, value=500, step=10)

# ------------------------------------------------------------------------------
# MOTOR MATEMÁTICO E VALIDAÇÕES (MITIGAÇÃO DO RISCO R01)
# ------------------------------------------------------------------------------
margem_contrib_unitario = preco_venda - custo_var_unitario

# Validação do Risco R01 (Divisão por zero e Margem Negativa)
if preco_venda <= 0:
    st.error("⚠️ **Erro de Validação:** O Preço de Venda deve ser maior que zero.")
elif margem_contrib_unitario <= 0:
    st.warning(f"⚠️ **Alerta Financeiro:** O Preço de Venda (R$ {preco_venda:.2f}) é menor ou igual ao Custo Variável Unitário (R$ {custo_var_unitario:.2f}). A Margem de Contribuição é negativa ou nula (R$ {margem_contrib_unitario:.2f}). Ajuste os valores para calcular o Ponto de Equilíbrio.")
else:
    # Cálculo do PEO
    peo_unidades = custo_fixo_total / margem_contrib_unitario
    peo_receita = peo_unidades * preco_venda
    margem_contrib_percentual = (margem_contrib_unitario / preco_venda) * 100

    # --------------------------------------------------------------------------
    # DASHBOARD DE RESULTADOS (EXIBIÇÃO EXECUTIVA)
    # --------------------------------------------------------------------------
    st.subheader("📌 Indicadores Económico-Operacionais")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Custo Fixo Total", f"R$ {custo_fixo_total:,.2f}")
    col2.metric("Custo Var. Unitário", f"R$ {custo_var_unitario:,.2f}")
    col3.metric("Margem de Contribuição", f"R$ {margem_contrib_unitario:,.2f}", f"{margem_contrib_percentual:.1f}%")
    col4.metric("Ponto de Equilíbrio (PEO)", f"{peo_unidades:.0f} un.", f"R$ {peo_receita:,.2f}")

    st.markdown("---")

    # --------------------------------------------------------------------------
    # GRÁFICO DINÂMICO DO PONTO DE EQUILÍBRIO (BREAK-EVEN POINT)
    # --------------------------------------------------------------------------
    col_grafico, col_dados = st.columns([2, 1])

    with col_grafico:
        st.subheader("📈 Gráfico de Ponto de Equilíbrio Operacional")
        
        # Gerar intervalo de produção
        eixo_unidades = np.linspace(0, max(capacidade_maxima, int(peo_unidades * 1.4)), 100)
        linha_custo_total = custo_fixo_total + (custo_var_unitario * eixo_unidades)
        linha_receita_total = preco_venda * eixo_unidades

        # Plot com Matplotlib
        fig, ax = plt.subplots(figsize=(8, 4.5), dpi=100)
        ax.plot(eixo_unidades, linha_custo_total, label='Custo Total (R$)', color='#C00000', linewidth=2.5)
        ax.plot(eixo_unidades, linha_receita_total, label='Receita Total (R$)', color='#2E75B6', linewidth=2.5)
        ax.axhline(y=custo_fixo_total, color='#7F7F7F', linestyle='--', label='Custo Fixo Total (R$)', alpha=0.7)
        
        # Destaque do PEO
        ax.scatter([peo_unidades], [peo_receita], color='#70AD47', s=120, zorder=5, label=f'Ponto de Equilíbrio ({peo_unidades:.0f} un)')

        ax.set_title("Análise de Break-Even Point da Linha de Produção", fontsize=11, fontweight='bold')
        ax.set_xlabel("Volume de Produção/Vendas (Unidades)", fontsize=9)
        ax.set_ylabel("Valor Monetário (R$)", fontsize=9)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.legend(loc='upper left', fontsize=8)
        
        st.pyplot(fig)

    with col_dados:
        st.subheader("📋 Resumo da Estrutura")
        
        df_resumo = pd.DataFrame({
            "Componente de Custo": ["Aluguel/Admin", "Depreciação Máquinas", "CIF Fixo", "Matéria-Prima/un", "MOD/un", "Energia/un"],
            "Tipo": ["Fixo", "Fixo", "Fixo", "Variável", "Variável", "Variável"],
            "Valor (R$)": [aluguel_seguros, depreciacao_maquinas, cif_fixo, materia_prima, mao_de_obra_direta, energia_outros_var]
        })
        
        st.dataframe(df_resumo, hide_index=True, use_container_width=True)

        # Botão de Exportação para o Relatório Gerencial
        csv = df_resumo.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Exportar Dados de Custos (CSV)",
            data=csv,
            file_name="relatorio_custos_fabris.csv",
            mime="text/csv",
        )
