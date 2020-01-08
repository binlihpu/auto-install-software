#!/usr/bin/env bash

# auto install go

if [ `whoami` != "root" ]; then
    echo "please use root run it"
    exit 1
fi

pushd /tmp >/dev/null
file_url="https://dl.google.com/go/go1.13.3.linux-amd64.tar.gz"
file_name=`echo $file_url | awk -F '/' '{print $NF}'`

wget -c $file_url

rm -rf /usr/local/go

tar -C /usr/local -xzf $file_name

popd >/dev/null

cat /etc/bash.bashrc|grep -q ":/usr/local/go/bin" || echo "export PATH=\$PATH:/usr/local/go/bin" >>/etc/bash.bashrc

echo "install go success!"