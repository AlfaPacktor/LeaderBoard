import streamlit as st
import json
import os
import time
import html

# =====================================================
# НАСТРОЙКИ
# =====================================================

DATA_FILE = "data/employees.json"

st.set_page_config(
    page_title="LeaderBoard",
    page_icon="🏆",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# =====================================================
# CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&display=swap');

/* =====================================================
   ОСНОВНЫЕ НАСТРОЙКИ
   ===================================================== */

html, body, [class*="css"] {
    font-family: 'Montserrat', Arial, sans-serif;
    color: #111111;
}

.stApp {
    background-color: #e9e9e9;
}

/* Убираем стандартное меню */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* Основной контейнер */

.block-container {
    max-width: 900px;
    padding-top: 45px;
    padding-bottom: 40px;
}


/* =====================================================
   ЗАГОЛОВОК
   ===================================================== */

.eyebrow {
    font-size: 10px;
    letter-spacing: 3px;
    color: #777777;
    margin-bottom: 12px;
}

.live-dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    background: #d71920;
    border-radius: 50%;
    margin-right: 7px;
}

.title {
    font-size: 72px;
    font-weight: 800;
    letter-spacing: -5px;
    line-height: 0.9;
    margin-bottom: 15px;
    color: #111111;
}

/* Только Board красный */

.title-red {
    color: #d71920 !important;
}

.red-line {
    width: 58px;
    height: 6px;
    background: #d71920;
    margin-bottom: 14px;
}

.subtitle {
    font-size: 12px;
    letter-spacing: 2px;
    color: #777777;
    text-transform: uppercase;
    margin-bottom: 24px;
}


/* =====================================================
   СТРОКА УЧАСТНИКА
   ===================================================== */

.row {
    display: grid;
    grid-template-columns: 75px 1fr 90px;

    align-items: center;

    min-height: 60px;

    margin-bottom: 0px;

    padding: 6px 16px 6px 6px;

    background: #f7f7f7;

    border: 1px solid #d4d4d4;

    border-left: 5px solid transparent;

    transition: 0.2s;
}

.row:hover {
    background: #ffffff;
    transform: translateX(3px);
}


/* Первое место */

.row-first {
    border-left-color: #c49a00;
}

/* Второе место */

.row-second {
    border-left-color: #888888;
}

/* Третье место */

.row-third {
    border-left-color: #925528;
}


/* =====================================================
   МЕСТО
   ===================================================== */

.rank-area {
    position: relative;

    display: flex;

    justify-content: center;

    align-items: center;
}

.rank {
    font-size: 18px;
    color: #777777;
}

.cup {
    position: absolute;

    left: 1px;
    top: 0;

    font-size: 17px;
}

.gold {
    color: #b88a00;
}

.silver {
    color: #777777;
}

.bronze {
    color: #925528;
}


/* =====================================================
   ИМЯ УЧАСТНИКА
   ===================================================== */

.name {
    font-size: 16px;
    font-weight: 700;
    color: #111111;
}


/* =====================================================
   ПОЛОСА РЕЙТИНГА
   ===================================================== */

.bar {
    height: 3px;

    width: 90%;

    background: #d5d5d5;

    margin-top: 6px;
}

.bar-inner {
    height: 3px;

    background: #d71920;
}


/* =====================================================
   РЕЙТИНГ
   ===================================================== */

.score {
    text-align: right;

    font-size: 26px;

    font-weight: 800;

    color: #111111;
}


/* =====================================================
   FOOTER
   ===================================================== */

.footer {
    display: flex;

    justify-content: space-between;

    margin-top: 15px;

    color: #777777;

    font-size: 9px;

    letter-spacing: 1.5px;

    text-transform: uppercase;
}


/* =====================================================
   МОБИЛЬНАЯ ВЕРСИЯ
   ===================================================== */

