# leitor de Contagem de Impressa
#versao 1.0
#Efetua a leitura do  numedo de serie e do contador da impressora atraves do IP

#deve ser criado um arquivo txt chamado ips.txt na pasta da aplicação
#conteudo do arquivo 
#cooperativa xxxx: nome da cooperativa
#Local e e numero da impressora:ip da impressora
# exemplo
# Cooperativa 2222: Rio de Janeiro
# impressora 1:17x.xxx.xxx.xxx

    #1.3.6.1.2.1.1.1 - sysDescr
    #1.3.6.1.2.1.1.2 - sysObjectID
    ##1.3.6.1.2.1.1.3 - sysUpTime
    #1.3.6.1.2.1.1.4 - sysContact
    #1.3.6.1.2.1.1.5 - sysName
    #1.3.6.1.2.1.1.6 - sysLocation
    #1.3.6.1.2.1.1.7 - sysServices 
    #contador 1.3.6.1.2.1.43.10.2.1.4.1.1
    #serie 1.3.6.1.2.1.43.5.1.1.17.1    

from tkinter import *
from pysnmp.hlapi import *
import os
from datetime import datetime
import codecs
  
class Application:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "10")
        self.primeiroContainer = Frame(master)
        self.primeiroContainer["pady"] = 10
        
        self.primeiroContainer.pack()
  
        self.segundoContainer = Frame(master)
        self.segundoContainer["padx"] = 20
        self.segundoContainer.pack()
  
        self.terceiroContainer = Frame(master)
        self.terceiroContainer["padx"] = 20
        self.terceiroContainer.pack()
  
        self.quartoContainer = Frame(master)
        self.quartoContainer["pady"] = 20
        self.quartoContainer["width"] = 20
        

        self.quartoContainer.pack()
        
  
        self.titulo = Label(self.primeiroContainer, text="Leituras de Contadores")
        self.titulo["font"] = ("Arial", "10", "bold")
        self.titulo.pack()
  
        self.log = Text(self.segundoContainer)
        self.log["font"] = ("Arial", "10", "bold")
        self.log["width"] = 200
        self.log["height"] = 45
        
        self.log.pack()
  
        self.autenticar = Button(self.quartoContainer)
        self.autenticar["text"] = "Efetuar Leitura"
        self.autenticar["font"] = ("Calibri", "8")
        self.autenticar["width"] = 12
        self.autenticar["command"] = self.lerContadores
        self.autenticar.pack()
  
        self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
        self.mensagem.pack()

        self.impressoras=""
        self.cont=0

        
  
    #Método verificar senha
    def lerContadores(self):  
        now = datetime.now()
        self.log.insert (END, "DATA:"+(str(now.day)+"/"+str(now.month)+"/"+str(now.year))+"\n")
        impressoras={}
    
        files=(read_file("ips.txt"))
        
        for line in files:
            y=(line)            
            x=y.split(":")
            if y.strip(" ").strip("\n")!="":          
                impressoras.update({x[0]:x[1].strip('\n')})
        
    
        leitura=""
        for impres,val in impressoras.items():            
            if impres[0:11]=="Cooperativa":
                self.log.insert (END, '=============='+impres+':'+val+ '==============================='+ "\n")
            else:
                ler=lerImpressoras(val,'1.3.6.1.2.1.43.5.1.1.17.1','1.3.6.1.2.1.43.10.2.1.4.1.1')
                
                #leitura=leitura+impres+'\t\t\t\t\t'+val+ '\t\t\t\t\t\tserie:'+ler[0]+'\t\t\t\t\t\tContador:'+ ler[1]+"\n"
                self.log.insert (END, impres+'\t\t\t\t\t'+"172.xx.xxx.xx"+ '\t\t\t\t\t\tserie:'+ler[0]+'\t\t\t\t\t\tContador:'+ ler[1]+"\n")
                
        

           

   
def read_file( filename):
    file =  codecs.open(filename,  'r')
    return file

#verifica se arquivo existe
def verifica_arquivo(filename):
    arquivo=os.path
    return arquivo.isfile(filename)




def lerImpressoras(ip,codigo,codigo2):  
    serieImpressora = getCmd(SnmpEngine(),
                  CommunityData('public'),
                  UdpTransportTarget((ip, 161)),
                  ContextData(),
                  ObjectType(ObjectIdentity(codigo)),
                  ObjectType(ObjectIdentity(codigo2)))
    errorIndication, errorStatus, errorIndex, varBinds = next(serieImpressora)

    if errorIndication:  # SNMP engine errors
        return  ["OFF","OFF"]
        
    else:
        if errorStatus:  # SNMP agent errors
            print('%s at %s' % (errorStatus.prettyPrint(), varBinds[int(errorIndex)-1] if errorIndex else '?'))
        else:
            serie=str(varBinds[0])
            serie=serie.split("=")
            contador=str(varBinds[1])
            contador=contador.split("=")
            return [serie[1],contador[1]]
         
  
root = Tk()
root.title("Leitura de Contadores de Impressoras")
Application(root)
root.mainloop()
