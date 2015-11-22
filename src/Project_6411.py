'''
Created on Aug 23, 2014

@author: Meet
'''
import sys
import os.path
from string import whitespace
import re


def addData():
    tablename = input('Enter table name:')
    fileschemaname=tablename+'schema.slc'
    filedataname=tablename+'data.slc'
    
    while not os.path.isfile(fileschemaname):
        print('No such schema found')
        tablename = input('Enter another table name:')
        fileschemaname=tablename+'schema.slc'
        filedataname=tablename+'data.slc'
    
    schemafile=open(fileschemaname,'r')
    contents=schemafile.readlines()
    count=contents[1]
    #count #of lines to get the last value i.e. index
   
    with open(fileschemaname) as myfile:
        totallines = sum(1 for line in myfile)
    tempindex=(contents[totallines-1])
    if tempindex[-1:]=='\n':
        index=tempindex[:-1]
    else:
        index=tempindex
   
   
   
    allcolumns=''
    i=0
    while i<int(count):
        #split and get the first element as column name
        columnname=((contents[2+i]).split('|'))[0]
        value=input('enter '+columnname)
        #check for end of line
        if contents[2+i].split('|')[1][-1:]=='\n':
            templn=contents[2+i].split('|')[1][:-1]
        else:
            templn=contents[2+i].split('|')[1]
            
        ok=checkdatatype(value,templn)
        #print(ok)
        while not ok:
            print('data u entered doesnt match the column type')
            value=input('enter '+columnname)
            
            ok=checkdatatype(value,templn)
            print(ok)
            
        if index==columnname:
            #print('index is:'+index+'1')
            #print('col is:'+columnname)
            ans=checkindexuniqueness(i,filedataname,value)
            
            while ans:
                print('Cant allow duplicates in index columns')
                value=input('enter '+columnname)
                ans=checkindexuniqueness(i,filedataname,value)
        
        if i==int(count)-1:
            allcolumns=allcolumns+value+'\n'
            #datafile.write(value+'\n')
        else:
            allcolumns=allcolumns+value+'|'
            #datafile.write(value+'|')
        i=i+1
    
    #check if file already exists
    if os.path.isfile(filedataname):
        datafile=open(filedataname,'a')
    else:
        datafile=open(filedataname,'w')
    
    datafile.write(allcolumns)
    datafile.close()

def createdb():
    tablename = input('Enter table name:')
    filename=tablename+'schema.slc'
    
    #check if file already exists
    while os.path.isfile(filename):
        print('table name already exists')
        tablename = input('Enter another table name:')
        filename=tablename+'schema.slc'
            
    
    
    
    
    count = input('Enter number of columns')
    #if user didnt enter digit
    i=0
    while not (count.isdigit()):
        print('please enter valid integer number')
        count = input('Enter number of columns')
        
    columnlist=[]
    allcolumns=''
    while i<int(count):
        #get column input here
        column=input('enter column name & type separated with |: ')
        result=checkcolumn(column)
        
        while not result:
            column=input('enter column name & type separated with |: ')
            result=checkcolumn(column)
        
        issafe=checkcolumnexist(column.split('|')[0],columnlist)
        #check if column already exists
		while not issafe:
            print('column name already exists')
            column=input('enter column name & type separated with |: ')
            result=checkcolumn(column)
            
            while not result:
                column=input('enter column name & type separated with |: ')
                result=checkcolumn(column)
            
            issafe=checkcolumnexist(column.split('|')[0],columnlist)
            
        #print('good to go')
        columnlist.append(column.split('|')[0])
        allcolumns=allcolumns+column+'\n'
        i=i+1
    
    #write to file
    try:
        file = open(filename,'w')   # Trying to create a new file or open one,if exist it will truncate data
    except:
        print('Something went wrong! Can\'t tell what?')
        sys.exit(0)
        
    file.write(tablename+'\n')
    file.write(count+"\n")
    file.write(allcolumns)
    file.close()
    
    indexcolumn=input('enter index column')
    ans=checkindex(filename, count, indexcolumn)
    
    while not ans:
        print('No such column found')
        indexcolumn=input('enter index column')
        ans=checkindex(filename, count, indexcolumn)
    
    try:
        file = open(filename,'a')   # Trying to create a new file or open one,if exist it will truncate data
    except:
        print('Something went wrong! Can\'t tell what?')
        sys.exit(0)
    
    if (indexcolumn=='\n') or indexcolumn=='' or (not indexcolumn):
        file.write('null\n')
    else:
        file.write(indexcolumn+'\n')
    file.close()
    print()

