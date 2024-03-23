FROM python:3.10.12

WORKDIR /usr/local/bin

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT ["/bin/bash","/usr/local/bin/File.sh"]