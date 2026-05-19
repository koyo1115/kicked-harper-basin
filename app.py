import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors

def kicked_harper_map(x, p, K, L):
    pn = (p + K * np.sin(x)) % (2 * np.pi)
    xn = (x - L * np.sin(pn)) % (2 * np.pi)
    return xn, pn

def check_exit(x, p):
    if (x - 0)**2 + (p - 0)**2 <= 0.09:
        return 1
    elif (x - np.pi)**2 + (p - np.pi)**2 <= 0.09:
        return 2
    return 0

def get_basin_id(x0, p0, K, L, max_iter):
    curr_x, curr_p = x0, p0
    s = check_exit(curr_x, curr_p)
    if s > 0:
        return s
    for i in range(max_iter):
        curr_x, curr_p = kicked_harper_map(curr_x, curr_p, K, L)
        s = check_exit(curr_x, curr_p)
        if s > 0:
            return s
    return 0

st.title("Kicked Harper Basin")

K = st.slider("K", 0.0, 10.0, 2.0)
L = st.slider("L", 0.0, 10.0, 2.0)

res = 1000
max_iter = 1000

ba = np.zeros((res, res), dtype=int)
x_range = np.linspace(0, 2*np.pi, res)
p_range = np.linspace(0, 2*np.pi, res)

for i in range(res):
    for j in range(res):
        ba[j, i] = get_basin_id(x_range[i], p_range[j], K, L, max_iter)

colors = ['black', 'crimson', 'royalblue']
cmap = matplotlib.colors.ListedColormap(colors)

fig, ax = plt.subplots()
ax.imshow(ba, origin='lower', extent=[0, 2*np.pi, 0, 2*np.pi],
          cmap=cmap, vmin=0, vmax=2)
ax.set_xlabel("x")
ax.set_ylabel("p")
ax.set_title(f"K={K}, L={L}")

st.pyplot(fig)