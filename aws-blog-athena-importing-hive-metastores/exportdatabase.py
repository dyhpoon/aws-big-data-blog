import sys, os

schema=sys.argv[1]

command="hive --database "+schema+" -e 'show tables' -S"
tables=[]
separator='!echo \;;'

os.system("rm "+schema+"*.hql 2> /dev/null")
os.system("rm "+schema+"output 2> /dev/null")

p = os.popen(command,"r")
while 1:
    line = p.readline()
    if not line: break
    tables.append(line)

print "\nFound "+str(len(tables))+" tables in database..."

with open(schema+'_tables.hql',mode='w+') as output:
   for i in tables:
      output.write('!echo DROP TABLE `'+i[:-1]+'`\;;\n')
      output.write('show create table '+i[:-1]+';\n')
      output.write(separator+'\n')

command="hive -f "+schema+"_tables.hql -S >> "+schema+".output"
p = os.system(command)

sqlfile=open(schema+'_export.hql', mode="w+")
sqlfile.write("-- HIVE SCHEMA EXPORT FILE. DO NOT EDIT THIS FILE --\n")

with open(schema+'.output', mode="r") as ddlfile:
   reader=ddlfile.read()
   for i,part in enumerate(reader.split("DROP ")):
      if "EXTERNAL TABLE" in part:
         sqlfile.write( "DROP "+part)

print "\nDatabase metadata exported to "+schema+"_export.hql."   
os.system("rm "+schema+"_tables.hql 2> /dev/null")
os.system("rm "+schema+".output 2> /dev/null")
