# New ports collection makefile for:	py-carbon
# Date created:		2011-07-22
# Whom:			Scott Sanders <ssanders@taximagic.com>
#
# $FreeBSD$
#

PORTNAME=	carbon
PORTVERSION=	0.9.8
CATEGORIES=	net-mgmt python
MASTER_SITES=	http://launchpad.net/graphite/1.0/${PORTVERSION}/+download/
PKGNAMEPREFIX=	${PYTHON_PKGNAMEPREFIX}

MAINTAINER=	ssanders@taximagic.com
COMMENT=	Backend data caching and persistence daemon for Graphite

LICENSE=	ASL

MAKE_JOBS_SAFE=	yes

FETCH_ARGS=	"-pRr"		# default '-AFpr' prevents 302 redirects by launchpad

BUILD_DEPENDS=  ${PYTHON_SITELIBDIR}/twisted/__init__.py:${PORTSDIR}/devel/py-twistedCore

USE_PYTHON=	2.5+
USE_PYDISTUTILS=	yes
PYDISTUTILS_NOEGGINFO=	yes
#PYDISTUTILS_INSTALLARGS+=	--install-lib=${LIBDIR}  \
#				--install-scripts=${BINDIR}

CARBON_DBDIR?=	"/var/db/carbon"

USE_RC_SUBR=	carbon-aggregator.sh carbon-cache.sh carbon-relay.sh

.include <bsd.port.pre.mk>

pre-install:
	rm -f ${WRKSRC}/setup.cfg

post-patch:
	@${REINPLACE_CMD} -e "s|LOCAL_DATA_DIR=\"/opt/graphite/storage/whisper/\"|LOCAL_DATA_DIR=\"${CARBON_DBDIR}/whisper/\"|" ${WRKSRC}/lib/carbon/conf.py
	@${REINPLACE_CMD} -e "s|/opt/graphite/storage|${CARBON_DBDIR}|g" ${WRKSRC}/conf/carbon.conf.example
	cd ${WRKSRC}/bin && \
		rm -f *.orig
	@${REINPLACE_CMD} -e "s|%%CARBON_DBDIR%%|${CARBON_DBDIR}|g" \
		-e "s|%%ETCDIR%%|${ETCDIR}|g" ${WRKSRC}/setup.py

.include <bsd.port.post.mk>
