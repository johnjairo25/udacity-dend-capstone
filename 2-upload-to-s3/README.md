# Uploading Files to S3

After processing the contents of the original files, we need to move them
to Amazon S3 to make them available for further processing. This folder
contains the script to upload the files to Amazon S3.

To run the script execute the following bash command:

```bash
python upload_to_s3.py
```

## File Structure

In this folder there are two files, one configuration file and one python script:

- `upload_to_s3.py`: Script that uploads the result files of the data-exploration.
- `aws.cfg`: S3 configuration file. To set up the parameters for your case
check the `aws.cfg.sample`.
