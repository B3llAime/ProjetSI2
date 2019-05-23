'''
import MySQLdb
from DockerManage import *
#from _mysql import NULL

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="a", # your password
                    db="dbaas")

cur = db.cursor()

#cur.execute("select * from dbaas.credentials where username='"+username+"' and password='"+password+"'"): 

def getDockerDetails(dockerobject):
    return NULL


def addDockerDetails(dockerobject):
    tmp="insert into docker_relation (userid,dockerid) values ('"+dockerobject.username+"','"+dockerobject.docker_id+"')"
    print tmp
    cur.execute(tmp)
    
    tmp="insert into docker_details (docker_id,docker_name,database,cpu,memory,port) values ('"+dockerobject.docker_id+"','"+dockerobject.name+"','"+dockerobject.database+"','"+"','"+dockerobject.cpu+"','"+dockerobject.memory+"','"+dockerobject.port+"')"
    print tmp
    cur.execute(tmp)
    
    return NULL 
'''