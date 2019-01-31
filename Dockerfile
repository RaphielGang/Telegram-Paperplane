

FROM base/devel
# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH
ENV PYTHON_VERSION 3.7.2
RUN pacman -Syu --noconfirm && pacman -S python3 python-pip postgresql postgresql-libs neofetch git --noconfirm
# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not 
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python3","-m","userbot"]
