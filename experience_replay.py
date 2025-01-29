from collections import deque
import random

class ReplayBuffer:
    def __init__(self, capacity):
        self.buffer = deque([],maxlen=capacity)

    def append(self, transition):
        self.buffer.append(transition)

    def sample(self, sample_size):
        return random.sample(self.buffer, sample_size)
    
    def __len__(self):
        return len(self.buffer)