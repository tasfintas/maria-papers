"""
ghush_mechanism.py  -  step 2 of the Ghush enrichment.

Reads ghush_enriched.csv (from ghush_enrich.py) and adds columns that describe HOW the
bribe happened, read from the free-text description:

  actors            who is named as taking/asking (semicolon list, e.g. "peon_clerk;broker")
  first_actor       the actor mentioned earliest in the text (a heuristic, not a fact)
  initiator         official_demanded / citizen_asked_or_offered / broker / unclear
  channels          where/how it was handed over (semicolon list)
  f_*               yes/no flags for recurring patterns (obstruction, delay, threat, ...)
  pattern_type      ONE label per report, picked by ordered rules from the flags
  mech_evidence     the exact words that triggered pattern_type (so you can audit it)

Same rules as step 1: regex over Bengali + English + Banglish, first match wins where a single
label is needed, and every label keeps its evidence.

Usage:  python ghush_mechanism.py ghush_enriched.csv ghush_mechanism.csv
"""
import re
import sys
import unicodedata

import pandas as pd

sys.path.insert(0, __file__.rsplit("/", 1)[0] if "/" in __file__ else ".")
from ghush_enrich import norm, rx  # noqa: E402  (same normalisation as step 1)


def R(p):
    return rx(p)


# ---------------------------------------------------------------- who
ACTORS = {
    "peon_clerk": R(r"পিয়ন|পিওন|প্যায়াদা|অফিস সহায়ক|অফিস সহকারী|অফিস স্টাফ|কেরানি|করণিক|পেশকার|সহকারী|কর্মচারী|কর্মচারি|স্টাফ|\bpeon\b|\bclerk\b|\bstaff\b|office assistant|ahayok|karmochari"),
    "officer": R(r"কর্মকর্তা|অফিসার|ইন্সপেক্টর|ইনস্পেক্টর|পরিদর্শক|কমিশনার|এসি\s*ল্যান্ড|এসিল্যান্ড|ইউএনও|\bacland\b|সার্ভেয়ার|তহশিলদার|রেজিস্ট্রার|সাব রেজিস্ট্রার|ম্যানেজার|পরিচালক|সচিব|\bofficer\b|\binspector\b|karmokorta|\bmanager\b|\bsir\b|স্যার"),
    "police": R(r"পুলিশ|কনস্টেবল|\bsi\b|এসআই|ওসি|সার্জেন্ট|ট্রাফিক|আনসার|র[‍]?্যাব|\bpolice\b|\btraffic\b|\bconstable\b|\bpulish\b"),
    "broker": R(r"দালাল|এজেন্ট|বিচৌলিয়া|মধ্যস্থতা|মাধ্যমে|কম্পিউটারের দোকান|ভেন্ডর|\bdalal\b|\bagent\b|\bbroker\b|middleman|দোকান"),
    "elected_member": R(r"চেয়ারম্যান|মেম্বার|কাউন্সিলর|মেয়র|সংসদ সদস্য|এমপি|\bmp\b|\bchairman\b|\bmember\b|\bmayor\b"),
    "teacher_head": R(r"প্রধান শিক্ষক|হেডমাস্টার|শিক্ষক|অধ্যক্ষ|প্রিন্সিপাল|\bprincipal\b|\bteacher\b|headmaster"),
    "hospital_staff": R(r"ওয়ার্ড বয়|ওয়ার্ডবয়|আয়া|নার্স|সিস্টার|ব্রাদার|ডাক্তার|স্বাস্থ্যকর্মী|\bdoctor\b|\bnurse\b|ward boy|\bsister\b"),
    "party_local_leader": R(r"নেতা|ক্যাডার|ছাত্রলীগ|ছাত্রদল|যুবলীগ|যুবদল|আওয়ামী|বিএনপি|জামায়াত|\bleader\b|cadre|চাঁদাবাজ|মাস্তান"),
}

