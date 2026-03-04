import requests
import streamlit as st

# =============================
# CONFIG
# =============================
API_BASE = "https://movie-rec-466x.onrender.com"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# =============================
# MODERN UI STYLE
# =============================
st.markdown("""
<style>

.block-container{
padding-top:1rem;
max-width:1500px;
}

h1,h2,h3{
font-weight:700;
}

.small-muted{
color:#9ca3af;
font-size:0.9rem;
}

.movie-title{
font-size:0.9rem;
text-align:center;
height:2.4rem;
overflow:hidden;
}

.poster-card{
border-radius:16px;
overflow:hidden;
transition:all .25s ease;
}

.poster-card:hover{
transform:scale(1.05);
}

.card{
background:rgba(255,255,255,0.7);
border-radius:16px;
padding:20px;
box-shadow:0 6px 18px rgba(0,0,0,0.06);
}

.sidebar-title{
font-size:1.2rem;
font-weight:600;
}

</style>
""", unsafe_allow_html=True)


# =============================
# STATE
# =============================
if "view" not in st.session_state:
    st.session_state.view = "home"

if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None


qp_view = st.query_params.get("view")
qp_id = st.query_params.get("id")

if qp_view in ("home","details"):
    st.session_state.view = qp_view

if qp_id:
    try:
        st.session_state.selected_tmdb_id = int(qp_id)
        st.session_state.view = "details"
    except:
        pass


def goto_home():
    st.session_state.view="home"
    st.query_params["view"]="home"
    if "id" in st.query_params:
        del st.query_params["id"]
    st.rerun()


def goto_details(tmdb_id:int):
    st.session_state.view="details"
    st.session_state.selected_tmdb_id=int(tmdb_id)
    st.query_params["view"]="details"
    st.query_params["id"]=str(int(tmdb_id))
    st.rerun()


# =============================
# API
# =============================
@st.cache_data(ttl=30)
def api_get_json(path:str, params:dict|None=None):

    try:
        r=requests.get(f"{API_BASE}{path}",params=params,timeout=25)

        if r.status_code>=400:
            return None,f"HTTP {r.status_code}: {r.text[:300]}"

        return r.json(),None

    except Exception as e:
        return None,f"Request failed: {e}"


# =============================
# GRID
# =============================
def poster_grid(cards, cols=6, key_prefix="grid"):

    if not cards:
        st.info("No movies to show")
        return

    rows=(len(cards)+cols-1)//cols
    idx=0

    for r in range(rows):

        colset=st.columns(cols)

        for c in range(cols):

            if idx>=len(cards):
                break

            m=cards[idx]
            idx+=1

            tmdb_id=m.get("tmdb_id")
            title=m.get("title","Untitled")
            poster=m.get("poster_url")

            with colset[c]:

                if poster:
                    st.image(poster,use_column_width=True)

                else:
                    st.write("🖼️ No Poster")

                if st.button("Open",key=f"{key_prefix}_{r}_{c}_{idx}_{tmdb_id}"):

                    if tmdb_id:
                        goto_details(tmdb_id)

                st.markdown(
                    f"<div class='movie-title'>{title}</div>",
                    unsafe_allow_html=True
                )


# =============================
# TFIDF helper
# =============================
def to_cards_from_tfidf_items(tfidf_items):

    cards=[]

    for x in tfidf_items or []:

        tmdb=x.get("tmdb") or {}

        if tmdb.get("tmdb_id"):

            cards.append({
                "tmdb_id":tmdb["tmdb_id"],
                "title":tmdb.get("title") or x.get("title"),
                "poster_url":tmdb.get("poster_url")
            })

    return cards


# =============================
# TMDB SEARCH PARSER
# =============================
def parse_tmdb_search_to_cards(data,keyword:str,limit:int=24):

    keyword_l=keyword.strip().lower()

    if isinstance(data,dict) and "results" in data:

        raw=data.get("results") or []
        raw_items=[]

        for m in raw:

            title=(m.get("title") or "").strip()
            tmdb_id=m.get("id")
            poster=m.get("poster_path")

            if not title or not tmdb_id:
                continue

            raw_items.append({
                "tmdb_id":int(tmdb_id),
                "title":title,
                "poster_url":f"{TMDB_IMG}{poster}" if poster else None,
                "release_date":m.get("release_date","")
            })

    elif isinstance(data,list):

        raw_items=[]

        for m in data:

            tmdb_id=m.get("tmdb_id") or m.get("id")
            title=(m.get("title") or "").strip()

            if not title or not tmdb_id:
                continue

            raw_items.append({
                "tmdb_id":int(tmdb_id),
                "title":title,
                "poster_url":m.get("poster_url"),
                "release_date":m.get("release_date","")
            })

    else:
        return [],[]


    matched=[x for x in raw_items if keyword_l in x["title"].lower()]
    final_list=matched if matched else raw_items

    suggestions=[]

    for x in final_list[:10]:

        year=(x.get("release_date") or "")[:4]
        label=f"{x['title']} ({year})" if year else x["title"]

        suggestions.append((label,x["tmdb_id"]))


    cards=[{
        "tmdb_id":x["tmdb_id"],
        "title":x["title"],
        "poster_url":x["poster_url"]
    } for x in final_list[:limit]]

    return suggestions,cards


