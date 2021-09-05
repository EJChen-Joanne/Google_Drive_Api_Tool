from tqdm import tqdm
from time import sleep

count = 0

def show_progress(filename,total_count):
    
    global count
    count+=1
    for i in tqdm(range(100),desc="({0}/{1}) {2}".format(count,total_count,filename),unit="Bytes",leave=True):
        sleep(0.01)

def number_count():
    
    global count
    count += 1

    return count