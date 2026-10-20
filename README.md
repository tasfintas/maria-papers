# Maria's Papers

An animated, tap-through story of one woman's life told through the bribes asked at each stage of it, from a birth certificate to a death certificate.

**Maria is a composite, not a real person.** Every amount, delay and trick in the story comes from real reports on [GhushSite](https://ghush.site), a public ledger where people in Bangladesh anonymously report bribes they were asked for.

It is also a sample of the work I offer NGOs: **I take your data and turn it into a story or a presentation people can read and share.**

**How to use it:** 16 steps, one per life stage. Left: an animated scene (who is in the room, who asks, who pays). Right: the story, the amount asked vs. the amount paid, and one real detail from the reports. Use Prev / Next, the arrow keys, or swipe.

---

## Where the data comes from

| | |
|---|---|
| **Source** | [ghush.site](https://ghush.site), an anonymous public ledger of bribery reports from Bangladesh. Reports are mostly in Bengali, some in English or mixed "Banglish". |
| **What is on each report** | Office (a dropdown the reporter picks), amount in BDT, outcome (paid / refused / pending), a verification status, a title, place and division, a free-text description, and how many people confirmed it. |
| **What I collected** | 5,405 reports, the newest ones the site listed: posted roughly **2 Sep to 6 Oct 2026**, collected on **8 Oct 2026** from the public listing pages with a Playwright scraper. The site shows relative times ("3 days ago"), so posted dates are approximate. |
| **Outcomes** | 3,850 paid, 1,242 refused, 313 pending. |
| **Used for stories** | Only reports with a written description of at least 140 characters (3,570 of 5,405) and no personal-information flag. 248 reports are flagged by the site as containing personal info and are never used. |
| **Not in this repo** | The raw report file. This repo holds only the report IDs behind each scene (`data/maria_story.csv`). Please check GhushSite's terms and contact its maintainers before redistributing any report text. |

## How we built it, step by step

**0. The questions first.** Before touching the data I wrote down: (1) *What am I trying to understand?* How a bribe actually happens at each stage of a life, not just how big it is. (2) *How do I think it works in real life, so what should I see if I'm right?* People go for a task, get sent around, get frustrated, and then someone offers a shorter path, often with several steps. (3) *What is the smallest piece of data that would show me wrong?* If that run-around pattern is rare, the story is built on a few lucky reports. After each step I checked whether the thinking or the data surprised me.

**1. Ingest.** Scrape the public listing pages into one CSV, `ghush_reports.csv` (16 columns). Keep the scrape time on every row.

**2. Enrich: what is this report about?** (`pipeline/ghush_enrich.py`)
The site's own "office" dropdown is too coarse: about 31% of reports sit in "other public services", a bucket that mixes birth registration, police, NID, utilities, contractor bills and more. So the script reads what the report *says*.
- Rule-based text matching over Bengali, English and Banglish, with Unicode normalisation (NFC) and zero-width characters removed.
- Rules run in order and the first match wins, with a fall-through: title only, then title + description + place, then the office dropdown, then `unclassified`. A `service_basis` column records which step decided.
- Output: `service` (e.g. `passport_application`), `institution`, and one of **15 life stages** (Birth, School & exams, Health, Adult ID, Driving & vehicles, Travel & abroad, Marriage, Work & career, Business, Home & land, Money & loans, Utilities & civic, Police & courts, Retirement & old age, Death & inheritance).
- Result: 113 of 5,405 reports (2%) stay `Unclear`.

| Life stage | Reports | | Life stage | Reports |
|---|---:|---|---|---:|
| Home & land | 1,456 | | Utilities & civic | 307 |
| Travel & abroad | 675 | | Health | 275 |
| Work & career | 536 | | Retirement & old age | 196 |
| Driving & vehicles | 448 | | School & exams | 191 |
| Business | 445 | | Birth | 150 |
| Police & courts | 346 | | Adult ID | 146 |
| Unclear | 113 | | Money & loans | 66 |
| Death & inheritance | 33 | | Marriage | 22 |

**3. Read the mechanism: how did the bribe happen?** (`pipeline/ghush_mechanism.py`)
A second pass over the description adds a small codebook: who is mentioned first (`first_actor`), who asked (`initiator`), through which channel (counter, aside, broker, roadside), and one `pattern_type` such as `broker_route`, `obstruct_then_ask`, `delay_then_ask`, `aside_private_ask`, `pay_to_speed_up`, `extra_on_top_of_fee`. Again ordered rules, first match wins, with the matching text kept as evidence (`mech_evidence`).

**4. Validate by sampling.** I read samples by hand and fixed what I found. Estimated accuracy: roughly **80 to 85% for service labels** and **70 to 75% for patterns**. Bugs the sampling caught, for example: `পানি` (water) inside `কোম্পানি` (company) mislabelled a customs report as water; `টিকা` (vaccine) inside a place name; `রেশন` inside `কর্পোরেশন`; `জেল` (jail) matching `জেলা` (district); `শতাংশ` meaning land area, not percent. Each became a rule fix.

**5. Aggregate per life stage.** Median amount **asked** (from refused and pending reports) and median amount **paid** (from paid reports), plus the most common pattern. Medians, because the amounts have extreme outliers. About 2,300 paid and 900 asked reports sit behind the 16 scenes' medians.

**6. Pick the story.** For each stage I chose a representative service (passport for travel, trade licence for business, land mutation for home and land, and so on), took its medians so the numbers stay consistent across the story, and wrote the composite scene. I then added the most vivid real details from the reports (a dalal's own code typed where the email should go, a tip at every handover in a delivery ward, a sweeper who runs the land office from his shop) as clearly labelled single-report details. Output: `data/maria_story.csv`.

**7. Serve.** `site/build.py` turns the story table into `data/story.json` and a single static `index.html`: no server, no tracking, nothing to host but GitHub Pages. The characters, scenes and animations are original vector art drawn in code (`site/`), in a flat style with a palette inspired by [The Pudding's IVF journey](https://pudding.cool/2026/03/ivf).

## Read this before quoting a number

- **Selection bias.** Ghush records people who felt wronged. Smooth, arranged bribes are probably under-reported. This shows how bribes are *asked*, not how often they happen.
- **Asked vs. paid are different groups.** The "asked" median comes from refused and pending reports, the "paid" median from paid reports, so asked can be lower than paid, and gaps of 10x are real (people report being asked far more than they finally pay).
- **Thin stages.** Marriage (22), Money & loans (66) and Death & inheritance (33) have few reports. Scene 14 rests on a single report and has no median.
- **The "real detail" lines are single stories**, paraphrased. IDs are in `data/story.json`.
- **What `amount_bdt` means** (final amount paid vs. amount demanded) is inferred from how the site records it, not confirmed with its maintainers.
- **Classification is rules, not a model.** About a fifth of service labels and a quarter of patterns may be wrong.

## Repo layout

```
index.html           the page (built)
data/maria_story.csv the 16-scene table: story, medians, report counts, source report IDs
data/story.json      the same, as the page reads it
pipeline/            ghush_enrich.py, ghush_mechanism.py (need the raw CSV, not included)
site/                build.py, scenes.py, chars.py, chars2.py, template.html
```

## Run it

```bash
pip install pandas
python site/build.py      # rebuilds index.html and data/story.json from data/maria_story.csv
```

Open `index.html` in a browser. It is hosted with GitHub Pages (Settings, Pages, deploy from the `main` branch root).

## Credits

Built by Taz with Claude (Anthropic): data work, scenes and code were written together. Characters, scenes and animations are original; no stock art is used. Data: GhushSite. Layout inspiration: The Pudding.
