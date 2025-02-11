FROM python:3.12.3-slim 

RUN pip install uv

WORKDIR /app

COPY pyproject.toml pyproject.toml
RUN uv sync

COPY . /app

CMD ["uv", "run", "main.py"]