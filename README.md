> WARNING!!! Running this app may cause security issues . Please, read the documentation carefully before use.

### Clone and build docker image
Clone:
```bash
git clone https://github.com/s3kkt/tengri.git && cd tengri
```
Build:
```bash
docker build -t tengri:latest .
```

### Environment variables

| Variable name | Required | Annotation |
| ------------- |:---: | ---------- |
| `NOMAD_ADDR` |True | Nomad connection string, e.g.`https://login:password@nomad.example.com` |
| `MODE` | True | Run mode selector: `local` or `exporter` |
| `VARIABLES_PREFIXES` | False | Comma separated environment variables prefixes. Variables, statrs with that prefixes will be displayed as labels. Explicitly named credentials in connection strings like `https://user:pass@service.example.com` will be replaced with `***SECRET***` e.g. `https://***SECRET***@service.example.com`
 |
| `RESTRICTED_VARIABLES` | False | Comma separated keywords. Variables, contains those keywords will be excluded from labels. This option has priority over`VARIABLES_PREFIXES` |
| `URL_SUFFIX` | False | If your consul-template service generates dynamic server names, domain suffixes can be set to add `url` label, e.g.`url="http://job-name.example.com"`|

Set `VARIABLES_PREFIXES` and `RESTRICTED_VARIABLES` is strongly recommended. If not, all of environmet variables from your Nomad jobs will be added to labels.

### Tengri has 2 launch options defined by environment variable `MODE`:

- Tiny tool to convert your nomad job name into `bash` command to run image manually in command line. Useful for fasten debug process of faulty runs.
- Service, which returns `ENV` objects for each nomad job as labels in prometheus metrics format.

### Local mode
Run:
```bash
docker run -d -it --rm --name tengri -p 8080:8080 \
-e MODE='local' \
-e NOMAD_ADDR='https://login:password@nomad.example.com' \
tengri:latest /bin/bash
```
Output example:
```bash
$ docker run -it --rm -e var1=... -e var2=... -e varN=... image_name
```
### Exporter mode
```bash
docker run -it --rm --name tengri -p 8080:8080 \
-e MODE='exporter' \
-e NOMAD_ADDR='https://login:password@nomad.example.com' \
-e VARIABLES_PREFIXES='VAR1,VAR2,VAR3' \
-e RESTRICTED_VARIABLES='KW1,KW2,KW3' \
-e URL_SUFFIX='example.com' \
tengri:latest /bin/bash
```