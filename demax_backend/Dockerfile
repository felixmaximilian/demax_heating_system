FROM arm32v7/python:3.9-bullseye

RUN mkdir /app

COPY demax_backend /app
COPY pyproject.toml /app

WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

#RUN curl -sSfL https://sh.rustup.rs > rustup.sh && \
#    sh rustup.sh -y --default-toolchain none --profile minimal && \
#    rm -f rustup.sh \
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH=/root/.cargo/bin:$PATH
#RUN --security=insecure mkdir -p /root/.cargo && chmod 777 /root/.cargo && mount -t tmpfs none /root/.cargo
RUN echo $PATH
RUN echo `rustc --version`

RUN pip install --upgrade pip

RUN pip install "cryptography<3.0"

ENV POETRY_VERSION=1.1.15 \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    PATH="$PATH:/root/.local/bin"

RUN --mount=type=tmpfs,target=/root/.cargo pip3 install poetry==$POETRY_VERSION
RUN poetry config virtualenvs.create false

RUN poetry install --no-interaction --no-ansi --no-dev --with rpi


CMD ["python", "-m", "main"]