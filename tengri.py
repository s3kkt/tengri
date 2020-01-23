from lib.nomad import read_job_spec


def docker_string(job_id):
    job_config = {}
    if job_id:
        job_spec = read_job_spec(job_id)
        job_config['image'] = job_spec['TaskGroups'][0]['Tasks'][0]['Config']['image']
        job_config['env_vars'] = job_spec['TaskGroups'][0]['Tasks'][0]['Env']
        env_args = " ".join(
            "-e {}=\"{}\"".format(key, value.replace("!", "\\!")) for key, value in job_config['env_vars'].items()
        )
        return str('docker run -it --rm' + ' ' + env_args + ' ' + job_config['image'])
    else:
        print('No JOB_ID defined!')


if __name__ == "__main__":
    job_id = 'enter-job-name'
    try:
        print(docker_string(job_id))
    except Exception as ex:
        print(f"execution failure: {str(ex)}")
