from django.shortcuts import render
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from PIL import Image
from .models import Img
from .forms import ImageForm

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# Create your views here.
def get_cropped_image_if_2_eyes(image_path):
    print(image_path)
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        roi_color = img[y:y+h, x:x+w]
        return roi_color

class_labels = ['Ronaldo','Ibrahimovic','Messi','Mbappe','Neymar']

path = r'C:\Users\flyas\Desktop\HarshitJain\21 Days\21_Days_Harshit_Jain\Project\my_model'

model = load_model(path)


def predicting(img_path):
    image = get_cropped_image_if_2_eyes(img_path)
    image = cv2.resize(image, (300,300))
    image = image / 255
    pre = np.argmax(model.predict(np.array([image])))
    return class_labels[pre]

def index(request):
    Img.objects.all().delete()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_obj = form.instance
            result = predicting('.'+str(img_obj.image.url))
            return render(request, 'predict/index.html', {'form': form, 'img_obj': img_obj, 'result': result})
    else:
        form = ImageForm()
    return render(request, 'predict/index.html',{'form': form})
