import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from graph_data import graph
from dijkstra import dijkstra
from centrality import calculate_centrality
from ai_recommendation import generate_ai_recommendation
import graph_data
# ======================================
# DATA MASTER
# ======================================
SKIN_TYPES = [
    "Berminyak",
    "Kering",
    "Kombinasi",
    "Sensitif"
]
# ======================================
# PAGE CONFIG
# ======================================
st.set_page_config(
    page_title="SkinCare DSS",
    page_icon="🧴",
    layout="wide"
)
# ======================================
# SESSION STATE
# ======================================
if "skin_types" not in st.session_state:
    st.session_state.skin_types = [
        "Berminyak",
        "Kering",
        "Kombinasi",
        "Sensitif"
    ]
# ======================================
# HEADER
# ======================================
st.title("🧴 SkinCare DSS")
st.subheader("Decision Support System Pemilihan Pelembab Menggunakan Graph dan Dijkstra")
st.markdown("---")
# ======================================
# INPUT USER
# ======================================
col1, col2 = st.columns(2)
with col1:
    skin_type = st.selectbox(
        "Pilih Tipe Kulit",
        st.session_state.skin_types
    )
with col2:
    problem = st.selectbox(
        "Pilih Masalah Kulit",
        list(graph[skin_type].keys())
    )
# ======================================
# ANALISIS
# ======================================
if st.button("🔍 Analisis Sekarang"):
    # Jalur tipe kulit -> masalah kulit
    base_cost = graph[skin_type][problem]
    # Dijkstra mulai dari masalah kulit
    distances, previous = dijkstra(graph, problem)
    moisturizer_nodes = []
    for node in distances:
        if node not in graph:
            moisturizer_nodes.append(node)
    ranking = []
    for moisturizer in moisturizer_nodes:
        if distances[moisturizer] != float("inf"):
            total_score = base_cost + distances[moisturizer]
            ranking.append(
                (
                    moisturizer,
                    total_score
                )
            )
    ranking.sort(key=lambda x: x[1])
    if ranking:
        best_product = ranking[0][0]
        best_score = ranking[0][1]
    else:
        best_product = "Tidak ada rekomendasi"
        best_score = "-"
    st.success("Analisis berhasil dilakukan")
    # ======================================
    # JALUR DIJKSTRA
    # ======================================
    st.subheader("📍 Jalur Perhitungan Dijkstra")

    path = []

    current = best_product

    while current in previous:
        path.append(current)
        current = previous[current]

    path.append(problem)

    path.reverse()

    final_path = [skin_type] + path

    # Tampilkan jalur
    st.info(" ➜ ".join(final_path))

    # ======================================
    # DETAIL PERHITUNGAN BOBOT
    # ======================================

    st.subheader("🧮 Detail Perhitungan Bobot")

    total = 0

    # Skin Type -> Problem
    bobot_awal = graph[skin_type][problem]

    st.write(
        f"**{skin_type} ➜ {problem}** = {bobot_awal}"
    )

    total += bobot_awal

    # Problem -> Ingredient -> Product
    for i in range(1, len(path)):

        source = path[i - 1]
        target = path[i]

        if source in graph and target in graph[source]:

            weight = graph[source][target]

            st.write(
                f"**{source} ➜ {target}** = {weight}"
            )

            total += weight
        st.success(
            f"🎯 Total Bobot Jalur = {total}"
        )
    calculation_data = []

    calculation_data.append(
        [skin_type, problem, bobot_awal]
    )

    for i in range(1, len(path)):
        source = path[i - 1]
        target = path[i]

        if source in graph and target in graph[source]:
            calculation_data.append(
                [
                    source,
                    target,
                    graph[source][target]
                ]
            )

    df_calc = pd.DataFrame(
        calculation_data,
        columns=[
            "Dari",
            "Ke",
            "Bobot"
        ]
    )

    st.dataframe(
        df_calc,
        use_container_width=True
    )
    # ======================================
    # AI RECOMMENDATION
    # ======================================
    ai_result = generate_ai_recommendation(
        skin_type,
        problem,
        best_product
    )
    st.subheader("🤖 AI Recommendation")
    st.info(ai_result)
    st.success(
        f"Produk terbaik: {best_product}"
    )
    st.caption(
        "Rekomendasi dihasilkan dari kombinasi "
        "algoritma Dijkstra dan modul AI Recommendation."
    )
    st.markdown("---")
    st.subheader("🏆 Top 5 Rekomendasi Skincare")
    for i, (produk, skor) in enumerate(
            ranking[:5],
            start=1
        ):
            st.success(f"{i}. {produk}")
            st.caption(f"Skor: {skor}")
