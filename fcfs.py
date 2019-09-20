from xeger import Xeger
from PCB import PCB
from terminaltables import AsciiTable
import msvcrt
import subprocess as sp 
from datetime import datetime
from datetime import timedelta
import time
from calculator import makeOperation
import re

globalClock = datetime.strptime("00:00", "%M:%S")
endedList = list()
lockedList = list()
queueReady = list()


def getReady(memorySpace): 
    tableData = [['ID', 'Tiempo Maximo Esperado', 'Tiempo Restante']]
    for pendingTask in memorySpace:
        tableData.append([pendingTask.getID(),
                          str(pendingTask.getTME().second) + "'s", 
                          str(pendingTask.getTR().second) + "'s"])
    table = AsciiTable(tableData)
    print (table.table)

def getExcecutable(process):
    tableData = [['ID', 
                  'Operación', 
                  'Tiempo de llegada', 
                  'Tiempo Max. Esperado', 
                  'Tiempo Restante' , 
                  'Tiempo de Respuesta',
                  'Tiempo de Espera',
                  'Tiempo de Servicio']]
    
    tableData.append([process.getID(), 
                      process.getOperation(), 
                      str(process.getAT().second) + "'s" ,
                      str(process.getTME().second) + "'s", 
                      str(process.getTR().second) + "'s", 
                      str(process.getTFS()) + "'s", 
                      str(process.getWaitingTime().second) + "'s",
                      str(process.getServiceTime().second) + "'s"
                      ])
    
    table = AsciiTable(tableData)
    print (table.table)

def getLocked(queueLocked):
    incrementTime = timedelta(seconds=1)
    tableData = [['ID', 'Tiempo transcurrido en bloqueado']]
    for task in queueLocked:
        tableData.append([task.getID(),str(task.getTLock().second) + "'s"])
        task.setTLock(task.getTLock() + incrementTime)
        task.setWaitingTime(task.getTFS() + task.getTLock())
    table = AsciiTable(tableData)
    print (table.table)

def getEnded(queueEnded):
    incrementTime = timedelta(seconds=1)
    tableData = [['ID', 
                  'Operación', 
                  'Resultado', 
                  'Tiempo de Finalización', 
                  'Tiempo de llegada', 
                  'Tiempo Max. Esperado', 
                  'Tiempo Restante' , 
                  'Tiempo de Respuesta',
                  'Tiempo de Espera',
                  'Tiempo de Servicio']]
    for task in queueEnded:
        if not task.getError():
            tableData.append([task.getID(),
                              task.getOperation(), 
                              task.getResult(), 
                              str(task.getTF().second) + "'s", 
                              str(task.getAT().second) + "'s" ,
                              str(task.getTME().second) + "'s", 
                              str(task.getTR().second) + "'s", 
                              str(task.getTFS()) + "'s", 
                              str(task.getWaitingTime().second ) + "'s",
                              str(task.getServiceTime().second ) + "'s"
                            ])
        else:
            tableData.append([task.getID(),
                              task.getOperation(), 
                              task.getErrorMessages(), 
                              str(task.getTF().second) + "'s", 
                              str(task.getAT().second) + "'s" ,
                              str(task.getTME().second) + "'s", 
                              str(task.getTR().second) + "'s", 
                              str(task.getTFS()) + "'s", 
                              str(task.getWaitingTime().second ) + "'s",
                              str(task.getServiceTime().second) + "'s"
                            ])
    table = AsciiTable(tableData)
    print (table.table)

