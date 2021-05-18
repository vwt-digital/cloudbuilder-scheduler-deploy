[![CodeFactor](https://www.codefactor.io/repository/github/vwt-digital/cloudbuilder-scheduler-deploy/badge)](https://www.codefactor.io/repository/github/vwt-digital/cloudbuilder-scheduler-deploy)

# Deployment of Cloud Scheduler
This cloudbuilder simplifies the deployment of a cloud scheduler.

The cloudbuilder image can be used in the cloudbuild.yaml
```yaml
- name: 'eu.gcr.io/{cloudbuilders}/cloudbuilder-scheduler-deploy'
```

The syntax for the scheduler deploy script is identical to the syntax of the standard `gcloud scheduler jobs create` command.

## CLI arguments
The following CLI arguments are supported:
    - `name` `[positional]` `[required]`: Scheduler Job name;
    - `--project` `[required]`: GCP Project ID;
    - `--scheduler-type` `[optional]`: GCP Project ID (see [Scheduler Type](#scheduler-type).

### Deployment variables
Deployment variables for the `gcloud scheduler jobs create` can be specified in 2 ways (in sequence of priority)
1.  Command line parameters. Parameters specified on the `scheduler-deploy.py` have the highest priority. These values override the values from option 2)
2.  By default, the following options are added to the command line:
    - `--http-method=POST`
    - `--max-backoff=5s`
    - `--max-retry-attempts=0`
    - `--min-backoff=5s`
    
### Scheduler Type
There are three different types of Cloud Schedulers [defined by Google](https://cloud.google.com/sdk/gcloud/reference/scheduler/jobs/create#COMMAND):
    - `app-engine`: Create a Cloud Scheduler job with an App Engine target;
    - `http`: Create a Cloud Scheduler job that triggers an action via HTTP;
    - `pubsub`: Create a Cloud Scheduler job with a Pub/Sub target.

To deploy one of these, use the `--scheduler-type` flag within the deployment. The default type is `http`.

## Example
The example below shows a `cloudbuild.yaml` fragment
```yaml
  - name: 'eu.gcr.io/{cloudbuilders}/cloudbuilder-scheduler-deploy'
    id: 'Deploy my important scheduler'
    entrypoint: 'bash'
    args:
      - '-c'
      - |
        scheduler_deploy.py ${PROJECT_ID}-my-important-job \
          --project="${PROJECT_ID}" \
          --schedule='5 4 * * *' \
          --uri="https://google.com/"
```

This will result in:
```shell
gcloud scheduler jobs describe ${PROJECT_ID}-my-important-job --quiet
gcloud scheduler jobs delete ${PROJECT_ID}-my-important-job --quiet  # If previous command is successful
gcloud scheduler jobs create http ${PROJECT_ID}-my-important-job \
  --project="${PROJECT_ID}" \
  --schedule='5 4 * * *' \
  --uri="https://google.com/" \
  --http-method=POST \
  --max-backoff=5s \
  --max-retry-attempts=0 \
  --min-backoff=5s
```

