#!/bin/bash

# Сначала установите сигналы, чтобы приложение корректно завершалось при получении сигнала SIGINT и SIGTERM
trap 'killall $(jobs -p) && wait $(jobs -p)' SIGINT SIGTERM

# Запустите Gunicorn в фоновом режиме
gunicorn -w 4 --bind 0.0.0.0:5000 wsgi &

# Следите за изменениями файлов и перезапускайте Gunicorn при изменении
while true; do
    # Используйте stat для получения времени изменения файла app.py
    mtime=$(stat -c %Y endpoints/* app.py)

    # Если время изменения файла app.py не равно времени последнего изменения, перезапустите Gunicorn
    if [[ "$mtime" != "$last_mtime" ]]; then
        echo "app.py or endpoints/files was modified at $(date)!"
        last_mtime="$mtime"
        killall gunicorn
        gunicorn -w 4 --bind 0.0.0.0:5000 wsgi &
    fi

    # Проверка каждые 2 секунды
    sleep 2
done

# Скрипт никогда не дойдет до этой строки
exit 0