def somethingOnQueueReady():
    global globalClock
    global endedList
    global lockedList
    global queueReady
    
    incrementTime = timedelta(seconds=1)
    executableProcess = queueReady.pop(0)
    executableProcess.setResult(0)
    
    if not executableProcess.getFirstServe():
        executableProcess.setFirstServe(True)
        executableProcess.setTFS(globalClock - executableProcess.getAT())
        
    while executableProcess.getTR().second > 0:
        
        proc = checkLockedQueue()
        if proc : 
            queueReady.append(proc)
        key=''
        
        executableProcess.setServiceTime(executableProcess.getServiceTime()+incrementTime)
        executableProcess.setTR(executableProcess.getTR() - incrementTime)
            
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8')
            key = key.lower()
            if key == 'i':
                lockedList.append(executableProcess)
                break
            elif key == 'e':
                executableProcess.setError(True)
                executableProcess.addMessage('Finalizacion con error')
                break
            elif key == 'p':
                print('Presiona la tecla "C" para continuar')
                while True:
                    if msvcrt.kbhit():
                        key = msvcrt.getch().decode('utf-8')
                        key = key.lower() 
                        if key == 'c':
                            break
                        
        tmp = sp.call('cls',shell=True)  
        
        printTables()
        
        getExcecutable(executableProcess)
        
        time.sleep(1)
    tmp = sp.call('cls',shell=True)  
        
    printTables()
    if key != 'i':   
        if not executableProcess.getError():
            operationList = []
            operationList = re.split(r"(\x2a|\x2b|\x2d|\x2f|\x5e|\x25)",executableProcess.getOperation())
            
            for word in operationList:
                    if word == "":
                        operationList.remove(word)
            
            result = makeOperation(operationList)
            executableProcess.setResult(result)
        
        executableProcess.setTF(globalClock)
        executableProcess.setReturnTime(globalClock - executableProcess.getAT())
        if executableProcess.getTLock().second > 0: 
            executableProcess.setWaitingTime(executableProcess.getTFS() + executableProcess.getTLock() - incrementTime)
        else:
            executableProcess.setWaitingTime(executableProcess.getTFS() + executableProcess.getTLock())
        endedList.append(executableProcess)
        
        

def printTables():
    global globalClock
    global endedList
    global lockedList
    global queueReady
    incrementTime = timedelta(seconds=1)
    globalClock += incrementTime
    print(f"[*] Temporizador Global --->  {globalClock.second}'s")
    if len(lockedList) > 0:
        getLocked(lockedList)
    else:
        print("[-] No hay procesos bloqueados")
    if len(endedList) > 0:
        getEnded(endedList)  
    else:
        print("[-] No hay procesos terminados")
    if len(queueReady) > 0:
        getReady(queueReady)
    else:
        print("[-] No hay procesos en memoria")
        
def checkLockedQueue():
    global lockedList
    incrementTime = timedelta(seconds=1) 
    if len(lockedList) > 0:
        for process in lockedList:
            if process.getTLock().second > 0:
                if (process.getTLock().second  % 10) == 0:
                    process.setTLock(process.getTLock() + incrementTime)
                    proc = process
                    lockedList.remove(process) 
                    return proc
                
def motor():
    global queueReady
    while len(queueReady) > 0 or len(lockedList) > 0:
        if len(queueReady) > 0:
            somethingOnQueueReady()
            proc = checkLockedQueue()
            if proc : 
                queueReady.append(proc)
        else:
            tmp = sp.call('cls',shell=True)  
            printTables()
            proc = checkLockedQueue()
            if proc : 
                queueReady.append(proc)
            time.sleep(1)
        
    tmp = sp.call('cls',shell=True)
    getEnded(endedList)

def main(n):
    global globalClock
    global queueReady
    RAM = list()
    completeOperationMatch = r"(\x2d)?\d(\x2a|\x2b|\x2d|\x5e|\x2f|\x25)\d"
    timeReg = r"(00:0[7-9]|00:1[0-8])"
    RAM.append([])
    memorySpace = 0
    for id in range(n):
        id += 1
        x = Xeger(limit=5)
        operation = x.xeger(completeOperationMatch)
        TME = x.xeger(timeReg)
        TASK = PCB(id,operation,TME, "00:00")
        TASK.setTR(TME)
        RAM[memorySpace].append(TASK)
        if id % 4 == 0:
            memorySpace += 1
            RAM.append([])
    #print(RAM)
    while len(RAM) > 0:
        queueReady = RAM.pop(0)
        for process in queueReady:
            process.setArriveTime(globalClock)
        motor()
        #print(RAM)   
        
    
        