'''
Created on Feb 4, 2018

@author: rob
'''

import sys
import mmap
import datetime


def exitapplication(message):
    print(message)
    input("Press Enter to continue...")
    sys.exit()

def errorCheckDelimiterCount(parsedline,inProvadm,inProvdat, provadmDelCountError, provdatDelCountError):
    if inProvadm == True:
        if parsedline.count(';') != 26:
            provadmDelCountError = provadmDelCountError + 1
    if inProvdat == True:
        if parsedline.count(';') != 11:
            provdatDelCountError = provdatDelCountError + 1
    return(provadmDelCountError,provdatDelCountError)
    
def main():
    
    #setting variables
    lineCount = 0
    createProvadm = True
    createProvdat = True
    now=datetime.datetime.now()
    addToProvadm = False
    addToProvdat = False
    headerProvadm = 'Lablittera;Namn;Adress;Postnr;Ort;Kommunkod;Projekt;Laboratorium;Provtyp;Provtagare;Registertyp;ProvplatsID;Provplatsnamn;Specifik provplats;Provtagningsorsak;Provtyp;Provtypspecifikation;Bedömning;Kemisk bedömning;Mikrobiologisk bedömning;Kommentar;År;Provtagningsdatum;Provtagningstid;Inlämningsdatum;Inlämningstid;'
    headerProvdat = 'Lablittera;Metodbeteckning;Parameter;Mätvärdetext;Mätvärdetal;Mätvärdetalanm;Enhet;Rapporteringsgräns;Detektionsgräns;Mätosäkerhet;Mätvärdespår;Parameterbedömning;Kommentar;'
    provadmDelCountError = 0
    provdatDelCountError = 0

    #open dialogue "Browse to .lab-file"


    #read file
    file = open('/home/rob/programming/references/test_data/example_intarlab_file.lab', mode='r', encoding='utf8')
    lines = file.readlines()
    filemmap = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
    file.close()
    
    #check mandatory variables in .lab-file
    if filemmap.find(b'#Interlab') == -1:
        exitapplication('There is no "#Interlab" tag in the file. Exiting application.')
    if filemmap.find(b'#Version') == -1:
        exitapplication('There is no "#Version" tag in the file. Exiting application.')
    if filemmap.find(b'#Textavgr') == -1:
        exitapplication('There is no "#Textavgränsare" tag in the file. Exiting application.')
    if filemmap.find(b'#Decimaltecken') == -1:
        exitapplication('There is no "#Decimaltecken" tag in the file. Exiting application.')

    #go through each line in file, skip blank lines
    
    for line in lines:
        line.encode('utf8')
        line = line.strip()
        lineCount = lineCount+1
        if line == '':
            continue
        
        #check version
        if line.find('#Version=') != -1:
            print('Checking version...')
            fileVersion = line[-(len(line))+line.find('=')+1:]
            fileVersion.strip()
            print ('.lab file version is',fileVersion)
            
            if fileVersion == '4.0':
                print ('Version supported. Continuing...')
            else:
                exitapplication('Only version 4.0 is supported. Exiting application.')
                
        #check text separator
        if line.find('#Textavgränsare=') != -1:
            print('Checking text separator option...')
            textavgransare = line[-(len(line))+line.find('=')+1:]
            textavgransare.strip()
            print(textavgransare)
            if textavgransare != 'Nej' and textavgransare != 'Ja':
                exitapplication('The option "#Textavgränsare" is not defined or invalid. Exiting application.')
            print('Textavgränsare is set to "',textavgransare,'"')
        
        #check  decimal sign
        if line.find('#Decimaltecken=') != -1:
            print('Checking decimal sign option...')
            decimalSign = line[-(len(line))+line.find('=')+1:]
            decimalSign.strip()
            print(decimalSign)
            if decimalSign != '.' and decimalSign != ',':
                exitapplication('The option "#Decimaltecken" is not defined or invalid. Exiting application.')
            print('Decimal sign is set to "',decimalSign,'"')
            
        #parsing provadm and provdat
        
        if line.find('#Provadm') != -1:
            addToProvadm = True
            addToProvdat = False
            if createProvadm == True:
                createProvadm = False
                fileNameProvadm = 'Provadm_'+now.strftime("%Y-%m-%d-%H:%M")+'.txt'
                fileProvadm = open(fileNameProvadm,"w", encoding='utf8')
                fileProvadm.write(headerProvadm)
            continue

        if line.find('#Provdat') != -1:
            addToProvadm = False
            addToProvdat = True
            if createProvdat == True:
                createProvdat = False
                fileNameProvdat = 'Provdat_'+now.strftime("%Y-%m-%d-%H:%M")+'.txt'
                fileProvdat = open(fileNameProvdat,"w", encoding='utf8')
                fileProvadm.write(headerProvdat)
            continue
        
        if line.find('Lablittera') != -1:
            continue

        if addToProvadm == True:
            fileProvadm.write(line)
            fileProvadm.write('\n')
            provadmDelCountError, provdatDelCountError = errorCheckDelimiterCount(line,addToProvadm,addToProvdat, provadmDelCountError, provdatDelCountError)

        if addToProvdat == True:
            fileProvdat.write(line)
            fileProvdat.write('\n')
            provadmDelCountError, provdatDelCountError = errorCheckDelimiterCount(line,addToProvadm,addToProvdat, provadmDelCountError, provdatDelCountError)

    fileProvadm.close()
    fileProvdat.close()
    
    print('PROVADM')
    print('Numbers of lines parsed ')
    print('Number of delimiter errors in provadm ',provadmDelCountError)
    
    print('')
    
    print('PROVDAT')
    print('Numbers of lines parsed ')
    print('Number of delimiter errors in provdat ',provdatDelCountError)
                
main();

# Function that checks count of delimiter ; signs. If it differs on a row, then error message should appear in the end, but not stop program.
# Make writing to log
# Make function for checking number of ";"
# Hard code column names and write them into provadm and provdat


# TODO
# 1. Error messages in console, like delimiter count
# 2. Writing to log with error messages
# 3. Consider it to be a two part program, one that extracts the files, one that parses it and analyses it. When parsing the files, consider using pyTables. 
