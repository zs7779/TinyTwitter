import logging, uuid, base64, datetime
import boto3
from botocore.exceptions import ClientError

def isHashTag(word):
    if len(word) < 2:
        return False
    if word[0] == '#':
        # only digit cannot be hashtag
        if word[1:].isdigit():
            return False
        if word[1:].isalnum():
            return True
    return False

def isMention(word):
    if len(word) < 2:
        return False
    if word[0] == '@' and word[1:].isalnum():
        return True
    return False

def presign_s3_post(user, avatar=False, file_type="", file_size_limit=5500000,
                    bucket='project-tt-bucket', expiration=300):
    s3_client = boto3.client('s3')
    
    # bucket = 'project-tt-compress'
    key = str(base64.urlsafe_b64encode( \
        uuid.uuid5(uuid.NAMESPACE_URL, \
            f'{user.id}-{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}' \
        ).bytes \
    ).rstrip(b'='), 'utf-8') + file_type
    
    folder = 'avatar/' if avatar else 'images/'
    
    try:
        response = s3_client.generate_presigned_post(bucket, folder+key,
            Fields=None,
            Conditions=[
            ["content-length-range", 0, file_size_limit],
            ["starts-with", "$Content-Type", "image/"],
            ],
            ExpiresIn=expiration
        )
    except ClientError as e:
        logging.error(e)
        return None

    logging.info(f'Presign for {user.username} successful')
    return response

def s3_delete(key, bucket='project-tt-bucket'):
    s3_client = boto3.client('s3')

    try:
        response = s3_client.delete_object(
            Bucket=bucket,
            Key=key,
        )
    except ClientError as e:
        logging.error(e)
        return None

    logging.info(f'Delete {bucket}/{key} successful')
    return response