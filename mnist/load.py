import torch
import torch.nn as nn
import torchvision.datasets as dsets
import torchvision.transforms as transforms
from torch.autograd import Variable

xcodeinput = """
0.3059  0.2863  0.2824  0.2863  0.2863  0.2980  0.2941  0.3020  0.3020  0.2980  0.3020  0.2902  0.2745  0.2784  0.2706  0.2627  0.2627  0.2627  0.2510  0.2353  0.2275  0.2235  0.2078  0.1922  0.1804  0.1843  0.1882  0.1843
  0.3059  0.2902  0.2902  0.2863  0.2941  0.2980  0.2941  0.3020  0.3020  0.2980  0.2941  0.2863  0.2824  0.2863  0.2784  0.2667  0.2667  0.2627  0.2471  0.2392  0.2314  0.2353  0.2196  0.2000  0.1843  0.1843  0.1843  0.1882
  0.3098  0.2980  0.2980  0.2941  0.3020  0.3059  0.3020  0.3059  0.2980  0.3137  0.3451  0.3216  0.2863  0.2902  0.2824  0.2784  0.2745  0.2667  0.2471  0.2392  0.2431  0.2275  0.1961  0.1922  0.1882  0.1882  0.1922  0.1961
  0.3176  0.3059  0.3020  0.3020  0.3098  0.3059  0.3098  0.3059  0.3020  0.4392  0.6471  0.4863  0.2824  0.2902  0.2824  0.2784  0.2784  0.2706  0.2588  0.2471  0.2392  0.2980  0.3647  0.2863  0.1961  0.1961  0.1922  0.2000
  0.3255  0.3098  0.3020  0.3020  0.3098  0.3059  0.3098  0.2902  0.3804  0.6118  0.6706  0.3686  0.2784  0.2902  0.2824  0.2824  0.2824  0.2745  0.2706  0.2549  0.2275  0.4627  0.8078  0.4118  0.1922  0.2039  0.2000  0.2118
  0.3255  0.3098  0.3020  0.3059  0.3137  0.3176  0.3020  0.3412  0.5647  0.7020  0.4471  0.2902  0.3020  0.2941  0.2863  0.2824  0.2824  0.2784  0.2667  0.2549  0.2392  0.4941  0.7294  0.3686  0.1961  0.2039  0.2000  0.2000
  0.3255  0.3137  0.3020  0.3098  0.3216  0.3137  0.3137  0.4980  0.6980  0.5451  0.3216  0.3098  0.3137  0.2980  0.2863  0.2824  0.2863  0.2745  0.2667  0.2510  0.2510  0.5294  0.6824  0.3216  0.1922  0.2118  0.2000  0.1961
  0.3294  0.3137  0.3020  0.3098  0.3255  0.3020  0.4235  0.6706  0.6431  0.3686  0.3098  0.3255  0.3137  0.3020  0.2941  0.2902  0.2863  0.2784  0.2745  0.2510  0.2706  0.5725  0.6000  0.2667  0.1961  0.2078  0.2000  0.2000
  0.3294  0.3176  0.3020  0.3137  0.3059  0.3529  0.6000  0.7020  0.4510  0.3059  0.3294  0.3176  0.3059  0.3020  0.2941  0.2863  0.2824  0.2745  0.2706  0.2431  0.2941  0.6000  0.5843  0.2588  0.1882  0.2039  0.1961  0.2000
  0.3333  0.3176  0.3020  0.3059  0.3137  0.5020  0.7216  0.5725  0.3294  0.3216  0.3333  0.3216  0.3098  0.3059  0.2941  0.2902  0.2902  0.2745  0.2706  0.2431  0.3255  0.6157  0.5686  0.2588  0.1843  0.2000  0.2000  0.2000
  0.3373  0.3176  0.3059  0.2980  0.4235  0.6941  0.6706  0.3725  0.2824  0.3137  0.3098  0.3098  0.3059  0.3020  0.2980  0.2980  0.2941  0.2824  0.2745  0.2471  0.3804  0.6431  0.5412  0.2392  0.1843  0.1961  0.1961  0.2000
  0.3373  0.3216  0.2941  0.3529  0.6275  0.7333  0.5725  0.3843  0.3725  0.3529  0.3294  0.3059  0.2941  0.2824  0.2745  0.2745  0.2706  0.2588  0.2471  0.2353  0.4471  0.6627  0.5059  0.2196  0.1804  0.1882  0.1922  0.2118
  0.3373  0.3176  0.3098  0.5569  0.8000  0.7490  0.7059  0.7216  0.7176  0.6941  0.6431  0.5804  0.5255  0.4706  0.4275  0.4078  0.3882  0.3647  0.3373  0.3412  0.5373  0.6471  0.5098  0.2196  0.1843  0.1922  0.1882  0.2078
  0.3373  0.3137  0.3059  0.4784  0.5843  0.5529  0.5490  0.5608  0.5647  0.5843  0.6039  0.6275  0.6627  0.6863  0.6941  0.7059  0.7098  0.7059  0.7098  0.6824  0.6078  0.6314  0.4353  0.1961  0.1843  0.1843  0.1843  0.1961
  0.3373  0.3137  0.3059  0.3098  0.3176  0.3176  0.3176  0.3216  0.3176  0.3137  0.3098  0.3137  0.3216  0.3216  0.3333  0.3529  0.3725  0.4039  0.4235  0.4902  0.6235  0.6275  0.3098  0.1725  0.1882  0.1765  0.1804  0.1922
  0.3412  0.3176  0.3137  0.3137  0.3098  0.3176  0.3216  0.3216  0.3176  0.3137  0.3020  0.2980  0.2941  0.2745  0.2667  0.2667  0.2549  0.2471  0.2196  0.3451  0.6392  0.5961  0.2706  0.1725  0.1804  0.1725  0.1686  0.1765
  0.3412  0.3176  0.3137  0.3098  0.3176  0.3216  0.3255  0.3216  0.3216  0.3176  0.3059  0.3098  0.3020  0.2863  0.2824  0.2824  0.2745  0.2706  0.2471  0.4039  0.6549  0.5569  0.2392  0.1725  0.1765  0.1686  0.1608  0.1725
  0.3412  0.3176  0.3098  0.3059  0.3137  0.3176  0.3176  0.3216  0.3176  0.3098  0.3020  0.2980  0.2902  0.2784  0.2745  0.2745  0.2667  0.2588  0.2392  0.4275  0.6588  0.5176  0.2157  0.1686  0.1608  0.1529  0.1569  0.1647
  0.3373  0.3176  0.3098  0.3059  0.3059  0.3137  0.3137  0.3137  0.3098  0.3020  0.2941  0.2941  0.2902  0.2784  0.2745  0.2706  0.2627  0.2471  0.2392  0.4471  0.6471  0.4980  0.2000  0.1647  0.1608  0.1490  0.1490  0.1569
  0.3333  0.3176  0.3098  0.3059  0.3059  0.3098  0.3137  0.3137  0.3059  0.2980  0.2902  0.2902  0.2824  0.2745  0.2706  0.2627  0.2588  0.2392  0.2392  0.4667  0.6392  0.4863  0.1961  0.1608  0.1569  0.1451  0.1451  0.1490
  0.3294  0.3137  0.3020  0.2980  0.2980  0.3020  0.3059  0.3020  0.2941  0.2902  0.2824  0.2824  0.2745  0.2667  0.2627  0.2588  0.2510  0.2314  0.2392  0.4824  0.6275  0.4745  0.1843  0.1529  0.1451  0.1412  0.1373  0.1412
  0.3216  0.3059  0.2941  0.2902  0.2941  0.2980  0.2980  0.2941  0.2902  0.2824  0.2824  0.2784  0.2706  0.2627  0.2588  0.2471  0.2431  0.2196  0.2392  0.4980  0.6510  0.4627  0.1725  0.1490  0.1412  0.1333  0.1294  0.1373
  0.3176  0.3020  0.2902  0.2902  0.2902  0.2902  0.2941  0.2863  0.2863  0.2784  0.2745  0.2706  0.2627  0.2549  0.2510  0.2392  0.2314  0.2118  0.2353  0.4706  0.6510  0.4667  0.1686  0.1451  0.1333  0.1255  0.1255  0.1255
  0.3176  0.2980  0.2902  0.2863  0.2863  0.2863  0.2863  0.2824  0.2784  0.2706  0.2627  0.2588  0.2549  0.2471  0.2392  0.2275  0.2235  0.2039  0.2196  0.4314  0.6039  0.4902  0.1725  0.1373  0.1255  0.1216  0.1216  0.1176
  0.3059  0.2941  0.2863  0.2824  0.2824  0.2824  0.2784  0.2745  0.2706  0.2627  0.2588  0.2510  0.2392  0.2353  0.2235  0.2157  0.2118  0.1961  0.1843  0.3647  0.5647  0.4588  0.1608  0.1294  0.1216  0.1176  0.1137  0.1059
  0.3020  0.2902  0.2824  0.2784  0.2745  0.2745  0.2706  0.2667  0.2627  0.2549  0.2510  0.2431  0.2314  0.2275  0.2157  0.2000  0.1961  0.1922  0.1765  0.2157  0.2667  0.2157  0.1373  0.1294  0.1216  0.1098  0.1020  0.0980
  0.2980  0.2824  0.2745  0.2706  0.2667  0.2627  0.2627  0.2588  0.2549  0.2510  0.2431  0.2353  0.2235  0.2157  0.2000  0.1843  0.1843  0.1882  0.1804  0.1608  0.1412  0.1333  0.1333  0.1255  0.1137  0.0980  0.0902  0.0941
  0.2863  0.2745  0.2667  0.2627  0.2588  0.2549  0.2549  0.2510  0.2471  0.2431  0.2314  0.2235  0.2157  0.2039  0.1882  0.1765  0.1725  0.1765  0.1725  0.1647  0.1569  0.1451  0.1294  0.1176  0.1020  0.0902  0.0824  0.0863
"""

