FROM gcr.io/google.com/cloudsdktool/cloud-sdk:latest

COPY scheduler_deploy.py /usr/bin
ENTRYPOINT ["/usr/bin/scheduler_deploy.py"]
