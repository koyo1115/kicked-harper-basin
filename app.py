import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors

def kicked_harper_map(x, p, K, L):
    pn = (p + K * np.sin(x)) % (2 * np.pi)
    xn = (x - L * np.sin(pn)) % (2 * np.pi)
    return xn, pn

def check_exit(x, p, r1, r2, exit1_x, exit1_p, exit2_x, exit2_p):
    if (x - exit1_x)**2 + (p - exit1_p)**2 <= r1**2:
        return 1
    elif (x - exit2_x)**2 + (p - exit2_p)**2 <= r2**2:
        return 2
    return 0

def get_basin_id(x0, p0, K, L, max_iter, r1, r2, exit1_x, exit1_p, exit2_x, exit2_p):
    curr_x, curr_p = x0, p0
    s = check_exit(curr_x, curr_p, r1, r2, exit1_x, exit1_p, exit2_x, exit2_p)
    if s > 0:
        return s
    for i in range(max_iter):
        curr_x, curr_p = kicked_harper_map(curr_x, curr_p, K, L)
        s = check_exit(curr_x, curr_p, r1, r2, exit1_x, exit1_p, exit2_x, exit2_p)
        if s > 0:
            return s
    return 0

st.title("キックドハーパー写像 盆地図")
st.write("パラメータを設定して実行ボタンを押してください。")

st.subheader("パラメータ設定")
K = st.slider("K", 0.0, 10.0, 2.0)
L = st.slider("L", 0.0, 10.0, 2.0)
res = st.slider("解像度 (res)", 50, 300, 100)
max_iter = st.slider("最大反復回数 (max_iter)", 100, 2000, 500)

st.subheader("出口1（赤）の設定")
exit1_x = st.slider("出口1 x座標", 0.0, 2*np.pi, 0.0)
exit1_p = st.slider("出口1 p座標", 0.0, 2*np.pi, 0.0)
r1 = st.slider("出口1 半径", 0.1, 1.0, 0.3)

st.subheader("出口2（青）の設定")
exit2_x = st.slider("出口2 x座標", 0.0, 2*np.pi, float(np.pi))
exit2_p = st.slider("出口2 p座標", 0.0, 2*np.pi, float(np.pi))
r2 = st.slider("出口2 半径", 0.1, 1.0, 0.3)

if st.button("実行"):
    with st.spinner("計算中..."):
        ba = np.zeros((res, res), dtype=int)
        x_range = np.linspace(0, 2*np.pi, res)
        p_range = np.linspace(0, 2*np.pi, res)

        for i in range(res):
            for j in range(res):
                ba[j, i] = get_basin_id(x_range[i], p_range[j], K, L, max_iter,
                                        r1, r2, exit1_x, exit1_p, exit2_x, exit2_p)

    colors = ['black', 'crimson', 'royalblue']
    cmap = matplotlib.colors.ListedColormap(colors)

    fig, ax = plt.subplots()
    ax.imshow(ba, origin='lower', extent=[0, 2*np.pi, 0, 2*np.pi],
              cmap=cmap, vmin=0, vmax=2)

    circle1 = plt.Circle((exit1_x, exit1_p), r1, color='red', fill=False, linewidth=2)
    circle2 = plt.Circle((exit2_x, exit2_p), r2, color='blue', fill=False, linewidth=2)
    ax.add_patch(circle1)
    ax.add_patch(circle2)

    ax.set_xlabel("x")
    ax.set_ylabel("p")
    ax.set_title(f"K={K}, L={L}")

    st.pyplot(fig)
    st.success("計算完了！")