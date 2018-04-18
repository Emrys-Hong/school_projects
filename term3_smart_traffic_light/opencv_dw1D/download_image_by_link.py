import urllib.request
import cv2
import numpy as np
import os


def store_raw_images():
    neg_images_link = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid=n04096066'
    neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
    pic_num = 904

    if not os.path.exists('neg1'):
        os.makedirs('neg1')

    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            urllib.request.urlretrieve(i, "neg1/" + str(pic_num) + ".jpg")
            img = cv2.imread("neg1/" + str(pic_num) + ".jpg", cv2.IMREAD_GRAYSCALE)
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, (100, 100))
            cv2.imwrite("neg1/" + str(pic_num) + ".jpg", resized_image)
            pic_num += 1


        except Exception as e:
            print(str(e))

def find_uglies():
    match = False
    for file_type in ['neg1']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_image_path = str(file_type)+'/'+str(img)
                    ugly = cv2.imread('uglies/'+str(ugly))
                    question = cv2.imread(current_image_path)
                    if ugly.shape == question.shape and not(np.bitwise_xor(ugly,question).any()):
                        print('That is one ugly pic! Deleting!')
                        print(current_image_path)
                        os.remove(current_image_path)
                except Exception as e:
                    print(str(e))

def create_pos_n_neg():
    for file_type in ['neg']:

        for img in os.listdir(file_type):

            if file_type == 'pos':
                line = file_type + '/' + img + ' 1 0 0 50 50\n'
                with open('info.dat', 'a') as f:
                    f.write(line)
            elif file_type == 'neg':
                line = file_type + '/' + img + '\n'
                with open('bg.txt', 'a') as f:
                    f.write(line)

def resize_pos_images():
    for i in range(1):

        img = cv2.imread("/Users/MH/Desktop/thymio.jpg", cv2.IMREAD_GRAYSCALE)
        # should be larger than samples / pos pic (so we can place our image on it)
        resized_image = cv2.resize(img, (50,50))
        cv2.imwrite("thymio.jpg", resized_image)

resize_pos_images()
# create_pos_n_neg()