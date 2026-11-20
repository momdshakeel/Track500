"""Look & feel for the NSE 500 scanner: fonts, global CSS, hero, KPI cards and
sortable, responsive HTML tables that follow Streamlit's light/dark theme."""
import json
import hashlib
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

_TABLE_COMPONENT = components.declare_component(
    "marketpulse_result_table", path=str(Path(__file__).with_name("table_component"))
)

# ---------------------------------------------------------------- fonts
FONTS = {
    "Inter": "Inter",
    "Poppins": "Poppins",
    "DM Sans": "DM Sans",
    "Manrope": "Manrope",
    "IBM Plex Sans": "IBM Plex Sans",
    "Space Grotesk": "Space Grotesk",
    "Source Sans 3": "Source Sans 3",
    "System default": None,
}
_FALLBACK = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif"


def font_url(name: str) -> str:
    fam = FONTS.get(name)
    if not fam:
        return ""
    return (f"https://fonts.googleapis.com/css2?family={fam.replace(' ', '+')}"
            f":wght@400;500;600;700&display=swap")


def font_family(name: str) -> str:
    fam = FONTS.get(name)
    return f"'{fam}', {_FALLBACK}" if fam else _FALLBACK


# ---------------------------------------------------------------- page CSS
_PAGE_CSS = """
<style>
__IMPORT__
:root{--ui-font:__FAMILY__;--accent:#6366f1;--accent2:#ec4899;
--line:color-mix(in srgb,currentColor 13%,transparent);--soft:color-mix(in srgb,currentColor 5%,transparent)}
.stApp,.stApp div,.stApp p,.stApp label,.stApp li,.stApp h1,.stApp h2,.stApp h3,.stApp h4,
.stApp input,.stApp textarea,.stApp button,.stApp a,.stApp td,.stApp th{font-family:var(--ui-font)!important}
.block-container{width:100%;padding:1.4rem clamp(.8rem,2.2vw,2rem) 3rem!important;max-width:1600px}
header[data-testid="stHeader"]{background:transparent}
footer{visibility:hidden}
[data-testid="stAppDeployButton"],.stAppDeployButton{display:none!important}
div[data-testid="stElementContainer"]:has(> div > style),.element-container:has(> style){display:none}

/* hero */
.hero{display:flex;justify-content:space-between;align-items:center;gap:9px;flex-wrap:wrap;margin:1px 0 9px;
padding:10px 14px;border:1px solid var(--line);border-radius:14px;
background:linear-gradient(120deg,color-mix(in srgb,var(--accent) 9%,var(--soft)),var(--soft));
box-shadow:0 3px 10px color-mix(in srgb,currentColor 3%,transparent)}
.eyebrow{font-size:.61rem;letter-spacing:.12em;text-transform:uppercase;opacity:.62;font-weight:650}
.title{font-size:clamp(1.35rem,2.1vw,1.75rem);font-weight:700;line-height:1.08;margin:.14rem 0 .2rem;
background:linear-gradient(90deg,var(--accent),var(--accent2));-webkit-background-clip:text;
background-clip:text;color:transparent!important;-webkit-text-fill-color:transparent;letter-spacing:-.02em}
.sub{opacity:.76;font-size:.79rem;max-width:1000px;line-height:1.32}
.chips{display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-start}
.chip{border:1px solid var(--line);background:var(--soft);border-radius:999px;padding:3px 8px;
font-size:.66rem;white-space:nowrap;backdrop-filter:blur(8px)}
.chip b{font-weight:600}

/* KPI cards */
.kpis{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:8px;margin:2px 0 10px}
.kpi{position:relative;overflow:hidden;border-radius:10px;padding:8px 9px 7px 13px;min-width:0;
border:1px solid var(--line);background:color-mix(in srgb,var(--soft) 70%,transparent);
transition:transform .16s ease,border-color .16s ease,box-shadow .16s ease}
.kpi:hover{transform:translateY(-2px);border-color:color-mix(in srgb,var(--kc,var(--accent)) 48%,var(--line));
box-shadow:0 8px 20px color-mix(in srgb,currentColor 7%,transparent)}
.kpi:before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--kc,var(--accent))}
.kpi .l{font-size:.6rem;letter-spacing:.065em;text-transform:uppercase;opacity:.68;font-weight:650;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.kpi .v{font-size:1.42rem;font-weight:700;line-height:1.04;letter-spacing:-.02em;margin-top:2px}
.kpi .s{font-size:.62rem;opacity:.64;margin-top:2px;line-height:1.15;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-height:0}

/* tabs as pills (works with old and new Streamlit tab markup) */
[role="tablist"]{gap:8px!important;overflow-x:auto;border-bottom:none!important;box-shadow:none!important;
padding:2px 2px 10px;scrollbar-width:thin;scroll-snap-type:x proximity}
@media (min-width:900px){[role="tablist"]{flex-wrap:wrap!important;overflow:visible!important}}
[role="tablist"] [role="tab"]{border-radius:999px!important;padding:7px 16px!important;height:auto!important;
white-space:nowrap;flex-shrink:0;scroll-snap-align:start;background:var(--soft)!important;border:1px solid var(--line)!important;cursor:pointer}
[role="tablist"] [role="tab"] p{font-size:.88rem;font-weight:600;margin:0}
[role="tablist"] [role="tab"][aria-selected="true"]{background:var(--accent)!important;border-color:var(--accent)!important}
[role="tablist"] [role="tab"][aria-selected="true"] p{color:#fff!important}
.react-aria-SelectionIndicator,[data-baseweb="tab-highlight"],[data-baseweb="tab-border"]{display:none!important}

/* sidebar + widgets */
section[data-testid="stSidebar"]{border-right:1px solid var(--line)}
section[data-testid="stSidebar"] h2,section[data-testid="stSidebar"] h3{font-size:1rem;letter-spacing:-.01em}
.stButton>button,.stDownloadButton>button{border-radius:10px;border:1px solid var(--line);font-weight:600}
.stDownloadButton>button{background:var(--soft)}
div[data-baseweb="select"]>div,.stTextInput input{border-radius:10px!important}
.meters{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px;margin:6px 0 18px}
.meter{border:1px solid var(--line);background:var(--soft);border-radius:14px;padding:12px 15px 11px}
.meter .mh{display:flex;justify-content:space-between;align-items:baseline;font-size:.8rem;font-weight:600}
.meter .mh b{font-size:1.25rem;letter-spacing:-.01em}
.meter .mt{height:8px;border-radius:99px;background:var(--line);margin-top:8px;overflow:hidden}
.meter .mf{height:100%;border-radius:99px;background:linear-gradient(90deg,var(--accent),var(--accent2))}
.meter .mn{font-size:.72rem;opacity:.6;margin-top:6px}
.advdec{display:flex;height:14px;border-radius:99px;overflow:hidden;margin:6px 0 4px;background:var(--line)}
.advdec .a{background:#10b981}.advdec .d{background:#ef4444}
.advlbl{display:flex;justify-content:space-between;font-size:.8rem;font-weight:600;margin-bottom:14px}
.tabnote{opacity:.72;font-size:.88rem;line-height:1.5;margin:2px 0 12px;max-width:1000px;overflow-wrap:anywhere}
.tabnote b{font-weight:600}
.screen-info{display:flex;flex-direction:column;justify-content:center;min-height:72px;padding:4px 2px}
.screen-info .kicker{font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;opacity:.55;font-weight:700}
.screen-info .heading{font-size:1.05rem;font-weight:700;line-height:1.2;margin:3px 0}
.screen-info .description{font-size:.82rem;line-height:1.4;opacity:.7}
.st-key-screen-library-control{padding:8px 10px 1px;border-radius:12px;
background:linear-gradient(110deg,color-mix(in srgb,var(--accent) 10%,var(--soft)),var(--soft));
border:1px solid color-mix(in srgb,var(--accent) 26%,var(--line))}
.st-key-screen-library-control [data-baseweb="select"]>div{
background:color-mix(in srgb,var(--accent) 5%,var(--soft))!important;
border-color:color-mix(in srgb,var(--accent) 38%,var(--line))!important}
.st-key-screen-library-control [data-baseweb="select"]:hover>div{
border-color:color-mix(in srgb,var(--accent) 58%,var(--line))!important}
div[data-testid="stSelectbox"] label{font-size:.76rem!important;font-weight:700!important;letter-spacing:.02em}
div[data-testid="stSelectbox"] [data-baseweb="select"]>div{min-height:44px!important}
@media (max-width:1100px) and (min-width:641px){.kpis{grid-template-columns:repeat(4,minmax(0,1fr))}}
@media (max-width:900px){.sub{max-width:100%}.kpis{gap:8px}}
@media (max-width:640px){
  .block-container{padding-top:2.8rem!important;padding-bottom:2rem!important;padding-left:.7rem!important;padding-right:.7rem!important}
  .hero{align-items:flex-start;gap:7px;margin-bottom:8px;padding:10px 10px;border-radius:12px}.title{font-size:clamp(1.28rem,5.2vw,1.6rem)}
  .sub{font-size:.76rem;line-height:1.32}.chips{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));width:100%;gap:4px}
  .chip{font-size:.62rem;white-space:normal;overflow-wrap:anywhere;padding:3px 6px;text-align:center}
  .kpis{grid-template-columns:repeat(2,minmax(0,1fr));gap:6px;margin-bottom:9px}
  .kpi{padding:8px 8px 7px 12px;border-radius:9px}.kpi:before{width:3px}
  .kpi:hover{transform:none}
  .kpi .l{font-size:.6rem}.kpi .v{font-size:1.24rem}.kpi .s{font-size:.62rem;line-height:1.15}
  [role="tablist"]{gap:6px!important;padding-bottom:8px}
  [role="tablist"] [role="tab"]{padding:7px 12px!important}
  [role="tablist"] [role="tab"] p{font-size:.82rem}
  [role="radiogroup"]{flex-wrap:wrap!important;gap:6px 12px!important}
  .meters{grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}
  .meter{padding:10px;border-radius:11px}.meter .mh{font-size:.74rem}.meter .mh b{font-size:1.05rem}
  .advlbl{gap:8px;font-size:.7rem;flex-wrap:wrap}
  .stDownloadButton>button,.stButton>button{min-height:42px}
}
@media (max-width:380px){
  .block-container{padding-left:.55rem!important;padding-right:.55rem!important}
  .kpi .v{font-size:1.16rem}.kpi .l{font-size:.57rem}.kpi .s{font-size:.6rem}
  .meter .mn{font-size:.65rem}.chip{font-size:.66rem}
}
</style>
"""