# ---------------------------------------------------------------- initiator
OFFICIAL_DEMAND = R(r"চেয়েছ|চাইল|চাইত|চায়|চান\b|চাওয়া|চাই\b|দাবি|দাবী|দাবি করে|বলল[ে]?.{0,25}টাকা|বলে.{0,25}টাকা|টাকা লাগবে|টাকা দিতে হবে|দিতে হবে|দিতে হয়|দিতে বাধ্য|বাধ্য করে|বাধ্য হয়ে|ঘুষ লাগে|ঘুস লাগে|নিয়েছে|নেয়\b|নিল\b|আদায়|demand|asked for|\bwanted\b|chaise|chay\b|chaio|chaici|chaicilo|laghbe|lagbe|dite hobe|nise|neya|nei\b|dabi")
CITIZEN_ASKED = R(r"কত হলে|কত দিলে|কত দিতে হবে|কতো হলে|জিজ্ঞেস|জিজ্ঞাসা|জানতে চাই|কত লাগ|কতো লাগ|কত টাকা লাগ|নিজে থেকে|নিজেই দ(িয়|ি)|আমি দিতে চাই|আমি স্বেচ্ছায়|দ্রুত করার জন্য.{0,30}(দিয়েছ|দিলাম|দিয়েছি)|তাড়াতাড়ি করার জন্য|জরুরি.{0,30}(দিয়েছ|দিলাম|দিয়েছি)|স্পিড মানি.{0,30}(দিয়েছ|দিলাম)|খুশি করে|খুশী করে|ঝামেলা এড়াতে|ঝামেলা এড়িয়ে|জানতে চাইলাম|ask(ed)? (him|her|them|how much)|how much|koto lage|koto taka|jiggesh|jigges")
BROKER_ROUTE = R(r"দালাল|বিচৌলিয়া|দালাল.{0,40}(মাধ্যমে|ধরে|দিয়ে|কাছে|কাছে গেলে)|(মাধ্যমে|ধরে|দিয়ে).{0,25}দালাল|দালালের|দালালকে|দালাল ধরে|দালাল নামে|এজেন্টের মাধ্যমে|এজেন্ট ধরে|dalal|broker|agent")

# ---------------------------------------------------------------- channel (where/how it is handed over)
CHANNELS = {
    "aside_private": R(r"একপাশে|এক পাশে|আড়ালে|আলাদা (ভাবে|করে|রুমে|কক্ষে)|ডেকে নিয়ে|ডেকে নিল|ডেকে নেয়|ভিতরে ডেকে|ভেতরে ডেকে|গোপনে|কানে কানে|ইশারা|ইঙ্গিত|ঈঙ্গিত|সরাসরি না বলে|প্রকাশ্যে না|নিরিবিলি|রুমে ডেকে|কক্ষে ডেকে|আলাদা ডেকে|একান্তে|hint|ishara|alada"),
    "open_in_office": R(r"প্রকাশ্য|সবার সামনে|সবার সামনেই|টেবিলে|টেবিলের নিচে|টেবিল এর নিচে|ড্রয়ার|অফিসের ভেতর|অফিসের ভিতরে|সরাসরি (বলে|চায়|চাইল|চাই|দাবি)|মুখ ফুটে|সরাসরি"),
    "roadside_checkpoint": R(r"রাস্তা|রাস্তায়|রাস্তার পাশে|চেকপোস্ট|গাড়ি থামিয়ে|থামিয়ে|আটক|মোড়ে|সিগনাল|সিগন্যাল|হাইওয়ে|মহাসড়ক|ব্রিজ|টোল|ঘাট"),
    "phone": R(r"ফোন করে|ফোনে|কল করে|কল দিয়ে|হোয়াটসঅ্যাপ|ইমো|whatsapp|\bphone\b|\bcall\b|মোবাইলে"),
    "mobile_banking": R(r"বিকাশ|বিকাস|নগদ|রকেট|\bbkash\b|\bnagad\b|\brocket\b|মোবাইল ব্যাংকিং|মোবাইল ব্যাংকিং|এমএফএস"),
    "broker_outside": R(r"অফিসের (সামনে|বাইরে|বাহিরে|পাশে)|বাইরে ছিল|বাইরের (দোকান|লোক)|সামনের দোকান|সামনে দোকান|কম্পিউটারের দোকান|ফটোকপির দোকান|ফটোকপি দোকান|দোকানে (যেতে|পাঠ|নিয়ে)"),
    "site_visit_field": R(r"পরিদর্শনে|ভিজিটে|ভিজিট করে|সরেজমিনে|মাঠে|সার্ভে করতে|তদন্তে (এসে|আসে)|বাসায় এসে|প্রতিষ্ঠানে এসে|কারখানায় এসে|দোকানে এসে|গোডাউনে|শোরুমে এসে|ফিল্ডে"),
    "gate_access": R(r"গেটে|গেইটে|ঢুকতে|ঢোকার|দেখা করতে|সাক্ষাৎ|সাক্ষাত|ভিজিটর|visitor|ভেতরে যেতে|ভিতরে যেতে"),
    "online_system": R(r"অনলাইনে (আবেদন|করে|করার)|অনলাইন সিস্টেম|পোর্টাল|ওয়েবসাইট|সার্ভার|সাইট|portal|\bonline\b"),
}

