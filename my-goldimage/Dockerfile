FROM %UBUNTU_BASE_IMAGE

LABEL maintainer="me@here"

ENV TZ="UTC"
ENV LANG="C.UTF-8"
ENV LC_ALL="C.UTF-8"
ENV DEBIAN_FRONTEND="noninteractive"
ENV HOME="/srv"

# Overriding default path as the default is unsafe -
# /usr/local/sbin is searched before /sbin (dangerous).
ENV PATH="/sbin:/bin:/usr/sbin:/usr/bin"

# Extra for this implementation
ENV PATH="${PATH}:/usr/local/sbin:/usr/local/bin:/opt/bin:/opt/local/bin:/srv/.local/bin"

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        file \
        git \
        gpg \
        htop \
        iputils-ping \
        jq \
        locales \
        locales-all \
        lsb-release \
        python3-dotenv \
        python3-requests \
        tini \
        unzip \
        vim \
        && apt-get clean
        # Don't delete the indexes as they will be
        # used by decendent images \
        #&& rm -rf /var/lib/apt/lists/*

RUN update-locale LANG=${LC_ALL}

RUN echo "********************"
RUN echo "* NOTICE: The following files (if any) will have their special bits cleared:"
RUN find / -type f -user root -perm /a+Xs -ls 2>/dev/null || true
RUN find / -type f -user root -perm /a+Xs 2>/dev/null -print0 | xargs --verbose -0 --no-run-if-empty chmod --verbose a-Xs || true
RUN echo "********************"

RUN mkdir -p /opt/bin /opt/local/bin

RUN groupadd -g 780 app && \
    useradd -r -M -d /srv -u 780 -g app app && \
    chown -R app:app /srv

COPY files/issue /etc/issue
COPY files/issue /etc/issue.net
COPY files/py-tini.py /py-tini.py

COPY --chown=root:root files/.bashrc /root/
COPY --chown=app:app files/.bashrc ${HOME}/

RUN ssh-keyscan github.com > /etc/ssh/ssh_known_hosts

# Maps to /var/run
RUN chmod 1777 /run

USER app

WORKDIR ${HOME}

#############################################################
# TINI:
#
# * It protects you from software that accidentally creates
# zombie processes, which can (over time!) starve your entire
# system for PIDs (and make it unusable).
#
# * It ensures that the default signal handlers work for
# the software you run in your Docker image. For example,
# with Tini, SIGTERM properly terminates your process even
# if you didn't explicitly install a signal handler for it.
#
# * It does so completely transparently! Docker images that
# work without Tini will work with Tini without any changes.
#
# https://github.com/krallin/tini
ENTRYPOINT ["python3", "/py-tini.py"]

CMD ["/usr/bin/bash"]
