def upload_sqlite(file_name, file, connection):
    """
    Uploads sqlite file to AWS using Fyle SDK
    :param file_name: Name of the file to be uploaded
    :param file: file object
    :param connection: Fyle connection
    :return: file_id
    """
    file_id = connection.Files.post(file_name)['id']
    s3_upload_url = connection.Files.create_upload_url(file_id)['url']
    connection.Files.upload_file_to_aws('application/x-sqlite3', file, s3_upload_url)
    return file_id
