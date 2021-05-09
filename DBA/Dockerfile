FROM python:3
WORKDIR /home/tom/Desktop/endboss
COPY totaalfile.py totaalfile.py
COPY Runner.sh Runner.sh

RUN apt-get update
RUN apt-get -y upgrade

RUN apt-get install -y python3
RUN apt-get install -y python3-pip


RUN pip3 install beautifulsoup4 
RUN pip3 install requests
RUN pip3 install redis
RUN pip3 install pymongo


CMD ["./Runner.sh"]
ENTRYPOINT ["bash"]
