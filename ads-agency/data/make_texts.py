"""Generate ready-to-send texts for the 50-company NE list (texts-ne-50.md)."""
import re
import sys
sys.path.insert(0, "data")
from ne50_930 import LEADS

SEEN = [
    "the headline on your ad just says \"fb.com\"",
    "your ad is running a wood chipper sale headline 8 times, which looks like the wrong ad got posted",
    "the headline on your ad just says \"instagram.com\", and it's been the same ad since June",
    "the headline on your ad just says \"instagram.com\"",
    "your 5 ads have headlines that say \"fb.me\" or are blank",
    "most of your 8 ads have no headline, and one is still pushing spring cleanups in the fall",
    "3 of your 4 ads have blank headlines",
    "your ad has no headline at all",
    "your newest ad has no headline",
    "your ad has no headline and it's been running unchanged since last year",
    "the only ad you're running is a hiring ad, so nothing is going out to customers",
    "you're only running hiring ads right now, nothing aimed at customers",
    "one of your ads has 9 headlines crammed in and another repeats the same line 8 times",
    "your ad headline is just the company name with no offer",
    "your ad headline is just the company name with no offer",
    "your ad headline is just the company name with no offer",
    "your ad headline is just the company name with no offer",
    "your ad headline is just the company name, and it's been the same ad since April",
    "one of your ads has 4 headlines in it and 3 of them are the same",
    "your ad uses the same template headlines another Maine tree company is running",
    "your ad uses stuffed template headlines and it's been the same one since June",
    "your ad has the same headline repeated 3 times",
    "you have the same ad copied 3 times with no offer",
    "you have the same ad copied 3 times since June",
    "your ad headline is just your service area, with no offer",
    "your ad headline is \"Got Trees?\" with no offer behind it",
    "your ad doesn't give people a reason to call now",
    "your two ads both use the same generic curb appeal headline",
    "your two ads both use the same generic headline",
    "your ad headlines are just your phone number",
    "your ad says \"free estimate\" but doesn't give people a reason to pick you",
    "your ad doesn't say what makes you different or why to call now",
    "the same free-estimate ad has been running since April",
    "the same free-estimate ad has been running since May",
    "you've had one ad running since June with nothing for fall",
    "your ad is pretty generic and doesn't give people a reason to call now",
    "your ad is pretty generic and doesn't give people a reason to call now",
    "your ad is pretty generic and has been running since August",
    "your only ad is over a year old",
    "you're still running a summer maintenance ad in the fall",
    "you've had the same reviews ad running since June",
    "you've only got one ad from August, nothing for fall storm work",
    "your offers are good, but there's no easy way for people to send you their info",
    "you've got one patio ad running with no offer",
    "your photos are great, but there's no offer or spring pre-booking push",
    "you've got one design ad running with no offer",
    "your 4 ads only use 2 headlines between them",
    "your only ad is the soil test offer, nothing for cleanups or hardscape",
    "your August fall-program ad is still running unchanged",
    "you're only running aeration ads, nothing for hardscape or spring",
]
assert len(SEEN) == len(LEADS)
ALREADY = {"C&G Outdoor Services", "East Coast Tree Service", "AllGreen Lawn & Tree Care"}

def text(l, seen):
    name, owner = re.sub(r"\s*\(.*?\)", "", l[0]), l[4]
    hi = f"Hi {owner}," if owner else "Hi,"
    if l[0] in ALREADY:
        return (f"{hi} Josh from ApexLeads again. Just following up on the Facebook ad ideas I sent for {name}. "
                f"Here's a one-page sheet on how I work and what it costs. Happy to walk you through it in 5 minutes. (508) 492-9796")
    return (f"{hi} this is Josh with ApexLeads in Blackstone. I was looking at {name}'s Facebook ads and noticed {seen}. "
            f"That usually means fewer calls than you should be getting. I put together a couple ideas for what I'd change. "
            f"Want me to send them over? Free, no strings. - Josh, (508) 492-9796")

out = ["# Ready-to-Send Texts: 50 New England Companies",
       "",
       "Copy each text and send it from your phone. Start with the A list.",
       "",
       "- **If they reply \"sure\" or \"what is it\":** send the service sheet image (`business-kit/service-sheet.png`) with the reply text at the bottom.",
       "- **If the number is a landline** (the text fails or never delivers): call it or message their Facebook page with the same words.",
       "- **Send 10–15 a day, not all 50 at once.** Bulk texts from a new number can get flagged as spam.",
       "- Mark each one off and tell me who replied so I can update your pipeline.",
       ""]
for pri, title in (("A", "A list: visibly broken ads (send these first)"), ("B", "B list: generic or copied ads"), ("C", "C list: decent ads, easy upgrades")):
    out += [f"## {title}", ""]
    for l, seen in zip(LEADS, SEEN):
        if l[6] != pri:
            continue
        tag = " *(follow-up: already messaged)*" if l[0] in ALREADY else ""
        out += [f"### ☐ {l[0]} · {l[1]}, {l[2]} · {l[3]}{tag}", "", text(l, seen), ""]
out += ["## When they reply",
        "",
        "**They say yes / send it:**",
        "> Here's what I'd change on your ad, plus a one-page sheet on how I work. You can pay $50 per lead, 15% of jobs from the ads, or $900 a month flat. Month to month, no contract. Want to hop on a quick 10-minute call this week? [attach service-sheet.png and their spec ad if I made one]",
        "",
        "**They ask the price first:**",
        "> Three options, your pick: $50 per lead, 15% of the jobs that come from the ads, or $900 a month flat. Ad spend goes on your own card to Facebook. Month to month, cancel anytime.",
        "",
        "**They say not interested:**",
        "> No problem, thanks for letting me know. If you want a second set of eyes on your ads before spring, I'm here.",
        "",
        "**No reply after 3 days:**",
        "> Hi, Josh from ApexLeads again. Didn't want this to get buried. Happy to send those ad ideas whenever you have a minute.",
        ""]
open("texts-ne-50.md", "w").write("\n".join(out))
print("ok")