# ======================================
# MEMBANGUN GRAPH
# ======================================
G = nx.DiGraph()
# Simpan graph di session state
if "graph_data" not in st.session_state:
    st.session_state.graph_data = graph_data
for source in graph:
    for target, weight in graph[source].items():
        G.add_edge(
            source,
            target,
            weight=weight
        )
# ======================================
# STATISTIK GRAPH
# ======================================
st.subheader("📊 Statistik Graph")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric(
        "Jumlah Node",
        G.number_of_nodes()
    )
with c2:
    st.metric(
        "Jumlah Edge",
        G.number_of_edges()
    )
with c3:
    st.metric(
        "Density",
        round(nx.density(G), 3)
    )
# ======================================
# VISUALISASI GRAPH
# ======================================
show_full_graph = st.checkbox(
    "🌐 Tampilkan Graph Lengkap"
)
st.subheader("🌐 Visualisasi Graph")

if show_full_graph:
    G = nx.DiGraph()
    for source in graph:
        for target, weight in graph[source].items():
            G.add_edge(source, target, weight=weight)
else:
    G = nx.DiGraph()
    G.add_edge(
        skin_type,
        problem,
        weight=graph[skin_type][problem]
    )
    for ingredient, w1 in graph[problem].items():
        G.add_edge(
            problem,
            ingredient,
            weight=w1
        )
        for moisturizer, w2 in graph[ingredient].items():
            G.add_edge(
                ingredient,
                moisturizer,
                weight=w2
            )
# =========================
# POSISI NODE MANUAL
# =========================
pos = {}
if show_full_graph:
    skin_types = [
        "Berminyak",
        "Kering",
        "Kombinasi",
        "Sensitif"
    ]
    problems = [
        "Jerawat",
        "Bekas Jerawat",
        "Kusam",
        "Pori Besar"
    ]
    ingredients = [
        "Salicylic Acid",
        "Centella",
        "Tea Tree",
        "Niacinamide",
        "Alpha Arbutin",
        "Ceramide",
        "Vitamin C",
        "Tranexamic Acid",
        "Zinc PCA",
        "Cica-B5"
    ]
    products = []
    for node in G.nodes():
        if (
            node not in skin_types
            and node not in problems
            and node not in ingredients
        ):
            products.append(node)
    pos = {}
    # Kolom 1 : Jenis kulit
    for i, node in enumerate(skin_types):
        pos[node] = (0, -i * 4)
    # Kolom 2 : Masalah kulit
    for i, node in enumerate(problems):
        pos[node] = (4, -i * 4)
    # Kolom 3 : Kandungan aktif
    for i, node in enumerate(ingredients):
        if node in G.nodes():
            pos[node] = (8, -i * 2)
    # Kolom 4 : Produk
    for i, node in enumerate(products):
        pos[node] = (14, -i * 2)
else:
    # Tipe kulit
    pos[skin_type] = (0, 0)
    # Masalah kulit
    pos[problem] = (3, 0)
    ingredient_y = 6
    for ingredient in graph[problem]:
        # Kandungan
        pos[ingredient] = (6, ingredient_y)
        moisturizer_y = ingredient_y
        # Pelembab
        for moisturizer in graph[ingredient]:
            pos[moisturizer] = (
                10,
                moisturizer_y
            )
            moisturizer_y -= 2
        ingredient_y -= 6
# =========================
# WARNA NODE
# =========================
node_colors = []
for node in G.nodes():
    if node in [
        "Berminyak",
        "Kering",
        "Kombinasi",
        "Sensitif"
    ]:
        node_colors.append("skyblue")
    elif node in [
        "Jerawat",
        "Bekas Jerawat",
        "Kusam",
        "Pori Besar"
    ]:
        node_colors.append("lightcoral")
    elif node in [
        "Salicylic Acid",
        "Centella",
        "Tea Tree",
        "Niacinamide",
        "Alpha Arbutin",
        "Ceramide",
        "Vitamin C",
        "Tranexamic Acid",
        "Zinc PCA"
    ]:
        node_colors.append("gold")
    else:
        node_colors.append("lightgreen")
# =========================
# GAMBAR GRAPH
# =========================
fig, ax = plt.subplots(figsize=(20, 14))
nx.draw(
    G,
    pos,
    with_labels=False,
    node_color=node_colors,
    node_size=3000,
    arrows=True,
    ax=ax
)
for node, (x, y) in pos.items():
    ax.text(
        x + 0.3,
        y,
        node,
        fontsize=15,
        fontweight="bold",
        va="bottom"
    )
