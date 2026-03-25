import streamlit as st
import pymssql

st.set_page_config(page_title="TriSys", page_icon="🏢", layout="wide")

# ── DB ────────────────────────────────────────────────────────────────────────
def get_conn():
    return pymssql.connect(
        server=st.secrets["DB_SERVER"],
        port=int(st.secrets["DB_PORT"]),
        database=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        charset="UTF-8",
    )

# ── Session Init ──────────────────────────────────────────────────────────────
for k, v in [("logged_in", False), ("user", None), ("page", "login")]:
    if k not in st.session_state:
        st.session_state[k] = v

# ── Dialogs ───────────────────────────────────────────────────────────────────
@st.dialog("客戶資料")
def cust_dialog(row=None):
    is_edit = row is not None
    code   = st.text_input("客戶代碼", value=row["cust_code"] if is_edit else "", disabled=is_edit)
    name   = st.text_input("客戶名稱", value=row["cust_name"] if is_edit else "")
    remark = st.text_input("備註說明", value=row.get("remark") or "" if is_edit else "")
    c1, c2 = st.columns(2)
    if c1.button("取消", use_container_width=True): st.rerun()
    if c2.button("儲存", use_container_width=True, type="primary"):
        if not code.strip() or not name.strip():
            st.error("代碼與名稱為必填"); return
        try:
            conn = get_conn(); cur = conn.cursor()
            if is_edit:
                cur.execute("UPDATE cust SET cust_name=%s,remark=%s WHERE cust_code=%s", (name, remark, code))
            else:
                cur.execute("INSERT INTO cust(cust_code,cust_name,remark) VALUES(%s,%s,%s)", (code, name, remark))
            conn.commit(); conn.close()
            st.session_state.pop("cust_edit", None)
            st.rerun()
        except Exception as e:
            st.error(str(e))

@st.dialog("廠商資料")
def fact_dialog(row=None):
    is_edit = row is not None
    code   = st.text_input("廠商代碼", value=row["fact_code"] if is_edit else "", disabled=is_edit)
    name   = st.text_input("廠商名稱", value=row["fact_name"] if is_edit else "")
    remark = st.text_input("備註說明", value=row.get("remark") or "" if is_edit else "")
    c1, c2 = st.columns(2)
    if c1.button("取消", use_container_width=True): st.rerun()
    if c2.button("儲存", use_container_width=True, type="primary"):
        if not code.strip() or not name.strip():
            st.error("代碼與名稱為必填"); return
        try:
            conn = get_conn(); cur = conn.cursor()
            if is_edit:
                cur.execute("UPDATE fact SET fact_name=%s,remark=%s WHERE fact_code=%s", (name, remark, code))
            else:
                cur.execute("INSERT INTO fact(fact_code,fact_name,remark) VALUES(%s,%s,%s)", (code, name, remark))
            conn.commit(); conn.close()
            st.rerun()
        except Exception as e:
            st.error(str(e))

@st.dialog("商品資料")
def item_dialog(row=None, fact_options=None):
    is_edit = row is not None
    code = st.text_input("商品代碼", value=row["item_code"] if is_edit else "", disabled=is_edit)
    name = st.text_input("商品名稱", value=row["item_name"] if is_edit else "")
    fact_codes = [f[0] for f in (fact_options or [])]
    fact_labels = [f"{f[0]} {f[1]}" for f in (fact_options or [])]
    default_idx = fact_codes.index(row["fact_code"]) if is_edit and row.get("fact_code") in fact_codes else 0
    sel = st.selectbox("廠商", options=fact_labels, index=default_idx) if fact_labels else st.text_input("廠商代碼", value=row.get("fact_code","") if is_edit else "")
    fact_code = fact_codes[fact_labels.index(sel)] if fact_labels else sel
    c1, c2 = st.columns(2)
    if c1.button("取消", use_container_width=True): st.rerun()
    if c2.button("儲存", use_container_width=True, type="primary"):
        if not code.strip() or not name.strip():
            st.error("代碼與名稱為必填"); return
        try:
            conn = get_conn(); cur = conn.cursor()
            if is_edit:
                cur.execute("UPDATE item SET item_name=%s,fact_code=%s WHERE item_code=%s", (name, fact_code, code))
            else:
                cur.execute("INSERT INTO item(item_code,item_name,fact_code) VALUES(%s,%s,%s)", (code, name, fact_code))
            conn.commit(); conn.close()
            st.rerun()
        except Exception as e:
            st.error(str(e))

