

FROM python:3.9.0-alpine

COPY requirements.txt aligo.json /

RUN mkdir /root/.aligo && \
    mv aligo.json /root/.aligo/aligo.json && \
    /usr/local/bin/python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install --upgrade setuptools -i https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip install -r requirements.txt && \
    rm -rf requirements.txt && \
    echo "https://mirrors.aliyun.com/alpine/v3.9/main/" > /etc/apk/repositories && \
    echo "https://mirrors.aliyun.com/alpine/v3.9/community/" >> /etc/apk/repositories && \
    apk upgrade --no-cache apk-tools && \
    apk add --no-cache openssh tzdata nodejs npm && \
    npm install -g crypto-js && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    sed -i "s/#PermitRootLogin.*/PermitRootLogin yes/g" /etc/ssh/sshd_config && \
    ssh-keygen -t dsa -P "" -f /etc/ssh/ssh_host_dsa_key && \
    ssh-keygen -t rsa -P "" -f /etc/ssh/ssh_host_rsa_key && \
    ssh-keygen -t ecdsa -P "" -f /etc/ssh/ssh_host_ecdsa_key && \
    ssh-keygen -t ed25519 -P "" -f /etc/ssh/ssh_host_ed25519_key && \
    echo "root:03456" | chpasswd && \
    /usr/sbin/sshd




