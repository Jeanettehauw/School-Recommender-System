import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.title("🏫 CariSekolah.ID")

df = pd.read_csv("school_dataset_fixed.csv")

def get_recommendations(user_input, top_n=3):
    df_filtered = df[df['Jenis Sekolah'] == user_input['Jenis Sekolah']].copy()

    fasilitas_str = ", ".join(user_input["Fasilitas"]) if isinstance(user_input["Fasilitas"], list) else user_input["Fasilitas"]
    ekskul_str = ", ".join(user_input["Ekskul"]) if isinstance(user_input["Ekskul"], list) else user_input["Ekskul"]
    
    user_features = " ".join([
        user_input["Daerah"],
        user_input["Kota"],
        # user_input["Jenis Sekolah"],
        user_input["Tipe Sekolah"],
        user_input["Akreditasi"],
        fasilitas_str,
        ekskul_str,
        user_input["Kurikulum"],
        user_input["Transportasi"],
        user_input["Bahasa Pengantar"],
        user_input["Pendidikan Agama"],
        user_input["Anggaran SPP (Rp)"],
        user_input["Biaya Masuk (Rp)"],
    ]).lower()

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([user_features] + df_filtered['content'].tolist())
    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
    df_filtered['score'] = cosine_sim
    return df_filtered.sort_values(by='score', ascending=False).head(top_n)

st.subheader("Child's Information")
age = st.number_input("Age :", min_value=2, step=1)
gender = st.selectbox("Gender :", ("Girl", "Boy"))
next_edu_lvl = st.selectbox("Education Level :", ("Pre-School", "TK-A", "TK-B", "SD", "SMP", "SMA"))

facilities = [
    "Aula",
    "Kolam Renang",
    "Lab Komputer",
    "Lapangan",
    "Ruang Musik",
    "Perpustakaan",
    "Ruang Seni"
]

ekskul = [
    "Basket",
    "Futsal",
    "KIR",
    "Musik",
    "Pencak Silat",
    "Pramuka",
    "Robotik",
    "Tari"
]

transport = [
    "Tidak Ada",
    "Antar Jemput Pribadi",
    "Bus Sekolah"
]

school_type = ["Internasional", "Nasional", "Nasional Plus", "Negeri"]

agama = ["Tidak Ada", "Budha", "Hindu", "Islam", "Katolik", "Kristen"]

bahasa = ["Bahasa Indonesia", "Bahasa Inggris", "Jepang", "Mandarin" ]

kota_list = [
    "Jakarta Barat", "Jakarta Timur", "Jakarta Pusat", "Jakarta Utara", "Jakarta Selatan"
]

jkt_utara = [
    'Penjaringan', 'Pademangan', 'Tanjung Priok', 'Koja',
    'Pantai Indah Kapuk', 'Kelapa Gading', 'Cilincing'
]

jkt_timur = [
    'Matraman', 'Jatinegara', 'Pasar Rebo', 'Kramat Jati',
    'Cipayung', 'Ciracas', 'Cakung', 'Pulo Gadung', 'Duren Sawit'
]

jkt_selatan = [
    'Cilandak', 'Jagakarsa', 'Kebayoran Baru', 'Kebayoran Lama',
    'Pesanggrahan', 'Pasar Minggu', 'Pancoran', 'Mampang Prapatan',
    'Setiabudi', 'Tebet'
]

jkt_pusat = [
    'Gambir', 'Sawah Besar', 'Kemayoran', 'Senen',
    'Cempaka Putih', 'Menteng', 'Tanah Abang', 'Johar Baru'
]

jkt_barat = [
    'Cengkareng', 'Grogol Petamburan', 'Taman Sari', 'Tambora',
    'Kebon Jeruk', 'Kelapa Dua', 'Kalideres', 'Kembangan'
]

akreditasi = ["A", "B", "C"]

kurikulum = ["Kurikulum 2013", "Cambridge", "IB", "Kurikulum Merdeka"]

st.subheader("Location Preferences")
address = st.text_input("Home Address :")
kota = st.selectbox("City :", kota_list)
if kota == 'Jakarta Barat':
    city = st.selectbox("Region :", jkt_barat)
elif kota == 'Jakarta Utara':
    city = st.selectbox("Region :", jkt_utara)
elif kota == 'Jakarta Pusat':
    city = st.selectbox("Region :", jkt_pusat)
elif kota == 'Jakarta Selatan':
    city = st.selectbox("Region :", jkt_selatan)
else:
    city = st.selectbox("Region :", jkt_timur)
max_distance = st.number_input("Maximum Distance from Home :", min_value=0, step=1)
transport_select = st.selectbox("Transportation Options :", transport)

st.subheader("School Preferences")
type_sch = st.selectbox("Type of School Prefered :", school_type)
curriculum = st.selectbox("Curriculum Preference :", kurikulum)
tuition = st.number_input("Monthly Tuition Budget :", min_value=100000, step=1)
enroll = st.number_input("Initial Enrollment Fee Budget :", min_value=100000, step=1)
language = st.selectbox("Preferred Language of Instruction :", bahasa)

