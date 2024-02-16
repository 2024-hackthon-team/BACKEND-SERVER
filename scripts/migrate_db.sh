#!/bin/bash

# カレントディレクトリにdocker-compose.yamlがあるか確認
if [ ! -e docker-compose.yml ]; then
    echo "docker-compose.ymlが見つかりません、docker-compose.ymlと同じディレクトリで実行してください"
    exit 1
fi

docker compose exec backend_server python -m backend_server.migrate_db
