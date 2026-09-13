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

html, body, [class*="css"] {
    font-family: 'Montserrat', Arial, sans-serif;
}

.stApp {
    background-color: #e9e9e9;
}

.block-container {
    max-width: 900px;
    padding-top: 45px;
    padding-bottom: 50px;
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


/* Заголовок */

.eyebrow {
    font-size: 10px;
    letter-spacing: 3px;
    color: #777;
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
}

.title-red {
    color: #d71920;
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
    color: #777;
    text-transform: uppercase;
    margin-bottom: 32px;
}


/* Строка */

.row {
    display: grid;
    grid-template-columns: 85px 1fr 100px;
    align-items: center;

    min-height: 76px;

    margin-bottom: 7px;

    padding: 8px 20px 8px 8px;

    background: #f7f7f7;

    border: 1px solid #d4d4d4;

    border-left: 5px solid transparent;

    transition: 0.2s;
}

.row:hover {
    background: white;
    transform: translateX(4px);
}

.row-first {
    border-left-color: #c49a00;
}

.row-second {
    border-left-color: #888888;
}

.row-third {
    border-left-color: #925528;
}


/* Место */

.rank-area {
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
}

.rank {
    font-size: 20px;
    color: #777;
}

.cup {
    position: absolute;
    left: 3px;
    top: 0;

    font-size: 18px;
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


/* Имя */

.name {
    font-size: 18px;
    font-weight: 700;
}

.bar {
    height: 3px;
    width: 90%;
    background: #d5d5d5;
    margin-top: 9px;
}

.bar-inner {
    height: 3px;
    background: #d71920;
}


/* Рейтинг */

.score {
    text-align: right;
    font-size: 29px;
    font-weight: 800;
}


/* Footer */

.footer {
    display: flex;
    justify-content: space-between;

    margin-top: 20px;

    color: #777;

    font-size: 9px;

    letter-spacing: 1.5px;

    text-transform: uppercase;
}


/* Mobile */

@media (max-width: 600px) {

    .title {
        font-size: 50px;
    }

    .row {
        grid-template-columns: 60px 1fr 75px;
        min-height: 67px;
        padding-right: 12px;
    }

    .name {
        font-size: 13px;
    }

    .score {
        font-size: 21px;
    }

    .rank {
        font-size: 16px;
    }

    .cup {
        font-size: 15px;
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

with st.sidebar:

    st.markdown("### LeaderBoard")

    page = st.radio(
        "Раздел",
        [
            "🏆 LeaderBord",
            "⚙️ Администрирование"
        ]
    )


# =====================================================
# LEADERBOARD
# =====================================================

if page == "🏆 LeaderBord":

    employees = load_data()

    employees = sorted(
        employees,
        key=lambda x: x["rating"],
        reverse=True
    )


    # Заголовок

    st.markdown("""
    <div class="eyebrow">
        <span class="live-dot"></span>
        LIVE RANKING
    </div>

    <div class="title">
        Leader<span class="title-red">Bord</span>
    </div>

    <div class="red-line"></div>

    <div class="subtitle">
        Рейтинг участников конкурса
    </div>
    """, unsafe_allow_html=True)


    # Таблица

    for index, employee in enumerate(employees):

        place = index + 1

        rating = float(employee["rating"])

        # Максимальная длина полосы

        width = min(
            rating * 1.55,
            100
        )


        # Класс топ-3

        row_class = "row"

        if place == 1:
            row_class += " row-first"

        elif place == 2:
            row_class += " row-second"

        elif place == 3:
            row_class += " row-third"


        # Кубок

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
        <div class="rank">
            {place:02d}
        </div>
    </div>

    <div>
        <div class="name">
            {employee["name"]}
        </div>

        <div class="bar">
            <div
                class="bar-inner"
                style="width:{width}%">
            </div>
        </div>
    </div>

    <div class="score">
        {rating:.1f}
    </div>
</div>
"""

        st.markdown(row_html, unsafe_allow_html=True)


    st.markdown(
        """
        <div class="footer">

            <span>
                АВТООБНОВЛЕНИЕ
            </span>

            <span>
                LIVE
            </span>

        </div>
        """,
        unsafe_allow_html=True
    )


    # Автообновление

    time.sleep(3)

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
