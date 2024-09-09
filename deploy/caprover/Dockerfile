FROM kitware/trame:py3.10

ENV TRAME_CLIENT_TYPE="vue2"
COPY --chown=trame-user:trame-user . /deploy
RUN /opt/trame/entrypoint.sh build
