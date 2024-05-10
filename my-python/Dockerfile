FROM %GOLD_BASE_IMAGE_LATEST

USER root

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
	python3-numpy \
	python3-pip \
	python3-venv

ENV VIRTUAL_ENV="/opt/venv"

USER root

RUN install -v -d -o app -g app -p ${VIRTUAL_ENV}

USER app

RUN python3 -m venv $VIRTUAL_ENV --system-site-packages
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"
ENV PYTHONUNBUFFERED 1

RUN USER_SITE_DIR=$(python3 -m site --user-site) && \
    mkdir -p ${USER_SITE_DIR} && \
    echo "/opt/lib/python3" >> ${USER_SITE_DIR}/mycode.pth && \
    echo "/usr/lib/python3/dist-packages" >> ${USER_SITE_DIR}/mycode.pth

RUN python3 -m pip install --upgrade pip

USER root

RUN apt-get remove -y \
	g++ \
	gcc \
	&& apt-get autoremove -y

COPY files/python_libraries/ /opt/lib/python3/

ENV PYTHONPATH="/usr/lib/python3/dist-packages:/opt/lib/python3"

USER app

CMD ["python3"]
