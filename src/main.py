from src.fetch_data import obter_dados_climaticos, salvar_dados
from src.queries import temperatura_media, chuva_diaria_total

def main():
    cidade = input("Digite a cidade para buscar os dados climáticos: ")
    dados = obter_dados_climaticos(cidade)
    
    if dados:
        salvar_dados(dados)
        print("Dados salvos com sucesso!")

        print(f"Temperatura média em {cidade}: {temperatura_media(cidade)}°C")
        print(f"Total de chuva em {cidade}: {chuva_diaria_total(cidade)} mm")

if __name__ == "__main__":
    main()