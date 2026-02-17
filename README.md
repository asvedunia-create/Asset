# Asset Inventory Application (MVP)

Цей репозиторій містить стартовий MVP застосунку для автоматичної інвентаризації активів.

## Що вміє MVP

- Збирає дані з цільових хостів через:
  - `ssh` (Linux)
  - `winrm` (Windows)
- Визначає:
  - операційну систему
  - встановлені сервіси та їх версії
- Підтягує власника активу через інтеграційний шар AD (у MVP — stub).
- Зберігає результати в БД через SQLAlchemy (PostgreSQL або інша SQLAlchemy-сумісна БД).
- Надає веб-інтерфейс для:
  - перегляду списку активів
  - ручного оновлення даних без введення всіх параметрів вручну.

## Архітектура

- **FastAPI**: REST API + HTML сторінка.
- **SQLAlchemy**: моделі `Asset` та `Service`.
- **Collector Layer**:
  - `SSHCollector` (Linux)
  - `WinRMCollector` (Windows)
- **Directory Layer**:
  - `ADResolver` (інтерфейс для інтеграції з Active Directory).

## Запуск

1. Створіть віртуальне оточення й встановіть залежності:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Налаштуйте змінну БД (опційно):

```bash
export DATABASE_URL='postgresql+psycopg2://user:pass@localhost:5432/assetdb'
```

За замовчуванням використовується SQLite: `sqlite:///./asset.db`.

3. Запустіть застосунок:

```bash
uvicorn app.main:app --reload
```

4. Відкрийте:

- UI: `http://127.0.0.1:8000/`
- OpenAPI: `http://127.0.0.1:8000/docs`

## Як перевірити, що все працює

Нижче короткий smoke-check після запуску `uvicorn`.

1. Отримати поточний список активів (очікувано порожній `[]` на чистій БД):

```bash
curl -s http://127.0.0.1:8000/api/assets
```

2. Оновити/додати дані по Linux та Windows хосту:

```bash
curl -s -X POST http://127.0.0.1:8000/api/assets/refresh \
  -H 'Content-Type: application/json' \
  -d '{
    "targets": [
      {"hostname": "srv-linux-01", "address": "10.0.0.10", "protocol": "ssh"},
      {"hostname": "srv-win-01", "address": "10.0.0.20", "protocol": "winrm"}
    ]
  }'
```

3. Перевірити, що дані збережені:

```bash
curl -s http://127.0.0.1:8000/api/assets
```

У відповіді мають бути:
- `os_name: Linux` та сервіси `nginx`, `sshd` для `ssh` хоста;
- `os_name: Windows Server 2022` та сервіси `IIS`, `WinRM` для `winrm` хоста;
- `owner`, визначений через `ADResolver`.

4. Перевірити UI:
- відкрийте `http://127.0.0.1:8000/`;
- натисніть **Refresh**;
- у таблиці повинні з’явитися активи з OS/Owner/Services.

## API (ключові)

- `GET /api/assets` — список активів.
- `POST /api/assets/refresh` — оновити/додати дані по хостах.

Приклад payload:

```json
{
  "targets": [
    {"hostname": "srv-linux-01", "address": "10.0.0.10", "protocol": "ssh"},
    {"hostname": "srv-win-01", "address": "10.0.0.20", "protocol": "winrm"}
  ]
}
```

## Що потрібно додати в production

- Реальні конектори SSH/WinRM (наприклад Paramiko/pywinrm).
- Реальний AD lookup (ldap3 / Kerberos).
- Планувальник періодичного сканування (Celery/APScheduler).
- Аудит, RBAC, шифрування секретів, retry/pooling.
