import cv2
from pylab import array, plot, show, axis, arange, figure, uint8
from PIL import Image

image_file='/home/selvaprakash/BillD/Pics/Thang.jpg'
enh_img='/home/selvaprakash/BillD/Pics/Thang_enh.jpg'

def enhance_image(image_file,resi_image,enh_img):
    ori = Image.open(image_file)
    res = ori.resize((500, 600), Image.ANTIALIAS)
    res.save(resi_image)
    image = cv2.imread(resi_image,0) # load as 1-channel 8bit grayscale
    #cv2.imshow('image',image)
    maxIntensity = 255.0
    phi = 1
    theta = 1
    newImage1 = (maxIntensity/phi)*(image/(maxIntensity/theta))**2
    newImage1 = array(newImage1,dtype=uint8)

    cv2.imwrite(enh_img,newImage1)


    #cv2.imshow('newImage1',newImage1)


def main():
    enhance_image(image_file,enh_img)

if __name__=='__main__':
    main()