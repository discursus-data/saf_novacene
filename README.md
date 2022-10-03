# The OSS Social Analytics Framework - Novacene library
This library provides a client [resource](https://docs.dagster.io/concepts/resources) to interact with the [NovaceneAI](https://novacene.ai/) API.

It is part of the [Social Analytics Framework](https://github.com/lantrns-analytics/saf_core). Please visit the repo for more information on the framework, its mission and how to use it.

&nbsp;

# Library
## Configurations
The resource requires the following parameters to be initialized:
- host: URL to your Novacene instance
- login: Username to your instance
- password: Password to your instance

Here's an example of a config file:

```
resources:
  novacene_client:
    config:
      host: 
        env: NOVACENE_HOST
      login: 
        env: NOVACENE_LOGIN
      password: 
        env: NOVACENE_PASSWORD
```

# Methods
## novacene_resource.initiate_novacene_client
Initialize client to interact with the Novacene API

Configurations:
- novacene_configs: A configured resource for Novacene.

Example:
```
novacene_configs = config_from_files(['configs/novacene_configs.yaml'])

my_novacene_client_client = novacene_resource.initiate_novacene_client.configured(novacene_configs)
```

## novacene_resource.create_dataset
Uploads a dataset.

Parameters:
- filename: Name of file to be uploaded.
- df_upload: Dataframe to be uploaded.

Returns:
- response_json: JSON object on dataset created.

Example:
```
dataset_id = context.resources.novacene_client.create_dataset(filename, df_upload)
```

## novacene_resource.get_file
Downloads a dataset.

Parameters:
- file_url: URL of file to be downloaded.

Returns:
- df_file: Dataframe of file downloaded

Example:
```
df_file = context.resources.novacene_client.get_file(file_url)
```

## novacene_resource.enrich_dataset
Runs preditions on a dataset using previously trained models.

Parameters:
- dataset_id: ID of the dataset containing the input data.
- model_id: ID of the trained method.
- col_id: the column index of the data that predictions will be run on. 

Returns:
- response_json: JSON object on job created.

Example:
```
job_id = context.resources.novacene_client.enrich_dataset(dataset_id, model_id, col_id)
```

## novacene_resource.job_info
Retrieve information on a given job.

Parameters:
- job_id: A unique integer value identifying this enrichment jobs.

Returns:
- response_json: JSON object of job information.

Example:
```
job_info = context.resources.novacene_client.job_info(job_id)
```

&nbsp;

# Development of library
- Once improvements have been added to library
- Compile a new version: `python setup.py bdist_wheel`
- Commit branch and PR into new release branch
- Point projects to new release branch
