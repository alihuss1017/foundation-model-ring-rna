import zipfile
import os
import requests

def unzip_file(zip_file_path, extract_dir):
    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    os.remove(zip_file_path)

def scraping(file_type):
    base_url = "https://ngdc.cncb.ac.cn/circatlas/"

    species = ['human', 'macaca', 'mouse', 'rat', 'rabbit', 'cat', 'dog', 'pig', 'sheep', 'chicken']
    for name in species:

        download_dir = f'{file_type}_data'
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        file_to_download = [f'./analysis/bed/{name}_{file_type}_v3.0.zip']

        for file_path in file_to_download:
            data = {'downloadfile': file_path}

            print(f"Downloading {file_path}...")
            response = requests.post(base_url + "download_file.php", data=data, stream=True)
            
            if response.status_code == 200:
                file_name = os.path.basename(file_path)  # Get the file name from the path
                file_save_path = os.path.join(download_dir, file_name)

                with open(file_save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):  # Download in chunks
                        f.write(chunk)
                
                print(f"Downloaded {file_name}!")
            
                unzip_file(file_save_path, download_dir)
            else:
                print(f"Failed to download {file_path}. Status code: {response.status_code}")

scraping('bed')
scraping('sequence')