def updatedata():
    tablename = input('Enter table name:')
    fileschemaname=tablename+'schema.slc'
    filedataname=tablename+'data.slc'
    
    while not os.path.isfile(fileschemaname):
        print('No such schema found')
        tablename = input('Enter another table name:')
        fileschemaname=tablename+'schema.slc'
        filedataname=tablename+'data.slc'
    
    schemafile=open(fileschemaname,'r')
    contents=schemafile.readlines()
    count=contents[1]
    #index=contents[2+int(count)].strip()
    tempindex=contents[2+int(count)]
    if tempindex[-1:]=='\n':
        index=tempindex[:-1]
    else:
        index=tempindex
    #count #of lines to get the last value i.e. index
    
    #teindex.translate(None, whitespace)
   
    #print('index is:'+index)
    if index=='null':
        #that means no indexing
        #do normal adding
        allcolumns=''
        i=0
        while i<int(count):
            
            columnname=((contents[2+i]).split('|'))[0]
            value=input('enter '+columnname)
            ok=checkdatatype(value,contents[2+i].split('|')[1].strip())
            #print(ok)
            while not ok:
                print('data u entered doesnt match the column type')
                value=input('enter '+columnname)
                ok=checkdatatype(value,contents[2+i].split('|')[1].strip())
                print(ok)
                
            if i==int(count)-1:
                allcolumns=allcolumns+value+'\n'
                #datafile.write(value+'\n')
            else:
                allcolumns=allcolumns+value+'|'
                #datafile.write(value+'|')
            i=i+1
        
        #check if file already exists
        if os.path.isfile(filedataname):
            datafile=open(filedataname,'a')
        else:
            datafile=open(filedataname,'w')
        
        datafile.write(allcolumns)
        datafile.close()
    else:   #there is indexing
        
        allcolumns=''
        i=0
        while i<int(count):
            
            columnname=((contents[2+i]).split('|'))[0]
            value=input('enter '+columnname)
            ok=checkdatatype(value,contents[2+i].split('|')[1].strip())
            #print(ok)
            while not ok:
                print('data u entered doesnt match the column type')
                value=input('enter '+columnname)
                ok=checkdatatype(value,contents[2+i].split('|')[1].strip())
                print(ok)
                
            if index==columnname:
                #print('index is:'+index+'1')
                #print('col is:'+columnname)
                ans=checkindexuniqueness(i,filedataname,value)
                if ans:
                    deleteline(i,filedataname,value)
                    #print('deleted!')
            
            if i==int(count)-1:
                allcolumns=allcolumns+value+'\n'
                #datafile.write(value+'\n')
            else:
                allcolumns=allcolumns+value+'|'
                #datafile.write(value+'|')
            i=i+1
        
        #check if file already exists
        if os.path.isfile(filedataname):
            datafile=open(filedataname,'a')
        else:
            datafile=open(filedataname,'w')
        
        datafile.write(allcolumns)
        datafile.close()
    
def deletedata():
    tablename = input('Enter table name:')
    fileschemaname=tablename+'schema.slc'
    filedataname=tablename+'data.slc'
    
    while not os.path.isfile(fileschemaname):
        print('No such schema found')
        tablename = input('Enter another table name:')
        fileschemaname=tablename+'schema.slc'
        filedataname=tablename+'data.slc'
    
    schemafile=open(fileschemaname,'r')
    contents=schemafile.readlines()
    count=contents[1]
    #count #of lines to get the last value i.e. index
   
    with open(fileschemaname) as myfile:
        totallines = sum(1 for line in myfile)
    index=(contents[totallines-1]).strip()
    if index=='null':
        return 'No index found,cant delete!'
    
    
    value=input('enter '+index)
    
    i=0
    while i<int(count):
        if ((contents[2+i]).split('|'))[0]==index.strip():
            #columnnumber=i
            ans=checkindexuniqueness(i, filedataname, value)
            if ans:
                return deleteline(i, filedataname, value)
            else:
                return 'No such record found'
        i=i+1
              
    	
