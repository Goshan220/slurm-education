#!/usr/bin/python3
import argparse
import datetime
from collections import deque
from functools import partial
import random
import psycopg2
from faker import Faker


def set_team_resource_using(postgres_client, faker: Faker, observations_conf: dict, max_resources: int = 10):
    monitoring_delta = datetime.timedelta(hours=1)
    time_format = "%Y-%m-%d %H:%M:%S"
    team = faker.bs()

    with postgres_client.cursor() as cursor:
        for _ in range(max_resources):
            resource = faker.license_plate()
            for observations_type in observations_conf["observations_types"]:
                observation_datetime = datetime.datetime.now() - datetime.timedelta(
                    hours=observations_conf["max_observations"])
                for _ in range(observations_conf["max_observations"]):
                    cursor.execute("INSERT INTO usage_stats.resources (team, resource, dimension, collect_date, usage) VALUES (%s, %s, %s, %s, %s)",
                                   [team,
                                    resource,
                                    observations_type,
                                    observation_datetime.strftime(time_format),
                                    str(int(observations_conf["distribution"]() * 100))])

                    observation_datetime += monitoring_delta


def set_infrastructure_using_summary(company_branch):
    team_count = 4
    seed = int(company_branch)
    Faker.seed(seed)
    fake = Faker()
    random.seed(seed)

    distributions = deque((partial(random.betavariate, alpha=0.1, beta=0.1),
                           partial(random.betavariate, alpha=1, beta=3),
                           partial(random.betavariate, alpha=8, beta=8),
                           partial(random.betavariate, alpha=1, beta=1))
                          )

    with psycopg2.connect(**{
        "dbname": "postgres",
        "user": "postgres",
        "password": "q1w2e3",
        "host": "postgres",
    }) as postgres_client:
        for _ in range(team_count):
            distribution = distributions.pop()
            set_team_resource_using(postgres_client,
                                    fake,
                                    observations_conf={
                                        "max_observations": 200,
                                        "observations_types": ["CPU", "RAM", "NetFlow"],
                                        "distribution": distribution
                                    })
            distributions.appendleft(distribution)


def main():
    parser = argparse.ArgumentParser(description='Generate analytical data')
    parser.add_argument('seed', type=int, help='random generator seed')

    args = parser.parse_args()

    set_infrastructure_using_summary(args.seed + 100)


if __name__ == '__main__':
    main()
