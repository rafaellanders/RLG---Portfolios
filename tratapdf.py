from pypdf import PdfReader
import re as re

'''
informações relevantes:
(dados do cartório) -> Matrícula do imóvel
(dados do imóvel) -> Tipo de logradouro; Endereço; Número; Complemento; 
(Contato para Vistoria) -> Nome;
(dados do serviço) -> Grupo; Atividade;
(Dados da ordem de serviço) -> Id da demanda; Data de abertura;
'''

def abrepdf(caminho):
    caminhoPDF = caminho
    reader = PdfReader(caminhoPDF)
    retorno = extraiinfo(reader)
    return retorno
    

def extraiinfo(reader):
    #print(f"O PDF tem {len(reader.pages)} páginas.\n")
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text()
        
        #Patterns
        #Patterns dados do cartório
        patternMatricula = r"Matrícula do imóvel:\s*(.*?)Cartório:"
        #Patterns Contato para vistória
        patternNomeVistoria = r"Nome:\s*(.+)\nLocal"
        #Patterns dados do serviço
        patternGrupo = r"Grupo:\s*(.*?)Atividade:"
        patternAtividade = r"Atividade:\s*(.+)"
        #Patterns dados do imóvel
        patternEndereco = r"Endereço:\s*(.*?)Número:"
        patternNumero = r"Número:\s*(.+)"
        patternLogradouro = r"Tipo de logradouro:\s*(.+)"
        patternComplemento = r"Complemento:\s*(.*?)Tipo do imóvel:"
        #Patterns ordem de serviço
        patternId = r"Identificação da Demanda:\s*(.*?)Data"
        patternData = r"Data de Abertura:(\b\d{2}/\d{2}/\d{4}\b)"
        
        #Matches
        #Matches dados do cartório
        matchesMatricula = re.findall(patternMatricula, text, re.IGNORECASE)
        #Matches contato para vistória
        matchesNomeVistoria = re.findall(patternNomeVistoria, text, re.IGNORECASE)
        #Matches dados do serviço
        matchesGrupo = re.findall(patternGrupo, text, re.IGNORECASE)
        matchesAtividade = re.findall(patternAtividade, text, re.IGNORECASE)
        #Matches dados do imóvel
        matchesEndereco = re.findall(patternEndereco, text, re.IGNORECASE)
        matchesNumero = re.findall(patternNumero, text, re.IGNORECASE)
        matchesLogradouro = re.findall(patternLogradouro, text, re.IGNORECASE)
        matchesComplemento = re.findall(patternComplemento, text, re.IGNORECASE)
        #Matches Ordem de serviço
        matchesId = re.findall(patternId, text, re.IGNORECASE)
        matchesData = re.findall(patternData, text, re.IGNORECASE)

        dados = {}
        #Dados do cartório
        dados['matricula'] = matchesMatricula[0].strip()
        #Dados Contato para vistória
        dados['nome'] = matchesNomeVistoria[0].strip()
        #Dados do serviço
        dados['grupo'] = matchesGrupo[0].strip()
        dados['atividade'] = matchesAtividade[0].strip()
        #Dados do imóvel
        dados['endereco'] = matchesEndereco[0].strip()
        dados['numero']   = matchesNumero[0].strip()
        dados['logradouro'] = matchesLogradouro[0].strip()
        dados['complemento'] = matchesComplemento[0].strip()
        #Dados Ordem de Serviço
        dados['Id'] = matchesId[0].strip()
        dados['data'] = matchesData[0].strip()

        return dados


