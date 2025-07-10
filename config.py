from environs import Env

env = Env()
env.read_env()

DATABASE_PATH = env('DB_PATH')
