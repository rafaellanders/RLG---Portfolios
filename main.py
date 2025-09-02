import tratapdf as tp
import tratacsv as tc

def main():
    # Recebe como argumento o arquivo PDF e o CSV.
    # Classe para tratar o pdf
    # Classe para tratar o CSV
    # Injetar na tabela principal
    dados = tp.abrepdf("pdfs/angelo.pdf")
    caminho_csv = "csv/teste.csv"
    tc.abrecsv(dados, caminho_csv)


if __name__ == "__main__":
    main()