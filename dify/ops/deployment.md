[source](https://github.com/langgenius/dify)

# docker compose
Dependencies (no profile)
- `.env`, under same direcotry of docker-compose.yaml
- `/conf/conf.yaml` in container of image `langgenius/dify-sandbox:0.2.12`

hardware resource consumed
- 6 CPU
- 2 GB memory
- 6.5 GB container image

# package
use sandbox extension
- `/dependencies` in image `langgenius/dify-sandbox:0.2.12`: 你可以把需要的 Python 包、二进制工具或库放在这里， 在Code Node里使用