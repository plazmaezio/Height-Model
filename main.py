import random

height_data = []
first_tap_data = []
second_tap_data = []
third_tap_data = []
tap_data = []

# Reading the file and processing each line
with open('input_data.txt', 'r') as file:
    for line in file:
        # Remove any leading/trailing whitespace and split the line by commas
        parts = line.strip().split(',')

        height_data.append(float(parts[0].strip()))
        first_tap_data.append(float(parts[1].strip()))
        second_tap_data.append(float(parts[2].strip()))
        third_tap_data.append(float(parts[3].strip()))
tap_data = [first_tap_data, second_tap_data, third_tap_data]


# model
def f(time, theta):
    a, b = theta
    return a * time + b
    
# loss function
def L2_Loss_Function(_y, _y_hat):
    loss = 0.0

    for y, y_hat in zip(_y, _y_hat):
        loss += (y_hat - y)**2
    
    return loss


best_loss = float('inf')
best_model = None
N = 100_000
# main
tap_preference = int(input("1/2/3 tap? "))
for n in range(N):

    if tap_preference == 1:
        _time = random.uniform(0.01, 1) # first tap random input
        _height = random.uniform(20, 250) # first tap random prediction
    elif tap_preference == 2:
        _time = random.uniform(0.01, 2.5) # second tap random input
        _height = random.uniform(20, 250) # second tap random prediction
    elif tap_preference == 3:
        _time = random.uniform(0.01, 4) # third tap random input
        _height = random.uniform(20, 250) # third tap random prediction
    else:
        print("error")
        
    theta = (_time, _height)
    
    y_hat = []
    for time in tap_data[tap_preference - 1]:
        y_hat.append(f(time, theta))
        
    loss = L2_Loss_Function(height_data, y_hat)
    
    if(loss < best_loss):
        best_loss = loss
        best_model = theta
        print(f"new best loss: {best_loss}, new best model = (t: {theta[0]}, h:{theta[1]}")
        
    
    