num_epochs = 5
batch_size = 100
learning_rate = 0.001

# MNIST Dataset
train_dataset = dsets.MNIST(root='./data/',
                            train=True, 
                            transform=transforms.ToTensor(),
                            download=True)

test_dataset = dsets.MNIST(root='./data/',
                           train=False, 
                           transform=transforms.ToTensor())

# Data Loader (Input Pipeline)
train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                           batch_size=batch_size, 
                                           shuffle=True)

test_loader = torch.utils.data.DataLoader(dataset=test_dataset,
                                          batch_size=batch_size, 
                                          shuffle=False)

def printTensor(tensor, batch = 0, channel = 0):
    for i in range(tensor.shape[-2]):
        for j in range(tensor.shape[-1]):
            k = tensor.data[batch, channel, i, j] if len(tensor.shape) == 4 else tensor.data[i, j]
            print((" " if k >= 0 else "") + "%0.4f " % k, end="")
        print("")

# CNN Model (2 conv layer)
class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=5),
            nn.ReLU(),
            nn.MaxPool2d(2))
        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=5),
            nn.ReLU(),
            nn.MaxPool2d(2))
        self.fc = nn.Linear(4 * 4 * 32, 10)

    def forward(self, x):
        out = self.layer1[0](x)
        out = self.layer1[1](out)
        out = self.layer1[2](out)
        out = self.layer2[0](out)
        out = self.layer2[1](out)
        out = self.layer2[2](out)
        out = out.view(out.size(0), -1)
        print("Tensor fc input:")
        print(out.shape)
        printTensor(out)
        out = self.fc(out)
        print("Tensor fc output:")
        print(out.shape)
        printTensor(out)
        print("fc weight:")
        printTensor(self.fc.weight)
        return out


if __name__ == "__main__":
    model = CNN()
    model.load_state_dict(torch.load('cnn.pkl'))
    inputmatrix = []
    i = 0
    for line in xcodeinput.split("\n"):
        if len(line) == 0:
            continue
        inputmatrix.append([])
        for value in line.split(" "):
            if len(value) > 0:
                inputmatrix[i].append(float(value))
        i += 1
    # print(inputmatrix)
    image = Variable(torch.FloatTensor([[inputmatrix]]))
    # print(image.shape)
    output = model(image)
    # printTensor(model.parameters.state_dict)
    print(output)

    # for images, labels in test_loader:
    #     images = Variable(images)
    #     printTensor(images)
    #     outputs = model(images)
    #     # printTensor(outputs)
    #     break
    # print(model.state_dict)
    # print(model.state_dict())