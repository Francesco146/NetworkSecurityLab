FROM debian:bookworm
# Ref https://github.com/thiagoralves/OpenPLC_v3/blob/master/Dockerfile 
ARG script
ARG database

# Install applications
RUN apt-get update && apt-get -y install git sqlite3 python3 python3-pip && apt-get clean
RUN pip3 install --break-system-packages serial flask

# Install OpenPLC_v3
RUN git clone https://github.com/thiagoralves/OpenPLC_v3.git
WORKDIR /OpenPLC_v3
RUN git checkout d4d2a2a15120d9d3b14e0c4895164ca7bbd9a5f6
RUN ./install.sh docker

# copy PLC script and database script over
RUN mkdir /OpenPLC_v3/scripts
COPY $script /OpenPLC_v3/scripts/script.st
COPY $database /OpenPLC_v3/database.sh
COPY entrypoint.sh /OpenPLC_v3/entrypoint.sh
RUN chmod +x /OpenPLC_v3/entrypoint.sh /OpenPLC_v3/database.sh

EXPOSE 502
EXPOSE 8080
EXPOSE 20000
EXPOSE 43628

ENTRYPOINT ["/OpenPLC_v3/entrypoint.sh"]
