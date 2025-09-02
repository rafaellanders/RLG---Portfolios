import pandas as pd

def abrecsv(dados, caminho):
    df = pd.read_csv(caminho)
    if "CLIENTE" in df.columns:
        df = df.drop(columns=["CLIENTE"])
    
    nova_linha = {"O.S.": dados["Id"]
                  ,"MATRICULA": dados["matricula"]
                  ,"LOTE E QD": dados["complemento"]
                  ,"ENDEREÇO": (dados["endereco"]+" Nº "+dados["numero"])
                  ,"CONSTRUTOR": dados["nome"]
                  ,"STATUS": (dados["grupo"]+dados["atividade"]+" ABERTURA: "+dados["data"])
                  ,"VALOR LAUDO" : 0} 
    
    linhas_vazias = df.isna().all(axis=1)
    indices = df[linhas_vazias].index.tolist()

    df_top = df.iloc[:indices[0]]
    df_bottom = df.iloc[indices[0]:]

    df_nova = pd.DataFrame([nova_linha])

    df = pd.concat([df_top, df_nova, df_bottom], ignore_index=True)
    df.to_csv(caminho, index=False)

    return