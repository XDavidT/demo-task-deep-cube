from crypt import methods
from flask import Flask,send_from_directory
import boto3, botocore
import os,sys

app = Flask(__name__)
s3_client = boto3.client('s3')
s3 = boto3.resource('s3',
                    aws_access_key_id= os.environ.get('API_KEY'),
                    aws_secret_access_key=os.environ.get('API_SECRET'))


BUCKET_NAME = 'dc-devops-task'
TMP_FOLDER = os.getcwd()+'/tmp/'
@app.route('/<filename>',methods=['GET'])
def hello_world(filename):
    save_as = TMP_FOLDER+filename
    try:
        my_bucket = s3.Bucket(BUCKET_NAME)
        for file in my_bucket.objects.all():
            if os.path.basename(file.key) == filename:
                s3.Bucket(BUCKET_NAME).download_file(file.key,save_as)
                return send_from_directory(TMP_FOLDER, path=filename, as_attachment=True)
        return "No luck finding "+filename
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.",file=sys.stdout)
        else:
            print(e,file=sys.stdout)
        return "No luck finding "+filename



if __name__ == '__main__':
    if not os.path.exists(TMP_FOLDER):
        os.mkdir(TMP_FOLDER)

    app.run(host='0.0.0.0')