import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

sns.set_theme(style='whitegrid', context='talk')

df = pd.read_csv('world_ampas_oscar_winner_demographics.csv')

# Informações iniciais do dataset
print(df.info())
print(df.head())

# Sendo feito o tratamento de valores ausentes
df['religion'] = df['religion'].fillna('Desconhecido')
df['sexual_orientation'] = df['sexual_orientation'].fillna('Desconhecido')
df['birth_year'] = df['birth_year'].fillna(df['birth_year'].median())  

# Criação de coluna para idade no momento do prêmio
df['age_at_award'] = df['year_edition'] - df['birth_year']

# Encoding para variáveis categóricas
le = LabelEncoder()
df['race_ethnicity_encoded'] = le.fit_transform(df['race_ethnicity'].astype(str))
df['religion_encoded'] = le.fit_transform(df['religion'].astype(str))
df['sexual_orientation_encoded'] = le.fit_transform(df['sexual_orientation'].astype(str))

# Sendo feita as estatísticas descritivas  Mínimo, máximo, média, mediana e desvio padrão)
print(df[['age_at_award', 'birth_year', 'year_edition']].describe())
print(df.isnull().sum())  # fazendo a verificação de valores ausentes

# Criar coluna para décadas
df['decade'] = (df['year_edition'] // 10) * 10

# Gráfico 1: Distribuição de vencedores por década
winners_per_decade = df.groupby('decade').size().reset_index(name='winners')
plt.figure(figsize=(12, 6))
sns.barplot(x='decade', y='winners', data=winners_per_decade, palette='viridis')
plt.xlabel('Década')
plt.ylabel('Número de Vencedores')
plt.title('Número de Vencedores por Década')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Gráfico 2: Idade dos vencedores por categoria
plt.figure(figsize=(14, 8))
order = df.groupby('category')['age_at_award'].median().sort_values().index
sns.boxplot(x='age_at_award', y='category', data=df, order=order, palette='Set2')
plt.xlabel('Idade no Momento da Premiação')
plt.ylabel('Categoria')
plt.title('Distribuição da Idade dos Vencedores por Categoria')
plt.tight_layout()
plt.show()

# Gráfico 3: Evolução da diversidade étnica ao longo do tempo
ethnicity_over_time = df.groupby(['year_edition', 'race_ethnicity']).size().reset_index(name='count')
plt.figure(figsize=(14, 8))
ethnicities = ethnicity_over_time['race_ethnicity'].unique()
palette = sns.color_palette('husl', n_colors=len(ethnicities))
for ethnicity, color in zip(ethnicities, palette):
    subset = ethnicity_over_time[ethnicity_over_time['race_ethnicity'] == ethnicity]
    sns.lineplot(x='year_edition', y='count', data=subset, label=ethnicity, color=color)
plt.xlabel('Ano da Edição')
plt.ylabel('Quantidade de Vencedores')
plt.title('Evolução da Diversidade Étnica dos Vencedores ao Longo do Tempo')
plt.legend(title='Raça/Etnia', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Gráfico 4: Proporção de religiões entre os vencedores
religion_count = df['religion'].value_counts(normalize=True).reset_index()
religion_count.columns = ['religion', 'proportion']
plt.figure(figsize=(10, 6))
sns.barplot(x='proportion', y='religion', data=religion_count, palette='pastel')
plt.xlabel('Proporção')
plt.ylabel('Religião')
plt.title('Distribuição de Religiões entre os Vencedores do Oscar')
plt.tight_layout()
plt.show()

# Gráfico 5: Distribuição de orientação sexual
orientation_count = df['sexual_orientation'].value_counts(normalize=True).reset_index()
orientation_count.columns = ['sexual_orientation', 'proportion']
plt.figure(figsize=(10, 6))
sns.barplot(x='proportion', y='sexual_orientation', data=orientation_count, palette='coolwarm')
plt.xlabel('Proporção')
plt.ylabel('Orientação Sexual')
plt.title('Distribuição de Orientações Sexuais entre os Vencedores do Oscar')
plt.tight_layout()
plt.show()

# Gráfico 6: Correlação entre idade e ano de edição
plt.figure(figsize=(12, 6))
sns.scatterplot(x='year_edition', y='age_at_award', data=df, alpha=0.7, color='purple')
plt.xlabel('Ano da Edição')
plt.ylabel('Idade no Momento da Premiação')
plt.title('Correlação entre Ano da Edição e Idade dos Vencedores')
plt.tight_layout()
plt.show()

# Gráfico 7: Análise de gênero entre os vencedores
gender_count = df['gender'].value_counts(normalize=True).reset_index()
gender_count.columns = ['gender', 'proportion']
plt.figure(figsize=(10, 6))
sns.barplot(x='proportion', y='gender', data=gender_count, palette='cool')
plt.xlabel('Proporção')
plt.ylabel('Gênero')
plt.title('Distribuição de Gêneros entre os Vencedores do Oscar')
plt.tight_layout()
plt.show()
