"""Build phone-sized "I fixed your ad" spec mockups for warm leads.

Each company gets one HTML page (current-ad problem + 2 fixed drafts) and a PNG
per fixed ad, rendered with Playwright. Drafts only; nothing here is live.
"""
import html
import pathlib
import subprocess

OUT = pathlib.Path(__file__).parent

ROOF_SVG = """<svg class="img" viewBox="0 0 500 300" role="img" aria-label="{alt}">
<defs><linearGradient id="g{n}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{sky1}"/><stop offset="1" stop-color="{sky2}"/></linearGradient></defs>
<rect width="500" height="300" fill="url(#g{n})"/>
<polygon points="60,170 250,60 440,170" fill="{roof}"/>
<rect x="95" y="170" width="310" height="130" fill="{wall}"/>
<rect x="140" y="200" width="60" height="50" fill="#7da2c4" stroke="#fff" stroke-width="4"/>
<rect x="300" y="200" width="60" height="50" fill="#7da2c4" stroke="#fff" stroke-width="4"/>
<rect x="225" y="215" width="50" height="85" fill="#6b4a33"/>{extra}
<rect x="0" y="0" width="500" height="44" fill="rgba(0,0,0,.5)"/>
<text x="250" y="29" fill="#fff" font-size="{fs}" font-weight="700" text-anchor="middle" font-family="Arial, sans-serif">{banner}</text>
</svg>"""

YARD_SVG = """<svg class="img" viewBox="0 0 500 300" role="img" aria-label="{alt}">
<rect width="500" height="300" fill="#bcd9ef"/>
<rect y="190" width="500" height="110" fill="#5f9e4a"/>
<rect x="150" y="110" width="200" height="90" fill="#e8dcc6"/>
<polygon points="140,112 250,55 360,112" fill="#4a4f57"/>
<rect x="232" y="145" width="36" height="55" fill="#6b4a33"/>
<path d="M150 230 C 200 205, 300 205, 350 230" stroke="#c9b28f" stroke-width="22" fill="none"/>
<g fill="#3f7d34"><circle cx="90" cy="180" r="34"/><circle cx="410" cy="178" r="38"/><circle cx="130" cy="205" r="16"/><circle cx="375" cy="207" r="16"/></g>
<g fill="#e3703a"><circle cx="175" cy="205" r="7"/><circle cx="195" cy="208" r="7"/><circle cx="305" cy="208" r="7"/><circle cx="325" cy="205" r="7"/></g>
<rect x="0" y="0" width="500" height="44" fill="rgba(0,0,0,.5)"/>
<text x="250" y="29" fill="#fff" font-size="{fs}" font-weight="700" text-anchor="middle" font-family="Arial, sans-serif">{banner}</text>
</svg>"""

TREE_SVG = """<svg class="img" viewBox="0 0 500 300" role="img" aria-label="{alt}">
<rect width="500" height="300" fill="{sky}"/>
<rect y="215" width="500" height="85" fill="#6f9a4c"/>
<rect x="300" y="150" width="150" height="75" fill="#e8dcc6"/>
<polygon points="290,152 375,100 460,152" fill="#4a4f57"/>
<rect x="228" y="120" width="26" height="100" fill="#6b4a33"/>
<path d="M241 150 L205 110 M241 135 L285 95" stroke="#6b4a33" stroke-width="10" stroke-linecap="round"/>
<g fill="{leaf}"><circle cx="241" cy="95" r="55"/><circle cx="195" cy="115" r="38"/><circle cx="290" cy="105" r="40"/></g>
<g fill="#d9822b"><circle cx="120" cy="240" r="6"/><circle cx="140" cy="250" r="5"/><circle cx="90" cy="252" r="6"/><circle cx="165" cy="238" r="5"/></g>{extra}
<rect x="0" y="0" width="500" height="44" fill="rgba(0,0,0,.5)"/>
<text x="250" y="29" fill="#fff" font-size="{fs}" font-weight="700" text-anchor="middle" font-family="Arial, sans-serif">{banner}</text>
</svg>"""