st.subheader("Additional References")
akred = st.selectbox("School Accreditation Level :", akreditasi)
ekskul_select = []
st.text("Ekstrakulikuler   :")
for i, eks in enumerate(ekskul):
    if st.checkbox(eks, key=f"checkbox_{i}"):
        ekskul_select.append(eks)
fasilities_select = []
st.text("Facilities Needed:")
for fas in facilities:
    if st.checkbox(fas):
        fasilities_select.append(fas)
moral = st.selectbox("Religious or Moral Education :", agama)

st.subheader("Parent's Information")
with st.form("my_form"):
    # inputan user, misal
    name = st.text_input("Name")
    email = st.text_input("Email")

    # tombol submit
    submitted = st.form_submit_button("Submit")

def combine_features(row):
    return " ".join([
        str(row['Daerah']),
        str(row['Kota']),
        # str(row['Jenis Sekolah']),
        str(row['Tipe Sekolah']),
        str(row['Akreditasi']),
        str(row['Fasilitas']),
        str(row['Kurikulum']),
        str(row['Ekskul']),
        str(row['Transportasi']),
        str(row['Bahasa Pengantar']),
        str(row['Pendidikan Agama']),
        str(row['Anggaran SPP (Rp)']),
        str(row['Biaya Masuk (Rp)']),
    ]).lower()

df['content'] = df.apply(combine_features, axis=1)

# Evaluation Section -------------------------------------------------------
relevant_schools_1 = ['SMP Pelita Ilmu 121', 'Sekolah Harapan Bangsa 63']
relevant_schools_2 = ['Sekolah Harapan Bangsa 125', 'SMA Nusantara 137']
relevant_schools_3 = ['SD Bintang Timur 97', 'SD Bintang Timur 85']

user_1 = {
  "Kota": "Jakarta Utara",
  "Daerah": "Pademangan",
  "Jenis Sekolah": "SMP",
  "Tipe Sekolah": "Negeri",
  "Akreditasi": "B",
  "Fasilitas": ["Perpustakaan", "Lapangan"],
  "Ekskul": ["Robotik"],
  "Transportasi": "Tidak Ada",
  "Bahasa Pengantar": "Bahasa Indonesia",
  "Pendidikan Agama": "Islam",
  "Kurikulum": "Kurikulum 2013",
  "Anggaran SPP (Rp)": "0",
  "Biaya Masuk (Rp)": "0"
}

user_2 = {
  "Kota": "Jakarta Pusat",
  "Daerah": "Menteng",
  "Jenis Sekolah": "SMA",
  "Tipe Sekolah": "Internasional",
  "Akreditasi": "A",
  "Fasilitas": ["Aula"],
  "Ekskul": ["Robotik"],
  "Transportasi": "Bus Sekolah",
  "Bahasa Pengantar": "Bahasa Inggris",
  "Pendidikan Agama": "Kristen",
  "Kurikulum": "Cambridge",
  "Anggaran SPP (Rp)": "3000000",
  "Biaya Masuk (Rp)": "15000000"
}

user_3 = {
  "Kota": "Jakarta Selatan",
  "Daerah": "Pesanggrahan",
  "Jenis Sekolah": "SD",
  "Tipe Sekolah": "Nasional Plus",
  "Akreditasi": "A",
  "Fasilitas": ["Ruang Musik", "Perpustakaan"],
  "Ekskul": ["Pramuka"],
  "Transportasi": "Antar Jemput Pribadi",
  "Bahasa Pengantar": "Bahasa Inggris",
  "Pendidikan Agama": "Budha",
  "Kurikulum": "IB",
  "Anggaran SPP (Rp)": "3000000",
  "Biaya Masuk (Rp)": "18000000"
}

def precision_at_k(recommended, relevant, k=3):
    recommended_top_k = recommended[:k]
    hits = len(set(recommended_top_k) & set(relevant))
    return hits / k

def recall_at_k(recommended, relevant, k=3):
    recommended_top_k = recommended[:k]
    hits = len(set(recommended_top_k) & set(relevant))
    return hits / len(relevant) if relevant else 0

def f1_at_k(precision, recall):
    if precision + recall == 0:
        return 0
    return 2 * (precision * recall) / (precision + recall)

test_cases = [
    ("User 1", user_1, relevant_schools_1),
    ("User 2", user_2, relevant_schools_2),
    ("User 3", user_3, relevant_schools_3),
]

precision_scores = []
recall_scores = []
f1_scores = []

print("\n--- Running Precision@3, Recall@3, F1@3 Evaluation on Simulated Users ---\n")

for label, user_profile, ground_truth in test_cases:
    recs = get_recommendations(user_profile, top_n=3)
    recommended_names = recs["Nama Sekolah"].tolist()

    precision = precision_at_k(recommended_names, ground_truth, k=3)
    recall = recall_at_k(recommended_names, ground_truth, k=3)
    f1 = f1_at_k(precision, recall)

    precision_scores.append(precision)
    recall_scores.append(recall)
    f1_scores.append(f1)

    print(f"{label}")
    print(f"  Recommended: {recommended_names}")
    print(f"  Relevant:    {ground_truth}")
    print(f"  Precision@3: {precision:.2f}")
    print(f"  Recall@3:    {recall:.2f}")
    print(f"  F1@3:        {f1:.2f}\n")


