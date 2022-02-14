FROM centos/python-38-centos7:latest
USER root
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r ./requirements.txt
CMD [ "python", "./main.py" ]



