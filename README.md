# Get string for local run service from Nomad
- Создай в окружении переменную NOMAD_ADDR=https://login:password@nomad.url
- Присвой значение переменной job_id (название джобы как в nomad или consul)
- Запусти скрипт и получи строку для запуска контейнера с приложением локально в формате
```bash
$ docker run -it --rm -e var1=... -e var2=... -e varN=... image_name
```
