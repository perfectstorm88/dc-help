FROM centos:7

# Create app directory
WORKDIR /dc-help
COPY setup.py /dc-help
COPY dchelp /dc-help/dchelp
RUN yum install -y wget unzip vim \
   && yum clean all
RUN  wget https://pypi.io/packages/source/s/setuptools/setuptools-33.1.1.zip \
   &&  unzip setuptools-33.1.1.zip \
   && cd setuptools-33.1.1 \
   && python setup.py install \
   && cd /dc-help \
   && rm -rf setuptools-33.1.1* && python setup.py install \
   && echo "alias dc='docker-compose '">> ~/.bashrc && echo "alias dclog='docker-compose logs -f --tail=50 '">> ~/.bashrc
CMD ["tail","-f","/dev/null"]