edge_labels = nx.get_edge_attributes(
    G,
    "weight"
)
nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=edge_labels
)
plt.axis("off")
col1, col2 = st.columns([4,1])
with col1:
    st.pyplot(fig)        
# ======================================
# CENTRALITY
# ======================================
st.markdown("---")
st.subheader("⭐ Degree Centrality Analysis")
centrality = calculate_centrality(graph)
centrality_df = pd.DataFrame(
    centrality.items(),
    columns=[
        "Node",
        "Centrality Score"
    ]
)
centrality_df = centrality_df.sort_values(
    by="Centrality Score",
    ascending=False
)
st.dataframe(
    centrality_df,
    use_container_width=True
)
st.bar_chart(
    centrality_df.set_index("Node")
)
# ======================================
# FOOTER
# ======================================
st.markdown("---")
st.caption(
    "SkinCare DSS | Struktur Data - Graph, Dijkstra, Centrality Analysis"
)
# =========================
# INPUT NODE & EDGE
# =========================
st.subheader("➕ Tambah Data Baru")
menu = st.selectbox(
        "Pilih Data yang Ingin Ditambahkan",
        [
            "Jenis Kulit",
            "Masalah Kulit",
            "Kandungan",
            "Produk"
        ]
    )
# =====================
# TAMBAH JENIS KULIT
# =====================
if menu == "Jenis Kulit":
    kulit_baru = st.text_input(
        "Nama Jenis Kulit"
    )
    if st.button("Tambah Jenis Kulit"):
        if kulit_baru not in st.session_state.skin_types:
            st.session_state.skin_types.append(
                kulit_baru
            )
            graph[kulit_baru] = {}
            st.success(
                f"{kulit_baru} berhasil ditambahkan"
            )
        else:
            st.warning(
                "Jenis kulit sudah ada"
            )
# =====================
# TAMBAH MASALAH KULIT
# =====================
elif menu == "Masalah Kulit":
    jenis_kulit = st.selectbox(
        "Pilih Jenis Kulit",
        st.session_state.skin_types
    )
    masalah_baru = st.text_input(
        "Nama Masalah Kulit"
    )
    bobot = st.number_input(
        "Bobot",
        min_value=1,
        max_value=10,
        value=1
    )
    if st.button("Tambah Masalah Kulit"):

        # buat node jenis kulit jika belum ada
        if jenis_kulit not in graph:
            graph[jenis_kulit] = {}
        # hubungkan jenis kulit -> masalah
        graph[jenis_kulit][masalah_baru] = bobot

        # buat node masalah agar bisa punya kandungan
        if masalah_baru not in graph:
            graph[masalah_baru] = {}
        st.success(
            f"{masalah_baru} berhasil ditambahkan ke {jenis_kulit}"
        )
        st.write("Data terbaru:")
        st.write(graph[jenis_kulit])
# =====================
# TAMBAH KANDUNGAN
# =====================
elif menu == "Kandungan":
    jenis_kulit = st.selectbox(
        "Pilih Jenis Kulit",
        st.session_state.skin_types,
        key="jk_kandungan"
    )
    masalah = st.selectbox(
        "Pilih Masalah Kulit",
        list(graph[jenis_kulit].keys()),
        key="masalah_kandungan"
    )
    kandungan = st.text_input(
        "Nama Kandungan"
    )

    bobot = st.number_input(
        "Bobot Kandungan",
        min_value=1,
        value=1
    )
    if st.button("Tambah Kandungan"):
        graph[masalah][kandungan] = bobot
        if kandungan not in graph:
            graph[kandungan] = {}
        st.success(
            f"{kandungan} berhasil ditambahkan ke {masalah}"
        )
# =====================
# TAMBAH PRODUK
# =====================
elif menu == "Produk":
    jenis_kulit = st.selectbox(
        "Pilih Jenis Kulit",
        st.session_state.skin_types,
        key="jk_produk"
    )
    masalah = st.selectbox(
        "Pilih Masalah Kulit",
        list(graph[jenis_kulit].keys()),
        key="ms_produk"
    )
    kandungan = st.selectbox(
        "Pilih Kandungan",
        list(graph[masalah].keys()),
        key="kd_produk"
    )
    produk = st.text_input(
        "Nama Produk"
    )
    bobot = st.number_input(
        "Bobot Produk",
        min_value=1,
        value=1
    )
    if st.button("Tambah Produk"):
        graph[kandungan][produk] = bobot
        st.success(
            f"{produk} berhasil ditambahkan ke {kandungan}"
        )