import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

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

# 7. Visualizações
# Distribuição de Vencedores por Ano
plt.figure(figsize=(12, 6))
sns.countplot(x='year_edition', data=df)
plt.xticks(rotation=90)
plt.title('Número de Vencedores por Ano')
plt.show()

# Idade dos Vencedores por Categoria
plt.figure(figsize=(12, 6))
sns.boxplot(x='category', y='age_at_award', data=df)
plt.xticks(rotation=90)
plt.title('Distribuição da Idade dos Vencedores por Categoria')
plt.show()

# Evolução da Diversidade Étnica
plt.figure(figsize=(12, 6))
sns.lineplot(x='year_edition', y='race_ethnicity_encoded', data=df)
plt.title('Evolução da Diversidade Étnica dos Vencedores')
plt.show()