# ---------------------------------------------------------------- pattern flags
FLAGS = {
    "f_obstruction": R(r"কাগজ(পত্র)?\s*(ঠিক|সঠিক)\s*(নাই|নেই|না|নয়)|ভুল (ধরে|ধরার|দেখিয়ে|দেখায়|বের)|অযুহাত|অজুহাত|বাহানা|ফেরত (দেয়|দিল|পাঠায়)|রিজেক্ট|বাতিল (করে|করছে|করেছে|করল)|জমা (নেয় না|নিচ্ছে না|নেয়নি|নিতে চায় না)|আবেদন (নেয় না|গ্রহণ করে না|গ্রহণ করেনি)|সমস্যা (আছে|দেখায়)|ঝামেলা (করে|করছে|দেখায়)|না করে দেয়|কাজ করে না|হবে না|সম্ভব না|reject|problem dekhay|jhamela"),
    "f_delay": R(r"ঘুরা(য়|ল|চ্ছে|ইতে|নো|ইয়া)|ঘুরতে|দিনের পর দিন|মাসের পর মাস|বার বার|বারবার|বারংবার|আজ কাল|আজকাল|অপেক্ষা|দেরি|দেরী|ঝুলিয়ে|ফেলে রাখ|পড়ে (আছে|রয়েছে)|সময় (লাগবে|লাগে)|অনির্দিষ্ট|কয়েক মাস|সপ্তাহ|হয়রানি|হয়রানী|ghura|ghurai|deri|delay"),
    "f_threat": R(r"ভয় দেখ|হুমকি|হুমকী|মামলা (দিব|দিয়ে|দেবে|করে দেব|করব|করে দিব)|জেলে (দিব|দেব|পাঠা|ঢুকা)|জেল হবে|জেল খাট|ফাঁসিয়ে|ফাসিয়ে|বন্ধ করে দিব|বন্ধ করে দেব|লাইসেন্স বাতিল|সিলগালা|সিল করে|ক্ষতি করব|দেখে নেব|দেখে নিব|ধরে নিয়ে|থানায় নিয়ে|ডিটেন|চালান দেব|চালান করে দেব|threat"),
    "f_percentage_cut": R(r"\d+\s*%|\d+\s*শতাংশ\s*(হারে|কমিশন|টাকা|করে|ঘুষ)|\d+\s*(পার্সেন্ট|পারসেন্ট|percent)|পার্সেন্টেজ|পারসেন্টেজ|percentage|কমিশন(?!ার)"),
    "f_pay_to_skip": R(r"সিরিয়াল ছাড়া|সিরিয়াল না|লাইন ছাড়া|লাইনে না|দ্রুত|জরুরি|জরুরী|তাড়াতাড়ি|দ্রুততম|স্পিড মানি|speed money|urgent|\bfast\b|তাৎক্ষণিক|একদিনে|এক দিনে|ওইদিনই|সঙ্গে সঙ্গে"),
    "f_inflated_fee": R(r"সরকারি (ফি|ফী|রেট|খরচ)|সরকার নির্ধারিত|সরকারী (ফি|ফী|রেট|খরচ)|নির্ধারিত (ফি|ফী|মূল্য|খরচ)|রসিদ|রশিদ|ভাউচার|অতিরিক্ত|বাড়তি|বেশি (টাকা|নেয়|নিল)|ফি-র বাইরে|ফি এর বাইরে|ফি ছাড়াও|ফি বাবদ|কাগজে.{0,30}টাকা|official fee|extra"),
    "f_tea_money": R(r"চা\s*(খাওয়া|খাব|খেতে|খরচ|পানি|-পানি|নাস্তা|-নাস্তা)|চা-?পানি|মিষ্টি|মিস্টি|নাস্তা|নাশতা|বকশিশ|বখশিশ|বখসিস|খুশি|সম্মানী|উপহার|টিফিন|খরচ বাবদ|অফিস খরচ|কিছু (দেন|দিন|দিতে)|কিছু দিয়ে যান|একটু (দেখেন|দেখুন)|cha khawa|chaa|misti|tea money"),
    "f_no_receipt": R(r"রসিদ (দেয়নি|দেয় না|দেয়নি|দিল না|ছাড়া)|রশিদ (দেয়নি|দেয় না|ছাড়া)|রিসিট (দেয়নি|ছাড়া)|কোনো রসিদ|কোন রসিদ|receipt"),
    "f_repeat_demand": R(r"আবার (চাইল|চায়|টাকা|দাবি|দিতে)|পুনরায় (টাকা|চাইল|দাবি)|আরও (টাকা|চাইল|দাবি)|আরো (টাকা|চাইল|দাবি)|আবারও|দ্বিতীয়বার|দ্বিতীয় বার|দুইবার|দুবার|কয়েকবার|পরে আবার|এরপর আবার|আবার.{0,15}ঘুষ"),
    "f_hint_not_direct": R(r"ইঙ্গিত|ঈঙ্গিত|ইশারা|বুঝিয়ে|বুঝে নিন|বুঝে নেন|ঘুরিয়ে|আকারে ইঙ্গিতে|ইশারা ইঙ্গিতে|কিছু দিতে হবে|কিছু লাগবে|খরচ লাগবে|খরচ আছে|খরচাপাতি|বুঝতে পারি|বুঝলাম"),
    "f_refused_to_pay": R(r"দিইনি|দেইনি|দিই নাই|দেই নাই|দেইনা|দিতে রাজি হইনি|রাজি হইনি|রাজি হইনি|অস্বীকার|প্রত্যাখ্যান|দিতে চাইনি|দিতে চাই নাই|দিব না|দেব না|দিবো না|দিলাম না|দেয়নি|টাকা ছাড়াই"),
    "f_paid": R(r"দিয়েছি|দিছি|দিয়েছিলাম|দিলাম|দিতে হয়েছে|দিতে হল|দিতে হলো|দিয়ে দিলাম|দিয়ে দিই|পরিশোধ করি|পরিশোধ করেছি|দিতে বাধ্য হ|দিয়ে করাতে|দিয়ে করি|টাকা দিয়ে|দিয়েই|payment|paid|dilam|diyechi|diyeci|dici|dilam"),
    "f_after_service_done": R(r"কাজ (শেষ|হওয়ার)\s*পর|কাজ হয়ে (গেলে|যাওয়ার)|কাজ হওয়ার পর|দেওয়ার পর.{0,20}(টাকা|চায়|চাইল)|হাতে পাওয়ার (আগে|পর)|সনদ (নিতে|দিতে|হাতে)|সার্টিফিকেট (নিতে|হাতে)|ডেলিভারি (নিতে|দিতে)|সই করার পর|স্বাক্ষর করার পর|সাইন করার পর|আগে.{0,10}কাজ"),
}

