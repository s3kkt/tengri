from lib.nomad import read_job_spec, get_jobs
from aiohttp import web
import os
import re
import aiohttp


run_mode = os.getenv("MODE", 'local')
prefixes = os.getenv("VARIABLES_PREFIXES", '').split(',')
restricted_prefixes = os.getenv("RESTRICTED_VARIABLES", '').split(',')
url_suffix = os.getenv("URL_SUFFIX")


async def hello(request):
    return web.Response(text="Nomad jobs configuration extractor\n")


async def get_version(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=5) as response:
            if response.status == 200 and response.content_type == 'text/plain':
                return await response.text(encoding='windows-1251')
            else:
                return 'None'


async def metrics_handler(request):
    jobs_list = get_jobs()
    output_lines = []
    app_version = 'None'
    job_url = 'None'
    for job in jobs_list:
        if job["Type"] != 'service':
            continue
        job_spec = read_job_spec(job["ID"])
        job_conf = job_spec['TaskGroups'][0]['Tasks'][0]['Env']
        image = job_spec['TaskGroups'][0]['Tasks'][0]['Config']['image']
        if url_suffix:
            job_url = 'http://' + job["ID"] + url_suffix
            version_url = job_url + '/version'
            app_version = await get_version(version_url)
        if not job_conf:
            output_lines.append(
                'nomad_job_configuration{image=' + '\"' + image + '\"' + ', ' + 'url=' + '\"' + job_url + '\"} 1\n'
            )
        else:
# TODO: generate labels lists at startup. Put labels to Redis and refresh every N seconds?
            all_labels = job_conf.keys()
            labels_list = []
            restricted_labels = []
            for label in all_labels:
                for pr in prefixes:
                    if label.startswith(pr):
                        labels_list.append(label)
                        break
            for label in labels_list:
                for pr in restricted_prefixes:
                    if len(re.findall(pr, label)) != 0:
                        restricted_labels.append(label)
                        break
            app_config = ", ".join(
                "{}=\"{}\"".format(key.lower(), re.sub('://.*:.*@', '://***SECRET***@', value))
                for key, value in job_conf.items() if key in labels_list and key not in restricted_labels
            )
            metric_output = ''
            if app_config:
                metric_output = f'{metric_output}{app_config}, '

            output_lines.append(
                f'nomad_job_configuration{"{"}{metric_output}'
                f'image="{image}", '
                f'app_version="{app_version}", '
                f'url="{job_url}"{"}"} 1'
            )
    return web.Response(text='\n'.join(output_lines))


async def job_id_handler(job):
    job_id = job.match_info.get('job', "")
    job_config = {}
    if job_id:
        job_spec = read_job_spec(job_id)
        job_config['image'] = job_spec['TaskGroups'][0]['Tasks'][0]['Config']['image']
        job_config['env_vars'] = job_spec['TaskGroups'][0]['Tasks'][0]['Env']
        env_args = " ".join(
            "-e {}=\'{}\'".format(key, value.replace("!", "\\!")) for key, value in job_config['env_vars'].items()
            )
    return web.Response(text='docker run -it --rm' + ' ' + env_args + ' ' + job_config['image'])


if run_mode == 'local':
    app = web.Application()
    app.add_routes([web.get('/', hello),
                    web.get('/{job}', job_id_handler)])
elif run_mode == 'cloud':
    app = web.Application()
    app.add_routes([web.get('/', hello),
                    web.get('/metrics', metrics_handler)])

if __name__ == '__main__':
    web.run_app(app)