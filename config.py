from environs import Env

env = Env()
env.read_env()

DATABASE_PATH = env('DB_PATH')
CROSS_RATE_BASE_CURRENCY = env('CROSS_RATE_BASE_CURRENCY')
