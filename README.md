# frigate_project_br

## Compose up/down docker container
```bash
docker compose up -d

docker compose down
```

## Restart Frigate container
```bash
docker restart frigate
```

## Docker log for admin pw
```bash
docker logs frigate
```



# To reset admin user password in config.yml file add following
```config
auth:
  reset_admin_password: true
```