STARS = '<g fill="#f5b50a">' + "".join(
    f'<polygon transform="translate({x},{y})" points="12,0 15.6,8 24,8.8 17.6,14.4 19.6,23.2 12,18.4 4.4,23.2 6.4,14.4 0,8.8 8.4,8"/>'
    for x, y in [(170, 245), (200, 245), (230, 245), (260, 245), (290, 245)]) + "</g>"

SNOW = '<g fill="#fff">' + "".join(
    f'<circle cx="{x}" cy="{y}" r="3"/>' for x, y in [(40, 60), (120, 80), (330, 70), (460, 90), (410, 55), (200, 75)]) + \
    '</g><polygon points="60,170 250,60 440,170 425,170 250,72 75,170" fill="#fff"/>'

COMPANIES = [
    dict(slug="fbc-roofing", name="FBC Roofing", initials="FBC", color="#0b5c8e",
         domain="fbc-hawaii.com", owner="David",
         problem="Your live ads show the headline <b>“{{product.name}}”</b>. It's a template placeholder that never got filled in, so every person who sees the ad sees broken text instead of an offer. It's been running like that since about March.",
         ads=[
             dict(label="Fix 1: Free inspection", art="roof", banner="FREE ROOF CHECK ON OAHU", sky=("#f6c177", "#fbe3c0"), extra="",
                  body="Oahu sun and salt are hard on roofs. ☀️\U0001F30A\n\nWe'll get up there, photograph everything, and tell you straight: repair, replace, or leave it alone.\n\n⭐ 54+ Yelp reviews\n\U0001F4CD Honolulu & all of Oahu\n\nBook your free roof check below. \U0001F447",
                  headline="Free Roof Check + Photo Report", cta="Get quote"),
             dict(label="Fix 2: Reviews", art="roof", banner="OAHU TRUSTS FBC ROOFING", sky=("#8fc5e8", "#dff0fa"), extra=STARS,
                  body="Honolulu homeowners have left FBC 54+ reviews on Yelp. ⭐⭐⭐⭐⭐\n\nLocal crew. Straight answers. A roof built for island weather.\n\nTap below for a free estimate.",
                  headline="Free Estimate From a Local Oahu Roofer", cta="Get quote"),
         ]),
    dict(slug="jt-elite-landscaping", name="JT Elite Landscaping", initials="JT", color="#2f6b2a",
         domain="jtelitelandscaping.com", owner="the owner",
         problem="Your Facebook ad's headline shows <b>“{{product.name}}”</b>. It's a template that never got filled in, so the ad shows broken text instead of your work. It looks like it's been running since about March.",
         ads=[
             dict(label="Fix 1: Fall to spring pre-booking", art="yard", banner="WANT A NEW YARD BY SPRING?",
                  body="The best landscapers in the Seattle area are booked solid by April. \U0001F331\n\nGet your design done this fall and winter, and you're first on the install schedule in spring.\n\n✅ Design, install & maintenance\n\U0001F4CD Seattle area\n\nTap below for a free design consult.",
                  headline="Free Design Consult, Book Spring Now", cta="Get quote"),
             dict(label="Fix 2: Fall cleanup", art="yard", banner="FALL CLEANUP – BOOK NOW",
                  body="Leaves, beds, final mow, gutters cleared. \U0001F342\n\nGet your yard winter-ready before the rain sets in. Spots fill fast in October.\n\nTap below to get on the schedule.",
                  headline="Book Your Fall Cleanup", cta="Get quote"),
         ]),
    dict(slug="reds-roofing", name="Reds Roofing & Renovations", initials="RR", color="#b3261e",
         domain="redsroofingak.com", owner="Karley or Sheldon",
         problem="Your ad crams <b>6 headlines into one</b>: “Alaska Tough Roofing | Alaska Tough Roofing | Alaska Roofing Done Right | …”. Two of them are the same, and nothing tells people why to call before snow flies.",
         ads=[
             dict(label="Fix 1: Beat the snow", art="roof", banner="GET YOUR ROOF CHECKED BEFORE SNOW", sky=("#8fb3d9", "#dfe9f3"), extra=SNOW, fs=18,
                  body="Anchorage: snow load season is weeks away. ❄️\n\nA small leak now is ice-dam damage by January. We'll inspect, photograph everything, and give you a straight answer.\n\n\U0001F396️ Veteran woman-owned, family-run\n⭐ 4.8 stars on Google\n✅ GAF certified · BBB accredited\n\nBook your free roof check below. \U0001F447",
                  headline="Free Pre-Winter Roof Check", cta="Get quote"),
             dict(label="Fix 2: Trust", art="roof", banner="VETERAN WOMAN-OWNED · GAF CERTIFIED", sky=("#1f2a36", "#3b4a5a"), extra=STARS, fs=17,
                  body="Family-run roofers serving Anchorage and Southeast Alaska.\n\nWe show up when we say we will, clean up every nail, and give you a price you can trust.\n\n⭐ 4.8 stars on Google\n✅ GAF certified · BBB accredited\n\nTap below for a free estimate.",
                  headline="Free Estimate From Reds Roofing", cta="Get quote"),
         ]),
    dict(slug="durafoam-roofing", name="Durafoam Roofing", initials="DF", color="#c2410c",
         domain="durafoaminc.com", owner="Tim or Curtis",
         problem="Your roofing ad has <b>no headline at all</b>. People see a picture and scroll past, because nothing tells them what you're offering or why to call now.",
         ads=[
             dict(label="Fix 1: Monsoon damage check", art="roof", banner="MONSOON HIT YOUR ROOF?", sky=("#6b7b8f", "#c9d3dd"), extra="",
                  body="Phoenix monsoon season is rough on flat and foam roofs. ⛈️\n\nPonding water, cracked coating, lifted edges: small problems now turn into leaks when winter rain hits.\n\n\U0001F3E0 Family-owned in Phoenix since 1989\n✅ Foam, tile, shingle & coatings\n\nBook a free roof check below. \U0001F447",
                  headline="Free Post-Monsoon Roof Check", cta="Get quote"),
             dict(label="Fix 2: Recoat vs replace", art="roof", banner="RECOAT BEFORE YOU REPLACE", sky=("#f4a261", "#fde2c4"), extra="",
                  body="If your foam roof is still solid underneath, a recoat can add years for a fraction of the cost of a new roof. ☀️\n\nWe'll tell you honestly which one you need.\n\n\U0001F3E0 Phoenix's foam roofing family since 1989\n\nTap below for a free estimate.",
                  headline="Free Foam Roof Estimate", cta="Get quote"),
         ]),
    dict(slug="cc-services", name="C&C Services", initials="C&C", color="#1d4ed8",
         domain="Schofield / Wausau, WI", owner="Cody",
         problem="You're running <b>12 ads with only 4 headlines</b>, each copied 3 times, so Meta is splitting your budget instead of testing anything. And one says <b>“Now booking for September and October”</b>, which is already out of date.",
         ads=[
             dict(label="Fix 1: Beat the snow", art="roof", banner="ROOF CHECK BEFORE THE SNOW", sky=("#8fb3d9", "#dfe9f3"), extra=SNOW,
                  body="Central Wisconsin: first snow is close. ❄️\n\nStorm damage you can't see from the ground turns into ice dams and leaks by January. We'll inspect, photograph everything, and help with your insurance claim if it's covered.\n\n✅ GAF certified, 15+ years\n\U0001F4CD Wausau, Schofield & nearby\n\nBook your free inspection below. \U0001F447",
                  headline="Free Storm Damage Inspection", cta="Get quote"),
             dict(label="Fix 2: Now booking November", art="roof", banner="NOW BOOKING NOVEMBER", sky=("#c07a3e", "#f1d2ae"), extra="",
                  body="Still need a new roof before winter? We have a few November spots left. \U0001F3E0\n\nInsurance help included, so we handle the paperwork with your adjuster.\n\n✅ GAF certified, 15+ years in Central Wisconsin\n\nTap below to grab a spot.",
                  headline="Get on the November Schedule", cta="Get quote"),
         ]),
    dict(slug="premium-tree-landscape", name="Premium Tree & Landscape", initials="PT", color="#2f6b2a",
         domain="premiumtreeandlandscape.com", owner="Charlie", title="3 draft Facebook ads",
         ads=[
             dict(label="Ad 1: Tree removal before winter", art="tree", banner="GET RISKY TREES DOWN BEFORE WINTER",
                  sky="#9fb7cc", leaf="#5b7f3a", fs=17,
                  body="Nor'easter season is coming. \U0001F32C️\n\nThat dead limb over your roof or driveway is a lot cheaper to take down now than after it comes through the ceiling.\n\n\U0001F333 Tree removal, trimming & climbing\n✅ Fully insured\n\U0001F4CD Falmouth & nearby towns\n\nTap below for a free estimate. \U0001F447",
                  headline="Free Tree Removal Estimate", cta="Get quote"),
             dict(label="Ad 2: Fall cleanup", art="tree", banner="FALL CLEANUP – BOOK YOUR SPOT", sky="#f1c27d",
                  leaf="#c96a2b",
                  body="Leaves, beds, last mow, brush hauled away. \U0001F342\n\nGet your yard winter-ready before the first freeze. Cleanup spots fill fast in October and November.\n\n✅ Fully insured, local crew\n\nTap below to get on the schedule.",
                  headline="Book Your Fall Cleanup", cta="Get quote"),
             dict(label="Ad 3: Storm cleanup", art="tree", banner="STORM DAMAGE? WE'LL CLEAN IT UP", sky="#6b7b8f",
                  leaf="#3f7d34", fs=18,
                  body="Branches down? Tree on the fence? \U0001F327️\n\nWe handle storm cleanup, tree removal and brush chipping fast, so your yard is safe again.\n\n\U0001F333 \"Climbing to exceed expectations daily\"\n✅ Fully insured\n\nTap below and we'll call you back today.",
                  headline="Fast Storm Cleanup, Free Quote", cta="Get quote"),
         ]),
    dict(slug="eml-services", name="EML Services", initials="EML", color="#1f5f8b",
         domain="Danbury, CT", owner="EML Services", title="3 draft Facebook ads",
         ads=[
             dict(label="Ad 1: Fall cleanup", art="yard", banner="FALL CLEANUP – BOOK NOW",
                  body="Leaves, beds, last mow, gutters cleared. \U0001F342\n\nGet your yard winter-ready before the first freeze. Fall cleanup spots in Danbury fill fast.\n\n✅ Full-service landscaping, tree work & masonry\n\U0001F4CD Danbury & nearby towns\n\nTap below to get on the schedule. \U0001F447",
                  headline="Book Your Fall Cleanup", cta="Get quote"),
             dict(label="Ad 2: Patio & stonework (book for spring)", art="yard", banner="NEW PATIO BY SUMMER?", fs=20,
                  body="Patios, walkways, walls and steps built to last through New England winters. \U0001F9F1\n\nPlan it this fall, and you're first on the build schedule in spring.\n\n✅ Masonry + landscaping, one crew\n\nTap below for a free design estimate.",
                  headline="Free Patio & Masonry Estimate", cta="Get quote"),
             dict(label="Ad 3: Tree work before winter", art="tree", banner="TAKE CARE OF RISKY TREES BEFORE SNOW",
                  sky="#9fb7cc", leaf="#5b7f3a", fs=16,
                  body="Heavy snow + a dead limb over your roof = an expensive January. \U0001F328️\n\nPruning, trimming and removal, done safely before the storms hit.\n\n\U0001F4CD Danbury & nearby towns\n\nTap below for a free estimate.",
                  headline="Free Tree Work Estimate", cta="Get quote"),
         ]),
    dict(slug="nature-bound-garden", name="Nature Bound Garden Landscaping", initials="NB", color="#2f6b2a",
         domain="South Shore, MA", owner="Nature Bound Garden Landscaping", title="3 draft Facebook ads",
         ads=[
             dict(label="Ad 1: Fall cleanup", art="yard", banner="SOUTH SHORE FALL CLEANUPS",
                  body="Leaves, beds, last mow, everything hauled away. \U0001F342\n\nGet your yard winter-ready before the first freeze. Family owned, serving Weymouth, Braintree, Hingham and the South Shore.\n\nTap below to get on the fall schedule. \U0001F447",
                  headline="Book Your Fall Cleanup", cta="Get quote"),
             dict(label="Ad 2: Design & build (book for spring)", art="yard", banner="YOUR DREAM YARD BY SPRING",
                  body="Patios, plantings, walkways and full yard makeovers, designed this winter and built first thing in spring. \U0001F331\n\n15+ years of design & construction on the South Shore.\n\nTap below for a free design consult.",
                  headline="Free Landscape Design Consult", cta="Get quote"),
             dict(label="Ad 3: Trust / local", art="yard", banner="FAMILY OWNED · SOUTH SHORE", fs=19,
                  body="A local family crew that shows up when they say, cleans up every time, and treats your yard like their own. \U0001F3E1\n\nWeymouth · Braintree · Hingham · Cohasset · Norwell · Hanover\n\nTap below for a free, no-pressure estimate.",
                  headline="Free, No-Pressure Estimate", cta="Get quote"),
         ]),
    dict(slug="tree-busters", name="Tree Busters of Cape Cod", initials="TB", color="#1f4f2b",
         domain="Falmouth, MA", owner="Dominic", title="3 draft Facebook ads",
         ads=[
             dict(label="Ad 1: Before nor'easter season", art="tree", banner="TAKE DOWN RISKY TREES BEFORE WINTER",
                  sky="#9fb7cc", leaf="#5b7f3a", fs=16,
                  body="Nor'easter season on the Cape is coming. \U0001F32C️\n\nThat leaning pine or dead limb over your roof is a lot cheaper to handle now than after the next storm.\n\n\U0001F333 Tree removal & trimming · stump grinding\n\U0001F3E1 Family owned, 30 years combined experience\n\U0001F4CD Falmouth & the Cape\n\nTap below for a free estimate. \U0001F447",
                  headline="Free Tree Removal Estimate", cta="Get quote"),
             dict(label="Ad 2: Stump grinding", art="tree", banner="STILL STARING AT THAT STUMP?",
                  sky="#bcd9ef", leaf="#3f7d34",
                  body="Old stumps are trip hazards, bug magnets and lawnmower killers. \U0001FAB5\n\nWe grind them below grade so you can plant grass or garden right over the spot.\n\n\U0001F4CD Falmouth & surrounding Cape Cod towns\n\nTap below for a quick quote.",
                  headline="Stump Grinding, Free Quote", cta="Get quote"),
             dict(label="Ad 3: Snow removal contracts", art="tree", banner="LOCK IN SNOW REMOVAL NOW", sky="#dfe9f3",
                  leaf="#2f5f35", fs=19,
                  body="Don't get stuck digging out after the first big storm. ❄️\n\nSign up now for reliable snow removal from a local Falmouth crew, for homes and businesses.\n\nTap below to reserve your spot for the season.",
                  headline="Reserve Your Snow Removal Spot", cta="Get quote"),
         ]),
    dict(slug="everest207", name="Everest207 Landscaping", initials="E207", color="#1f4f6b",
         domain="Wells, ME", owner="Michael", title="3 draft Facebook ads",
         problem="You're running <b>the same ad 6 times</b>, and the headline is just <b>“Everest207 Landscaping”</b>. There's no offer and no reason to act now, so Meta splits your budget across copies instead of testing anything.",
         ads=[
             dict(label="Ad 1: Fall cleanup", art="yard", banner="FALL CLEANUP – BOOK BEFORE THE FREEZE", fs=17,
                  body="Leaves, beds, last mow, everything hauled away. \U0001F342\n\nGet your yard winter-ready before the first freeze. Fall cleanup spots in Wells, the Kennebunks and York fill fast.\n\n⭐ 5.0 on Angi · fully insured\n\U0001F4CD Southern Maine\n\nTap below to get on the schedule. \U0001F447",
                  headline="Book Your Fall Cleanup", cta="Get quote"),
             dict(label="Ad 2: Patio & hardscape (book for spring)", art="yard", banner="NEW PATIO BY SUMMER?", fs=20,
                  body="Patios, walkways, retaining walls and stone steps, built to handle Maine winters. \U0001F9F1\n\nDesign it this fall and you're first on our build schedule in spring. Book before the new year and get early-bird pricing.\n\n\"The quality of the patio was beyond my expectations.\" – Google review\n\nTap below for a free design estimate.",
                  headline="Free Patio & Hardscape Estimate", cta="Get quote"),
             dict(label="Ad 3: Reviews / trust", art="yard", banner="SOUTHERN MAINE TRUSTS EVEREST207", fs=18,
                  body="Local crew. Shows up on time. Leaves your yard better than they found it. \U0001F3E1\n\n⭐ 5.0 on Angi · 100% recommended\n✅ Landscaping, hardscaping, stump removal & drainage\n\U0001F4CD Wells · Kennebunk · Ogunquit · York · Sanford\n\nTap below for a free, no-pressure estimate.",
                  headline="Free, No-Pressure Estimate", cta="Get quote"),
         ]),
    dict(slug="cg-outdoor", name="C&G Outdoor Services", initials="C&G", color="#2f5f35",
         domain="Naugatuck, CT", owner="Ryan", title="2 fixed Facebook ads",
         problem="Your ad's headline is literally <b>“fb.com”</b>. People see a link, not a reason to call, so most scroll right past it.",
         ads=[
             dict(label="Fix 1: Risky trees before winter", art="tree", banner="TAKE DOWN RISKY TREES BEFORE SNOW",
                  sky="#9fb7cc", leaf="#5b7f3a", fs=16,
                  body="Heavy snow + a dead limb over your roof = an expensive January. 🌨️\n\nGet a licensed arborist to look at it now, before the storms hit.\n\n🌳 Licensed arborist · tree removal & pruning\n📍 Naugatuck & nearby towns\n\nTap below for a free estimate. 👇",
                  headline="Free Tree Estimate From an Arborist", cta="Get quote"),
             dict(label="Fix 2: Storm cleanup", art="tree", banner="STORM DAMAGE? WE'LL HANDLE IT", sky="#6b7b8f",
                  leaf="#3f7d34", fs=19,
                  body="Branches down? Tree on the fence? 🌧️\n\nFast storm cleanup and tree removal from a local, licensed arborist.\n\nTap below and we'll call you back today.",
                  headline="Fast Storm Cleanup, Free Quote", cta="Get quote"),
         ]),
    dict(slug="east-coast-tree", name="East Coast Tree Service", initials="ECT", color="#1f4f2b",
         domain="Tewksbury, MA", owner="East Coast Tree Service", title="2 fixed Facebook ads",
         problem="One of your running ads says <b>“European Wood Chippers For Sale”</b> 8 times, so homeowners looking for tree work see an equipment sale instead.",
         ads=[
             dict(label="Fix 1: Before nor'easter season", art="tree", banner="GET RISKY TREES DOWN BEFORE WINTER",
                  sky="#9fb7cc", leaf="#5b7f3a", fs=17,
                  body="Nor'easter season is coming. 🌬️\n\nThat leaning tree over your house is a lot cheaper to handle now than after it comes down.\n\n🌳 Removal, trimming & pruning\n⏱️ 24-hour emergency storm service\n📍 Reading, Billerica, Tewksbury & nearby\n\nTap below for a free estimate. 👇",
                  headline="Free Tree Removal Estimate", cta="Get quote"),
             dict(label="Fix 2: 24/7 storm damage", art="tree", banner="TREE DOWN? WE'RE ON IT 24/7", sky="#6b7b8f",
                  leaf="#3f7d34", fs=20,
                  body="Storm damage doesn't wait for business hours. ⛈️\n\nEast Coast Tree Service handles emergency tree removal day or night across Middlesex and Essex counties.\n\nTap below and we'll call you back fast.",
                  headline="24/7 Emergency Tree Service", cta="Get quote"),
         ]),
    dict(slug="allgreen-lawn-tree", name="AllGreen Lawn & Tree Care", initials="AG", color="#2f6b2a",
         domain="Norwood, MA", owner="AllGreen Lawn & Tree Care", title="2 fixed Facebook ads",
         problem="Your ad's headline is just <b>“instagram.com”</b>, and it's been the same ad since June. Nothing tells people why to call now.",
         ads=[
             dict(label="Fix 1: Fall lawn program", art="yard", banner="FIX YOUR LAWN THIS FALL", fs=21,
                  body="Fall is the best time of year to fix a thin, patchy lawn. 🍂\n\nAeration, overseeding and a winter fertilizer now = a thick green lawn in spring.\n\n📍 Norwood & surrounding towns\n\nTap below for a free lawn evaluation. 👇",
                  headline="Free Fall Lawn Evaluation", cta="Get quote"),
             dict(label="Fix 2: Tree & shrub care", art="tree", banner="PROTECT YOUR TREES BEFORE WINTER",
                  sky="#9fb7cc", leaf="#3f7d34", fs=17,
                  body="Winter wind, snow and ice are hard on trees and shrubs. 🌨️\n\nPruning and a fall health treatment now help them make it to spring.\n\nLocal lawn & tree care team in Norwood.\n\nTap below for a free estimate.",
                  headline="Free Tree & Shrub Estimate", cta="Get quote"),
         ]),
]

