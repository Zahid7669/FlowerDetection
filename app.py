from flask import Flask, render_template, request
import torch
import torchvision.transforms as transforms
from PIL import Image
from models import ResNet9

app = Flask(__name__)

# Load the saved model from a .pth file
state_dict = torch.load('model.pth', map_location=torch.device('cpu'))

# Instantiate the ResNet9 model and load the saved state dict
model = ResNet9(in_channels=3, num_classes=5)
model.load_state_dict(state_dict)

# Switch the model to evaluation mode
model.eval()



# Define the image transformations
transform = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Define the class labels
labels = ['dandelion', 'rose', 'daisy', 'sunflower', 'tulip']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def predict():
    file = request.files['image']
    img = Image.open(file.stream)
    img = transform(img)
    img = img.unsqueeze(0)

    # Make a prediction using the model
    with torch.no_grad():
        output = model(img)
        _, predicted = torch.max(output.data, 1)
        prediction = labels[predicted.item()]
        # print(prediction)

    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
