
FROM debian:latest

RUN apt update && apt upgrade -y
RUN apt install git curl python3-pip ffmpeg -y
RUN pip3 install -U pip
RUN cd /
RUN git clone https://github.com/Jeff-04/telegram-bot-python
RUN cd telegram-bot-python
WORKDIR /telegram-bot-python
RUN pip3 install -r requirements.txt
CMD python3 convert_document.py