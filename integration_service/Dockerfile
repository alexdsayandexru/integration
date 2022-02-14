FROM centos/python-38-centos7:latest
USER root

ENV CONTAINER_HOME=/var/www

ADD . $CONTAINER_HOME
WORKDIR $CONTAINER_HOME

RUN pip install -r $CONTAINER_HOME/requirements.txt

RUN pip install cx_Oracle --upgrade
COPY lib/oracle-instantclient19.14-basic-19.14.0.0.0-1.x86_64.rpm oracle-instantclient19.14-basic-19.14.0.0.0-1.x86_64.rpm
RUN yum -y install oracle-instantclient19.14-basic-19.14.0.0.0-1.x86_64.rpm