CSS = """
:root{--bg:#f0f2f5;--card:#fff;--text:#050505;--muted:#65676b;--btn:#e4e6eb;--tag:#fff4d6;--tagtext:#7a5500;--bad:#fde8e8;--badtext:#8a1c1c}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#18191a;--card:#242526;--text:#e4e6eb;--muted:#b0b3b8;--btn:#3a3b3c;--tag:#3d3320;--tagtext:#ffd780;--bad:#3a1f1f;--badtext:#ffb4b4}}
:root[data-theme="dark"]{--bg:#18191a;--card:#242526;--text:#e4e6eb;--muted:#b0b3b8;--btn:#3a3b3c;--tag:#3d3320;--tagtext:#ffd780;--bad:#3a1f1f;--badtext:#ffb4b4}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:15px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
main{max-width:500px;margin:0 auto;padding:16px}h1{font-size:18px;margin:4px 0 2px}.sub{color:var(--muted);font-size:13px;margin:0 0 12px}
.problem{background:var(--bad);color:var(--badtext);border-radius:10px;padding:12px;font-size:14px}
.label{display:inline-block;background:var(--tag);color:var(--tagtext);font-size:12px;font-weight:600;padding:3px 8px;border-radius:6px;margin:18px 0 8px}
.post{background:var(--card);border-radius:10px;box-shadow:0 1px 2px rgba(0,0,0,.15);overflow:hidden}
.head{display:flex;gap:10px;align-items:center;padding:12px 12px 6px}.avatar{width:40px;height:40px;border-radius:50%;color:#fff;display:grid;place-items:center;font-weight:800;font-size:13px;flex:none}
.name{font-weight:600}.meta{color:var(--muted);font-size:12px}.body{padding:4px 12px 10px;white-space:pre-line}.img{display:block;width:100%;height:auto}
.cta{display:flex;align-items:center;gap:10px;padding:10px 12px;background:var(--bg)}.cta .txt{flex:1;min-width:0}.domain{color:var(--muted);font-size:12px;text-transform:uppercase}
.headline{font-weight:600}.btn{background:var(--btn);font-weight:600;font-size:14px;padding:8px 12px;border-radius:6px;white-space:nowrap}
.foot{color:var(--muted);font-size:12px;margin-top:20px}
"""


