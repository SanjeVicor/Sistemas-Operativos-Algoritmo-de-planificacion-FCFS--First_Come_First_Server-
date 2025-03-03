from datetime import datetime

class PCB:
    def __init__(self, id, operation, TME, otherTime ):
        self.id             = id
        self.operation      = operation
        self.TME            = datetime.strptime(TME, "%M:%S")    
        self.TR             = datetime.strptime(TME, "%M:%S")    
        self.TLock          = datetime.strptime(otherTime, "%M:%S") 
        self.AT             = datetime.strptime(otherTime, "%M:%S")
        self.TF             = datetime.strptime(otherTime, "%M:%S")
        self.TFS            = datetime.strptime(otherTime, "%M:%S")
        self.WaitingTime    = datetime.strptime(otherTime, "%M:%S")
        self.ServiceTime    = datetime.strptime(otherTime, "%M:%S")
        self.error          = False
        self.FS             = False
        self.errorMessage   = list()
    
    def setFirstServe(self, FS):
        self.FS = FS
    
    def getFirstServe(self):
        return self.FS
        
    def getID(self):
        return self.id
    
    def setResult(self, result):
        self.result = result
    
    def getResult(self):
        return self.result
    
    def addMessage(self, message):
        self.errorMessage.append(message)
    
    def getErrorMessages(self):
        messages = ""
        for error in self.errorMessage:
            messages += error + ','
        return messages
        
    def setError(self, error):
        self.error = error
    
    def getOperation(self):
        return self.operation
    
    def getError(self):
        if self.error:
           return self.error  
    
    def getValues(self):
        return self.id , self.programerName  , self.operation  , self.result , self.TME , self.getError() ,  self.getErrorMessages()  

#---------------TIEMPOS---------------
    def setTLock(self, TLock):
        self.TLock = TLock
    
    def getTLock(self):
        return self.TLock 
        
    def setTLL(self,TLL):#Tiempo de llegada
        self.TLL = TLL    
        
    def getTLL(self):
        return self.TLL 
      
    def getTME(self): #Tiempo Max. Esperado
        return self.TME
    
    def setNewTime(self, TR): #Tiempo Restante
        TR = TR[2:]
        self.TR = datetime.strptime(TR, "%M:%S")    
    
    def setTR(self, TR):#Tiempo Restante
        self.TR = TR   
    
    def getTR(self):#Tiempo Restante
        try:
            return datetime.strptime(self.TR, "%M:%S")
        except:
            return self.TR
    
    def setArriveTime(self,globalClock): #Tiempo de llegada
        self.AT = globalClock
    
    def getAT(self):
        return self.AT

    def setTFS(self, T): #Tiempo de Respuesta
        self.TFS = T
    
    def getTFS(self):
        return self.TFS
    
    def setTF(self,TF): #tiempo de finalizacion
        self.TF = TF
    
    def getTF(self):
        return self.TF
    
    def setReturnTime(self, T):#tiempo de retorno
        self.ReturnTime = T
    
    def getReturnTime(self):
        return self.ReturnTime
        
    def setWaitingTime(self, T):#tiempo de espera
        self.WaitingTime = T
    
    def getWaitingTime(self):
        return self.WaitingTime
    
    def setServiceTime(self, T):#tiempo de servicio
        self.ServiceTime = T
    
    def getServiceTime(self):
        return self.ServiceTime    