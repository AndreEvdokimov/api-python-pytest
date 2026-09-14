# http-python-pytest

Учебный HTTP-клиент к GitLab API на Python: `httpx` (async), pytest, моки `respx`.

## Запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
pytest -m "not integration" -q
```

Рабочий GitLab (`-m integration`) запускается только с `GITLAB_TOKEN` в `.env` с ссылкой на рабочий сервер GitLab.

TODO: добавить свой клиент на `FastAPI` и установку БД в Docker-контейнере для сохранения полученных данных от GitLab.