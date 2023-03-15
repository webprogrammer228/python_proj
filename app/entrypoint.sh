#!/bin/bash

# Установка сигналы, чтобы приложение корректно завершалось при получении сигнала SIGINT и SIGTERM
trap 'killall $(jobs -p) && wait $(jobs -p)' SIGINT SIGTERM

# Запуск Gunicorn в фоновом режиме
gunicorn -w 4 --bind 0.0.0.0:5000 wsgi &

while true; do
    # stat для получения времени изменения файлов .py
    mtime=$(stat -c %Y endpoints/* app.py)

    # Если время изменения файлов .py не равно времени последнего изменения, перезапустить Gunicorn
    if [[ "$mtime" != "$last_mtime" ]]; then
        echo "app.py or endpoints/files was modified at $(date)!"
        last_mtime="$mtime"
        killall gunicorn
        gunicorn -w 4 --bind 0.0.0.0:5000 wsgi &
    fi

    # Проверка каждые 2 секунды
    sleep 2
done

exit 0
