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
    
def matchfunc(pattern, text, default="0"):
    matches = re.findall(pattern, text, re.IGNORECASE)
    return matches[0].strip() if matches else default

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

        dados = {}
        #Dados do cartório
        dados['matricula'] = matchfunc(patternMatricula, text)
        #Dados Contato para vistória
        dados['nome'] = matchfunc(patternNomeVistoria, text)
        #Dados do serviço
        dados['grupo'] = matchfunc(patternGrupo, text)
        dados['atividade'] = matchfunc(patternAtividade, text)
        #Dados do imóvel
        dados['endereco'] = matchfunc(patternEndereco, text)
        dados['numero']   = matchfunc(patternNumero, text)
        dados['logradouro'] = matchfunc(patternLogradouro, text)
        dados['complemento'] = matchfunc(patternComplemento, text)
        #Dados Ordem de Serviço
        dados['Id'] = matchfunc(patternId, text)
        dados['data'] = matchfunc(patternData, text)

        return dados


