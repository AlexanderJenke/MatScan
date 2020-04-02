import matplotlib.pyplot as plt
import numpy as np
import torch
from torch.nn import MSELoss
from torch.optim import Adam

all_numbers = [2, 2, 2, 5, 5, 5, 12, 18, 25, 35, 50, 60, 97, 115, 139, 154, 167, 216, 239, 273]


class f(torch.nn.Module):
    def __init__(self):
        super(f, self).__init__()
        self.exp = torch.nn.Parameter(torch.tensor(1.2), True)
        self.m = torch.nn.Parameter(torch.tensor(0.0), True)

    def forward(self, x):
        return x ** self.exp - self.m


if __name__ == '__main__':
    numbers = all_numbers[10:]
    y = torch.tensor(numbers).float()
    x = torch.tensor(range(1, len(numbers) + 1)).float()
    net = f().float()
    optimizer = Adam(net.parameters(), lr=0.01)
    loss_fn = MSELoss()

    for epoch in range(99999):
        o = net(x)
        if torch.isnan(o).any():
            break
        loss = loss_fn(o, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print(f"{epoch}: x-{net.m:0.5f} ** {net.exp:0.5f} -> {loss.item()}")
        epoch += 1

    xp = np.arange(-10, len(numbers)+1, 0.1)
    plt.plot(xp, net(torch.tensor(xp)).detach().numpy())
    plt.plot(x, y)
    plt.title(f"y = (x-{net.m:0.5f}) ** {net.exp:0.5f}")
    plt.show()

    """
    exp = torch.tensor(1.2, requires_grad=True)
    m = torch.tensor(0.0, requires_grad=True)
    y = torch.tensor(numbers)
    x = torch.tensor(range(len(numbers)))

    opt = Adam([exp, m], lr=0.001)

    print(x)
    print(y)

    for i in range(3):

        loss = 0.0

        for j in range(len(x)):
            p = (x[j] + m).pow(exp)
            print("x:", x[i])
            print("p:", p)
            print("y:", y[i])
            l = (y[i] - p).pow(2)
            print("l:", l)
            print("")
            loss += l

        print(loss)
        loss.backward()

        print("exp.grad:", exp.grad)

        opt.step()
        opt.zero_grad()

        print(i, f"(x-{m:.5f})^{exp:.5f}")
        print("------------")
"""
