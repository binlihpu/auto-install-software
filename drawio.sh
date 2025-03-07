#!/bin/bash

VERSION="v20.2.8"

if [ -n "$1" ];then VERSION=$1; fi

FILEURL=https://github.com/jgraph/drawio-desktop/releases/download/v${VERSION}/drawio-x86_64-${VERSION}.AppImage

_main() {
    which sudo >/dev/null && SUDO="sudo"

    cd /tmp \
    && wget -c $FILEURL -O drawio.AppImage \
    && ${SUDO} mkdir -p /opt/drawio \
    && ${SUDO} cp drawio.AppImage /opt/drawio \
    && ${SUDO} chmod +x /opt/drawio/drawio.AppImage

    [ $? -ne 0 ] && return
    cat << EOF > /opt/drawio/drawio.svg
<?xml version="1.0" encoding="utf-8"?>
<!-- Generator: Adobe Illustrator 21.1.0, SVG Export Plug-In . SVG Version: 6.00 Build 0)  -->
<svg version="1.1" id="Ebene_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
         viewBox="0 0 161.6 161.6" style="enable-background:new 0 0 161.6 161.6;" xml:space="preserve">
<style type="text/css">
        .st0{fill:#F08705;}
        .st1{fill:#DF6C0C;}
        .st2{fill:#FFFFFF;}
        .st3{fill:#333333;}
</style>
<g>
        <path class="st0" d="M161.6,154.7c0,3.9-3.2,6.9-6.9,6.9H6.9c-3.9,0-6.9-3.2-6.9-6.9V6.9C0,3,3.2,0,6.9,0h147.8
                c3.9,0,6.9,3.2,6.9,6.9L161.6,154.7L161.6,154.7z"/>
        <g>
                <path class="st1" d="M161.6,154.7c0,3.9-3.2,6.9-6.9,6.9H55.3l-32.2-32.7l20-32.7l59.4-73.8l58.9,60.7L161.6,154.7z"/>
        </g>
        <path class="st2" d="M132.7,90.3h-17l-18-30.6c4-0.8,7-4.4,7-8.6V28c0-4.9-3.9-8.8-8.8-8.8h-30c-4.9,0-8.8,3.9-8.8,8.8v23.1
                c0,4.3,3,7.8,6.9,8.6L46,90.4H29c-4.9,0-8.8,3.9-8.8,8.8v23.1c0,4.9,3.9,8.8,8.8,8.8h30c4.9,0,8.8-3.9,8.8-8.8V99.2
                c0-4.9-3.9-8.8-8.8-8.8h-2.9L73.9,60h13.9l17.9,30.4h-3c-4.9,0-8.8,3.9-8.8,8.8v23.1c0,4.9,3.9,8.8,8.8,8.8h30
                c4.9,0,8.8-3.9,8.8-8.8V99.2C141.5,94.3,137.6,90.3,132.7,90.3z"/>
</g>
</svg>
EOF
    echo """[Desktop Entry]
Name=drawio
Exec=/opt/drawio/drawio.AppImage
Terminal=false
Type=Application
Icon=/opt/drawio/drawio.svg
StartupWMClass=drawio
X-AppImage-Version=${VERSION}
Comment=diagrams.net desktop
MimeType=application/vnd.jgraph.mxfile;application/vnd.visio;
Categories=Graphics;
""" | ${SUDO} tee  /usr/share/applications/drawio.desktop >/dev/null \
    && echo "install drawio ${VERSION} success"
}

_main