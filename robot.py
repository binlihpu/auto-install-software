import requests
import re
from typing import TextIO,Tuple
from git import Repo

class Robot(object):

    def __init__(self):
        self.req = requests.Session()
        self.changed = {}
        self.repo = Repo()

    def start(self):
        for key in self.__class__.__dict__.keys():
            if key.startswith('_') or key in ['start']:
                continue
            getattr(self,key, None)()

        self._done()

    def _done(self):
        if bool(self.changed):
            origin = self.repo.remote('origin')
            commmit_message = 'update ' + ''.join(['%s:%s,' %(key, value) for (key, value) in self.changed.items()]).rstrip(',')
            self.repo.index.add([key for key in self.changed])
            self.repo.index.commit(commmit_message)
            origin.push()
        


    def code_server(self):
        with open("code-server.sh","r+") as f:
            self._change_version_tag_github(f,"cdr/code-server")

    def docker_compose(self):
        with open("docker-compose.sh","r+") as f:
            self._change_version_tag_github(f,"docker/compose")

    def drawio(self):
        with open("drawio.sh","r+") as f:
            self._change_version_tag_github(f,"jgraph/drawio-desktop")

    def firefox(self):
        ack = self.req.get("https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=zh-CN", allow_redirects=False)
        if ack.status_code == 302:
            real_download_url = ack.headers.get('Location')
            match = re.search(r'.*firefox-(.*)\.tar.*',real_download_url)
            if real_download_url and match:
                version = match.group(1)
                with open("firefox.sh", "r+") as f:
                    lines = f.readlines()
                    for index,line in enumerate(lines):
                        if line.startswith("fileUrl") is False:
                            continue
                        curVersion = re.search(r'.*firefox-(.*)\.tar.*',line.split('=')[-1].strip('\n').strip('"')).group(1)
                        if real_download_url != line.split('=')[-1].strip('\n').strip('"'):
                            lines[index] = 'fileUrl="{url}"\n'.format(url=real_download_url)
                            f.seek(0)
                            f.truncate()
                            f.writelines(lines)
                            self.changed.setdefault(f.name, version)
                            print(f"更新成功:firefox {curVersion} --> {version}")
                            break
                        else:
                            print(f"更新忽略:firefox 当前版本:{curVersion} --> 远程版本:{version}")
                            break

    def go(self):
        ack = self.req.get('https://golang.org/dl/')
        if ack.status_code == 200:
            match = re.search(r'.*download downloadBox.*go(.*)\.linux-amd64.*gz"',ack.text)
            if match:
                version = match.group(1)
                with open("go.sh", "r+") as f:
                    lines = f.readlines()
                    for index,line in enumerate(lines):
                        if line.startswith("VERSION") is False:
                            continue
                        curVersion = line.split('=')[-1].strip('\n').strip('"')
                        if  curVersion != version:
                            lines[index] = 'VERSION="{version}"\n'.format(version=version)
                            f.seek(0)
                            f.truncate()
                            f.writelines(lines)
                            self.changed.setdefault(f.name, version)
                            print(f"更新成功:go {curVersion} --> {version}")
                            break
                        else:
                            print(f"更新忽略:go 当前版本:{curVersion} --> 远程版本:{version}")
                            break

    def hugo(self):
        with open("hugo.sh","r+") as f:
            self._change_version_tag_github(f,"gohugoio/hugo")

    def java(self):
        pass

    def node(self):
        with open("node.sh","r+") as f:
            self._change_version_tag_github(f,"nodejs/node")

    def ohmyzsh(self):
        pass

    def postman(self):
        pass

    def protoc(self):
        with open("protoc.sh","r+") as f:
            self._change_version_tag_github(f,"protocolbuffers/protobuf")

    def rclone(self):
        with open("rclone.sh","r+") as f:
            self._change_version_tag_github(f,"rclone/rclone")

    def sublime_text(self):
        pass

    def syncthing(self):
        with open("syncthing.sh","r+") as f:
            self._change_version_tag_github(f,"syncthing/syncthing")

    def vscode(self):
        ack = self.req.get('https://code.visualstudio.com/sha/download?build=stable&os=linux-x64', allow_redirects=False)
        if ack.status_code == 302:
            real_download_url = ack.headers.get('Location')
            real_download_url = real_download_url.replace("az764295.vo.msecnd.net/stable","vscode.cdn.azure.cn/stable")
            if real_download_url.endswith('.tar.gz'):
                with open('vscode.sh', 'r+') as f:
                    lines = f.readlines()
                    for index,line  in enumerate(lines):
                        if line.startswith('fileUrl') is False:
                            continue
                        if real_download_url != line.split('=')[-1].strip('\n').strip('"'):
                            lines[index] = 'fileUrl="{url}"\n'.format(url=real_download_url)
                            f.seek(0)
                            f.truncate()
                            f.writelines(lines)
                            print(f"更新成功:vscode {line.split('/')[-2]} --> {real_download_url.split('/')[-2]}")
                            self.changed.setdefault(f.name, real_download_url.split('/')[-2][:5])
                        else:
                            print(f"更新忽略:vscode 当前版本:{line.split('/')[-2]} --> 远程版本:{real_download_url.split('/')[-2]}")
                            break

    def tigervnc(self):
        ack = self.req.get("http://tigervnc.bphinz.com/nightly/nightly.html")
        if ack.status_code == 200:
            match = re.search(r'>tigervnc-(.*)x86_64.tar.gz', ack.text)
            if match:
                fileName = match.group(0).lstrip(">")
                fileUrl = f'http://tigervnc.bphinz.com/nightly/xc/x86_64/{fileName}'
                with open("tigervnc.sh", "r+") as f:
                    self._update_file(f, fileName, fileUrl)

    def etcd(self):
        with open("etcd.sh","r+") as f:
            self._change_version_tag_github(f,"etcd-io/etcd")

    def upx(self):
        with open("upx.sh","r+") as f:
            self._change_version_tag_github(f,"upx/upx")

    def lua(self):
        with open("lua.sh","r+") as f:
            self._change_version_tag_github(f,"lua/lua")

    # 只用于修改从github检查版本号的脚本文件
    def _change_version_tag_github(self,f:TextIO,name:str):
        lines = f.readlines()
        for index,line in enumerate(lines):
            if line.startswith("VERSION"):
                latest, success = self._check_for_github_release(name)
                if success is False:
                    print(f"更新失败:{name} {latest}")
                    break
                nowVersion = line.split('=')[-1].strip('\n').strip('"')
                if self._compare_verion(nowVersion,latest) is False:
                    print(f"更新忽略:{name} 当前版本:{nowVersion} 远程版本:{latest}")
                    break
                if nowVersion != latest:
                    lines[index] = 'VERSION="{version}"\n'.format(version=latest)
                    f.seek(0)
                    f.truncate()
                    f.writelines(lines)
                    self.changed.setdefault(f.name, latest)
                    print(f"更新成功:{name} {nowVersion} --> {latest}")
                    break
                else:
                    print(f"更新忽略:{name} 当前版本:{nowVersion} 远程版本:{latest}")

    def _check_for_github_release(self,name:str) ->Tuple[str, bool]:
        url = 'https://api.github.com/repos/{name}/releases/latest'.format(name=name)
        ack = self.req.get(url=url)
        if ack.status_code == 200:
            return ack.json()['tag_name'],True
        else:
            return f"code:{ack.status_code}, err:{ack.reason}",False

    def _update_file(self,f: TextIO, fileName, fileUrl):
        lines = f.readlines()
        isChanged = False
        for index, line in enumerate(lines):
            if line.startswith("fileUrl") and fileUrl != line.split('=')[-1].strip('\n').strip('"'):
                lines[index] = 'fileUrl="{url}"\n'.format(url=fileUrl)
                chengedMsg = fileUrl.split('/')[-2][:5]
                if f.name == "tigervnc.sh":
                    chengedMsg = 'latest'
                self.changed.setdefault(f.name, chengedMsg)
                isChanged = True
            elif isChanged and line.startswith("fileName") and fileName != line.split('=')[-1].strip('\n').strip('"'):
                lines[index] = 'fileName="{name}"\n'.format(name=fileName)
        if isChanged:
            f.seek(0)
            f.truncate()
            f.writelines(lines)
    
    # 比较版本号 latestV是否大于nowV
    def _compare_verion(self,nowV:str, latestV:str) ->bool:
        nowVersionNumArr = nowV.lstrip("v").split(".")
        latestVersionNumArr = latestV.lstrip("v").split(".")
        
        if len(nowVersionNumArr) > len(latestVersionNumArr):
            latestVersionNumArr.extend([0 for _ in range(len(nowVersionNumArr)-len(latestVersionNumArr))])
        elif len(nowVersionNumArr) < len(latestVersionNumArr):
            nowVersionNumArr.extend([0 for _ in range(len(latestVersionNumArr)-len(nowVersionNumArr))])

        for index2,v in enumerate(latestVersionNumArr):
            v2 = int(nowVersionNumArr[index2])
            if int(v) > v2:
                return True
            elif int(v) < int(nowVersionNumArr[index2]):
                return False
        return False


if __name__ == "__main__":
    robot = Robot()
    robot.start()
