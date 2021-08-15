from .network import FINED
from PIL import Image
import numpy as np
import torch
import torchvision.transforms as transforms

class ImagePredictor:
    def __init__(self):        
        self.predictor = FINED()
        model_path = "/media/commlab/TenTB/home/jan/LearnFastAPI/FINED-service/app/modules/fined/weights/final-model.pth"
        self.predictor.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

    def predict(self, image, fname):            
        transforms_image = transforms.Compose(
            [transforms.Resize((400, 400)),
            transforms.ToTensor(),        
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
        image = transforms_image(image) 
        image = image.unsqueeze(0)

        output = self.predictor(image)    
        retn = 255 - (output * 255)

        result = Image.fromarray(retn)
        result.save( "/media/commlab/TenTB/home/jan/LearnFastAPI/FINED-service/static/img/%s_result.png" % fname)
        
        return retn