print("📊 Average Metrics Across All Users")
print(f"  Precision@3: {sum(precision_scores)/len(precision_scores):.2f}")
print(f"  Recall@3:    {sum(recall_scores)/len(recall_scores):.2f}")
print(f"  F1@3:        {sum(f1_scores)/len(f1_scores):.2f}")

# Evaluation Section -------------------------------------------------------

if submitted: 
    user_input = {
        "Daerah" : city,
        "Kota" : kota,
        "Jenis Sekolah" : next_edu_lvl,
        "Tipe Sekolah" : type_sch,
        "Akreditasi" : akred,
        "Fasilitas" : fasilities_select,
        "Kurikulum" : curriculum,
        "Ekskul" : ekskul_select,
        "Transportasi" : transport_select,
        "Bahasa Pengantar" : language,
        "Pendidikan Agama" : moral,
        "Anggaran SPP (Rp)" : str(tuition),
        "Biaya Masuk (Rp)" : str(enroll)
    }

    def render_school_card(row):
        st.markdown(f"""
        <div style="
            border: 1px solid #e0e0e0;
            border-radius: 16px;
            padding: 1.8em;
            margin-bottom: 1.5em;
            background-color: rgba(255, 255, 255, 0.10);
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            font-family: 'Segoe UI', sans-serif;
        ">
            <h2 style="color: #FFFFFF; margin-bottom: 0.4em; text-align: center">
                🏫 {row['Nama Sekolah']}
            </h2>
            <p style="margin: 0.2em 0;"><span style="font-weight:600">📍 Address:</span> {row['Alamat']}, {row['Daerah']}, {row['Kota']}</p>
            <p style="margin: 0.2em 0;"><span style="font-weight:600">🎓 Level:</span> {row['Jenis Sekolah']} &nbsp;&nbsp; <span style="font-weight:600">🏷 Type:</span> {row['Tipe Sekolah']}</p>
            <p style="margin: 0.2em 0;"><span style="font-weight:600">📝 Accreditation:</span> {row['Akreditasi']} &nbsp;&nbsp; <span style="font-weight:600">📚 Curriculum:</span> {row.get('Kurikulum', '-')}</p>
            <p style="margin: 0.2em 0;"><span style="font-weight:600">💰 Tuition:</span> Rp {row['Anggaran SPP (Rp)']} &nbsp;&nbsp; <span style="font-weight:600">🧾 Enrollment Fee:</span> Rp {row['Biaya Masuk (Rp)']}</p>
            <p style="margin: 0.2em 0;"><span style="font-weight:600">🏗 Facilities:</span> {row['Fasilitas']}</span></p>
            <p style="margin: 0.2em 0;"><span style="font-weight:600">🎯 Extracurriculars:</span> {row['Ekskul']}</span></p>
            <p style="margin: 0.2em 0;"><span style="font-weight:600">🧭 Religious Education:</span> {row['Pendidikan Agama']}</p>
            <p style="margin: 0.2em 0;"><span style="font-weight:600">🌐 Website:</span> <a href="{row['Website']}" target="_blank" style="color:#1f77b4;text-decoration:none;">{row['Website']}</a></p>
        </div>
        """, unsafe_allow_html=True)

    st.header(f"Top 3 Recommended Schools for {name}'s Child")
    try:
        recom = get_recommendations(user_input, top_n=3)
        recommended_names = recom["Nama Sekolah"].tolist()

        for idx, row in recom.iterrows():
            # st.markdown(f"""
            # ---
            # ### 🏫 {row['Nama Sekolah']}
            # - **Jenjang:** {row['Jenis Sekolah']}
            # - **Tipe:** {row['Tipe Sekolah']}
            # - **Alamat:** {row['Alamat']}
            # - **Daerah:** {row['Daerah']}
            # - **Kota:** {row['Kota']}
            # - **Akreditasi:** {row['Akreditasi']}
            # - **Fasilitas:** {row['Fasilitas']}
            # - **Ekskul:** {row['Ekskul']}
            # - **Transportasi:** {row['Transportasi']}
            # - **Bahasa Pengantar:** {row['Bahasa Pengantar']}
            # - **Agama:** {row['Pendidikan Agama']}
            # - **SPP:** Rp {row['Anggaran SPP (Rp)']}
            # - **Biaya Masuk:** Rp {row['Biaya Masuk (Rp)']}
            # - **No Telepon:** {row['No Telepon']}
            # - **Website:** {row['Website']}
            # """)
            render_school_card(row)

            print("")
            print(f"{row['Nama Sekolah']}: {row['score']}")

    except Exception as e:
        st.error(f"Gagal merekomendasikan sekolah: {e}")