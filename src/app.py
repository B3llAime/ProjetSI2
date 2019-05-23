# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for
import os
import subprocess
import MySQLdb
import paramiko
from _mysql import NULL
#from MySQLHelper import *
import MySQLdb



# Initialize the Flask application
app = Flask(__name__)


######################################################################################################################

class DockerModel:
    username=NULL
    docker_id=NULL
    name=NULL
    database=NULL
    cpu=NULL
    memory=NULL
    port=NULL

###########  CONNECTION   ##############################################################################################

def createUnixConnection(ip,uname,password):
    con = paramiko.SSHClient()
    con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    con.connect(ip, username=uname, password=password)
    return con

def endUnixConnection(con):
    con.close()
    return None

##############  DOCKER MGMT      ##################################################################################################

def createDocker(dockerobj):
    if dockerobj.database=='mongodb':
        tmp_str = 'docker run -i -t -d -p 27017 -v /root/Docker/database_files:/tmp/db_files -m '+dockerobj.memory+" mongodb"
        print tmp_str
    stdin, stdout, stderr = con1.exec_command(tmp_str)
    
    dockerobj.docker_id= stdout.readlines()[0].rstrip()
    dockerobj= getDockerDetails(dockerobj)
    addDockerDetails(dockerobj)
    return dockerobj

def getDockerDetails(dockerobj):
    tmp_str_port="docker inspect "+dockerobj.docker_id[:5]+" | grep HostPort | awk {'print $2'} | cut -d '\"' -f 2"
    stdin, stdout, stderr = con1.exec_command(tmp_str_port)
    dockerobj.port=stdout.readlines()[0].rstrip()
   
    return dockerobj


##############  DOCKER DATABASE MGMT     ##################################################################################################

docker_db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="a", # your password
                    db="dbaas")

docker_cur = docker_db.cursor()



def addDockerDetails(dockerobject):
    tmp="insert into docker_relation (`userid`,`dockerid`) values ('"+dockerobject.username+"','"+dockerobject.docker_id+"');"
    print tmp
    docker_cur.execute(tmp)
    docker_db.commit()
    tmp="insert into docker_details (`docker_id`,`docker_name`,`database`,`cpu`,`memory`,`port`) values ('"+dockerobject.docker_id+"','"+dockerobject.name+"','"+dockerobject.database+"','"+dockerobject.cpu+"','"+dockerobject.memory+"','"+dockerobject.port+"');"
    print tmp
    docker_cur.execute(tmp)
    docker_db.commit()
    #docker_db.close()
    return NULL 

def getAllDockerUser(username):
    tmp ="select rel.dockerid,doc.docker_name,doc.database,doc.cpu,doc.memory,doc.port from docker_relation AS rel, docker_details as doc  where userid='"+username+"' and dockerid=doc.docker_id;"
    print tmp
    docker_cur.execute(tmp)
    data=docker_cur.fetchall()
    print data
    return data
    
##############  INITIALIZATION   ##################################################################################################
    
con1=createUnixConnection('localhost', 'root', 'a')



############################




# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('login_form_submit.html')

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case

login_db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="a", # your password
                      db="dbaas") # name of the data base

# you must create a Cursor object. It will let
#  you execute all the queries you need
login_cur = login_db.cursor()


@app.route('/hello/', methods=['POST'])
def hello():
    username=request.form['yourusername']
    password=request.form['yourpassword']
    if login_cur.execute("select * from dbaas.credentials where username='"+username+"' and password='"+password+"'"):
        login_db.close()
        return render_template('login_form_action.html', username=username, password=password)
    else:
        login_db.close()
        return render_template('failed_login.html')


@app.route('/hello/create_container', methods=['POST'])
def redirect_create_container():
    username=request.form['username']
    return render_template('create_container.html',username=username)


@app.route('/hello/submit_container', methods=['POST'])
def redirect_submit_container():
    dockerobj=DockerModel ()
    
    dockerobj.username=request.form['username']
    dockerobj.name=request.form['docker_name']
    dockerobj.database=request.form['database']
    dockerobj.cpu=request.form['cpu']
    dockerobj.memory=request.form['memory']
    dockerobj=createDocker(dockerobj)
    return render_template('view_container.html',username=dockerobj.username,docker_id=dockerobj.docker_id,name=dockerobj.name,database=dockerobj.database,cpu=dockerobj.cpu,memory=dockerobj.memory,port=dockerobj.port)



@app.route('/hello/view_container', methods=['POST'])
def view_container():
    dockerobj=DockerModel ()
    
    dockerobj.username=request.form['username']
    dockerobj.docker_id=request.form['docker_id']
    dockerobj.name=request.form['docker_name']
    dockerobj.database=request.form['database']
    dockerobj.cpu=request.form['cpu']
    dockerobj.memory=request.form['memory']
    dockerobj.memory=request.form['port']

    return render_template('view_container.html',username=dockerobj.username,docker_id=dockerobj.docker_id,name=dockerobj.name,database=dockerobj.database,cpu=dockerobj.cpu,memory=dockerobj.memory,port=dockerobj.port)



@app.route('/hello/view_all_container', methods=['POST'])
def view_all_container():
    username=request.form['username']
    data=getAllDockerUser(username);
    return render_template('view_all_container.html',username=username,data=data)
    

# Run the app :)
if __name__ == '__main__':
  app.run( 
        debug=True,
        host="192.168.141.128",
        port=int("8080")
  )

