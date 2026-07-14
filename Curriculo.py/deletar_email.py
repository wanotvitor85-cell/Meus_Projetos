#Objetivo: Acessar o email do Gmail via IMAP e ler os emails da caixa de entrada
#Finalidade: Ler os emails e encontrar os emails que não foram respondidos, deletando-os após um mês, e salvando os emails respondidos em um banco de dados para futuras consultas.
import sqlite3
import imaplib
import email
import os 
import base64
import datetime
#Conectamos o servidor do Gmail via IMAP
object = imaplib.IMAP4_SSL('imap.gmail.com' )   
#Passamos o login e a senha do email que queremos acessar
login =  #Adicione um email da sua preferência
senha = #Adicione a senha criada deste email, caso dê falha, procure "Gerenciamento de conta" vá em segurança e clique em "Verificação em duas etapas", por fim, crie uma senha para aplicativos.

object.login(login, senha)


object.list()
object.select(mailbox='inbox', readonly=True)

resposta, data = object.search(None, 'ALL')
ids = data[0]


id_list = ids.split()
#Loopando cada email da caixa de entrada
for i in id_list:
#Decodificando o email para que possamos ler o conteúdo
    print('Email ID:', i)
    resultados, dados = object.fetch(i, '(RFC822)') 
    texto_email = dados[0][1]
    texto_email = texto_email.decode('utf-8')   
    texto_email = email.message_from_string(texto_email)
#Loopando cada parte do email para encontrar o conteúdo do email
    for part in texto_email.walk():
#Se tiver anexo, pegar as partes do anexo e salvar em uma pasta local
        if part.get_content_type() == 'multipart/alternative':
            continue
        if part.get('Content-Disposition') is None:
            continue
        filename = part.get_filename()  
        print('Filename:', filename)
        arquivo= open(filename, 'wb')
        arquivo.write(part.get_payload(decode=True))
        arquivo.close()
#Criar uma função para salvar os emails respondidos em um banco de dados(Essa função só será útil caso haja um banco de dados implementado).
def salvar_emails_respondidos():
    #Conectando ao banco de dados
    conn = sqlite3.connect('emails_respondidos.db')
    c = conn.cursor()
    #Criando a tabela de emails respondidos
    c.execute('''CREATE TABLE IF NOT EXISTS emails_respondidos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  email TEXT NOT NULL,
                  data_resposta TEXT NOT NULL)''')
    #Loopando cada email da caixa de entrada
    for i in id_list:
        resultados, dados = object.fetch(i, '(RFC822)')
        texto_email = dados[0][1]
        texto_email = texto_email.decode('utf-8')
        texto_email = email.message_from_string(texto_email)
        #Verificando se o email foi respondido
        if texto_email['In-Reply-To'] is not None:
            #Salvando o email respondido no banco de dados
            c.execute("INSERT INTO emails_respondidos (email, data_resposta) VALUES (?, ?)", (texto_email['From'], datetime.datetime.now()))
            conn.commit()
    conn.close()
    
#Criar uma função para deletar os emails que não foram respondidos após um mês.
def deletar_emails():
    if datetime.datetime.now() - datetime.timedelta(days=30) > datetime.datetime.now():
        for i in id_list:
            object.store(i, '+FLAGS', '\\Deleted')
        object.expunge()


# A implementação das funções de salvar_emails_respondidos() e deletar_emails() deve ser feita em um contexto 
# onde o banco de dados e a lógica de negócios estejam corretamente configurados. 
# Por isso, não é possível executar essas funções diretamente neste script.
# Porém o projeto tende a ser implementado em um contexto maior, como uma aplicação web ou um serviço de backend, onde essas funções podem ser chamadas de forma apropriada.



