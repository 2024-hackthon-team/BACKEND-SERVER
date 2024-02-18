# How to start the project

1. `.env`を作る

`cp .env.example .env`をし、`.env`を適切に設定する

2. `docker-compose up`を実行する


# Note

- パッケージマネージャーは`poetry`を使用している
- 新しいパッケージを追加する場合は、dockerをrebuildする必要がある、`sh ./scripts/rebuild-docker.sh`を実行する
- pythonのバージョン管理は`pyenv`を使用している、`pyenv`が入っている場合は自動的にpython 3.10.12になるはず
