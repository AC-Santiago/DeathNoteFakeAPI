FROM python:3.11.11-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK=1

ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

ADD https://astral.sh/uv/install.sh /uv-installer.sh

RUN sh /uv-installer.sh && rm /uv-installer.sh

ENV PATH="/root/.local/bin/:$PATH"

WORKDIR /DeathNoteFake

COPY ./pyproject.toml /DeathNoteFake/pyproject.toml

COPY ./uv.lock /DeathNoteFake/uv.lock

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-install-project --no-dev

COPY ./app /DeathNoteFake/app

COPY ./app/json /DeathNoteFake/app/json

RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --frozen --no-dev

ENV PATH="/DeathNoteFake/.venv/bin:$PATH"

EXPOSE 8000

CMD ["fastapi", "run","app/main.py", "--host", "0.0.0.0", "--port", "8000"]
