# Для правильної роботи додатку потрібно створити файл .flaskenv і додати чи підставити значення де потрібно
FLASK_APP=run.py
FLASK_ENV=development  # включити debug-режим
FLASK_DEBUG=1          # debug-режим увімкнено
FLASK_RUN_PORT=8080    # запуск на порту 8080
FLASK_RUN_HOST=0.0.0.0 # дозволяє доступ з інших пристроїв в локальній мережі
SECRET_KEY=your_secret_key_here
OUATH2_CLIENT_ID=your_client_id_here
OUATH2_CLIENT_SECRET=your_client_secret_here
OUATH2_META_URL=https://accounts.google.com/.well-known/openid-configuration