def bulkLoad():
    tablename = input('Enter table name:')
    fileschemaname=tablename+'schema.slc'
    filedataname=tablename+'data.slc'
    
    while not os.path.isfile(fileschemaname):
        print('No such schema found')
        tablename = input('Enter another table name:')
        fileschemaname=tablename+'schema.slc'
        filedataname=tablename+'data.slc'
    
    schemafile=open(fileschemaname,'r')
    contents=schemafile.readlines()
    countcol=contents[1]
    #print(int(countcol))
    apdfile=input('enter name of .apd file')
    
    if os.path.isfile(apdfile):
        file=open(apdfile,'r')
        lines=file.readlines()
        file.close()
    else:
        print('No file found')
        return
    
    with open(fileschemaname) as myfile:
           totallines = sum(1 for line in myfile)
           tempindex=(contents[totallines-1])
    if(tempindex[-1:]=='\n'):
            index=tempindex[1][:-1]
    else:
            index=tempindex
    
    try:
        insertfile=open(filedataname,'w')   # Trying to create a new file or open one
    except:
        print('Something went wrong! Can\'t tell what?')
        sys.exit(0) # quit Python     
    
    wholebulk=''
    for line in lines:
        if (line=='\n') or line=='' or (not line):
            continue
        if not (line.count('|')==int(countcol)-1):
            continue
        
        elements=line.strip().split('|')
        flag=True
        #print(elements)
        i=0
        while i<int(countcol):
            
            if checkdatatype(line.split('|')[i], ((contents[2+i]).split('|'))[1].strip()):
                #print('done')
                i=i+1
                #continue
            else:
                flag=False
                break    
            #i=i+1
        
        if flag:
            insertfile.write(line)
            #print(elements)
    
    insertfile.close()
#join two tables
def displayjoin():
    tablename1 = input('Enter table 1 name:')
    fileschemaname1=tablename1+'schema.slc'
    filedataname1=tablename1+'data.slc'
    
    while not os.path.isfile(fileschemaname1):
        print('No such schema found')
        tablename1 = input('Enter another table name:')
        fileschemaname1=tablename1+'schema.slc'
        filedataname1=tablename1+'data.slc'
        
    tablename2 = input('Enter table 2 name:')
    fileschemaname2=tablename2+'schema.slc'
    filedataname2=tablename2+'data.slc'
    
    while not os.path.isfile(fileschemaname2):
        print('No such schema found')
        tablename2 = input('Enter another table name:')
        fileschemaname2=tablename2+'schema.slc'
        filedataname2=tablename2+'data.slc'
        
    joincol=input('enter join column:')

    collist1=getcolumnlist(fileschemaname1)
    collist2=getcolumnlist(fileschemaname2)
    
    if ((joincol in collist1) and (joincol in collist2)):
        colnumber1=findcolumnnumber(fileschemaname1,joincol)
        colnumber2=findcolumnnumber(fileschemaname2,joincol)
        #print(colnumber1)
        #print(colnumber2)
        totallines1=gettotallines(filedataname1)
        totallines2=gettotallines(filedataname2)
        lines1 = tuple(open(filedataname1, 'r'))
        lines2 = tuple(open(filedataname1, 'r'))
        x=0
        y=0
        output=[]
        while x<totallines1:
            while y<totallines2:
                if lines1[x].split('|')[colnumber1]==lines2[y].split('|')[colnumber2]:
                    templine2output=''
                    a=0
                    while a<len(collist2):
                        if not a==colnumber2:
                            if (lines2[y].split('|'))[a][-1:]=='\n':
                                addline=(lines2[y].split('|'))[a][:-1]
                            else:
                                addline=lines2[y].split('|')[a]
                            #print(lines2[y].split('|')[a])
                            templine2output=templine2output+'|'+addline
                            
                        a=a+1
                    
                    if lines1[x][-1:]=='\n':
                        addline=lines1[x][:-1]
                    else:
                        addline=lines1[x][:-1]
                    output.append(addline+templine2output)
                    #print(output)
                y=y+1
            
            x=x+1
        
        for printline in output:
            print(printline)
        
    else:
        print('join column doesnt exist in both tables')
        return
    
    