@st.dialog("用戶資料")
def user_dialog(row=None):
    is_edit = row is not None
    userid   = st.text_input("用戶帳號", value=row["userid"] if is_edit else "", disabled=is_edit)
    username = st.text_input("用戶名稱", value=row.get("username","") if is_edit else "")
    pwd      = st.text_input("密碼", value=row.get("pwd","") if is_edit else "", type="password")
    c1, c2 = st.columns(2)
    if c1.button("取消", use_container_width=True): st.rerun()
    if c2.button("儲存", use_container_width=True, type="primary"):
        if not userid.strip() or not username.strip() or not pwd.strip():
            st.error("帳號、名稱、密碼為必填"); return
        try:
            conn = get_conn(); cur = conn.cursor()
            if is_edit:
                cur.execute("UPDATE [user] SET username=%s,pwd=%s WHERE userid=%s", (username, pwd, userid))
            else:
                cur.execute("INSERT INTO [user](userid,username,pwd) VALUES(%s,%s,%s)", (userid, username, pwd))
            conn.commit(); conn.close()
            st.rerun()
        except Exception as e:
            st.error(str(e))

# ── Pages ─────────────────────────────────────────────────────────────────────
def page_login():
    st.markdown("<h1 style='text-align:center;margin-top:80px'>🏢 TriSys</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:gray'>資料維護系統</p>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1, 1])
    with col:
        userid = st.text_input("帳號")
        pwd    = st.text_input("密碼", type="password")
        if st.button("登入", use_container_width=True, type="primary"):
            if not userid or not pwd:
                st.error("請輸入帳號與密碼")
            else:
                try:
                    conn = get_conn()
                    cur  = conn.cursor(as_dict=True)
                    cur.execute("SELECT userid,username FROM [user] WHERE userid=%s AND pwd=%s", (userid, pwd))
                    row = cur.fetchone(); conn.close()
                    if row:
                        st.session_state.logged_in = True
                        st.session_state.user = row
                        st.session_state.page = "main"
                        st.rerun()
                    else:
                        st.error("帳號或密碼錯誤")
                except Exception as e:
                    st.error(f"連線錯誤：{e}")

def page_main():
    c1, c2 = st.columns([9, 1])
    c1.title(f"TriSys　歡迎，{st.session_state.user.get('username') or st.session_state.user.get('userid')}")
    if c2.button("登出"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()
    st.divider()
    cols = st.columns(4)
    for col, (label, pg) in zip(cols, [("🏢 客戶資料", "cust"), ("🏭 廠商資料", "fact"), ("📦 商品資料", "item"), ("👤 用戶資料", "user")]):
        if col.button(label, use_container_width=True):
            st.session_state.page = pg
            st.rerun()

def _header(title):
    c1, c2 = st.columns([1, 9])
    if c1.button("← 返回"):
        st.session_state.page = "main"; st.rerun()
    c2.subheader(title)

def page_cust():
    _header("客戶資料維護")
    try:
        conn = get_conn(); cur = conn.cursor(as_dict=True)
        cur.execute("SELECT cust_code,cust_name,remark FROM cust ORDER BY cust_code")
        rows = cur.fetchall(); conn.close()
    except Exception as e:
        st.error(str(e)); return

    if st.button("＋ 新增客戶", type="primary"): cust_dialog()

    if rows:
        import pandas as pd
        df = pd.DataFrame(rows)
        st.dataframe(df.rename(columns={"cust_code":"客戶代碼","cust_name":"客戶名稱","remark":"備註"}), use_container_width=True, hide_index=True)
        codes = [r["cust_code"] for r in rows]
        sel = st.selectbox("選擇要操作的客戶代碼", options=[""] + codes)
        if sel:
            row = next(r for r in rows if r["cust_code"] == sel)
            c1, c2 = st.columns(2)
            if c1.button("修改", use_container_width=True): cust_dialog(row)
            if c2.button("刪除", use_container_width=True, type="secondary"):
                if st.session_state.get("cust_del_confirm") == sel:
                    try:
                        conn = get_conn(); cur = conn.cursor()
                        cur.execute("DELETE FROM cust WHERE cust_code=%s", (sel,))
                        conn.commit(); conn.close()
                        st.session_state.pop("cust_del_confirm", None)
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
                else:
                    st.session_state["cust_del_confirm"] = sel
                    st.warning(f"再按一次刪除確認刪除 {sel}")
    else:
        st.info("尚無資料")

def page_fact():
    _header("廠商資料維護")
    try:
        conn = get_conn(); cur = conn.cursor(as_dict=True)
        cur.execute("SELECT fact_code,fact_name,remark FROM fact ORDER BY fact_code")
        rows = cur.fetchall(); conn.close()
    except Exception as e:
        st.error(str(e)); return

    if st.button("＋ 新增廠商", type="primary"): fact_dialog()

    if rows:
        import pandas as pd
        df = pd.DataFrame(rows)
        st.dataframe(df.rename(columns={"fact_code":"廠商代碼","fact_name":"廠商名稱","remark":"備註"}), use_container_width=True, hide_index=True)
        codes = [r["fact_code"] for r in rows]
        sel = st.selectbox("選擇要操作的廠商代碼", options=[""] + codes)
        if sel:
            row = next(r for r in rows if r["fact_code"] == sel)
            c1, c2 = st.columns(2)
            if c1.button("修改", use_container_width=True): fact_dialog(row)
            if c2.button("刪除", use_container_width=True, type="secondary"):
                if st.session_state.get("fact_del_confirm") == sel:
                    try:
                        conn = get_conn(); cur = conn.cursor()
                        cur.execute("DELETE FROM fact WHERE fact_code=%s", (sel,))
                        conn.commit(); conn.close()
                        st.session_state.pop("fact_del_confirm", None)
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
                else:
                    st.session_state["fact_del_confirm"] = sel
                    st.warning(f"再按一次刪除確認刪除 {sel}")
    else:
        st.info("尚無資料")

def page_item():
    _header("商品資料維護")
    try:
        conn = get_conn(); cur = conn.cursor(as_dict=True)
        cur.execute("SELECT i.item_code,i.item_name,i.fact_code,f.fact_name FROM item i LEFT JOIN fact f ON i.fact_code=f.fact_code ORDER BY i.item_code")
        rows = cur.fetchall()
        cur.execute("SELECT fact_code,fact_name FROM fact ORDER BY fact_code")
        facts = [(r["fact_code"], r["fact_name"]) for r in cur.fetchall()]
        conn.close()
    except Exception as e:
        st.error(str(e)); return

    if st.button("＋ 新增商品", type="primary"): item_dialog(fact_options=facts)

    if rows:
        import pandas as pd
        df = pd.DataFrame(rows)
        st.dataframe(df.rename(columns={"item_code":"商品代碼","item_name":"商品名稱","fact_code":"廠商代碼","fact_name":"廠商名稱"}), use_container_width=True, hide_index=True)
        codes = [r["item_code"] for r in rows]
        sel = st.selectbox("選擇要操作的商品代碼", options=[""] + codes)
        if sel:
            row = next(r for r in rows if r["item_code"] == sel)
            c1, c2 = st.columns(2)
            if c1.button("修改", use_container_width=True): item_dialog(row, facts)
            if c2.button("刪除", use_container_width=True, type="secondary"):
                if st.session_state.get("item_del_confirm") == sel:
                    try:
                        conn = get_conn(); cur = conn.cursor()
                        cur.execute("DELETE FROM item WHERE item_code=%s", (sel,))
                        conn.commit(); conn.close()
                        st.session_state.pop("item_del_confirm", None)
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
                else:
                    st.session_state["item_del_confirm"] = sel
                    st.warning(f"再按一次刪除確認刪除 {sel}")
    else:
        st.info("尚無資料")

def page_user():
    _header("用戶資料維護")
    try:
        conn = get_conn(); cur = conn.cursor(as_dict=True)
        cur.execute("SELECT userid,username,pwd FROM [user] ORDER BY userid")
        rows = cur.fetchall(); conn.close()
    except Exception as e:
        st.error(str(e)); return

    if st.button("＋ 新增用戶", type="primary"): user_dialog()

    if rows:
        import pandas as pd
        df = pd.DataFrame(rows)
        st.dataframe(df.rename(columns={"userid":"帳號","username":"名稱","pwd":"密碼"}), use_container_width=True, hide_index=True)
        ids = [r["userid"] for r in rows]
        sel = st.selectbox("選擇要操作的帳號", options=[""] + ids)
        if sel:
            row = next(r for r in rows if r["userid"] == sel)
            c1, c2 = st.columns(2)
            if c1.button("修改", use_container_width=True): user_dialog(row)
            if c2.button("刪除", use_container_width=True, type="secondary"):
                if st.session_state.get("user_del_confirm") == sel:
                    try:
                        conn = get_conn(); cur = conn.cursor()
                        cur.execute("DELETE FROM [user] WHERE userid=%s", (sel,))
                        conn.commit(); conn.close()
                        st.session_state.pop("user_del_confirm", None)
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
                else:
                    st.session_state["user_del_confirm"] = sel
                    st.warning(f"再按一次刪除確認刪除 {sel}")
    else:
        st.info("尚無資料")

# ── Router ────────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    page_login()
else:
    pg = st.session_state.page
    if   pg == "main": page_main()
    elif pg == "cust": page_cust()
    elif pg == "fact": page_fact()
    elif pg == "item": page_item()
    elif pg == "user": page_user()