# =============================
# SIDEBAR
# =============================
with st.sidebar:

    st.markdown("### 🎬 Navigation")

    if st.button("🏠 Home"):
        goto_home()

    st.divider()

    home_category=st.selectbox(
        "Home Feed",
        ["trending","popular","top_rated","now_playing","upcoming"],
        index=0
    )

    grid_cols=st.slider("Grid columns",4,8,6)


# =============================
# HEADER (UPDATED)
# =============================
st.markdown("""
<div style="margin-bottom:10px">

<h1 style="font-size:2.5rem;margin-bottom:0">🎬 Movona</h1>

<p class="small-muted" style="margin-top:4px">
AI Movie Recommendation System
</p>

<p class="small-muted" style="margin-top:-6px">
Discover movies you'll love
</p>

<p style="font-size:0.8rem;color:#9ca3af;margin-top:4px">
Built by <b>Ramandeep Singh</b>
</p>

</div>
""", unsafe_allow_html=True)

st.markdown(
"""
<hr style="border: none; height: 2px;
background: linear-gradient(to right,#6366f1,#ec4899,#f59e0b);
margin-top:10px;margin-bottom:20px;">
""",
unsafe_allow_html=True)


st.caption(
"Search → Select movie → View details → Get recommendations"
)

# ==========================================================
# HOME
# ==========================================================
if st.session_state.view=="home":

    typed=st.text_input(
        "Search movie",
        placeholder="Try: avatar, batman, avengers..."
    )

    st.divider()

    if typed.strip():

        if len(typed.strip())<2:
            st.caption("Type at least 2 characters")

        else:

            data,err=api_get_json(
                "/tmdb/search",
                params={"query":typed.strip()}
            )

            if err or data is None:
                st.error(err)

            else:

                suggestions,cards=parse_tmdb_search_to_cards(
                    data,typed.strip(),limit=24
                )

                if suggestions:

                    labels=["-- Select movie --"]+[s[0] for s in suggestions]
                    selected=st.selectbox("Suggestions",labels,index=0)

                    if selected!="-- Select movie --":

                        label_to_id={s[0]:s[1] for s in suggestions}
                        goto_details(label_to_id[selected])

                st.markdown("### Results")
                poster_grid(cards,cols=grid_cols,key_prefix="search")

        st.stop()


    st.markdown(f"### 🏠 {home_category.replace('_',' ').title()}")

    home_cards,err=api_get_json(
        "/home",
        params={"category":home_category,"limit":24}
    )

    if err or not home_cards:
        st.error(err)
        st.stop()

    poster_grid(home_cards,cols=grid_cols,key_prefix="home")


# ==========================================================
# DETAILS
# ==========================================================
elif st.session_state.view=="details":

    tmdb_id=st.session_state.selected_tmdb_id

    if not tmdb_id:
        st.warning("No movie selected")
        if st.button("← Back"):
            goto_home()
        st.stop()

    data,err=api_get_json(f"/movie/id/{tmdb_id}")

    if err or not data:
        st.error(err)
        st.stop()


    left,right=st.columns([1,2.2])

    with left:

        if data.get("poster_url"):
            st.image(data["poster_url"],use_column_width=True)

    with right:

        st.markdown(f"## {data.get('title','')}")

        release=data.get("release_date") or "-"
        genres=", ".join([g["name"] for g in data.get("genres",[])]) or "-"

        st.markdown(f"Release: {release}")
        st.markdown(f"Genres: {genres}")

        st.divider()

        st.write(data.get("overview") or "No overview")


    if data.get("backdrop_url"):

        st.markdown("### Backdrop")
        st.image(data["backdrop_url"],use_column_width=True)


    st.divider()

    st.markdown("### Recommendations")


    title=(data.get("title") or "").strip()

    bundle,err2=api_get_json(
        "/movie/search",
        params={"query":title,"tfidf_top_n":12,"genre_limit":12}
    )

    if not err2 and bundle:

        st.markdown("#### Similar Movies")
        poster_grid(
            to_cards_from_tfidf_items(bundle.get("tfidf_recommendations")),
            cols=grid_cols,
            key_prefix="tfidf"
        )

        st.markdown("#### More Like This")
        poster_grid(
            bundle.get("genre_recommendations",[]),
            cols=grid_cols,
            key_prefix="genre"
        )