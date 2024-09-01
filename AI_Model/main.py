import random

height_data = []
time_data = []

# Reading the file and processing each line
def read_input_data(file_path, tap_choice):
    with open(file_path, 'r') as file:
        for line in file:
            # Remove any leading/trailing whitespace and split the line by commas
            parts = line.strip().split(',')
            
            if parts[tap_choice].strip() != "-":
                height_data.append(float(parts[0].strip()))
                time_data.append(float(parts[tap_choice].strip()))
            elif parts[tap_choice].strip() != "-":
                height_data.append(float(parts[0].strip()))
                time_data.append(float(parts[tap_choice].strip()))
            elif parts[tap_choice].strip() != "-":
                height_data.append(float(parts[0].strip()))
                time_data.append(float(parts[tap_choice].strip()))

def read_model_values(file_path, line_number):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for line in lines:
        if line.startswith(f"{line_number}:"):
            # Extract the part after "line_number:"
            _, values_str = line.split(':', 1)
            values_str = values_str.strip()
            
            # Split the first value and the second part
            first_value_str, second_value_str = values_str.split(',', 1)
            first_value_str = first_value_str.strip()
            second_value_str = second_value_str.strip()
            
            # Convert the first value and the second value/tuple
            first_value = eval(first_value_str)
            if '(' in second_value_str and ')' in second_value_str:
                second_value = tuple(float(v.strip()) for v in second_value_str.strip('()').split(','))
            else:
                second_value = None if second_value_str == "None" else eval(second_value_str)
            
            return first_value, second_value

    # If line number is not found, return None
    return None

def write_model_values(file_path, line_number, new_value, new_tuple_values):
    # Read the file contents
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Update the specific line
    for i, line in enumerate(lines):
        if line.startswith(f"{line_number}:"):
            if isinstance(new_tuple_values, tuple):
                tuple_str = ', '.join(map(str, new_tuple_values))
                lines[i] = f"{line_number}: {new_value}, ({tuple_str})\n"
            else:
                lines[i] = f"{line_number}: {new_value}, {new_tuple_values}\n"
            break

    # Write the updated contents back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

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

def GetHeightFromTime(tap_preference, time, file_path):
    _, best_model = read_model_values(file_path, tap_preference)

    return f(time, best_model)

# main
N = 0
tap_preference = int(input("1/2/3 tap? ")) # AICI

read_input_data("Ai_Model/input_data.txt", tap_preference)
best_model_file_path = "AI_Model/best_model.txt"
best_loss, best_model = read_model_values(best_model_file_path, tap_preference)

initial_time_range = None
initial_height_range = 115
decay_rate = 0.99  # Start with a moderate decay rate
for n in range(N):
    if tap_preference == 1:
        if best_model == None:  
            _time = random.uniform(0.01, 1) # first tap random input
            _height = random.uniform(20, 250) # first tap random prediction
        else:
            initial_time_range = 0.5
            # _time = best_model[0] + random.uniform(-0.5, 0.5)
            # _height = best_model[1] + random.uniform(-115, 115)
    elif tap_preference == 2:
        if best_model == None:
            _time = random.uniform(0.01, 2.5) # second tap random input
            _height = random.uniform(20, 250) # second tap random prediction
        else:
            initial_time_range = 1.25
            # _time = best_model[0] + random.uniform(-1.25, 1.25)
            # _height = best_model[1] + random.uniform(-115, 115)
    elif tap_preference == 3:
        if best_model == None:
            _time = random.uniform(0.01, 4) # third tap random input
            _height = random.uniform(20, 250) # third tap random prediction
        else:
            initial_time_range = 2
            # _time = best_model[0] + random.uniform(-2, 2)
            # _height = best_model[1] + random.uniform(-115, 115)
    else:
        print("error")
        
    if best_model != None:
        time_range = initial_time_range * (decay_rate ** (n / N))
        height_range = initial_height_range * (decay_rate ** (n / N)) 
        _time = best_model[0] + random.uniform(-time_range, time_range)
        _height = best_model[1] + random.uniform(-height_range, height_range)
    
    theta = (_time, _height)
            
    y_hat = []
    for time in time_data:
        y_hat.append(f(time, theta)) # AICI (va trebui numa sa fac apel de f(time, theta)
        #f(time, theta)
        # time - input-ul
        # theta - cel mai bun model dupa antrenament 
        
    loss = L2_Loss_Function(height_data, y_hat)
    
    # Monitor loss and adjust decay_rate if necessary
    if n % 10000 == 0:  # Example check every 10,000 iterations
        loss = L2_Loss_Function(height_data, y_hat)
        if loss < best_loss * 0.95:  # If the loss improves significantly
            decay_rate = min(decay_rate * 1.01, 0.999)  # Slightly increase decay rate
        elif loss > best_loss * 1.05:  # If the loss worsens
            decay_rate = max(decay_rate * 0.99, 0.90)  # Slightly decrease decay rate
    #----------------------------------------------------
    
    if(loss < best_loss):
        best_loss = loss
        best_model = theta
        print(f"new best loss: {best_loss}, new best model = (t: {theta[0]}, h:{theta[1]}")
       
#write_model_values(best_model_file_path, tap_preference, best_loss, theta) 
    
print("am terminat de antrenat")
x = float(input("number: "))
print(GetHeightFromTime(tap_preference, x, best_model_file_path))