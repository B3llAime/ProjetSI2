import paramiko
import MySQLdb

def createUnixConnection(ip,uname,password):
    con = paramiko.SSHClient()
    con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    con.connect(ip, username=uname, password=password)
    return con

def endUnixConnection(con):
    con.close()
    return None


con1=createUnixConnection('localhost', 'root', 'a')
stdin, stdout, stderr = con1.exec_command("for i in `docker ps -a | grep -v cadvisor | awk 'NR>1{print $1}'`;do docker stop $i && docker rm $i;done")
endUnixConnection(con1)

docker_db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="a", # your password
                    db="dbaas")

docker_cur = docker_db.cursor()
docker_cur.execute("truncate docker_relation")
docker_db.commit()
docker_cur.execute("truncate docker_details")
docker_db.commit()
docker_db.close()
