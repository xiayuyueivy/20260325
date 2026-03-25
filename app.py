import streamlit as st
import pymssql

st.set_page_config(page_title="TriSys", page_icon="🏢", layout="centered")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* 隱藏 Streamlit 預設 header/footer */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stAppViewContainer"] { background: #f0f2f5; }
[data-testid="stMain"] > div { padding-top: 1rem; }

/* 表格外框 */
.tbl-wrap {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 1px 6px rgba(0,0,0,0.08);
  overflow: hidden;
  margin-bottom: 12px;
}
/* 表頭 */
.tbl-head {
  display: flex;
  background: #1677ff;
  color: #fff;
  font-size: 13px;
  font-weight: 600;
  padding: 10px 0;
}
.tbl-head span { padding: 0 12px; flex: var(--flex, 1); }
/* 表格列 */
.tbl-row {
  display: flex;
  align-items: center;
  font-size: 13px;
  border-bottom: 1px solid #f0f0f0;
  padding: 6px 0;
  background: #fff;
}
.tbl-row:last-child { border-bottom: none; }
.tbl-row:hover { background: #fafafa; }
.tbl-cell { padding: 4px 12px; flex: var(--flex, 1); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.tbl-empty { text-align: center; color: #aaa; padding: 24px; font-size: 13px; }

/* 頁面標題列 */
.page-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
}
.page-title { flex: 1; font-size: 17px; font-weight: 700; color: #333; }

/* 按鈕微調 */
[data-testid="stButton"] button {
  font-size: 12px !important;
  padding: 4px 10px !important;
}
</style>
""", unsafe_allow_html=True)

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
        if not code.strip() or not name.strip(): st.error("代碼與名稱為必填"); return
        try:
            conn = get_conn(); cur = conn.cursor()
            if is_edit:
                cur.execute("UPDATE cust SET cust_name=%s,remark=%s WHERE cust_code=%s", (name, remark, code))
            else:
                cur.execute("INSERT INTO cust(cust_code,cust_name,remark) VALUES(%s,%s,%s)", (code, name, remark))
            conn.commit(); conn.close(); st.rerun()
        except Exception as e: st.error(str(e))

@st.dialog("確認刪除")
def cust_del_dialog(code):
    st.warning(f"確定刪除客戶「{code}」？此操作無法復原。")
    c1, c2 = st.columns(2)
    if c1.button("取消", use_container_width=True): st.rerun()
    if c2.button("確定刪除", use_container_width=True, type="primary"):
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("DELETE FROM cust WHERE cust_code=%s", (code,))
            conn.commit(); conn.close(); st.rerun()
        except Exception as e: st.error(str(e))

@st.dialog("廠商資料")
def fact_dialog(row=None):
    is_edit = row is not None
    code   = st.text_input("廠商代碼", value=row["fact_code"] if is_edit else "", disabled=is_edit)
    name   = st.text_input("廠商名稱", value=row["fact_name"] if is_edit else "")
    remark = st.text_input("備註說明", value=row.get("remark") or "" if is_edit else "")
    c1, c2 = st.columns(2)
    if c1.button("取消", use_container_width=True): st.rerun()
    if c2.button("儲存", use_container_width=True, type="primary"):
        if not code.strip() or not name.strip(): st.error("代碼與名稱為必填"); return
        try:
            conn = get_conn(); cur = conn.cursor()
            if is_edit:
                cur.execute("UPDATE fact SET fact_name=%s,remark=%s WHERE fact_code=%s", (name, remark, code))
            else:
                cur.execute("INSERT INTO fact(fact_code,fact_name,remark) VALUES(%s,%s,%s)", (code, name, remark))
            conn.commit(); conn.close(); st.rerun()
        except Exception as e: st.error(str(e))

@st.dialog("確認刪除")
def fact_del_dialog(code):
    st.warning(f"確定刪除廠商「{code}」？此操作無法復原。")
    c1, c2 = st.columns(2)
    if c1.button("取消", use_container_width=True): st.rerun()
    if c2.button("確定刪除", use_container_width=True, type="primary"):
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("DELETE FROM fact WHERE fact_code=%s", (code,))
            conn.commit(); conn.close(); st.rerun()
        except Exception as e: st.error(str(e))

@st.dialog("商品資料")
def item_dialog(row=None, fact_options=None):
    is_edit = row is not None
    code  = st.text_input("商品代碼", value=row["item_code"] if is_edit else "", disabled=is_edit)
    name  = st.text_input("商品名稱", value=row["item_name"] if is_edit else "")
    fact_codes  = [f[0] for f in (fact_options or [])]
    fact_labels = [f"{f[0]} - {f[1]}" for f in (fact_options or [])]
    default_idx = fact_codes.index(row["fact_code"]) if is_edit and row.get("fact_code") in fact_codes else 0
    if fact_labels:
        sel_label = st.selectbox("主供應商", options=["-- 請選擇 --"] + fact_labels,
                                 index=default_idx + 1 if is_edit else 0)
        fact_code = fact_codes[fact_labels.index(sel_label)] if sel_label != "-- 請選擇 --" else ""
    else:
        fact_code = st.text_input("主供應商代碼", value=row.get("fact_code", "") if is_edit else "")
    c1, c2 = st.columns(2)
    if c1.button("取消", use_container_width=True): st.rerun()
    if c2.button("儲存", use_container_width=True, type="primary"):
        if not code.strip() or not name.strip(): st.error("代碼與名稱為必填"); return
        try:
            conn = get_conn(); cur = conn.cursor()
            if is_edit:
                cur.execute("UPDATE item SET item_name=%s,fact_code=%s WHERE item_code=%s", (name, fact_code, code))
            else:
                cur.execute("INSERT INTO item(item_code,item_name,fact_code) VALUES(%s,%s,%s)", (code, name, fact_code))
            conn.commit(); conn.close(); st.rerun()
        except Exception as e: st.error(str(e))

@st.dialog("確認刪除")
def item_del_dialog(code):
    st.warning(f"確定刪除商品「{code}」？此操作無法復原。")
    c1, c2 = st.columns(2)
    if c1.button("取消", use_container_width=True): st.rerun()
    if c2.button("確定刪除", use_container_width=True, type="primary"):
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("DELETE FROM item WHERE item_code=%s", (code,))
            conn.commit(); conn.close(); st.rerun()
        except Exception as e: st.error(str(e))

@st.dialog("用戶資料")
def user_dialog(row=None):
    is_edit  = row is not None
    userid   = st.text_input("用戶代碼", value=row["userid"] if is_edit else "", disabled=is_edit)
    username = st.text_input("用戶名稱", value=row.get("username", "") if is_edit else "")
    pwd      = st.text_input("用戶密碼", value=row.get("pwd", "") if is_edit else "")
    c1, c2 = st.columns(2)
    if c1.button("取消", use_container_width=True): st.rerun()
    if c2.button("儲存", use_container_width=True, type="primary"):
        if not userid.strip() or not username.strip() or not pwd.strip():
            st.error("代碼、名稱與密碼為必填"); return
        try:
            conn = get_conn(); cur = conn.cursor()
            if is_edit:
                cur.execute("UPDATE [user] SET username=%s,pwd=%s WHERE userid=%s", (username, pwd, userid))
            else:
                cur.execute("INSERT INTO [user](userid,username,pwd) VALUES(%s,%s,%s)", (userid, username, pwd))
            conn.commit(); conn.close(); st.rerun()
        except Exception as e: st.error(str(e))

@st.dialog("確認刪除")
def user_del_dialog(uid):
    st.warning(f"確定刪除用戶「{uid}」？此操作無法復原。")
    c1, c2 = st.columns(2)
    if c1.button("取消", use_container_width=True): st.rerun()
    if c2.button("確定刪除", use_container_width=True, type="primary"):
        try:
            conn = get_conn(); cur = conn.cursor()
            cur.execute("DELETE FROM [user] WHERE userid=%s", (uid,))
            conn.commit(); conn.close(); st.rerun()
        except Exception as e: st.error(str(e))

# ── Dialog trigger helpers ────────────────────────────────────────────────────
def _trigger(ns):
    """Check session state and open the appropriate dialog."""
    edit = st.session_state.pop(f"{ns}_edit", None)
    dele = st.session_state.pop(f"{ns}_del",  None)
    facts = st.session_state.pop(f"{ns}_facts", None)
    if edit is not None:
        if ns == "cust": cust_dialog(edit if edit != "__new__" else None)
        elif ns == "fact": fact_dialog(edit if edit != "__new__" else None)
        elif ns == "item": item_dialog(edit if edit != "__new__" else None, facts)
        elif ns == "user": user_dialog(edit if edit != "__new__" else None)
    if dele is not None:
        if ns == "cust": cust_del_dialog(dele)
        elif ns == "fact": fact_del_dialog(dele)
        elif ns == "item": item_del_dialog(dele)
        elif ns == "user": user_del_dialog(dele)

# ── Shared table renderer ─────────────────────────────────────────────────────
def render_table(headers, rows, key_fn, cell_fn, ns):
    """
    headers : list of (label, flex_width)   e.g. [("客戶代碼",2),("客戶名稱",3),("備註",3)]
    rows    : list of dict
    key_fn  : row -> unique key string
    cell_fn : row -> list of display strings (same length as headers)
    ns      : namespace for session state keys
    """
    # Build header HTML
    spans = "".join(
        f'<span style="flex:{w}">{lbl}</span>'
        for lbl, w in headers
    )
    spans += '<span style="flex:2;text-align:center">操作</span>'
    st.markdown(
        f'<div class="tbl-wrap"><div class="tbl-head">{spans}</div></div>',
        unsafe_allow_html=True,
    )

    if not rows:
        st.markdown('<div class="tbl-wrap"><div class="tbl-empty">尚無資料</div></div>', unsafe_allow_html=True)
        return

    total_flex = sum(w for _, w in headers) + 2
    col_ratios = [w for _, w in headers] + [1, 1]

    st.markdown('<div class="tbl-wrap">', unsafe_allow_html=True)
    for r in rows:
        cells = cell_fn(r)
        key   = key_fn(r)
        cols  = st.columns(col_ratios)
        for i, (text, (_, w)) in enumerate(zip(cells, headers)):
            cols[i].markdown(
                f'<div class="tbl-cell" style="flex:{w}">{text}</div>',
                unsafe_allow_html=True,
            )
        if cols[-2].button("修改", key=f"e_{ns}_{key}"):
            st.session_state[f"{ns}_edit"] = r
            st.rerun()
        if cols[-1].button("刪除", key=f"d_{ns}_{key}"):
            st.session_state[f"{ns}_del"] = key
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ── Pages ─────────────────────────────────────────────────────────────────────
def page_login():
    st.markdown("<h1 style='text-align:center;margin-top:60px;color:#1677ff'>TriSys</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#999;margin-bottom:32px'>資料維護系統</p>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        with st.container(border=True):
            userid = st.text_input("帳號", placeholder="請輸入帳號")
            pwd    = st.text_input("密碼", type="password", placeholder="請輸入密碼")
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
    c1.markdown(f"### TriSys &nbsp;<span style='font-size:14px;color:#888;font-weight:400'>歡迎，{st.session_state.user.get('username') or st.session_state.user.get('userid')}</span>", unsafe_allow_html=True)
    if c2.button("登出"):
        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.page = "login"
        st.rerun()
    st.divider()
    cols = st.columns(2)
    menus = [("🏢\n\n客戶資料", "cust"), ("🏭\n\n廠商資料", "fact"),
             ("📦\n\n商品資料", "item"), ("👤\n\n用戶資料", "user")]
    for i, (label, pg) in enumerate(menus):
        with cols[i % 2]:
            with st.container(border=True):
                if st.button(label, use_container_width=True, key=f"menu_{pg}"):
                    st.session_state.page = pg; st.rerun()

def _page_header(title, ns, facts=None):
    c1, c2, c3 = st.columns([1, 6, 1.5])
    if c1.button("← 返回", key=f"back_{ns}"):
        st.session_state.page = "main"; st.rerun()
    c2.markdown(f"**{title}**")
    if c3.button("＋ 新增", key=f"add_{ns}", type="primary"):
        st.session_state[f"{ns}_edit"] = "__new__"
        if facts is not None:
            st.session_state[f"{ns}_facts"] = facts
        st.rerun()

def page_cust():
    _trigger("cust")
    try:
        conn = get_conn(); cur = conn.cursor(as_dict=True)
        cur.execute("SELECT cust_code,cust_name,remark FROM cust ORDER BY cust_code")
        rows = cur.fetchall(); conn.close()
    except Exception as e:
        st.error(str(e)); return
    _page_header("客戶資料維護", "cust")
    render_table(
        headers=[("客戶代碼", 2), ("客戶名稱", 3), ("備註", 3)],
        rows=rows,
        key_fn=lambda r: r["cust_code"],
        cell_fn=lambda r: [r["cust_code"], r["cust_name"], r.get("remark") or ""],
        ns="cust",
    )

def page_fact():
    _trigger("fact")
    try:
        conn = get_conn(); cur = conn.cursor(as_dict=True)
        cur.execute("SELECT fact_code,fact_name,remark FROM fact ORDER BY fact_code")
        rows = cur.fetchall(); conn.close()
    except Exception as e:
        st.error(str(e)); return
    _page_header("廠商資料維護", "fact")
    render_table(
        headers=[("廠商代碼", 2), ("廠商名稱", 3), ("備註", 3)],
        rows=rows,
        key_fn=lambda r: r["fact_code"],
        cell_fn=lambda r: [r["fact_code"], r["fact_name"], r.get("remark") or ""],
        ns="fact",
    )

def page_item():
    try:
        conn = get_conn(); cur = conn.cursor(as_dict=True)
        cur.execute("""SELECT i.item_code,i.item_name,i.fact_code,
                              ISNULL(f.fact_name,'') AS fact_name
                       FROM item i LEFT JOIN fact f ON i.fact_code=f.fact_code
                       ORDER BY i.item_code""")
        rows = cur.fetchall()
        cur.execute("SELECT fact_code,fact_name FROM fact ORDER BY fact_code")
        facts = [(r["fact_code"], r["fact_name"]) for r in cur.fetchall()]
        conn.close()
    except Exception as e:
        st.error(str(e)); return
    _trigger("item")
    _page_header("商品資料維護", "item", facts=facts)
    render_table(
        headers=[("商品代碼", 2), ("商品名稱", 3), ("主供應商", 3)],
        rows=rows,
        key_fn=lambda r: r["item_code"],
        cell_fn=lambda r: [r["item_code"], r["item_name"], r.get("fact_name") or r.get("fact_code") or ""],
        ns="item",
    )

def page_user():
    _trigger("user")
    try:
        conn = get_conn(); cur = conn.cursor(as_dict=True)
        cur.execute("SELECT userid,username,pwd FROM [user] ORDER BY userid")
        rows = cur.fetchall(); conn.close()
    except Exception as e:
        st.error(str(e)); return
    _page_header("用戶資料維護", "user")
    render_table(
        headers=[("用戶代碼", 2), ("用戶名稱", 3), ("密碼", 3)],
        rows=rows,
        key_fn=lambda r: r["userid"],
        cell_fn=lambda r: [r["userid"], r.get("username") or "", r.get("pwd") or ""],
        ns="user",
    )

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
