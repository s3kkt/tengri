import os

NOMAD_ADDR = os.getenv('NOMAD_ADDR')


env_vars = {
    'nomad_url': NOMAD_ADDR,
}