# ---------------------------------------------------------------- one label per report (ordered, first match wins)
# (label, test function on (flags, initiator, channels, actors))
def pick_pattern(f, init, ch, actors):
    if init == "broker":
        return "broker_route", "broker words (dalal/agent route)"
    if "roadside_checkpoint" in ch and ("police" in actors):
        return "roadside_stop", "police + roadside words"
    if f["f_obstruction"] and (init == "official_demanded" or f["f_hint_not_direct"] or "aside_private" in ch):
        return "obstruct_then_ask", "obstruction words + demand/hint"
    if f["f_delay"] and init == "official_demanded":
        return "delay_then_ask", "delay words + demand"
    if "aside_private" in ch:
        return "aside_private_ask", "aside/private words"
    if f["f_percentage_cut"]:
        return "percentage_cut", "percent/commission words"
    if "gate_access" in ch and (f["f_paid"] or init == "official_demanded"):
        return "pay_for_access", "gate/meeting-access words + payment"
    if f["f_threat"]:
        return "threat_or_penalty", "threat words"
    if f["f_after_service_done"]:
        return "ask_after_service", "after-service words"
    if f["f_tea_money"]:
        return "small_gift_tea_money", "tea/sweets/expenses words"
    if f["f_pay_to_skip"] and init in ("citizen_asked_or_offered", "unclear"):
        return "pay_to_speed_up", "urgency words, citizen side"
    if init == "citizen_asked_or_offered":
        return "citizen_asked_first", "citizen asked/offered"
    if f["f_inflated_fee"] and init == "official_demanded":
        return "extra_on_top_of_fee", "extra/official-fee words + demand"
    if init == "official_demanded":
        return "direct_demand", "demand words only"
    return "short_or_vague", ""


