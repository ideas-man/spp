_pkgname=spp
pkgname=$_pkgname-git
pkgver=0.2.0
pkgrel=1
pkgdesc="Simple Python Prompt"

arch=('any')
license=('Unlicense')
depends=(python)
provides=($_pkgname)
source=('spp.py' 'spp.zsh')
install='spp.install'
sha256sums=('SKIP' 'SKIP')

package() {
    install -Dm 755 spp.py "$pkgdir/usr/bin/spp"
    install -Dm 644 spp.zsh "$pkgdir/usr/share/spp/spp.zsh"
}