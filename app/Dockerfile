FROM python:2.7

# for bcrypt
RUN apt install -y build-essential libffi-dev python-dev


# install masscan
RUN apt update && apt install -y git gcc make libpcap-dev clang python python-pip cron\
    && mkdir -p /root/masscan && git clone https://github.com/robertdavidgraham/masscan /root/masscan/ \
    && cd /root/masscan && make && ln -s /root/masscan/bin/masscan /usr/bin/masscan

# install python requirement
COPY ./requirement.txt /tmp/requirement.txt