def showmenu():
    print('Project_6411')
    print()
    
    print('1.Create database')
    print('2.Update record')
    print('3.Add record')
    print('4.Delete record')
    print('5.Bulk Load')
    print('6.Display Join')
    print('7.Report 1')
    print('8.Exit')
    
    choice=input('Enter your choice')
    choice=int(choice)
    while True:
        if choice==1:
            createdb()
        elif choice==2:
            updatedata()
        elif choice==3:
            addData()
        elif choice==4:
            deletedata()
        elif choice==5:
            bulkLoad()
        elif choice==6:
            displayjoin()
        elif choice==7:
            os.system("C:\\Users\\anadk_000\\workspace\\Project_6411\\Hask.exe")
        elif choice==8:
            sys.exit(1)
        else:
            print('invalid choice')
        
        showmenu()
        choice=input('Enter your choice')
        choice=int(choice)
    #operation=input("Enter your choice")
    #processRequest(operation)

def gettotallines(filename):
    with open(filename) as myfile:
        totallines = sum(1 for line in myfile)
    
    return totallines

def findcolumnnumber(fileschemaname1,joincol):
    file=open(fileschemaname1,'r')
    contents=file.readlines()
    countcol=int(contents[1])
    i=0
    while i<countcol:
        if (contents[2+i].split('|'))[0]==joincol:
            return i
        else:
            i=i+1

def getcolumnlist(filename):
    file=open(filename,'r')
    contents=file.readlines()
    countcol=int(contents[1])
    list=[]
    i=0
    while i<countcol:
        #print((contents[2+i].split('|'))[0])
        list.append((contents[2+i].split('|'))[0])
        i=i+1
    
    #print(list)
    return list 
    

def checkcolumnexist(column,list):
    if (column in list):
        return False
    else:
        return True
    
def deleteline(i,filename,value):
    #check if file already exists
    if os.path.isfile(filename):
        lines = tuple(open(filename, 'r'))
    else:
        return True
    linetodelete='null'
    for line in lines:
        if line.split('|')[i].strip()==value:
            linetodelete=line
    
    if linetodelete=='null':
        return 'no such record found'
    
    file=open(filename,'r')
    lines=file.readlines()
    file.close()
    
    f=open(filename,'w')
    for line in lines:
        if line!=linetodelete:
            f.write(line)
    f.close()
    return 'deleted successfully'
    
def checkindex(filename,count,str):
    if (str=='\n') or str=='' or (not str):
        return True
    flag=False
    lines = tuple(open(filename, 'r'))
    i=0;
    while i<int(count):
        temp=lines[2+i].split('|')
        if temp[0]==str:
        #print('found')
            flag=True
            break
        else:
            i=i+1
    #print(lines[2])   
    return flag
    
    
def checkindexuniqueness(i,filename,value):
    lines=''
    #check if file already exists
    if os.path.isfile(filename):
        lines = tuple(open(filename, 'r'))
    else:
        return False
    
    #count #of lines
    with open(filename) as myfile:
        totallines = sum(1 for line in myfile)
    j=0
    while j<totallines:
        if (lines[j]=='\n') or lines[j]=='' or (not lines[j]):
            continue
        if lines[j].split('|')[i].strip()==value:
            return True
        else:
            j=j+1
    
    return False
        
    

    
def checkcolumn(str):
    flag=False
    if not (str.count('|')<1 or str.count('|')>1):
        splittedstr=str.split('|')
        if (splittedstr[1]=='STRING' or splittedstr[1]=='INT' or splittedstr[1]=='FLOAT'):
            flag=True
        else:
            print('wrong datatype')
    else:
        print('there should be exactly one |')
    
    return flag

def test():
    s="msdlkfjdsf"
    #print(isinstance(s, basestring))
    k=123.0
    print(type(k) is float)
    word='sdfdf\n'
    if word[-1:]=='\n':
        word=word[:-1]
    print(word+'sokk')
        
          
    
def checkdatatype(value,datatype):
    
    if datatype=='STRING':
        return True
    elif datatype=='INT':
        return value.isdigit()
    elif datatype=='FLOAT':
        if re.match("^\d+?\.\d+?$", value) is None:
            return False
        else:
            return True
        


showmenu()


