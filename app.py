import streamlit as st
import anthropic
import json

st.set_page_config(
    page_title="Instagram Influencer Analiz",
    page_icon="📸",
    layout="wide"
)

st.markdown("""
<style>
.profile-card {
    background: linear-gradient(135deg, #833ab4 0%, #fd1d1d 50%, #fcb045 100%);
    padding: 22px 26px;
    border-radius: 16px;
    color: white;
    margin-bottom: 24px;
}
.profile-card h2 { margin: 0 0 6px 0; font-size: 1.6rem; }
.profile-card p  { margin: 0; opacity: 0.92; font-size: 0.95rem; }
.section-box {
    background: #f4f6ff;
    border-left: 5px solid #833ab4;
    padding: 14px 18px;
    border-radius: 8px;
    margin-bottom: 14px;
}
.storyboard-row {
    background: #1a1a2e;
    color: #e0e0e0;
    padding: 14px 18px;
    border-radius: 10px;
    margin-bottom: 10px;
    border-left: 4px solid #fcb045;
}
.tag-pill {
    display: inline-block;
    background: #833ab4;
    color: white;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.8rem;
    margin: 2px;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ────────────────────────────────────────────────────────────
if "profiles" not in st.session_state:
    st.session_state.profiles = {}
if "active_username" not in st.session_state:
    st.session_state.active_username = None

def active_profile():
    u = st.session_state.active_username
    return st.session_state.profiles.get(u) if u else None

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Sozlamalar")
    api_key = st.text_input(
        "🔑 Anthropic API Key",
        type="password",
        help="console.anthropic.com saytidan API key oling"
    )
    st.markdown("---")
    st.markdown("### 💾 Saqlangan Profillar")
    if st.session_state.profiles:
        usernames = list(st.session_state.profiles.keys())
        chosen = st.selectbox("Profil tanlang", usernames, format_func=lambda x: f"@{x}")
        if st.button("✅ Profilni faollashtirish", use_container_width=True):
            st.session_state.active_username = chosen
            st.success(f"@{chosen} faollashtirildi!")
        if st.session_state.active_username:
            st.info(f"Faol: **@{st.session_state.active_username}**")
    else:
        st.caption("Hali profil qo'shilmagan")

# ── Title ────────────────────────────────────────────────────────────────────
st.title("📸 Instagram Influencer Analiz")
st.markdown("**Influencer uslubini o'rganib, ssenariy va raskadirofka yaratish tizimi**")
st.markdown("---")

tab_add, tab_analysis, tab_create = st.tabs([
    "➕ Profil Qo'shish",
    "🔍 Uslub Tahlili",
    "🎬 Ssenariy & Raskadirofka",
])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — Add / Analyse Profile
# ════════════════════════════════════════════════════════════════════════════
with tab_add:
    st.markdown("### Instagram Influencer ma'lumotlarini kiriting")
    st.markdown(
        "Qanchalik ko'p ma'lumot kiritilsa, tahlil shunchalik aniq bo'ladi. "
        "Namuna postlar eng muhim qism hisoblanadi."
    )

    c1, c2 = st.columns(2)
    with c1:
        username   = st.text_input("👤 Instagram Username", placeholder="@username yoki username")
        profile_url = st.text_input("🔗 Profil havolasi", placeholder="https://www.instagram.com/username/")
        followers  = st.text_input("📊 Followers (taxminan)", placeholder="500K, 1.2M ...")
        engagement = st.text_input("❤️ O'rtacha engagement", placeholder="5%, 50K likes ...")
        audience   = st.text_input("👥 Asosiy auditoriya", placeholder="18-35 yosh, sport muxlislari ...")
    with c2:
        niche = st.selectbox("📂 Yo'nalish", [
            "Lifestyle", "Fashion & Beauty", "Fitness & Health", "Food & Cooking",
            "Travel", "Tech & Gaming", "Business & Finance", "Comedy & Entertainment",
            "Education", "Motivation & Mindset", "Music & Art", "Family & Parenting", "Other",
        ])
        lang = st.selectbox("🌐 Kontent tili", [
            "O'zbek", "Rus", "English", "Aralash (O'zbek+Rus)",
        ])
        formats = st.multiselect(
            "📱 Kontent formatlari",
            ["Reels", "Stories", "Carousel", "Single Photo", "IGTV", "Live"],
            default=["Reels", "Stories"],
        )

    bio = st.text_area("📝 Bio matni (profildan nusxa ko'chiring)", height=80,
                       placeholder="Misol: Fitness coach | Hayot go'zal | DM for collab 🔥")
    visual = st.text_area("🎨 Vizual uslub tavsifi", height=90,
                          placeholder="Misol: pastel ranglar, minimalist, golden-hour yorug'lik, "
                                      "Ko'p harakatli montaj, matn overlay ko'p ishlatiladi ...")
    samples = st.text_area(
        "📋 Namuna postlar / Captions (3–5 ta kiriting, har birini yangi qatordan boshlang)",
        height=180,
        placeholder="1. Bugun yana bir rekord! 5:00 AM uyg'ondim va...\n"
                    "2. Ko'p so'raydi: qanday motivatsiya topsam? Mening javobim...\n"
                    "3. 3 oy oldin bu kiyim sig'mas edi. Bugun esa...",
    )

    if st.button("🔍 Profilni Tahlil Qilish", type="primary", use_container_width=True):
        if not api_key:
            st.error("❌ Sidebar'dan Anthropic API Key kiriting")
        elif not username:
            st.error("❌ Username kiritish majburiy")
        elif not samples and not bio and not visual:
            st.error("❌ Kamida bio, vizual tavsif yoki namuna postlardan birini kiriting")
        else:
            clean = username.lstrip("@").strip()
            with st.spinner("🤖 Claude profil tahlil qilmoqda..."):
                try:
                    client = anthropic.Anthropic(api_key=api_key)
                    prompt = f"""Sen Instagram kontent strategisti va kreativ direktorsan.
Quyidagi influencer profilini CHUQUR tahlil qil va professional uslub qo'llanmasi yarat.

PROFIL MA'LUMOTLARI:
- Username: @{clean}
- Bio: {bio or '—'}
- Followers: {followers or '—'}
- Engagement: {engagement or '—'}
- Yo'nalish: {niche}
- Kontent formatlari: {', '.join(formats) if formats else '—'}
- Kontent tili: {lang}
- Asosiy auditoriya: {audience or '—'}
- Vizual uslub tavsifi: {visual or '—'}

NAMUNA POSTLAR / CAPTIONS:
{samples or '—'}

Quyidagi 6 bo'limda BATAFSIL va AMALIY tahlil yoz. Har bir bo'lim real va spesifik bo'lsin:

## 1. KONTENT USLUBI
- Ton va ovoz (rasmiy/norasmiy, energik/sokin, samimiy/professional)
- Xarakterli so'z va iboralar (u ko'p ishlatadiganlari)
- Hikoyalashtirish usuli (qanday qilib ko'ruvchini tortadi)
- Hook strategiyasi (birinchi 3 soniyada nima qiladi)
- Hazil va o'ziga xoslik belgilari

## 2. VIZUAL USLUB
- Rang palitasi (asosiy 3-4 rang)
- Estetik kayfiyat va mood
- Yoritish uslubi
- Kamera burchagi va kompozitsiya
- Montaj tezligi va kesim uslubi
- Matn overlay va grafika uslubi

## 3. CAPTION USLUBI
- Uzunlik va tuzilma
- Boshlanish formulasi (qanday ochiladi)
- Emoji ishlatish darajasi va uslubi
- Hashtag strategiyasi
- Call-to-action uslubi

## 4. KONTENT TUZILMASI (Reels uchun)
- Boshlanish–O'rta–Oxir sxemasi
- Pacing va ritm
- Har doim mavjud bo'lgan elementlar
- O'tish (transition) effektlari

## 5. AUDITORIYA BILAN MUNOSABAT
- Shaxsiy ulanish usuli
- Autentiklik belgilari
- Qaysi emotsiyani uyg'otadi

## 6. USLUB DNK (5 ta oltin qoida)
Bu influencer uchun 5 ta asosiy tamoyil:
HAMMA VAQT qiladigan 3 ta narsa va HECH QACHON qilmaydigan 2 ta narsa.

Tahlilni O'ZBEK TILIDA yoz. Har bir bo'limni aniq va amaliy qil."""

                    resp = client.messages.create(
                        model="claude-opus-4-6",
                        max_tokens=4096,
                        messages=[{"role": "user", "content": prompt}],
                    )
                    analysis = resp.content[0].text

                    st.session_state.profiles[clean] = {
                        "username": clean,
                        "url": profile_url,
                        "bio": bio,
                        "visual": visual,
                        "samples": samples,
                        "niche": niche,
                        "lang": lang,
                        "formats": formats,
                        "audience": audience,
                        "followers": followers,
                        "engagement": engagement,
                        "analysis": analysis,
                    }
                    st.session_state.active_username = clean
                    st.success(f"✅ @{clean} muvaffaqiyatli tahlil qilindi va saqlandi!")
                    st.info("👉 '🔍 Uslub Tahlili' yoki '🎬 Ssenariy & Raskadirofka' tabiga o'ting")

                except anthropic.AuthenticationError:
                    st.error("❌ API key noto'g'ri. Iltimos tekshiring.")
                except Exception as e:
                    st.error(f"❌ Xatolik: {e}")

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — Style Analysis
# ════════════════════════════════════════════════════════════════════════════
with tab_analysis:
    prof = active_profile()
    if not prof:
        st.info("👈 Avval '➕ Profil Qo'shish' tabida influencer profilini tahlil qiling")
    else:
        tags = " ".join(
            f'<span class="tag-pill">{f}</span>' for f in (prof.get("formats") or [])
        )
        st.markdown(f"""
<div class="profile-card">
  <h2>@{prof['username']}</h2>
  <p>
    📂 {prof['niche']} &nbsp;|&nbsp;
    👥 {prof.get('followers') or '—'} followers &nbsp;|&nbsp;
    ❤️ {prof.get('engagement') or '—'} engagement &nbsp;|&nbsp;
    🌐 {prof.get('lang')}
  </p>
  <p style="margin-top:8px">{tags}</p>
  {f"<p style='margin-top:6px'>🔗 <a href='{prof['url']}' style='color:white'>{prof['url']}</a></p>" if prof.get('url') else ''}
</div>
""", unsafe_allow_html=True)

        st.markdown("### 📊 To'liq Uslub Tahlili")
        st.markdown(prof["analysis"])

        st.download_button(
            "⬇️ Tahlilni TXT yuklab olish",
            data=prof["analysis"],
            file_name=f"{prof['username']}_uslub_tahlili.txt",
            mime="text/plain",
        )

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — Script + Storyboard Generator
# ════════════════════════════════════════════════════════════════════════════
with tab_create:
    prof = active_profile()
    if not prof:
        st.info("👈 Avval '➕ Profil Qo'shish' tabida influencer profilini tahlil qiling")
    else:
        st.markdown(f"### 🎬 @{prof['username']} uslubida kontent yaratish")

        c1, c2 = st.columns([3, 2])
        with c1:
            topic = st.text_area(
                "📌 Mavzu / G'oya",
                height=100,
                placeholder="Misol: 'Sabahgi routine — erta turish sirlari'\n"
                            "'Yangi iPhone 16 sharhi'\n"
                            "'30 kunda 10 kg yo'qotish tajribam'",
            )
        with c2:
            reel_type = st.selectbox("📱 Kontent turi", [
                "Reels (60-90 soniya)",
                "Reels (30 soniya)",
                "Reels (15 soniya — Trend)",
                "Stories (5-7 ta kadr)",
                "Carousel Post",
            ])
            out_lang = st.selectbox("🌐 Kontent tili", [
                "O'zbek", "Rus", "English", "Aralash (O'zbek+Rus)",
            ])
            mood = st.selectbox("🎭 Kayfiyat", [
                "Energetik & Motivatsion",
                "Informatsion & Ta'limiy",
                "Quvnoq & Hazilkash",
                "Hissiy & Samimiy",
                "Professional & Ekspert",
            ])

        if st.button("✨ Ssenariy & Raskadirofka Yaratish", type="primary", use_container_width=True):
            if not api_key:
                st.error("❌ Sidebar'dan Anthropic API Key kiriting")
            elif not topic.strip():
                st.error("❌ Mavzu kiriting")
            else:
                with st.spinner("🎬 Claude ssenariy va raskadirofka yaratmoqda..."):
                    try:
                        client = anthropic.Anthropic(api_key=api_key)
                        prompt = f"""Sen professional ssenariy yozuvchi (ssenarist) va raskadirofkachiSan.
Sen @{prof['username']} influencer'ining uslubini chuqur o'rgandingsan.

━━━━━━━━━━━━━━━━━━━━━━━━━
INFLUENCER USLUB TAHLILI:
━━━━━━━━━━━━━━━━━━━━━━━━━
{prof['analysis']}

━━━━━━━━━━━━━━━━━━━━━━━━━
VAZIFA PARAMETRLARI:
━━━━━━━━━━━━━━━━━━━━━━━━━
Mavzu: {topic}
Kontent turi: {reel_type}
Chiqish tili: {out_lang}
Kayfiyat: {mood}

Ikkita qism yarat:

╔══════════════════════════════════════════════╗
║  📝 QISM 1: SSENARIY (Script)               ║
╚══════════════════════════════════════════════╝

@{prof['username']} ning AYNAN O'Z OVOZI VA USLUBIDA to'liq ssenariy yoz.
Uning xarakterli iboralari, toni, hazili va o'ziga xos ifodalarini ishlatsin.

Tuzilma:

**🎣 HOOK (0–3 soniya):**
[Ko'ruvchini darhol ushlaydigan birinchi gap yoki harakat]

**🚀 KIRISH (3–8 soniya):**
[O'zini tanishtirish yoki mavzuga kirish — influencer uslubida]

**📖 ASOSIY KONTENT:**
[Har bir bosqich/nuqta alohida ko'rsatilsin]
[Influencer'ning hikoyalashtirish uslubida]

**🎯 XULOSA:**
[Qisqa va uning uslubida yakunlash]

**📣 CALL TO ACTION:**
[Kuzatuvchilarni nima qilishga undash — influencer'ning o'z usulida]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

╔══════════════════════════════════════════════╗
║  🎬 QISM 2: RASKADIROFKA (Storyboard)       ║
╚══════════════════════════════════════════════╝

@{prof['username']} ning VIZUAL ESTETIKASI, rang palitasi va montaj uslubida
har bir kadr uchun batafsil raskadirofka:

KADR 1:
⏱️ Vaqt: [0-3 soniya]
📹 Kadr turi: [Misol: Extreme close-up / Wide shot / Medium shot]
🎨 Vizual: [Ko'ruvchi ekranda nima ko'radi — ranglar, fon, harakat, yoritish]
✍️ Matn overlay: [Ekranda qanday matn yoki grafika chiqadi]
🎵 Audio: [Musiqa janri / tempo / ovoz balandligi]
🔄 O'tish: [Keyingi kadrga qanday o'tiladi — cut / fade / zoom / whip]

---

[Har bir kadr shu formatda, mavzuga mos barcha kadrlar uchun davom etsin]

ESLATMA: Raskadirofka @{prof['username']} ning vizual "imzosi"ni to'liq aks ettirsin —
uning rang palitasi, montaj ritmi va estetik uslubi sezilsin."""

                        resp = client.messages.create(
                            model="claude-opus-4-6",
                            max_tokens=5000,
                            messages=[{"role": "user", "content": prompt}],
                        )
                        output = resp.content[0].text

                        st.markdown("---")

                        # Split into two parts for display
                        if "QISM 2" in output or "RASKADIROFKA" in output:
                            split_markers = ["QISM 2", "╔══", "🎬 QISM 2", "━━━\n\n╔"]
                            split_idx = len(output)
                            for marker in split_markers:
                                idx = output.find(marker)
                                if idx != -1 and idx < split_idx:
                                    split_idx = idx

                            script_part = output[:split_idx].strip()
                            board_part  = output[split_idx:].strip()
                        else:
                            script_part = output
                            board_part  = ""

                        col_s, col_b = st.columns(2)
                        with col_s:
                            st.markdown("#### 📝 Ssenariy")
                            st.markdown(script_part)
                        with col_b:
                            st.markdown("#### 🎬 Raskadirofka")
                            st.markdown(board_part if board_part else output)

                        st.markdown("---")
                        dl_text = (
                            f"INFLUENCER: @{prof['username']}\n"
                            f"MAVZU: {topic}\n"
                            f"KONTENT TURI: {reel_type}\n"
                            f"{'='*50}\n\n"
                            + output
                        )
                        safe_topic = "".join(c for c in topic[:40] if c.isalnum() or c in " _-").strip()
                        st.download_button(
                            "⬇️ Ssenariy & Raskadirofkani yuklab olish (TXT)",
                            data=dl_text,
                            file_name=f"{prof['username']}_{safe_topic}.txt",
                            mime="text/plain",
                        )

                    except anthropic.AuthenticationError:
                        st.error("❌ API key noto'g'ri. Iltimos tekshiring.")
                    except Exception as e:
                        st.error(f"❌ Xatolik: {e}")
