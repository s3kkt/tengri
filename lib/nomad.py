import nomad

NOMAD = nomad.Nomad()


def get_jobs():
    try:
        jobs_list = NOMAD.jobs.get_jobs()
    except nomad.api.exceptions.BaseNomadException as e:
        print("Exception: " + str(e))
        print(e.nomad_resp.reason)
        print(e.nomad_resp.text)
        exit(127)
        return dict()
    return jobs_list


def read_job_spec(job):
    try:
        job_spec = NOMAD.job.get_job(job)
    except nomad.api.exceptions.BaseNomadException as e:
        print("Exception: " + str(e))
        print(e.nomad_resp.reason)
        print(e.nomad_resp.text)
        exit(127)
        return dict()
    return job_spec
