PORTNAME=	sonda-huawei
DISTVERSIONPREFIX=	v
DISTVERSION=	0.1.1
CATEGORIES=	net-mgmt python

MAINTAINER=	cleber@bsd.com.br
COMMENT=	Multi-source latency and loss probe for Huawei VRP edge routers
WWW=		https://github.com/cleberalves40/Sonda-Huawei

LICENSE=	BSD2CLAUSE
LICENSE_FILE=	${WRKSRC}/LICENSE

BUILD_DEPENDS=	${PYTHON_PKGNAMEPREFIX}setuptools>=61.0:devel/py-setuptools@${PY_FLAVOR} \
		${PYTHON_PKGNAMEPREFIX}wheel>=0:devel/py-wheel@${PY_FLAVOR}
RUN_DEPENDS=	${PYTHON_PKGNAMEPREFIX}netmiko>=4.2.0:net-mgmt/py-netmiko@${PY_FLAVOR} \
		${PYTHON_PKGNAMEPREFIX}tabulate>=0.9.0:devel/py-tabulate@${PY_FLAVOR}

USES=		python
USE_PYTHON=	autoplist concurrent pep517
USE_GITHUB=	yes
GH_ACCOUNT=	cleberalves40
GH_PROJECT=	Sonda-Huawei

NO_ARCH=	yes

.include <bsd.port.mk>

