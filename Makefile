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

FETCH_ARGS=	"-pRr"

USE_PYTHON=	2.5+
USE_PYDISTUTILS=	yes
PYDISTUTILS_NOEGGINFO=	yes
GRAPHITE_DIR=	graphite
GRAPHITE_BASE=	${PREFIX}/graphite
USE_RC_SUBR=	carbon-aggregator.sh carbon-cache.sh carbon-relay.sh
SUB_LIST=	GRAPHITE_BASE=${GRAPHITE_BASE}
PYDISTUTILS_INSTALLARGS+=	--install-data=${GRAPHITE_BASE} \
				--install-lib=${GRAPHITE_BASE}/lib  \
				--install-scripts=${GRAPHITE_BASE}/bin

.include <bsd.port.pre.mk>

pre-install:
	rm -f ${WRKSRC}/setup.cfg

post-patch:
	@${REINPLACE_CMD} -e "s|LOCAL_DATA_DIR=\"/opt/graphite/storage/whisper/\"|LOCAL_DATA_DIR=\"${GRAPHITE_BASE}/storage/whisper/\"|" ${WRKSRC}/lib/carbon/conf.py
	@${REINPLACE_CMD} -e "s|/opt/graphite|${GRAPHITE_BASE}|g" ${WRKSRC}/conf/carbon.conf.example
	cd ${WRKSRC}/bin && \
		rm -f *.orig

post-install:
	cd ${PREFIX}/bin && \
		ln -sf ${GRAPHITE_BASE}/bin/carbon-aggregator.py && \
		ln -sf ${GRAPHITE_BASE}/bin/carbon-relay.py && \
		ln -sf ${GRAPHITE_BASE}/bin/carbon-cache.py &&

.include <bsd.port.post.mk>
