############################################################
# Dockerfile to build MongoDB Images
# Base image : Ubuntu
############################################################

# Set the base image to Ubuntu
#FROM your base image
FROM ubuntu
#RUN apt-get update

# File Author / Maintainer
MAINTAINER Example Arun

#RUN apt-get install apache2 -y

# Copy the configuration files from host 
#ADD apache2files/apache2.conf /etc/apache2/apache2.conf
#ADD <curr_dir/file> <DEST_LOC_IN_DOCKER>
ADD mongo_script /tmp/mongo_script


# Expose the default port of MongoDB
EXPOSE 27017


# Set default container command when container starts
CMD bash -C '/tmp/mongo_script';'bash'
