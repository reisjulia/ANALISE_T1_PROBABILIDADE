import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

sns.set_theme(style='whitegrid', context='talk')

df = pd.read_csv('world_ampas_oscar_winner_demographics.csv')

# Fazendo o tratamento de valores ausentes
df['religion'] = df['religion'].fillna('Desconhecido')
df['sexual_orientation'] = df['sexual_orientation'].fillna('Desconhecido')
df['birth_year'] = df['birth_year'].fillna(df['birth_year'].median())  

df['age_at_award'] = df['year_edition'] - df['birth_year']

le = LabelEncoder()
df['race_ethnicity_encoded'] = le.fit_transform(df['race_ethnicity'].astype(str))
df['religion_encoded'] = le.fit_transform(df['religion'].astype(str))
df['sexual_orientation_encoded'] = le.fit_transform(df['sexual_orientation'].astype(str))

# Sendo feita as estatísticas descritivas do mínimo, máximo, média, mediana)
print(df[['age_at_award', 'birth_year', 'year_edition']].describe())
print(df.isnull().sum())  # Verificando valores ausentes

df['decade'] = (df['year_edition'] // 10) * 10

winners_per_decade = df.groupby('decade').size().reset_index(name='winners')
mean_winners = winners_per_decade['winners'].mean()
median_winners = winners_per_decade['winners'].median()

plt.figure(figsize=(12, 6))
sns.barplot(x='decade', y='winners', data=winners_per_decade, palette='viridis')
plt.axhline(y=mean_winners, color='r', linestyle='--', label='Média')  
plt.axhline(y=median_winners, color='g', linestyle='-.', label='Mediana')  
plt.xlabel('Década')
plt.ylabel('Número de Vencedores')
plt.title('Número de Vencedores por Década')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.show()

plt.figure(figsize=(14, 8))
order = df.groupby('category')['age_at_award'].median().sort_values().index
sns.boxplot(x='age_at_award', y='category', data=df, order=order, palette='Set2')

mean_age = df['age_at_award'].mean()
median_age = df['age_at_award'].median()
plt.axvline(x=mean_age, color='r', linestyle='--', label='Média')  
plt.axvline(x=median_age, color='g', linestyle='-.', label='Mediana')  

plt.xlabel('Idade no Momento da Premiação')
plt.ylabel('Categoria')
plt.title('Distribuição da Idade dos Vencedores por Categoria')
plt.legend()
plt.tight_layout()
plt.show()

ethnicity_over_time = df.groupby(['year_edition', 'race_ethnicity']).size().reset_index(name='count')
mean_count = ethnicity_over_time['count'].mean()

plt.figure(figsize=(14, 8))
ethnicities = ethnicity_over_time['race_ethnicity'].unique()
palette = sns.color_palette('husl', n_colors=len(ethnicities))
for ethnicity, color in zip(ethnicities, palette):
    subset = ethnicity_over_time[ethnicity_over_time['race_ethnicity'] == ethnicity]
    sns.lineplot(x='year_edition', y='count', data=subset, label=ethnicity, color=color)

plt.axhline(y=mean_count, color='r', linestyle='--', label='Média')  # Linha da média
plt.xlabel('Ano da Edição')
plt.ylabel('Quantidade de Vencedores')
plt.title('Evolução da Diversidade Étnica dos Vencedores ao Longo do Tempo')
plt.legend(title='Raça/Etnia', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

religion_count = df['religion'].value_counts(normalize=True).reset_index()
religion_count.columns = ['religion', 'proportion']
mean_proportion_religion = religion_count['proportion'].mean()

plt.figure(figsize=(10, 6))
sns.barplot(x='proportion', y='religion', data=religion_count, palette='pastel')
plt.axvline(x=mean_proportion_religion, color='r', linestyle='--', label='Média')  # Linha da média
plt.xlabel('Proporção')
plt.ylabel('Religião')
plt.title('Distribuição de Religiões entre os Vencedores do Oscar')
plt.legend()
plt.tight_layout()
plt.show()

orientation_count = df['sexual_orientation'].value_counts(normalize=True).reset_index()
orientation_count.columns = ['sexual_orientation', 'proportion']
mean_proportion_orientation = orientation_count['proportion'].mean()

plt.figure(figsize=(10, 6))
sns.barplot(x='proportion', y='sexual_orientation', data=orientation_count, palette='coolwarm')
plt.axvline(x=mean_proportion_orientation, color='r', linestyle='--', label='Média')  
plt.xlabel('Proporção')
plt.ylabel('Orientação Sexual')
plt.title('Distribuição de Orientações Sexuais entre os Vencedores do Oscar')
plt.legend()
plt.tight_layout()
plt.show()


plt.figure(figsize=(12, 6))
sns.scatterplot(x='year_edition', y='age_at_award', data=df, alpha=0.7, color='purple')

mean_age_correlation = df['age_at_award'].mean()
plt.axhline(y=mean_age_correlation, color='r', linestyle='--', label='Média')  

plt.xlabel('Ano da Edição')
plt.ylabel('Idade no Momento da Premiação')
plt.title('Correlação entre Ano da Edição e Idade dos Vencedores')
plt.legend()
plt.tight_layout()
plt.show()


