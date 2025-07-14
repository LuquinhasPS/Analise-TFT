import pandas as pd

# Defina o caminho para o seu arquivo.
# Se o script estiver na mesma pasta que o arquivo, basta o nome.
file_path = 'dataset.parquet'

try:
    # Carrega o arquivo Parquet para um DataFrame do pandas
    df = pd.read_parquet(file_path)

    # 1. Pega a lista de colunas do DataFrame
    nomes_das_colunas = df.columns.tolist()

    # 2. Imprime os nomes das colunas
    print("As colunas do arquivo são:")
    print(nomes_das_colunas)

    # (Opcional) Mostra as 5 primeiras linhas para ter uma ideia dos dados
    print("\n--- Amostra dos Dados (5 primeiras linhas) ---")
    print(df.head())

except FileNotFoundError:
    print(f"Erro: O arquivo '{file_path}' não foi encontrado.")
    print("Verifique se o nome do arquivo está correto e se ele está na mesma pasta que o script.")
except Exception as e:
    print(f"Ocorreu um erro ao ler o arquivo: {e}")