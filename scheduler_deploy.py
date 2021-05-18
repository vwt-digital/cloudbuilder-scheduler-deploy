#!/usr/bin/env python3

import argparse
import subprocess  # nosec

parser = argparse.ArgumentParser()
parser.add_argument("name", type=str, help="scheduler name")
parser.add_argument(
    "--project",
    type=str,
    help="the project where the scheduler will be deployed",
    required=True,
)
parser.add_argument(
    "--schedule",
    type=str,
    help="schedule on which the job will be executed",
    required=True,
)
parser.add_argument(
    "--scheduler-type",
    type=str,
    help="scheduler type (default: http)",
    choices=["app-engine", "http", "pubsub"],
    default="http",
)
args = parser.parse_known_args()

# Default scheduler deploy params
SCHEDULER_PARAMS = {
    "http-method": "POST",
    "max-backoff": "5s",
    "max-retry-attempts": 0,
    "min-backoff": "5s",
}


def deploy_scheduler(arguments, deploy_params):
    """
    Delete a scheduler before deployment

    :param arguments: Command Line arguments
    :param deploy_params: Default deployment parameters
    :type deploy_params: dict

    :return: Return code
    :rtype: int
    """

    # Compose command
    deploy_cmd = [
        "gcloud",
        "scheduler",
        "jobs",
        "create",
        str(arguments[0].scheduler_type),
        str(arguments[0].name),
    ]

    # Append command line params
    for arg in vars(arguments[0]):
        if arg not in ["name", "scheduler_type"]:
            deploy_cmd.append("--{}={}".format(arg, getattr(arguments[0], arg)))

    for param in arguments[1]:
        deploy_cmd.append("{}".format(param))

    # Append default params (only if not specified before)
    for key in deploy_params:
        found = False
        for param in deploy_cmd:
            if key in param:
                found = True

        if not found:
            cmd = "--{}".format(key)
            if deploy_params[key] is not None:
                cmd += "={}".format(deploy_params[key])
            deploy_cmd.append(cmd)

    # Execute command
    print(deploy_cmd)
    retval = subprocess.run(
        deploy_cmd, shell=False, stderr=subprocess.PIPE, timeout=300  # nosec
    )
    print(retval)
    return retval.returncode


def delete_scheduler(arguments):
    """
    Delete a scheduler before deployment

    :param arguments: Command Line arguments

    :return: Return code
    :rtype: int
    """

    # Compose command
    delete_cmd = [
        "gcloud",
        "scheduler",
        "jobs",
        "delete",
        str(arguments[0].name),
        "--{}={}".format("project", getattr(arguments[0], "project")),
        "--quiet",
    ]

    # Execute command
    print(delete_cmd)
    retval = subprocess.run(
        delete_cmd, shell=False, stderr=subprocess.PIPE, timeout=300  # nosec
    )
    print(retval)
    return retval.returncode


def describe_scheduler(arguments):
    """
    Describe a scheduler

    :param arguments: Command Line arguments

    :return: Job does exist
    :rtype: boolean
    """

    # Compose command
    describe_cmd = [
        "gcloud",
        "scheduler",
        "jobs",
        "describe",
        str(arguments[0].name),
        "--{}={}".format("project", getattr(arguments[0], "project")),
        "--quiet",
    ]

    # Execute command
    print(describe_cmd)
    retval = subprocess.run(
        describe_cmd, shell=False, stderr=subprocess.PIPE, timeout=300  # nosec
    )
    print(retval)

    return False if retval.returncode else True


def main():
    # Delete scheduler if existing
    if describe_scheduler(args):
        del_retval = delete_scheduler(args)
        if del_retval:
            return del_retval

    # Deploy scheduler
    dep_retval = deploy_scheduler(args, SCHEDULER_PARAMS)
    if dep_retval:
        return dep_retval

    return 0


if __name__ == "__main__":
    exit(main())