def inject_css(font: str, hide_sidebar: bool = False) -> None:
    css = (_PAGE_CSS
           .replace("__IMPORT__", f"@import url('{font_url(font)}');" if font_url(font) else "")
           .replace("__FAMILY__", font_family(font)))
    if hide_sidebar:
        css = css.replace("</style>", "section[data-testid='stSidebar'],button[data-testid='stSidebarCollapsedControl'],div[data-testid='stSidebarCollapsedControl']{display:none!important}</style>")
    st.markdown(css, unsafe_allow_html=True)


def hero(title: str, subtitle: str, chips: list, eyebrow: str = "MarketPulse 750 · Nifty Total Market") -> None:
    chip_html = "".join(f'<span class="chip">{c}</span>' for c in chips)
    st.markdown(
        f'<div class="hero"><div><div class="eyebrow">{eyebrow}</div>'
        f'<div class="title">{title}</div><div class="sub">{subtitle}</div></div>'
        f'<div class="chips">{chip_html}</div></div>', unsafe_allow_html=True)


def kpis(items: list) -> None:
    """items: (label, value, sub, colour)"""
    cards = "".join(
        f'<div class="kpi" style="flex:1 1 145px;min-width:120px;box-sizing:border-box;'
        f'position:relative;overflow:hidden;border:1px solid rgba(100,116,139,.24);'
        f'border-left:4px solid {c};border-radius:10px;padding:8px 9px 7px;'
        f'background:rgba(100,116,139,.055);">'
        f'<div class="l" style="font-size:.6rem;letter-spacing:.065em;text-transform:uppercase;'
        f'font-weight:650;opacity:.72;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{l}</div>'
        f'<div class="v" style="font-size:1.42rem;font-weight:700;line-height:1.04;letter-spacing:-.02em;margin-top:2px;">{v}</div>'
        f'<div class="s" style="font-size:.62rem;opacity:.68;margin-top:2px;line-height:1.15;'
        f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{s}</div></div>' for l, v, s, c in items)
    st.markdown(
        f'<div class="kpis" style="display:flex;flex-flow:row wrap;align-items:stretch;gap:8px;'
        f'width:100%;margin:2px 0 10px;">{cards}</div>',
        unsafe_allow_html=True,
    )


def meters(items: list) -> None:
    """items: (label, percent 0-100, small note)"""
    cards = "".join(
        f'<div class="meter"><div class="mh"><span>{l}</span><b>{p:.0f}%</b></div>'
        f'<div class="mt"><div class="mf" style="width:{max(0, min(100, p))}%"></div></div>'
        f'<div class="mn">{n}</div></div>' for l, p, n in items)
    st.markdown(f'<div class="meters">{cards}</div>', unsafe_allow_html=True)


def adv_dec(adv: int, dec: int, unch: int) -> None:
    total = max(adv + dec + unch, 1)
    st.markdown(
        f'<div class="advdec"><div class="a" style="width:{adv / total * 100:.1f}%"></div>'
        f'<div class="d" style="width:{dec / total * 100:.1f}%"></div></div>'
        f'<div class="advlbl"><span style="color:#10b981">▲ {adv} advancing</span>'
        f'<span style="opacity:.6">{unch} unchanged</span>'
        f'<span style="color:#ef4444">{dec} declining ▼</span></div>', unsafe_allow_html=True)


def note(text: str) -> None:
    st.markdown(f'<div class="tabnote">{text}</div>', unsafe_allow_html=True)


# ---------------------------------------------------------------- table columns
# type: sym txt rs chg sgn1 stage tt chk dot n0 n1 n2 pct spct bar text ago mult
# pri: 1 always shown | 2 hidden on small phones | 3 hidden on phones (tables scroll sideways otherwise)
SPEC = {
    "Symbol": dict(t="Symbol", type="sym", pri=1, left=True),
    "Trend_State": dict(t="Trend", type="text", pri=1, left=True),
    "Company Name": dict(t="Company", type="txt", pri=3, left=True),
    "Sector": dict(t="Sector", type="txt", pri=3, left=True),
    "Sector_Rank": dict(t="Sector #", type="n0", pri=3),
    "Sector_Strength": dict(t="Sector strength", type="bar", pri=3),
    "Liquid": dict(t="Liquid", type="chk", pri=2),
    "Avg_Value_Cr": dict(t="Avg value ₹ cr/day", type="cr", pri=2),
    "Market_Cap_Cr": dict(t="Mkt cap ₹ cr", type="cr0", pri=2),
    "RS_Rating": dict(t="RS", type="rs", pri=1),
    "RS_Excess_3M_%": dict(t="RS vs Nifty · 3M", type="spct", pri=2),
    "RS_Excess_6M_%": dict(t="RS vs Nifty · 6M", type="spct", pri=3),
    "RS_Improving": dict(t="RS improving", type="chk", pri=3),
    "RS_Change": dict(t="Chg", type="chg", pri=2),
    "Stage": dict(t="Stage", type="stage", pri=2, left=True),
    "TT_Score": dict(t="Trend Template", type="tt", pri=2),
    "RS_Line_New_High": dict(t="RS line high", type="chk", pri=3),
    "RS_Line_Near_High": dict(t="RS line near high", type="chk", pri=3),
    "RS_Blue_Dot": dict(t="Blue dot", type="dot", pri=3),
    "RSI14": dict(t="RSI", type="n1", pri=2),
    "Close": dict(t="Close", type="n2", pri=1),
    "Chg_1D_%": dict(t="1D change %", type="spct", pri=1),
    "Pct_From_52W_High": dict(t="From 52W high", type="pct", pri=2),
    "Pct_Above_50SMA": dict(t="Above 50 SMA", type="pct", pri=2),
    "Extension_State": dict(t="Extension", type="text", pri=3),
    "Volume_Pressure_20D": dict(t="20D volume pressure", type="text", pri=3),
    "Up_Down_Vol_Ratio_20D": dict(t="Up/down vol · 20D", type="mult", pri=3),
    "Pct_Above_52W_Low": dict(t="Above 52W low", type="pct", pri=3),
    "Weighted_Return_%": dict(t="Weighted return", type="spct", pri=3),
    "VCP": dict(t="VCP", type="chk", pri=2),
    "VCP_Contractions": dict(t="Pullbacks %", type="text", pri=2, left=True),
    "VCP_Vol_Contracting": dict(t="Vol shrinking", type="chk", pri=3),
    "Vol_Dry_Up": dict(t="Vol dry-up", type="chk", pri=3),
    "VCP_Setup": dict(t="VCP setup", type="chk", pri=2),
    "Pivot": dict(t="Pivot", type="n2", pri=2),
    "Pct_To_Pivot": dict(t="To pivot", type="pct", pri=1),
    "Vol_Breakout": dict(t="Breakout", type="chk", pri=2),
    "Breakout_Days_Ago": dict(t="When", type="ago", pri=2),
    "Breakout_Vol_x": dict(t="Breakout vol", type="mult", pri=2),
    "Vol_x_50d": dict(t="Vol today", type="mult", pri=3),
    "Stage1_Base": dict(t="Stage 1 base", type="chk", pri=3),
    "Base_Days": dict(t="Base length", type="days", pri=2),
    "Base_Depth_%": dict(t="Base depth", type="pct", pri=3),
    "Base_Forming": dict(t="Base forming", type="chk", pri=3),
    "Market_Above_10SMA": dict(t="Market above 10-day SMA", type="chk", pri=3),
    "Market_Above_20SMA": dict(t="Market above 20-day SMA", type="chk", pri=3),
    # industry table
    "Rank": dict(t="#", type="n0", pri=1),
    "Group": dict(t="Group", type="grp", pri=1, left=True),
    "Pct_Above_200": dict(t="Above 200 SMA", type="pct0", pri=3),
    "Pct_Stage2": dict(t="Stage 2", type="pct0", pri=3),
    "Sector_Score": dict(t="Strength", type="bar", pri=1),
    "Stocks": dict(t="Stocks", type="n0", pri=2),
    "Median_RS": dict(t="Median RS", type="n0", pri=2),
    "Avg_RS": dict(t="Avg RS", type="n1", pri=3),
    "Avg_RS_Change": dict(t="Avg chg", type="sgn1", pri=3),
    "Pct_RS80": dict(t="RS ≥ 80", type="pct0", pri=2),
    "Pct_TT_Pass": dict(t="Trend Template", type="pct0", pri=2),
    "TT_Pass_Count": dict(t="TT pass", type="n0", pri=3),
    "Blue_Dots": dict(t="Blue dots", type="n0", pri=3),
    "Avg_Weighted_Return_%": dict(t="Avg return", type="spct", pri=3),
    "Top_Stocks": dict(t="Leaders", type="text", pri=2, left=True),
}
COLS_DEFAULT = ["Symbol", "Trend_State", "Company Name", "Sector", "Sector_Rank", "RS_Rating",
                "Sector_Strength", "RS_Excess_3M_%", "RS_Excess_6M_%", "RS_Improving", "RS_Change",
                "Stage", "TT_Score",
                "Volume_Pressure_20D", "Up_Down_Vol_Ratio_20D", "Pct_Above_50SMA", "Extension_State",
                "Liquid", "Avg_Value_Cr", "Market_Cap_Cr", "RS_Line_New_High", "RS_Blue_Dot", "RSI14", "Close", "Chg_1D_%",
                "Pct_From_52W_High", "Pct_Above_52W_Low", "Weighted_Return_%"]
COLS_PATTERN = ["Symbol", "RS_Rating", "Stage", "TT_Score", "VCP", "VCP_Contractions", "Vol_Dry_Up",
                "VCP_Setup", "Pivot", "Pct_To_Pivot", "Close", "Chg_1D_%", "Vol_Breakout", "Breakout_Days_Ago",
                "Breakout_Vol_x", "Vol_x_50d", "Stage1_Base", "Base_Days", "Base_Depth_%", "Liquid",
                "Avg_Value_Cr", "Market_Cap_Cr", "Sector", "Company Name"]
COLS_SECTOR_STRENGTH = ["Rank", "Group", "Sector_Score", "Stocks", "Median_RS", "Avg_RS", "Avg_RS_Change",
                        "Pct_RS80", "Pct_TT_Pass", "Pct_Above_200", "Pct_Stage2", "TT_Pass_Count", "Blue_Dots",
                        "Avg_Weighted_Return_%", "Top_Stocks"]

# ---------------------------------------------------------------- table iframe
_TABLE_HTML = r"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
__IMPORT__
:root{--fg:#31333f;--bg:#fff;--accent:#6366f1;--accent2:#ec4899;--rowh:__ROWH__px;--ff:__FAMILY__;
--line:color-mix(in srgb,var(--fg) 14%,transparent);--soft:color-mix(in srgb,var(--fg) 6%,transparent);
--g:#047857;--a:#92400e;--r:#b91c1c;--b:#1d4ed8}
html.dark{--g:#34d399;--a:#fbbf24;--r:#f87171;--b:#60a5fa}
*{box-sizing:border-box}
html,body{margin:0;height:100%;background:var(--bg);color:var(--fg);font:13.5px/1.35 var(--ff)}
.wrap{height:calc(100vh - 48px);overflow:auto;border:1px solid var(--line);border-radius:14px;
overscroll-behavior:contain;scrollbar-width:thin;-webkit-overflow-scrolling:touch;touch-action:pan-x pan-y}
table{border-collapse:separate;border-spacing:0;width:100%;min-width:max-content}
th{position:sticky;top:0;z-index:3;padding:0 12px;height:42px;text-align:right;white-space:nowrap;cursor:pointer;
user-select:none;font-size:.7rem;text-transform:uppercase;letter-spacing:.06em;font-weight:700;
color:color-mix(in srgb,var(--fg) 78%,var(--bg));background:color-mix(in srgb,var(--accent) 8%,var(--bg));
border-bottom:1px solid color-mix(in srgb,var(--accent) 24%,var(--line))}
th:hover{color:var(--fg)}
th.l,td.l{text-align:left}
th .ar{display:inline-block;width:12px;color:var(--accent)}
td{height:var(--rowh);padding:0 12px;white-space:nowrap;text-align:right;border-bottom:1px solid var(--line);
font-variant-numeric:tabular-nums}
tr:last-child td{border-bottom:none}
tbody tr:nth-child(even) td{background:color-mix(in srgb,var(--fg) 3.5%,var(--bg))}
tbody tr:hover td{background:color-mix(in srgb,var(--accent) 10%,var(--bg))}
th:first-child,td:first-child{position:sticky;left:0;z-index:2;background:var(--bg)}
th:first-child{z-index:4;background:color-mix(in srgb,var(--accent) 8%,var(--bg))}
tbody tr:nth-child(even) td:first-child{background:color-mix(in srgb,var(--fg) 3.5%,var(--bg))}
a.sym{color:var(--accent);font-weight:700;text-decoration:none}
a.sym:hover{text-decoration:underline}
.symcell{display:inline-flex;align-items:center;gap:6px}
.info-btn{position:relative;flex:none;width:20px;height:20px;padding:0;border:1px solid var(--line);border-radius:50%;
background:var(--soft);color:var(--accent);font:700 11px/18px var(--ff);cursor:pointer}
.info-btn::after{content:"";position:absolute;inset:-8px}
@media(pointer:coarse){.info-btn{width:24px;height:24px;line-height:22px}.info-btn::after{inset:-10px}}
.info-btn:hover{background:var(--accent);color:#fff}
.ell{display:inline-block;max-width:210px;overflow:hidden;text-overflow:ellipsis;vertical-align:middle;
color:color-mix(in srgb,var(--fg) 70%,var(--bg))}
.badge{display:inline-block;min-width:38px;text-align:center;padding:2px 9px;border-radius:999px;font-weight:700}
.c1{background:#059669;color:#fff}
.c2{background:color-mix(in srgb,#10b981 22%,var(--bg));color:var(--g)}
.c3{background:color-mix(in srgb,#f59e0b 24%,var(--bg));color:var(--a)}
html.dark .c3{color:#fbbf24}
.c4{background:var(--soft);color:color-mix(in srgb,var(--fg) 75%,var(--bg))}
.c5{background:color-mix(in srgb,#ef4444 18%,var(--bg));color:var(--r)}
.chipx{display:inline-block;padding:2px 10px;border-radius:8px;font-size:.78rem;font-weight:600}
.s1{background:color-mix(in srgb,#3b82f6 18%,var(--bg));color:var(--b)}
.s2{background:color-mix(in srgb,#10b981 20%,var(--bg));color:var(--g)}
.s3{background:color-mix(in srgb,#f59e0b 22%,var(--bg));color:var(--a)}
html.dark .s3{color:#fbbf24}
.s4{background:color-mix(in srgb,#ef4444 18%,var(--bg));color:var(--r)}
.s0{background:var(--soft)}
.seg{display:inline-flex;gap:2px;vertical-align:middle;margin-right:7px}
.seg i{width:5px;height:13px;border-radius:2px;background:var(--line)}
.seg i.on{background:var(--accent)}
.seg.full i.on{background:var(--g)}
.ttn{font-weight:600}.full+.ttn{color:var(--g)}
.up{color:var(--g);font-weight:600}.dn{color:var(--r);font-weight:600}
.faint{opacity:.55}
.ok{color:var(--g);font-weight:700}
.dotx{display:inline-block;width:10px;height:10px;border-radius:50%;background:var(--accent);
box-shadow:0 0 0 3px color-mix(in srgb,var(--accent) 25%,transparent)}
.bar{display:flex;align-items:center;gap:9px;min-width:150px}
.bar .t{flex:1;height:8px;border-radius:99px;background:var(--soft);overflow:hidden}
.bar .f{height:100%;border-radius:99px;background:linear-gradient(90deg,var(--accent),var(--accent2))}
.bar b{min-width:24px;text-align:right}
.txt{color:color-mix(in srgb,var(--fg) 85%,var(--bg))}
.empty{text-align:center;padding:36px 12px;opacity:.6}
.searchbar{display:flex;align-items:center;gap:10px;margin:0 0 8px}
.searchbar input{flex:1;min-width:0;padding:9px 12px;border:1px solid var(--line);border-radius:9px;
background:var(--bg);color:var(--fg);font:inherit;outline:none}
.searchbar input:focus{border-color:var(--accent);box-shadow:0 0 0 2px color-mix(in srgb,var(--accent) 18%,transparent)}
.count{font-size:.82rem;opacity:.65;white-space:nowrap}
@media (max-width:620px){td,th{padding:0 8px}html,body{font-size:12.5px}}
@media (max-width:420px){.searchbar{gap:6px}.searchbar input{font-size:16px;padding:9px}.count{font-size:.72rem}}
</style></head><body>
<div class="searchbar" id="searchbar" style="display:none"><input id="search" type="search" autocomplete="off">
<span class="count" id="count"></span></div>
<div class="wrap"><table><thead id="h"></thead><tbody id="b"></tbody></table></div>
<script>
const P=__PAYLOAD__;
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fx=(v,d)=>v==null?'<span class="faint">–</span>':Number(v).toFixed(d);
const sg=(v,d,suf)=>v==null?'<span class="faint">–</span>':'<span class="'+(v>0?'up':v<0?'dn':'faint')+'">'+(v>0?'+':'')+Number(v).toFixed(d)+suf+'</span>';
let sk=P.sort[0],sd=P.sort[1];
const pc=c=>(c.pri==2?'p2':c.pri==3?'p3':'')+(c.left?' l':'');
let query='';
function cell(c,r){
  const v=r[c.k],k='<td class="'+pc(c)+'">';
  switch(c.type){
    case 'sym':return k+'<span class="symcell"><a class="sym" target="_blank" rel="noopener" href="https://www.tradingview.com/chart/?symbol=NSE%3A'+encodeURIComponent(v)+'">'+esc(v)+'</a><button class="info-btn" type="button" title="Stock details and chart" aria-label="Stock details and chart for '+esc(v)+'" data-symbol="'+esc(v)+'">i</button></span></td>';
    case 'grp':return k+'<b>'+esc(v)+'</b></td>';
    case 'cr0':return k+(v==null?'<span class="faint">–</span>':Number(v).toLocaleString('en-IN',{maximumFractionDigits:0}))+'</td>';
    case 'cr':return k+(v==null?'<span class="faint">–</span>':Number(v).toLocaleString('en-IN',{maximumFractionDigits:1}))+'</td>';
    case 'txt':return k+'<span class="ell" title="'+esc(v)+'">'+esc(v)+'</span></td>';
    case 'text':return k+(v?'<span class="txt">'+esc(v)+'</span>':'<span class="faint">–</span>')+'</td>';
    case 'rs':{if(v==null)return k+'–</td>';const q=v>=90?'c1':v>=80?'c2':v>=70?'c3':v>=50?'c4':'c5';return k+'<span class="badge '+q+'">'+v+'</span></td>';}
    case 'chg':return k+(v>0?'<span class="up">▲ '+v+'</span>':v<0?'<span class="dn">▼ '+Math.abs(v)+'</span>':'<span class="faint">0</span>')+'</td>';
    case 'sgn1':return k+sg(v,1,'')+'</td>';
    case 'spct':return k+sg(v,1,'%')+'</td>';
    case 'stage':{if(!v||v==='n/a')return k+'<span class="chipx s0">n/a</span></td>';const n=(v.match(/\d/)||[0])[0];return k+'<span class="chipx s'+n+'">'+esc(v.replace('Stage ','').replace(' · ',' · '))+'</span></td>';}
    case 'tt':{let s='';for(let i=1;i<=8;i++)s+='<i class="'+(i<=v?'on':'')+'"></i>';return k+'<span class="seg'+(v==8?' full':'')+'">'+s+'</span><span class="ttn">'+v+'/8</span></td>';}
    case 'chk':return k+(v?'<span class="ok">✓</span>':'<span class="faint">·</span>')+'</td>';
    case 'dot':return k+(v?'<span class="dotx" title="RS line at 52-week high before price"></span>':'<span class="faint">·</span>')+'</td>';
    case 'n0':return k+(v==null?'–':Math.round(v))+'</td>';
    case 'n1':return k+fx(v,1)+'</td>';
    case 'n2':return k+fx(v,2)+'</td>';
    case 'pct':return k+(v==null?'<span class="faint">–</span>':Number(v).toFixed(1)+'%')+'</td>';
    case 'pct0':return k+(v==null?'–':Math.round(v)+'%')+'</td>';
    case 'days':return k+(v?v+'d':'<span class="faint">–</span>')+'</td>';
    case 'ago':return k+(v==null?'<span class="faint">–</span>':v==0?'<span class="up">today</span>':v+'d ago')+'</td>';
    case 'mult':return k+(v==null?'<span class="faint">–</span>':Number(v).toFixed(1)+'×')+'</td>';
    case 'bar':return k+'<div class="bar"><div class="t"><div class="f" style="width:'+Math.max(0,Math.min(99,v||0))+'%"></div></div><b>'+(v==null?'–':v)+'</b></div></td>';
  }
  return k+esc(v)+'</td>';
}
function draw(){
  const rows=P.rows.filter((r,i)=>!query||P.searchRows[i].some(v=>String(v??'').toLocaleLowerCase().includes(query)));
  rows.sort((a,b)=>{let x=a[sk],y=b[sk];
    if(x==null&&y==null)return 0;if(x==null)return 1;if(y==null)return -1;
    if(typeof x==='string')return sd*x.localeCompare(y);
    return sd*(Number(x)-Number(y));});
  document.getElementById('h').innerHTML='<tr>'+P.cols.map(c=>'<th class="'+pc(c)+'" data-k="'+c.k+'">'+esc(c.t)+'<span class="ar">'+(c.k===sk?(sd>0?'▲':'▼'):'')+'</span></th>').join('')+'</tr>';
  document.getElementById('b').innerHTML=rows.length?rows.map(r=>'<tr>'+P.cols.map(c=>cell(c,r)).join('')+'</tr>').join('')
    :'<tr><td class="empty" colspan="'+P.cols.length+'" style="text-align:center;position:static">'+esc(query?'No rows match your search.':P.empty)+'</td></tr>';
  if(P.searchLabel){document.getElementById('searchbar').style.display='flex';
    document.getElementById('search').placeholder=P.searchLabel;
    document.getElementById('count').textContent=query?rows.length+' of '+P.rows.length+' rows':P.rows.length+' rows';}
  document.querySelectorAll('th').forEach(th=>th.onclick=()=>{const k=th.dataset.k;
    if(k===sk)sd=-sd;else{sk=k;sd=P.cols.find(c=>c.k===k).left?1:-1;}draw();});
  document.querySelectorAll('.info-btn').forEach(btn=>btn.onclick=e=>{e.stopPropagation();window.parent.postMessage({type:'marketpulse:chart-request',symbol:btn.dataset.symbol,nonce:Date.now()},'*');});
}
if(P.searchLabel)document.getElementById('search').addEventListener('input',e=>{query=e.target.value.trim().toLocaleLowerCase();draw();});
// follow the Streamlit theme (light / dark / custom) live
function sync(){
  let bg,fg;
  try{let d=window.parent.document,w=window.parent;if(!d.querySelector('.stApp')){w=window.parent.parent;d=w.document;}const app=d.querySelector('.stApp'),cs=w.getComputedStyle(app);bg=cs.backgroundColor;fg=cs.color;}catch(e){}
  if(!bg||bg==='rgba(0, 0, 0, 0)'||!fg){const d=matchMedia('(prefers-color-scheme: dark)').matches;bg=d?'rgb(14,17,23)':'rgb(255,255,255)';fg=d?'rgb(250,250,250)':'rgb(49,51,63)';}
  const r=document.documentElement;r.style.setProperty('--bg',bg);r.style.setProperty('--fg',fg);
  const m=(bg.match(/[\d.]+/g)||[255,255,255]).map(Number);r.classList.toggle('dark',(0.299*m[0]+0.587*m[1]+0.114*m[2])<128);
}
sync();setInterval(sync,1000);draw();
</script></body></html>"""


def table(df, keys, sort, font="Inter", density="Comfortable",
          empty="No stocks match the current filters.", titles=None, search_keys=None,
          search_label="Search stock / symbol or company name", market_context=None):
    """Render a sortable, theme-aware table. `sort` = (column key, -1 desc | 1 asc)."""
    cols = [dict(SPEC[k], k=k) for k in keys if k in df.columns and k in SPEC]
    for c in cols:
        if titles and c["k"] in titles:
            c["t"] = titles[c["k"]]
    data = json.loads(df[[c["k"] for c in cols]].to_json(orient="records")) if len(df) else []
    search_rows = (df[search_keys].fillna("").astype(str).values.tolist()
                   if search_keys and len(df) else [])
    rowh = 31 if density == "Compact" else 41
    height = (120 if not data else min(len(data) * rowh + 46, 640)) + 48
    payload = json.dumps({"cols": cols, "rows": data, "searchRows": search_rows,
                          "searchLabel": search_label if search_keys else "",
                          "sort": list(sort), "empty": empty}).replace("</", "<\\/")
    html = (_TABLE_HTML
            .replace("__IMPORT__", f"@import url('{font_url(font)}');" if font_url(font) else "")
            .replace("__FAMILY__", font_family(font))
            .replace("__ROWH__", str(rowh))
            .replace("__PAYLOAD__", payload))
    identity_key = "Symbol" if "Symbol" in df.columns else (df.columns[0] if len(df.columns) else "table")
    identity = df[identity_key].head(3).fillna("").astype(str).tolist() if len(df) and identity_key in df else []
    key_source = json.dumps([keys, search_keys or [], search_label, titles or {}, identity_key, identity], sort_keys=True)
    component_key = "mp_table_" + hashlib.md5(key_source.encode("utf-8")).hexdigest()[:14]
    clicked = _TABLE_COMPONENT(html=html, height=height, key=component_key, default=None)
    if isinstance(clicked, dict) and clicked.get("symbol"):
        nonce = clicked.get("nonce")
        if nonce and nonce != st.session_state.get("_last_table_chart_click"):
            st.session_state["_last_table_chart_click"] = nonce
            st.session_state["_symbol_chart_request"] = str(clicked["symbol"])
            st.rerun()


def _embed(html: str, height: int) -> None:
    """st.iframe on current Streamlit; the older components.html call as a fallback."""
    if hasattr(st, "iframe"):
        st.iframe(html, height=height)
    else:
        components.html(html, height=height, scrolling=False)


_KLINE_SRC = "https://cdn.jsdelivr.net/npm/klinecharts@10.1.1/dist/umd/klinecharts.min.js"

_CHART_HTML = r"""<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{--fg:#243042;--bg:#fff;--accent:#6366f1;--line:rgba(36,48,66,.16);--soft:rgba(36,48,66,.07)}
*{box-sizing:border-box}
html,body{margin:0;height:100%;overflow:hidden;background:var(--bg);color:var(--fg);
font:12.5px/1.3 system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}
body{display:flex;flex-direction:column;gap:6px}
#bar{display:flex;align-items:center;gap:8px;overflow-x:auto;white-space:nowrap;scrollbar-width:none;padding:1px 0}
#bar::-webkit-scrollbar{display:none}
.seg{display:inline-flex;border:1px solid var(--line);border-radius:8px;overflow:hidden;flex:none}
.seg button{border:0;background:transparent;color:inherit;font:inherit;font-weight:600;padding:5px 10px;cursor:pointer}
.seg button+button{border-left:1px solid var(--line)}
.seg button.on{background:var(--accent);color:#fff}
.chip{flex:none;display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);border-radius:999px;
background:transparent;color:inherit;font:inherit;padding:4px 10px;cursor:pointer;opacity:.62}
.chip i{width:8px;height:8px;border-radius:50%;background:var(--c)}
.chip.on{opacity:1;background:var(--soft)}
.sp{flex:1}
.hint{flex:none;opacity:.55;font-size:11px;cursor:help}
#chart{flex:1;min-height:220px;width:100%;border:1px solid var(--line);border-radius:10px;overflow:hidden;touch-action:none}
.err{padding:16px;opacity:.75}
@media(max-width:560px){.hint{display:none}.seg button{padding:5px 8px}}
</style></head><body>
<div id="bar">
 <div class="seg" id="rng"></div>
 <button class="chip on" id="t_ema" style="--c:#f59e0b" title="Exponential averages 10 and 21"><i></i>EMA 10/21</button>
 <button class="chip on" id="t_sma" style="--c:#3b82f6" title="Simple averages 50 and 200"><i></i>SMA 50/200</button>
 <button class="chip on" id="t_vol" style="--c:#10b981" title="Volume"><i></i>Volume</button>
 <button class="chip on" id="t_rs" style="--c:#ec4899" title="Price relative to the benchmark index"><i></i>RS line</button>
 <span class="sp"></span>
 <span class="hint" title="Drag to pan. Scroll or pinch to zoom.">Drag to pan · pinch to zoom</span>
</div>
<div id="chart"></div>
<script src="__KLINE_SRC__"></script>
<script>
const P=__PAYLOAD__;
const SPAN={'3M':63,'6M':126,'1Y':252,'2Y':504,'5Y':1260};
const $=id=>document.getElementById(id);
const on={ema:true,sma:true,vol:true,rs:true};
let chart=null,rng=SPAN[P.range]?P.range:'1Y',dark=false;

function rgb(s){const m=(s||'').match(/[\d.]+/g);return m&&m.length>=3?m.slice(0,3).map(Number):null}
function readTheme(){
  let bg,fg;
  try{let w=window.parent,d=w.document;if(!d.querySelector('.stApp')){w=w.parent;d=w.document;}
    const cs=w.getComputedStyle(d.querySelector('.stApp'));bg=cs.backgroundColor;fg=cs.color;}catch(e){}
  let b=rgb(bg),f=rgb(fg);
  if(!b||!f||bg==='rgba(0, 0, 0, 0)'){const d=matchMedia('(prefers-color-scheme: dark)').matches;
    b=d?[14,17,23]:[255,255,255];f=d?[250,250,250]:[36,48,66];}
  dark=(0.299*b[0]+0.587*b[1]+0.114*b[2])<128;
  const r=document.documentElement.style,a=x=>'rgba('+f.join(',')+','+x+')';
  r.setProperty('--fg','rgb('+f.join(',')+')');r.setProperty('--bg','rgb('+b.join(',')+')');
  r.setProperty('--line',a(.16));r.setProperty('--soft',a(.08));
  return {text:a(.78),grid:a(dark?.09:.07),line:a(.22),bg:'rgb('+b.join(',')+')'};
}
const NARROW=()=>innerWidth<560;
function chartStyles(t){
  const rule=NARROW()?'follow_cross':'always';
  const axis={axisLine:{color:t.line},tickLine:{color:t.line},tickText:{color:t.text,size:11}};
  return {grid:{horizontal:{color:t.grid},vertical:{color:t.grid}},
    candle:{tooltip:{showRule:rule,legend:{color:t.text,size:11,template:legends},title:{show:false,template:''}}},
    indicator:{tooltip:{showRule:rule,text:{color:t.text,size:11}}},
    xAxis:axis,yAxis:axis,separator:{color:t.line},
    crosshair:{horizontal:{line:{color:t.line},text:{backgroundColor:dark?'#475569':'#334155',color:'#fff'}},
               vertical:{line:{color:t.line},text:{backgroundColor:dark?'#475569':'#334155',color:'#fff'}}}};
}
const paneOf=n=>{const i=chart.getIndicators({name:n})[0];return i&&i.paneId;};
const sizePane=(n,h)=>{const id=paneOf(n);if(id)try{chart.setPaneOptions({id,height:h});}catch(e){}};
const IND={
  ema:()=>chart.createIndicator({name:'EMA',calcParams:[10,21],paneId:'candle_pane'},true),
  sma:()=>chart.createIndicator({name:'MA',calcParams:[50,200],paneId:'candle_pane'},true),
  vol:()=>{chart.createIndicator({name:'VOL',calcParams:[20]},false);sizePane('VOL',72);},
  rs:()=>{chart.createIndicator('MP_RS_LINE',false);sizePane('MP_RS_LINE',72);}
};
const DEL={ema:'EMA',sma:'MA',vol:'VOL',rs:'MP_RS_LINE'};
const fmt=v=>v==null?'–':Number(v).toLocaleString('en-IN',{minimumFractionDigits:2,maximumFractionDigits:2});
const fmtV=v=>v==null?'–':v>=1e7?(v/1e7).toFixed(2)+'Cr':v>=1e5?(v/1e5).toFixed(2)+'L':Math.round(v).toLocaleString('en-IN');
const legends=(data)=>{const k=data.current;if(!k)return [];
  return [{title:'O ',value:fmt(k.open)},{title:'H ',value:fmt(k.high)},{title:'L ',value:fmt(k.low)},
          {title:'C ',value:fmt(k.close)},{title:'Vol ',value:fmtV(k.volume)}];};
function setRange(r){
  rng=r;document.querySelectorAll('#rng button').forEach(b=>b.classList.toggle('on',b.dataset.r===r));
  if(!chart)return;
  const gap=NARROW()?16:48,n=Math.max(20,Math.min(SPAN[r],P.bars.length)),w=Math.max(200,$('chart').clientWidth-64-gap);
  try{chart.setOffsetRightDistance(gap);}catch(e){}
  chart.setBarSpace(Math.max(1,Math.min(50,w/n)));chart.scrollToRealTime();
}
function mark(){
  const ts=s=>{const a=s.split('-').map(Number);return Date.UTC(a[0],a[1]-1,a[2])-330*60000};
  const dash=c=>({line:{style:'dashed',color:c,size:1}});
  chart.createOverlay({name:'verticalStraightLine',points:[{timestamp:ts(P.start)}],styles:dash('#6366f1')});
  chart.createOverlay({name:'verticalStraightLine',points:[{timestamp:ts(P.end)}],styles:dash('#6366f1')});
  chart.createOverlay({name:'priceLine',points:[{timestamp:ts(P.end),value:P.pivot}],styles:dash('#f59e0b')});
  (P.bases||[]).forEach(b=>chart.createOverlay({name:'horizontalSegment',
    points:[{timestamp:ts(b._end),value:Number(b._pivot)},{timestamp:ts(b._breakout),value:Number(b._pivot)}],
    styles:{line:{style:'solid',color:'#94a3b8',size:2}}}));
}
function start(){
  const t=readTheme();
  if(!window.klinecharts){$('chart').innerHTML='<div class="err">Chart library did not load. Check the network and reload.</div>';return;}
  try{const f=window.frameElement;if(f){const vh=window.parent.innerHeight||0;
    if(vh){const h=Math.max(380,Math.min(Math.round(vh*.66),P.height+80));f.style.height=h+'px';f.setAttribute('height',h);}}}catch(e){}
  const rsBy=new Map(P.bars.map(b=>[b.timestamp,b.rs]));
  try{klinecharts.registerIndicator({name:'MP_RS_LINE',shortName:'RS vs index',series:'normal',precision:2,
    figures:[{key:'rs',title:'RS: ',type:'line'}],calc:d=>d.map(k=>({rs:rsBy.get(k.timestamp)??null}))});}catch(e){}
  chart=klinecharts.init('chart');chart.setTimezone('Asia/Kolkata');
  chart.setStyles(chartStyles(t));
  chart.setSymbol({ticker:P.symbol+' · NSE',pricePrecision:2,volumePrecision:0});chart.setPeriod({span:1,type:'day'});
  chart.setLocale('en-US');chart.setDataLoader({getBars:({callback})=>callback(P.bars)});
  ['ema','sma','vol','rs'].forEach(k=>IND[k]());
  setTimeout(()=>{mark();setRange(rng);},220);
  new ResizeObserver(()=>{chart.resize();setRange(rng);}).observe($('chart'));
}
$('rng').innerHTML=Object.keys(SPAN).map(r=>'<button type="button" data-r="'+r+'">'+r+'</button>').join('');
$('rng').onclick=e=>{const r=e.target.dataset&&e.target.dataset.r;if(r)setRange(r);};
['ema','sma','vol','rs'].forEach(k=>$('t_'+k).onclick=()=>{
  on[k]=!on[k];$('t_'+k).classList.toggle('on',on[k]);
  try{if(on[k])IND[k]();else chart.removeIndicator({name:DEL[k]});}catch(e){}
  setTimeout(()=>setRange(rng),30);
});
document.querySelectorAll('#rng button').forEach(b=>b.classList.toggle('on',b.dataset.r===rng));
start();
</script></body></html>
"""


def chart_explorer(bars, symbol: str, base_start: str, base_end: str, pivot: float,
                   base_history=None, visible_window="1Y", height: int = 560) -> None:
    """Render a transient chart: theme-aware, with in-chart range buttons and indicator toggles.

    All bars are sent once; the range buttons (3M-5Y) only zoom, so moving between ranges is
    instant and the moving averages are always calculated from the full history.
    """
    window = str(visible_window).upper()
    window = window if window in ("3M", "6M", "1Y", "2Y", "5Y") else "1Y"
    bases = [row for row in (base_history or []) if row.get("_breakout")]
    payload = json.dumps({"symbol": symbol, "bars": bars, "start": base_start, "end": base_end,
                          "pivot": float(pivot), "bases": bases, "range": window,
                          "height": int(height)}).replace("</", "<\\/")
    html = _CHART_HTML.replace("__KLINE_SRC__", _KLINE_SRC).replace("__PAYLOAD__", payload)
    _embed(html, int(height))
