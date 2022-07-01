from multiprocessing import Pool, cpu_count
from urllib import response
import requests
import timeit 
import urllib


API_KEY = "gC2JBMjaYE3XE8NZIlK4rhQBeqQKYyx6baq4CtzI"
APOD_ENDPOINT = 'https://api.nasa.gov/planetary/apod'
OUTPUT_IMAGES = '/Users/gonzo/Desktop/Python/PYTHON-BASIC/practice/7_concurrency/task2_apod_api/output'


def get_apod_metadata(metadata: list) -> list:
    return requests.get(APOD_ENDPOINT, params= metadata).json()


def download_apod_images(metadata):
    if metadata['media_type'] == 'image':
        urllib.request.urlretrieve(metadata['url'], OUTPUT_IMAGES+'/'+metadata['date']+'.jpg')
    else: 
        pass
    
    
def main():
    
    metadata = get_apod_metadata({'start_date':'2021-08-01','end_date':'2021-09-30','api_key':API_KEY})
    print('Starting multiprocessing with {}'.format(cpu_count()))
    pool = Pool()  # Create pool of workers
    start = timeit.default_timer()
    download = pool.map(download_apod_images, metadata)
    end = timeit.default_timer()
    pool.close()
    print('Finished multiprocessing in {}'.format(end-start))


if __name__ == '__main__':
    main()