@media (max-width: 600px) {

    .block-container {
        padding-top: 25px;
        padding-left: 12px;
        padding-right: 12px;
        padding-bottom: 25px;
    }

    .title {
        font-size: 48px;
        letter-spacing: -3px;
    }

    .subtitle {
        margin-bottom: 18px;
    }

    .row {
        grid-template-columns: 48px 1fr 65px;

        min-height: 52px;

        margin-bottom: 3px;

        padding: 5px 10px 5px 4px;
    }

    .name {
        font-size: 12px;
    }

    .score {
        font-size: 19px;
    }

    .rank {
        font-size: 15px;
    }

    .cup {
        font-size: 14px;
    }

    .bar {
        margin-top: 4px;
        width: 95%;
    }
}

</style>
""", unsafe_allow_html=True)
# =====================================================
# ЗАГРУЗКА ДАННЫХ
# =====================================================

def load_data():

    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


# =====================================================
# СОХРАНЕНИЕ ДАННЫХ
# =====================================================

def save_data(data):

    os.makedirs("data", exist_ok=True)

    with open(DATA_FILE, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4
        )


# =====================================================
# SIDEBAR
# =====================================================

page = st.radio(
    "Раздел",
    [
        "LeaderBord",
        "Администрирование"
    ],
    horizontal=True
)

# =====================================================
# LEADERBOARD
# =====================================================

if page == "LeaderBord":

    employees = load_data()

    employees = sorted(
        employees,
        key=lambda x: x["rating"],
        reverse=True
    )

    st.markdown(
        """
        <div class="eyebrow">
            <span class="live-dot"></span>
            LIVE RANKING
        </div>

        <div class="title">
            Leader<span class="title-red">Board</span>
        </div>

        <div class="red-line"></div>

        <div class="subtitle">
            Рейтинг участников конкурса
        </div>
        """,
        unsafe_allow_html=True
    )

    for index, employee in enumerate(employees):

        place = index + 1
        rating = float(employee["rating"])

        width = min(rating * 1.55, 100)

        row_class = "row"

        if place == 1:
            row_class += " row-first"

        elif place == 2:
            row_class += " row-second"

        elif place == 3:
            row_class += " row-third"

        cup = ""

        if place == 1:
            cup = '<div class="cup gold">♛</div>'

        elif place == 2:
            cup = '<div class="cup silver">♛</div>'

        elif place == 3:
            cup = '<div class="cup bronze">♛</div>'

        row_html = f"""
<div class="{row_class}">
    <div class="rank-area">
        {cup}
        <div class="rank">{place:02d}</div>
    </div>

    <div>
        <div class="name">{html.escape(str(employee["name"]))}</div>

        <div class="bar">
            <div class="bar-inner" style="width:{width}%"></div>
        </div>
    </div>

    <div class="score">{rating:.1f}</div>
</div>
"""

        st.html(row_html)

    st.markdown(
        """
        <div class="footer">
            <span>АВТООБНОВЛЕНИЕ</span>
            <span>LIVE</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    time.sleep(5)
    st.rerun()


# =====================================================
# АДМИНИСТРИРОВАНИЕ
# =====================================================

else:

    st.title("⚙️ Администрирование")

    st.caption(
        "Измените показатели сотрудников и нажмите «Обновить»."
    )

    employees = load_data()

    employees = sorted(
        employees,
        key=lambda x: x["rating"],
        reverse=True
    )


    new_values = {}


    for employee in employees:

        new_values[employee["name"]] = st.number_input(
            employee["name"],
            value=float(employee["rating"]),
            step=0.1,
            format="%.1f",
            key=employee["name"]
        )


    st.divider()


    if st.button(
        "ОБНОВИТЬ РЕЙТИНГ",
        type="primary",
        use_container_width=True
    ):

        for employee in employees:

            employee["rating"] = float(
                new_values[employee["name"]]
            )


        save_data(employees)

        st.success(
            "Рейтинг обновлён!"
        )

        time.sleep(1)

        st.rerun()
