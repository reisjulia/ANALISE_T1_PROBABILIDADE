import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

# Configuração do estilo dos gráficos
sns.set_theme(style='whitegrid', context='talk')

# 1. Importação dos Dados
df = pd.read_csv('world_ampas_oscar_winner_demographics.csv')

# 2. Análise Exploratória Inicial
print(df.head())
print(df.info())
print(df.isnull().sum())

# 3. Tratamento de Valores Ausentes
df['religion'] = df['religion'].fillna('Desconhecido')
df['sexual_orientation'] = df['sexual_orientation'].fillna('Desconhecido')

# 4. Cálculo da Idade no Momento da Premiação
df['age_at_award'] = df['year_edition'] - df['birth_year']

# 5. Codificação de Variáveis Categóricas
le = LabelEncoder()
df['race_ethnicity_encoded'] = le.fit_transform(df['race_ethnicity'].astype(str))
df['religion_encoded'] = le.fit_transform(df['religion'].astype(str))
df['sexual_orientation_encoded'] = le.fit_transform(df['sexual_orientation'].astype(str))

# 6. Estatísticas Descritivas
print(df['age_at_award'].describe())

# 7. Visualizações Melhoradas

# Gráfico 1: Distribuição de Vencedores por Ano (Agrupado por Década)
df['decade'] = (df['year_edition'] // 10) * 10
winners_per_decade = df.groupby('decade').size().reset_index(name='winners')

plt.figure(figsize=(12, 6))
sns.barplot(x='decade', y='winners', data=winners_per_decade, palette='viridis')
plt.xlabel('Década')
plt.ylabel('Número de Vencedores')
plt.title('Número de Vencedores por Década')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Gráfico 2: Idade dos Vencedores por Categoria (Ordenado por Mediana da Idade)
plt.figure(figsize=(14, 8))
order = df.groupby('category')['age_at_award'].median().sort_values().index
sns.boxplot(x='age_at_award', y='category', data=df, order=order, palette='Set2')
plt.xlabel('Idade no Momento da Premiação')
plt.ylabel('Categoria')
plt.title('Distribuição da Idade dos Vencedores por Categoria')
plt.tight_layout()
plt.show()

# Gráfico 3: Evolução da Diversidade Étnica ao Longo do Tempo
ethnicity_over_time = df.groupby(['year_edition', 'race_ethnicity']).size().reset_index(name='count')
total_per_year = df.groupby('year_edition').size().reset_index(name='total')
ethnicity_over_time = pd.merge(ethnicity_over_time, total_per_year, on='year_edition')
ethnicity_over_time['proportion'] = ethnicity_over_time['count'] / ethnicity_over_time['total']

plt.figure(figsize=(14, 8))
ethnicities = ethnicity_over_time['race_ethnicity'].unique()
palette = sns.color_palette('husl', n_colors=len(ethnicities))

for ethnicity, color in zip(ethnicities, palette):
    subset = ethnicity_over_time[ethnicity_over_time['race_ethnicity'] == ethnicity]
    sns.lineplot(x='year_edition', y='proportion', data=subset, label=ethnicity, color=color)

plt.xlabel('Ano da Edição')
plt.ylabel('Proporção de Vencedores')
plt.title('Evolução da Diversidade Étnica dos Vencedores ao Longo do Tempo')
plt.legend(title='Raça/Etnia', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()