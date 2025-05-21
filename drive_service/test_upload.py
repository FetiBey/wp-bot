# drive_service/test_upload.py

from uploader import upload_file_to_drive

# Yüklemek istediğin dosya adı (aynı klasörde olduğunu varsayıyoruz)
file_path = "drive_service/ev1.jpg"
file_name = "ev1_ilani.jpg"

url = upload_file_to_drive(file_path, file_name)
print("Drive bağlantısı:", url)