def art(ad, n):
    if ad["art"] == "tree":
        return TREE_SVG.format(alt=html.escape(ad["banner"]), banner=html.escape(ad["banner"]), fs=ad.get("fs", 20),
                               sky=ad.get("sky", "#bcd9ef"), leaf=ad.get("leaf", "#3f7d34"), extra=ad.get("extra", ""))
    if ad["art"] == "yard":
        return YARD_SVG.format(alt=html.escape(ad["banner"]), banner=html.escape(ad["banner"]), fs=ad.get("fs", 20))
    s1, s2 = ad["sky"]
    return ROOF_SVG.format(n=n, alt=html.escape(ad["banner"]), banner=html.escape(ad["banner"]), fs=ad.get("fs", 20),
                           sky1=s1, sky2=s2, roof="#3b3f46", wall="#c9b79c", extra=ad["extra"])


def page(c):
    posts = []
    for i, ad in enumerate(c["ads"]):
        posts.append(f"""<span class="label">{html.escape(ad['label'])}</span>
<article class="post"><div class="head"><div class="avatar" style="background:{c['color']}">{html.escape(c['initials'])}</div>
<div><div class="name">{html.escape(c['name'])}</div><div class="meta">Sponsored · \U0001F310</div></div></div>
<div class="body">{html.escape(ad['body'])}</div>{art(ad, i)}
<div class="cta"><div class="txt"><div class="domain">{html.escape(c['domain'])}</div><div class="headline">{html.escape(ad['headline'])}</div></div><div class="btn">{ad['cta']}</div></div></article>""")
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(c['name'])} Spec Ads</title><style>{CSS}</style></head><body><main>
<h1>{html.escape(c['name'])}: {c.get('title', '2 fixed Facebook ads')}</h1>
<p class="sub">Drafts by ApexLeads for {html.escape(c['owner'])}. Not live, and nothing runs without your approval.</p>
{f'<div class="problem"><b>What' + chr(39) + f's wrong with your current ad:</b> {c["problem"]}</div>' if c.get('problem') else ''}
{''.join(posts)}
<p class="foot">"Get quote" opens a short form: Do you own the home? What do you need? Zip code, name, phone. Leads go straight to your phone.</p>
</main></body></html>"""


SHOT_JS = """
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const p = await b.newPage({ viewport: { width: 430, height: 900 }, deviceScaleFactor: 2, colorScheme: 'light' });
  for (const slug of process.argv.slice(2)) {
    await p.goto('file://' + __OUT__ + '/' + slug + '.html');
    const posts = await p.$$('article.post');
    for (let i = 0; i < posts.length; i++) await posts[i].screenshot({ path: __OUT__ + '/' + slug + '-ad' + (i + 1) + '.png' });
    const prob = await p.$('.problem');
    if (prob) await prob.screenshot({ path: __OUT__ + '/' + slug + '-problem.png' });
  }
  await b.close();
})();
"""

if __name__ == "__main__":
    import sys
    if sys.argv[1:]:
        COMPANIES = [c for c in COMPANIES if c["slug"] in sys.argv[1:]]
    for c in COMPANIES:
        (OUT / f"{c['slug']}.html").write_text(page(c), encoding="utf-8")
    js = OUT / "_shot.js"
    js.write_text(SHOT_JS.replace("__OUT__", repr(str(OUT))))
    try:
        subprocess.run(["node", str(js), *[c["slug"] for c in COMPANIES]], check=True,
                       env={**__import__("os").environ, "NODE_PATH": subprocess.check_output(["npm", "root", "-g"], text=True).strip()})
    finally:
        js.unlink()
