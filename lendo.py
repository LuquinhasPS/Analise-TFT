# =================================================================
# PASSO 1: PREPARAÇÃO DO AMBIENTE (ESSENCIAL)
# =================================================================
# As importações devem vir primeiro
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# Tenta carregar o arquivo e criar o DataFrame 'df'
try:
    df = pd.read_parquet('dataset.parquet')
    print("Arquivo 'dataset.parquet' carregado com sucesso!")
    print(f"O dataset tem {df.shape[0]} linhas e {df.shape[1]} colunas.")
except FileNotFoundError:
    print("ERRO: Arquivo 'dataset.parquet' não encontrado. Verifique se ele está na mesma pasta que o script.")
    exit() # Interrompe o script se o arquivo não for encontrado

# Criar a coluna 'top_4' que será usada na Análise 2
df['top_4'] = (df['placement'] <= 4).astype(int)

# Configura o estilo dos gráficos
sns.set_style("whitegrid")

# =================================================================
# ANÁLISE 1: DANO TOTAL VS. COLOCAÇÃO
# =================================================================
print("\n--- Análise 1: Correlação entre Dano Total e Colocação ---")

dano = df['total_damage_to_players']
colocacao = df['placement']

correlation, p_value = stats.pearsonr(dano, colocacao)

print(f"Coeficiente de Correlação de Pearson (r): {correlation:.4f}")
print(f"P-valor: {p_value:.4f}")

if p_value < 0.05:
    print("-> A correlação é estatisticamente significativa: quanto MAIOR o dano, MELHOR (menor) a colocação.")
else:
    print("-> A correlação não é estatisticamente significativa.")

# Criação do gráfico da Análise 1
plt.figure(figsize=(10, 6))
sns.scatterplot(x=dano, y=colocacao, alpha=0.3)
plt.title('Dano Total Causado vs. Colocação Final')
plt.xlabel('Dano Total Causado aos Oponentes')
plt.ylabel('Colocação (1 = Melhor, 8 = Pior)')
plt.gca().invert_yaxis()

# =================================================================
# ANÁLISE 2: PROBABILIDADE DE TOP 4 COM MAIS OURO
# =================================================================
print("\n--- Análise 2: Probabilidade Condicional de Top 4 com Mais Ouro ---")

jogadores_com_mais_ouro = df[df['players_with_more_gold_left'] == 1]
outros_jogadores = df[df['players_with_more_gold_left'] == 0]

prob_top4_com_mais_ouro = jogadores_com_mais_ouro['top_4'].mean()
prob_top4_sem_mais_ouro = outros_jogadores['top_4'].mean()

print(f"Probabilidade de Top 4 TENDO MAIS OURO: {prob_top4_com_mais_ouro:.2%}")
print(f"Probabilidade de Top 4 NÃO TENDO MAIS OURO: {prob_top4_sem_mais_ouro:.2%}")

# Criação do gráfico da Análise 2
plt.figure(figsize=(8, 6))
prob_df = pd.DataFrame({
    'Grupo': ['Com Mais Ouro', 'Outros Jogadores'],
    'Probabilidade de Top 4': [prob_top4_com_mais_ouro, prob_top4_sem_mais_ouro]
})
barplot = sns.barplot(x='Grupo', y='Probabilidade de Top 4', data=prob_df)
for p in barplot.patches:
    barplot.annotate(f'{p.get_height():.2%}', (p.get_x() + p.get_width() / 2., p.get_height()), ha='center', va='center', xytext=(0, 9), textcoords='offset points')
plt.title('Probabilidade de Ficar no Top 4')
plt.ylabel('Probabilidade')
plt.ylim(0, 1)

# =================================================================
# ANÁLISE 3: NÍVEL DO JOGADOR VS. COLOCAÇÃO
# =================================================================
print("\n--- Análise 3: Regressão Linear entre Nível e Colocação ---")

nivel = df['level']
# A variável 'colocacao' já foi definida na Análise 1, mas podemos redefinir para clareza
# colocacao = df['placement']

slope, intercept, r_value, p_value_reg, std_err = stats.linregress(x=nivel, y=colocacao)

print(f"Equação da Reta: Colocação = {slope:.2f} * Nível + {intercept:.2f}")
print(f"Coeficiente de Determinação (R²): {r_value**2:.4f}")
print(f"-> {r_value**2:.2%} da variação na colocação pode ser explicada pelo nível do jogador.")

# Criação do gráfico da Análise 3
plt.figure(figsize=(10, 6))
sns.regplot(x=nivel, y=colocacao, line_kws={"color": "red"})
plt.title('Regressão Linear: Nível do Jogador vs. Colocação Final')
plt.xlabel('Nível do Jogador')
plt.ylabel('Colocação (1 = Melhor, 8 = Pior)')
plt.gca().invert_yaxis()

# =================================================================
# EXIBIÇÃO DOS GRÁFICOS
# =================================================================
# plt.show() exibe TODOS os gráficos que foram criados.
# O script irá pausar aqui até que você feche as janelas dos gráficos.
print("\nExibindo os gráficos. Feche as janelas dos gráficos para terminar a execução do script.")
plt.show()

# =================================================================
# DIAGNÓSTICO: INSPEÇÃO DE UNIDADES E SINERGIAS
# =================================================================

import pandas as pd

print("--- Iniciando Diagnóstico (Versão Corrigida) ---")

try:
    df = pd.read_parquet('dataset.parquet')
    
    # Pega a primeira linha da coluna 'units'
    if not df['units'].empty:
        primeira_lista_de_unidades = df['units'].iloc[0]
        
        # CORREÇÃO: Verificamos se o comprimento da lista/array é maior que 0
        if len(primeira_lista_de_unidades) > 0:
            # Pega a primeira unidade dessa lista
            primeira_unidade = primeira_lista_de_unidades[0]
            
            print("\n✅ Aqui estão todas as informações disponíveis para uma unidade:")
            print(primeira_unidade)
            
            print("\n❓ Agora, procure na saída acima pela chave que contém a lista de sinergias.")
            print("   Ela deve se parecer com algo como: 'synergies': ['Hextech', 'Enforcer']")

        else:
            print("AVISO: A primeira linha do seu arquivo não continha unidades para inspecionar.")
    else:
        print("AVISO: A coluna 'units' parece estar vazia.")

except Exception as e:
    print(f"Ocorreu um erro: {e}")