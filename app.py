import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuração da página
st.set_page_config(page_title="Calculadora Industrial", page_icon="📊", layout="centered")

st.title("📊 Calculadora Industrial - Ponto de Equilíbrio")
st.markdown("Insira os parâmetros abaixo para simular o custo e visualizar o gráfico em tempo real.")

# Barra lateral com os campos de entrada (Inputs)
st.sidebar.header("Parâmetros de Entrada")
cf = st.sidebar.number_input("Custo Fixo Total (R$):", min_value=0.0, value=5000.0, step=100.0)
cvu = st.sidebar.number_input("Custo Variável Unitário (R$):", min_value=0.0, value=25.0, step=1.0)
p = st.sidebar.number_input("Preço de Venda Unitário (R$):", min_value=0.0, value=50.0, step=1.0)
vol_max = st.sidebar.number_input("Volume Máximo de Simulação:", min_value=10, value=400, step=10)

# Validação R01: Prevenção de Inconsistências Matemáticas
margem_contrib = p - cvu

if p <= 0 or cf < 0 or cvu < 0:
    st.error("⚠️ Insira valores positivos válidos para os custos e preço de venda.")
elif margem_contrib <= 0:
    st.warning(f"⚠️ **Preço de Venda (R$ {p:.2f})** deve ser superior ao **Custo Variável (R$ {cvu:.2f})**.")
else:
    peo_unidades = cf / margem_contrib
    peo_receita = peo_unidades * p

    # Exibição dos Indicadores
    col1, col2, col3 = st.columns(3)
    col1.metric("Margem / Unidade", f"R$ {margem_contrib:.2f}")
    col2.metric("Ponto de Equilíbrio", f"{peo_unidades:.0f} un.")
    col3.metric("Faturamento Mínimo", f"R$ {peo_receita:,.2f}")

    # Geração do Gráfico
    unidades = np.linspace(0, max(vol_max, int(peo_unidades * 1.5)), 100)
    custo_total = cf + (cvu * unidades)
    receita_total = p * unidades

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(unidades, custo_total, label='Custo Total (R$)', color='#C00000', linewidth=2)
    ax.plot(unidades, receita_total, label='Receita Total (R$)', color='#2E75B6', linewidth=2)
    ax.scatter([peo_unidades], [peo_receita], color='#70AD47', s=100, zorder=5, label=f'Ponto de Equilíbrio ({peo_unidades:.0f} un)')

    ax.set_title("Gráfico de Ponto de Equilíbrio (Break-Even Point)", fontsize=12, fontweight='bold')
    ax.set_xlabel("Volume Produzido (Unidades)")
    ax.set_ylabel("Valor Monetário (R$)")
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper left')

    st.pyplot(fig)
