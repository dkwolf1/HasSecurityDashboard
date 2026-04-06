ARG BUILD_FROM
FROM $BUILD_FROM

ENV LANG=C.UTF-8
ENV VENV_PATH=/opt/venv
ENV PATH="$VENV_PATH/bin:$PATH"

RUN apk add --no-cache python3 py3-pip bash

RUN python3 -m venv $VENV_PATH \
    && $VENV_PATH/bin/pip install --no-cache-dir --upgrade pip \
    && $VENV_PATH/bin/pip install --no-cache-dir fastapi "uvicorn[standard]" python-multipart jinja2 aiofiles

WORKDIR /app
COPY app /app/app
COPY run.sh /app/run.sh
RUN chmod +x /app/run.sh

CMD [ "/app/run.sh" ] ]
