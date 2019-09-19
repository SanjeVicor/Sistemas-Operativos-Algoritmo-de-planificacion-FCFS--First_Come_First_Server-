from xeger import Xeger
from PCB import PCB
from terminaltables import AsciiTable
import msvcrt
import subprocess as sp 
from datetime import datetime
from datetime import timedelta
import time

globalClock = datetime.strptime("00:00", "%M:%S")
endedList = list()
lockedList = list()
queueReady = list()

def getReady(memorySpace): 
    tableData = [['ID', 'Tiempo Maximo Esperado', 'Tiempo Restante']]
    for pendingTask in memorySpace:
        tableData.append([pendingTask.getID(),str(pendingTask.getTME().second) + "'s", str(pendingTask.getTR().second) + "'s"])
    table = AsciiTable(tableData)
    print (table.table)

def getExcecutable(process):
    tableData = [['ID', 'Operación', 'Tiempo de llegada', 'Tiempo de Respuesta', 'Tiempo de espera', 'Tiempo de Servicio']]
    tableData.append([process.getID(),str(process.getTME().second) + "'s", str(process.getTR().second) + "'s"])
    table = AsciiTable(tableData)
    print (table.table)

def getLocked(queueLocked):
    incrementTime = timedelta(seconds=1)
    tableData = [['ID', 'Tiempo transcurrido en bloqueado']]
    for task in queueLocked:
        tableData.append([task.getID(),str(task.getTLock().second) + "'s"])
        task.setTLock(task.getTLock() + incrementTime)
    table = AsciiTable(tableData)
    print (table.table)

def getEnded(queueEnded):
    tableData = [['ID', 'Operación', 'Resultado']]
    for task in queueEnded:
        if not task.getError():
            tableData.append([task.getID(),task.getOperation(), task.getResult()])
        else:
            tableData.append([task.getID(),task.getOperation(), task.getErrorMessages()])
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
    while executableProcess.getTR().second > 0:
        proc = checkLockedQueue()
        if proc : 
            queueReady.append(proc)
        key=''
        executableProcess.setTR(executableProcess.getTR() - incrementTime)
            
        printTables()
        getExcecutable(executableProcess)
            
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
        time.sleep(1)
        tmp = sp.call('cls',shell=True)
    if key != 'i':    
        endedList.append(executableProcess)

def printTables():
    global globalClock
    global endedList
    global lockedList
    global queueReady
    getLocked(lockedList)
    getEnded(endedList)  
    getReady(queueReady)

def checkLockedQueue():
    global lockedList
    for process in lockedList:
        if process.getTLock().second == 10:
            proc = process
            lockedList.remove(process)
            return proc
    return None
            
def motor():
    global queueReady
    while len(queueReady) > 0 or len(lockedList) > 0:
        if len(queueReady) > 0:
            somethingOnQueueReady()
            proc = checkLockedQueue()
            if proc : 
                queueReady.append(proc)
        else:
            proc = checkLockedQueue()
            if proc : 
                queueReady.append(proc)
        
    tmp = sp.call('cls',shell=True)
    getEnded(endedList)

def main(n):
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
        motor()
        #print(RAM)   
        
    
        