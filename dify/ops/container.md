

access database by shell
1. `docker exec -it db-container /bin/bash`
2. `psql -U postgres`
    - password: `difyai123456`
3. use database `\c dify`

reset admin password
1. `docker exec -it api-container /bin/bash`
2. `flask reset-password`, and type in your email of admin

