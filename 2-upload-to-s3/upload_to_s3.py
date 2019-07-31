import boto3
import configparser

if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read_file(open('aws.cfg'))

    KEY = config.get('AWS', 'KEY')
    SECRET = config.get('AWS', 'SECRET')
    BUCKET = config.get('S3', 'BUCKET')

    s3 = boto3.resource('s3',
                        region_name='us-west-2',
                        aws_access_key_id=KEY,
                        aws_secret_access_key=SECRET
                        )

    s3.meta.client.upload_file('../datasets/results/Country.csv', BUCKET, 'Country.csv')
    s3.meta.client.upload_file('../datasets/results/GlobalLandTemperaturesByCity.csv', BUCKET, 'GlobalLandTemperaturesByCity.csv')
    s3.meta.client.upload_file('../datasets/results/GlobalLandTemperaturesByCountry.csv', BUCKET, 'GlobalLandTemperaturesByCountry.csv')
    s3.meta.client.upload_file('../datasets/results/suicide_rates.csv', BUCKET, 'suicide_rates.csv')
    s3.meta.client.upload_file('../datasets/results/world-happiness-report.json', BUCKET, 'world-happiness-report.json')