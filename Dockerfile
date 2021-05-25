FROM python:3.8
RUN apt-get update -y

COPY deps/ta-lib-0.4.0-src.tar.gz /ta-lib-0.4.0-src.tar.gz 
RUN tar -xzf /ta-lib-0.4.0-src.tar.gz && cd ta-lib/ && ./configure --prefix=/usr && make && make install
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip3 install -r requirements.txt

#######################
# Running purpose
#######################
COPY src/* /
ENTRYPOINT ["python3", "-u", "/main.py"]

######################
# Testing purpose
######################
# COPY test.py /test.py
# ENTRYPOINT ["python3", "-u", "test.py"]