def find_all(patterns, text):
    return [k for k, p in patterns.items() if p.search(text)]


def first_actor(text, found):
    best, pos = None, 10**9
    for a in found:
        m = ACTORS[a].search(text)
        if m and m.start() < pos:
            best, pos = a, m.start()
    return best or ""


def analyse(title, description):
    text = norm(" ".join([str(title or ""), str(description or "")]))
    actors = find_all(ACTORS, text)
    # these two are weak words on their own; keep only if clearly used as actor words
    flags = {k: bool(p.search(text)) for k, p in FLAGS.items()}
    channels = find_all(CHANNELS, text)

    if BROKER_ROUTE.search(text):
        init = "broker"
        if "broker" not in actors:
            actors.append("broker")
    elif CITIZEN_ASKED.search(text) and not re.search(r"আমাকে.{0,20}(চাইল|বলল|দাবি)", text):
        init = "citizen_asked_or_offered"
    elif OFFICIAL_DEMAND.search(text):
        init = "official_demanded"
    else:
        init = "unclear"

    label, why = pick_pattern(flags, init, channels, actors)
    return {
        "actors": ";".join(actors),
        "first_actor": first_actor(text, actors),
        "initiator": init,
        "channels": ";".join(channels),
        **flags,
        "pattern_type": label,
        "mech_evidence": why,
        "text_len": len(text),
    }


def enrich(df):
    rows = [analyse(r.title, r.description) for r in df.itertuples()]
    return pd.concat([df.reset_index(drop=True), pd.DataFrame(rows)], axis=1)


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "ghush_enriched.csv"
    dst = sys.argv[2] if len(sys.argv) > 2 else "ghush_mechanism.csv"
    df = pd.read_csv(src, encoding="utf-8-sig")
    out = enrich(df)
    out.to_csv(dst, index=False, encoding="utf-8-sig")
    print(len(out), "reports ->", dst)
    for c in ["initiator", "first_actor", "pattern_type"]:
        print("\n" + c)
        print(out[c].value_counts().to_string())
    print("\nflags (share of reports)")
    print(out[[c for c in out.columns if c.startswith("f_")]].mean().round(3).to_string())
