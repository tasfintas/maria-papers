"""
ghush_enrich.py - add service / institution / life_stage columns to ghush_reports.csv

Why this exists: the site's "office" dropdown is too coarse. 31% of reports sit in
"other public services", and that bucket mixes birth registration, police, NID,
utilities, contractor bills and more. So we read what the report SAYS instead.

How it decides (first match wins, most specific rule first):
  1. look at the title only      (titles are short and specific)
  2. look at title + description + place
  3. fall back to the office the reporter picked on the site
  4. otherwise: unclassified
The column `service_basis` records which of these steps decided, so every label can be audited.

Usage:  python ghush_enrich.py ghush_reports.csv ghush_enriched.csv
"""
import re
import sys
import unicodedata

import pandas as pd

ZERO_WIDTH = re.compile("[​‌‍﻿]")


def norm(s):
    """Make text comparable: unicode NFC, drop zero-width chars, collapse spaces, lowercase."""
    if not isinstance(s, str):
        return ""
    s = unicodedata.normalize("NFC", s)
    s = ZERO_WIDTH.sub("", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def rx(pattern):
    # patterns go through the same normalization as the text, or they would never match
    return re.compile(unicodedata.normalize("NFC", pattern))


# (service, institution, life_stage, pattern, scope)
# scope "any"   -> may match title or description
# scope "title" -> title only (used where the word is too common inside descriptions)
RULES = [
    ("death_certificate_inheritance", "city_corp_or_union", "Death & inheritance",
     r"মৃত্যু\s*(সনদ|নিবন্ধন|সার্টিফিকেট|সনদপত্র)|death\s*cert|ওয়ারিশ|ওয়ারেশ|উত্তরাধিকার\s*সনদ|দাফন|মরদেহ", "any"),
    ("death_benefit_claim", "accounts_office", "Death & inheritance",
     r"মৃত্যুর\s*পর.{0,60}(চাকুরি|চাকরি|পেনশন|বেতন|ভাতা|ফান্ড)|mrittur.{0,40}(chakur|pension)|পারিবারিক পেনশন", "any"),
    ("birth_registration", "union_parishad_or_city_corp", "Birth",
     r"জন্ম\s*-?\s*(নিবন্ধন|নিবন্ধ|নিবন্দন|সনদ|সার্টিফিকেট)|জন্মনিবন্ধন|জম্মনিবন্ধ|birth\s*(cert|reg)|jonmo|janmo", "any"),
    ("police_clearance", "police", "Work & career",
     r"পুলিশ\s*ক্লিয়ারেন্স|police\s*clearance|ক্লিয়ারেন্স\s*সনদ|চারিত্রিক|পুলিশ\s*ভেরিফিকেশন|police\s*verification|character\s*cert", "any"),
    ("passport_police_verification", "police_special_branch", "Travel & abroad",
     r"(পাসপোর্ট|passport).{0,40}(ভেরিফি|verif|পুলিশ|police)|(ভেরিফি|verif|পুলিশ|police).{0,40}(পাসপোর্ট|passport)", "any"),
    ("passport_application", "passport_office", "Travel & abroad",
     r"পাসপোর্ট|পাসপোট|পাচপোর্ট|পার্সপোর্ট|পাসপোরট|passport", "any"),
    ("nid_service", "election_commission", "Adult ID",
     r"এনআইডি|এন\s*-?\s*আই\s*-?\s*ডি|\bnid\b|ভোটার|জাতীয় পরিচয়|নির্বাচন (অফিস|কমিশন)", "any"),
    ("marriage_registration", "marriage_registrar", "Marriage",
     r"বিবাহ|নিকাহ|কাজী|কাবিন|marriage|তালাক|ডিভোর্স|divorce", "title"),
    ("forest_environment", "forest_department", "Business",
     r"ফরেস্ট|বন\s*বিভাগ|বনবিভাগ|বন অধিদপ্তর|\bforest\b|কাঠ পারমিট|গাছ কাটা", "any"),
    ("marriage_registration", "marriage_registrar", "Marriage",
     r"নিকাহ\s*নামা|নিকাহনামা|কাজী অফিস|nikah|কাবিননামা", "any"),
    ("driving_licence_vehicle", "brta", "Driving & vehicles",
     r"ড্রাইভিং|ডাইভিং|ড্রাভিং|ড্রাইভার|driving|ব্লু\s*বুক|blue\s*book|ফিটনেস|রুট পারমিট|বিআরটিএ|brta|লার্নার|learner|new licen[sc]e|গাড়ির|মোটরসাইকেল|নাম্বার প্লেট|নম্বর প্লেট|ট্যাক্স টোকেন|টেক্স টোকেন|মালিকানা পরিবর্তন|বাইকের", "any"),
    ("traffic_police", "traffic_police", "Driving & vehicles",
     r"ট্রাফিক|traffic|সার্জেন্ট|হেলমেট|helm[ae]t|হেলমেট", "any"),
    ("holding_tax", "city_corp_or_pourashava", "Home & land",
     r"হোল্ডিং|holding\s*tax|পৌর\s*কর", "any"),
    ("land_tax", "land_office", "Home & land",
     r"খাজনা|ভূমি উন্নয়ন কর|ভূমি কর|ভুমি কর|দাখিলা|land\s*tax|khajna|khajana", "any"),
    ("land_mutation", "land_office", "Home & land",
     r"নাম\s*জারী?|নামজারি|নামজারী|খারিজ|mutation|namjari|namzari|mutration|খান্না|খতিয়ান|পর্চা|রেজিস্টার\s*[২2]|রেজিস্ট্রার\s*[২2]|register\s*2|মিস\s*কেইস|মিসকেস", "any"),
    ("land_registration_deed", "sub_registry", "Home & land",
     r"দলিল|সাব\s*-?\s*রেজিস্ট্র|সাব\s*-?\s*রেজিষ্ট্র|জমি\s*রেজি|জমির\s*রেজি|কবলা|dolil|\bdeed\b|রেজিস্ট্রার কার্যালয়|রেজিস্ট্রি করতে|রেজিষ্ট্রি", "any"),
    ("drug_food_regulator", "drug_or_food_authority", "Business",
     r"ড্রাগ\s*লাইসেন্স|drug\s*licen|ঔষধ প্রশাসন|ঔষধ প্রশাসন|খাদ্য নিরাপত্তা|বিএসটিআই", "any"),
    ("food_distribution", "food_office", "Utilities & civic",
     r"খাদ্য অফিস|খাদ্য গুদাম|খাদ্য কর্মকর্তা|food office|ওএমএস|\boms\b|কেরোসিন|রেশন ডিলার", "any"),
    ("trade_licence", "city_corp_or_union", "Business",
     r"ট্রেড\s*লাইসেন্স|ট্রেড লাইসেন্স|trade\s*licen[cs]e|trade licen|ট্রেড", "any"),
    ("factory_fire_inspection", "inspection_regulator", "Business",
     r"ফায়ার|fire\s*service|কলকারখানা|কল কারখানা|লে-আউট প্ল্যান|লে আউট প্ল্যান|layout plan|boiler|বয়লার|বিএসটিআই|bsti|পরিদর্শন অধিদপ্তর|পরিবেশ অধিদপ্তর|বিইআরসি|berc|বিস্ফোরক", "any"),
    ("cooperative_ngo_registration", "registration_authority", "Business",
     r"সমবায়|এনজিও|\bngo\b|যুব সংগঠন|ফিল্ম ক্লাব|ফিল্ম সোসাইটি|সমিতি নিবন্ধন|সংগঠন নিবন্ধন|সমিতির নিবন্ধন", "any"),
    ("customs_port", "customs_port", "Business",
     r"কাস্টমস|customs|শুল্ক|বন্দর|কনটেইনার|সিএন্ডএফ|c&f|বিল অব এন্ট্রি", "any"),
    ("vat_tax", "tax_office", "Business",
     r"ভ্যাট|\bvat\b|আয়কর|ইনকাম ট্যাক্স|income tax|\btin\b|টিআইএন|কর অফিস|কর অঞ্চল|এনবিআর|\bnbr\b|ট্যাক্স", "any"),
    ("tender_contractor_bill", "public_works", "Business",
     r"টেন্ডার|\btender\b|ঠিকাদার|contractor|\blged\b|এলজিইডি|পিডব্লিউডি|\bpwd\b|গণপূর্ত|সড়ক ও জনপথ|কাজের বিল|percentage|পারসেন্টেজ", "any"),
    ("bank_loan", "bank_or_financial", "Money & loans",
     r"ঋণ|লোন|\bloan\b|হাউজ বিল্ডিং ফাইন|hbfc", "any"),
    ("bank_loan", "bank_or_financial", "Money & loans",
     r"ব্যাংক|\bbank\b", "title"),
    ("building_plan_housing", "housing_authority", "Home & land",
     r"রাজউক|rajuk|নকশা অনুমোদন|বিল্ডিং প্ল্যান|ভবন (নির্মাণ|অনুমোদন)|গৃহায়ন|ফ্ল্যাট|প্লট বরাদ্দ|building plan", "any"),
    ("electricity", "electricity_utility", "Utilities & civic",
     r"বিদ্যুৎ|বিদ্যুত|ইলেকটি|\bmeter\b|bidyut|ডেসকো|desco|dpdc|ডিপিডিসি|মিটার|electric|বিউবো|ট্রান্সফরমার", "any"),
    ("water_gas", "water_gas_utility", "Utilities & civic",
     r"ওয়াসা|wasa|পানির লাইন|পানি সংযোগ|পানির সংযোগ|গ্যাস|তিতাস|titas|জালালাবাদ|গভীর নলকূপ", "any"),
    ("railway", "bangladesh_railway", "Utilities & civic",
     r"রেলওয়ে|রেল স্টেশন|রেলস্টেশন|রেল সেবা|railway|কমলাপুর|ট্রেনের টিকি|ট্রেন টিকি|রেলের", "any"),
    ("post_office_savings", "post_office", "Money & loans",
     r"পোস্ট অফিস|পোষ্ট অফিস|ডাকঘর|post office|সঞ্চয় ?পত্র", "any"),
    ("overseas_worker", "overseas_employment", "Travel & abroad",
     r"বিএমইটি|bmet|ইমিগ্রেশন|immigration|ভিসা|\bvisa\b|বিদেশ|বহির্গমন|ম্যানপাওয়ার|manpower|ফিঙ্গার|ওয়েজ আর্নার|প্রবাসী কল্যাণ", "any"),
    ("hospital_service", "hospital", "Health",
     r"হাসপাতাল|ডাক্তার|চিকিৎসা|রোগী|রোগির|ওষুধ|সিজার|ডেলিভারি|অপারেশন|ব্যান্ডেজ|বেড(?!়)|বেট(?!়)|কেবিন|\bicu\b|আইসিইউ|ইনজেকশন|ডেঙ্গু|এক্সরে|ক্লিনিক|স্বাস্থ্য|সিভিল সার্জন|civil surgeon|ডায়াগনস্টিক|diagnostic|hospital|doctor|medical|মেডিকেল|নার্স|ওয়ার্ড বয়", "any"),
    ("pension", "accounts_office", "Retirement & old age",
     r"পেনশন|pension|অবসর|retire|আনুতোষিক|গ্র্যাচুইটি|gratuity|ল্যাম্পগ্রান্ট|লাম্পগ্রান্ট", "any"),
    ("social_allowance", "union_parishad_or_social_welfare", "Retirement & old age",
     r"বয়স্ক ভাতা|ভাতা|বিধবা|প্রতিবন্ধী|মুক্তিযোদ্ধা|সমাজসেবা|সমাজ সেবা|ভিজিডি|ভিজিএফ|রেশন কার্ড|টিসিবি|ত্রাণ|অনুদান|চালের কার্ড|হতদরিদ্র", "any"),
    ("salary_arrears_accounts", "accounts_office", "Work & career",
     r"বকেয়া|এরিয়ার|জিপিএফ|\bgpf\b|ইনক্রিমেন্ট|বেতন|বিল পাস|হিসাব(রক্ষণ)? অফিস|একাউন্টস|অডিট|\baudit\b", "any"),
    ("student_exam_certificate", "school_college_or_board", "School & exams",
     r"ফরম\s*পূরণ|ফরমপূরণ|ফরম\s*পুরণ|এডমিট|প্রবেশপত্র|ভর্তি|পরীক্ষা|প্রশংসাপত্র|প্রসংশাপত্র|মার্কশীট|মার্কশিট|ট্রান্সক্রিপ্ট|রেজাল্ট|উপবৃত্তি|বৃত্তি|testimonial|\badmit\b|\bexam\b|admission", "any"),
    ("court", "court", "Police & courts",
     r"লেবার কোর্ট|লেবার কোট|শ্রম আদালত|labou?r court", "any"),
    ("govt_job_appointment", "employer_department", "Work & career",
     r"নিয়োগ|চাকরি|চাকুরি|চাকুরী|চাকরির|পোস্টিং|পদোন্নতি|বদলি|বদলী|স্থায়ীকরণ|প্রেষণ|এমপিও|\bmpo\b|ইনডেক্স|মাতৃত্বকালীন ছুটি|\bjob\b|appointment|transfer", "any"),
    ("education_sector_other", "school_college_or_board", "School & exams",
     r"স্কুল|কলেজ|বিদ্যালয়|বিশ্ববিদ্যালয়|মাদ্রাসা|শিক্ষক|শিক্ষিকা|\bschool\b|\bcollege\b|university|\bteacher\b", "any"),
    ("police_general", "police_thana", "Police & courts",
     r"থানা|পুলিশ|police|জিডি|জিটি|এজাহার|\bgd\b|uddhar|সাধারণ ডায়েরি|এসআই|ওসি|কনস্টেবল|র[‍]?্যাব|রিমান্ড|গ্রেফতার|গ্রেপ্তার|ফৌজদারি", "any"),
    ("court", "court", "Police & courts",
     r"আদালত|কোর্ট|জজ|নাজির|পেশকার|হাজিরা|জামিন|দস্তখত|সমন|নোটিশ জারি|adalot|adalote|\bcourt\b|মামলা|উকিল|বিচার|dostokhot", "any"),
    ("land_other", "land_office", "Home & land",
     r"জমি|জমির|ভূমি|ভুমি|দখল|সার্ভে|জরিপ|অধিগ্রহণ|ক্ষতিপূরণ|সীমানা|তহশিল|এসি ল্যান্ড|\bac land\b", "any"),
    ("extortion_chanda", "no_office_local_actors", "Business",
     r"চাঁদা|চাদা|\bchanda\b", "title"),
    ("trade_licence", "city_corp_or_union", "Business",
     r"licen[cs]e|লাইসেন্স|লাইসেন্সিং|লাইন্সেস", "late"),
    ("local_certificate", "union_parishad_or_pourashava", "Utilities & civic",
     r"নাগরিক সনদ|নাগরিকত্ব|প্রত্যয়ন|হেডম্যান|সনদ|সার্টিফিকেট|certificate|ইউনিয়ন পরিষদ|চেয়ারম্যান|মেম্বার|কাউন্সিলর|পৌরসভা|ইউনিয়ন", "any"),
]

COMPILED = [(s, i, st, rx(p), scope) for (s, i, st, p, scope) in RULES]

# Used only when no rule matched: the office the reporter chose on the site
OFFICE_FALLBACK = {
    "ভূমি অফিস": ("land_other", "land_office", "Home & land"),
    "হিসাবরক্ষণ অফিস": ("salary_arrears_accounts", "accounts_office", "Work & career"),
    "কর অফিস": ("vat_tax", "tax_office", "Business"),
    "কাস্টমস অফিস": ("customs_port", "customs_port", "Business"),
    "ট্রাফিক পুলিশ": ("traffic_police", "traffic_police", "Driving & vehicles"),
    "বিআরটিএ": ("driving_licence_vehicle", "brta", "Driving & vehicles"),
    "পাসপোর্ট অফিস": ("passport_application", "passport_office", "Travel & abroad"),
    "সিটি কর্পোরেশন": ("city_corp_other", "city_corp_or_pourashava", "Utilities & civic"),
    "সাব-রেজিস্ট্রি অফিস": ("land_registration_deed", "sub_registry", "Home & land"),
    "শিক্ষা অফিস": ("education_sector_other", "education_office", "School & exams"),
    "সরকারি হাসপাতাল": ("hospital_service", "hospital", "Health"),
}
OFFICE_FALLBACK = {unicodedata.normalize("NFC", k): v for k, v in OFFICE_FALLBACK.items()}


def classify(title, description, place, office):
    t = norm(title)
    full = " ".join([t, norm(description), norm(place)])

    for service, inst, stage, pat, scope in COMPILED:        # step 1: title only
        if scope != "late" and t and pat.search(t):
            return service, inst, stage, "title"
    for service, inst, stage, pat, scope in COMPILED:        # step 2: title + description + place
        if scope == "any" and pat.search(full):
            return service, inst, stage, "text"
    for service, inst, stage, pat, scope in COMPILED:        # step 2b: weak "late" rules, last resort
        if scope == "late" and pat.search(full):
            return service, inst, stage, "text"
    key = unicodedata.normalize("NFC", office) if isinstance(office, str) else ""
    if key in OFFICE_FALLBACK:                               # step 3: the office dropdown
        service, inst, stage = OFFICE_FALLBACK[key]
        return service, inst, stage, "office"
    return "unclassified", "unclassified", "Unclear", "none"


def enrich(df):
    out = df.copy()
    results = [classify(r.title, r.description, r.place, r.office) for r in out.itertuples()]
    out["service"], out["institution"], out["life_stage"], out["service_basis"] = zip(*results)
    out["title_norm"] = out["title"].map(norm)
    out["desc_has_bengali"] = out["description"].fillna("").str.contains(r"[ঀ-৿]")
    return out


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "ghush_reports.csv"
    dst = sys.argv[2] if len(sys.argv) > 2 else "ghush_enriched.csv"
    df = pd.read_csv(src, encoding="utf-8-sig")
    out = enrich(df)
    out.to_csv(dst, index=False, encoding="utf-8-sig")
    print(f"{len(out)} reports -> {dst}")
    print("\nhow each label was decided:")
    print(out.service_basis.value_counts().to_string())
    print("\nreports per life stage:")
    print(out.life_stage.value_counts().to_string())
