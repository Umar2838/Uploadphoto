from django.shortcuts import render
from .forms import UploadFileForm

def upload_to_s3(request):
    file_url = None

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']

            # Save the file to S3
            file_url = handle_uploaded_file(file)

    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form, 'file_url': file_url})


def handle_uploaded_file(file):
    import boto3
    from django.conf import settings

    s3 = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME,
    )

    # Define a unique name for the file
    file_name = f"uploads/{file.name}"

    # Upload file to S3 without ACL
    s3.upload_fileobj(
        file,
        settings.AWS_STORAGE_BUCKET_NAME,
        file_name,
        ExtraArgs={'ContentType': file.content_type}  # No ACL argument
    )

    # Return the file's public URL
    return f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{file_name}"
