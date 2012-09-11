# Maintainer: Leonidas Spyropoulos <artafinde at gmail dot com>

pkgname=python2-caatinga-git
pkgver=20120911
pkgrel=1
pkgdesc="Caatinga is a command line backup program written in Python - Git Version"
arch=('any')
url="https://github.com/headmastersquall/caatinga"
license=('GPL3')
depends=('python2')
makedepends=('git')
provides=('caatinga')
source=()
md5sums=()

_gitroot="https://github.com/headmastersquall/caatinga"
_gitname="caatinga"

build() {
    cd ${srcdir}
    msg "Connecting to GIT server.."

    if [ -d ${_gitname} ] ; then
        cd ${_gitname} && git pull origin
        msg "The local files are updated."
    else
        git clone ${_gitroot} ${_gitname}
    fi

    msg "GIT checkout done or server timeout"
    msg "Starting make.."
    
    cd ${srcdir}/${_gitname}
    python2 setup.py install --root="${pkgdir}/" --optimize=1
}

# vim:set ts=2 sw=2 et:
