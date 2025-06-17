import torch
import torch.nn as nn
import torch.optim as optim
import string
import random

# Define the training data (a sample text)
text = "Hello, how are you doing today?"

# Create character-to-index and index-to-character dictionaries
all_characters = string.printable
n_characters = len(all_characters)
char_to_index = {char: index for index, char in enumerate(all_characters)}
index_to_char = {index: char for index, char in enumerate(all_characters)}

# Convert the text to a tensor
def text_to_tensor(text):
    tensor = torch.zeros(len(text), dtype=torch.long)
    for c in range(len(text)):
        tensor[c] = char_to_index[text[c]]
    return tensor

# Create a simple RNN model
class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size
        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(input_size + hidden_size, output_size)

    def forward(self, input, hidden):
        combined = torch.cat((input, hidden), 1)
        hidden = self.i2h(combined)
        output = self.i2o(combined)
        return output, hidden

    def init_hidden(self):
        return torch.zeros(1, self.hidden_size)

# Training settings
input_size = n_characters
hidden_size = 128
output_size = n_characters
learning_rate = 0.005

# Instantiate the RNN model and set up the optimizer
rnn = RNN(input_size, hidden_size, output_size)
optimizer = optim.SGD(rnn.parameters(), lr=learning_rate)
criterion = nn.CrossEntropyLoss()

# Training loop
def train(input_tensor, target_tensor):
    hidden = rnn.init_hidden()
    rnn.zero_grad()
    loss = 0

    for i in range(input_tensor.size(0)):
        output, hidden = rnn(input_tensor[i].view(1, -1), hidden)
        l = criterion(output, target_tensor[i].view(-1))
        loss += l

    loss.backward()
    optimizer.step()

    return loss.item() / input_tensor.size(0)

# Training the model on the sample text
n_iterations = 1000
print_every = 100
plot_every = 10
all_losses = []
total_loss = 0

for iteration in range(1, n_iterations + 1):
    input_tensor = text_to_tensor(text)
    target_tensor = text_to_tensor(text)
    loss = train(input_tensor, target_tensor)
    total_loss += loss

    if iteration % print_every == 0:
        print(f"Iteration {iteration} Loss: {loss:.4f}")
    
    if iteration % plot_every == 0:
        all_losses.append(total_loss / plot_every)
        total_loss = 0

# Function to generate text
def generate_text(start_char='H', predict_len=100, temperature=0.5):
    with torch.no_grad():
        input = text_to_tensor(start_char)
        hidden = rnn.init_hidden()
        output_str = start_char

        for i in range(predict_len):
            output, hidden = rnn(input.view(1, -1), hidden)
            output_dist = output.data.view(-1).div(temperature).exp()
            top_i = torch.multinomial(output_dist, 1)[0]
            predicted_char = index_to_char[top_i]
            output_str += predicted_char
            input = text_to_tensor(predicted_char)

        return output_str

# Generate text
generated_text = generate_text(start_char='H', predict_len=200)
print("Generated Text:\n")
print(generated_text)