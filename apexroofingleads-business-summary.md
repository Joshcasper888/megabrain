# ApexRoofingLeads — Business & Facebook/Meta Setup Summary
Prepared by Harvey — 2026-09-28

## Business Overview
- Agency: ApexRoofingLeads, owned/run by Josh
- Service: Facebook/Instagram ad management for roofing (and landscaping) companies
- Pricing model: revenue-share — client covers ad spend directly to Meta (e.g. ~$3,000/mo), Apex takes 15% of the revenue those ads generate; no jobs, no fee
- Primary client-acquisition channel to date: cold email outreach to business owners

## CRM
- Source of truth: CRM artifact (https://claude.ai/artifact/GpPuQKyjUQskumXQGoKi1u)
- 1,413 total leads across roofing + landscaping verticals, multiple US cities
- Lead fields: city, email, industry, lastContact, name, notes, phone, status, website

## Cold Email Campaign
- Channel: Composio Gmail integration (apexroofingleads1@gmail.com)
- Target list: 758 leads pulled from the CRM
- Status: PAUSED per explicit instruction ("harvey u can stop there") — 8 of ~15 batches sent (~400 leads contacted), 317 leads never sent
- No further sends without new, explicit authorization from Josh
- CAN-SPAM opt-out footer in place: reply "unsubscribe" to be removed

## Reply Monitoring
- Hourly scheduled task checks the Gmail inbox for replies/unsubscribes, updates the matching CRM lead's status + notes, and sends a push notification only when genuine replies or opt-outs are found that run

## Native Gmail Connector (separate from the Composio channel above)
- Currently broken — repeated "Precondition check failed" errors
- Needs Josh to manually reconnect it in claude.ai settings if it's ever needed

## Call List
- 1,404-lead phone call list (Excel) built from CRM leads that have a phone number, sorted by city — already delivered to Josh

## Facebook / Instagram / Meta Ads Setup
- Facebook (Composio "facebook" toolkit — Pages/Messenger): connection active, account "Joshua Casper-Phipps" — but zero Facebook Pages currently managed, so Messenger sending isn't usable yet
- Instagram (Composio "instagram" toolkit): connection initiated, not yet confirmed active
- Key finding: Meta's Messenger Platform policy blocks true cold DMs — a business can only message a user who has messaged the Page first (or clicked a CTA/ad), so Facebook/Instagram can't replicate the cold-email outreach model directly
- Meta Ads (Composio "metaads" toolkit): connection initiated, but requires a Meta Developer App + Graph API access token (a real multi-step technical setup) — paused, since campaign-creation actions are blocked in this working environment regardless of token status
- A separate "fb_ads" MCP connector with full write access (campaign/ad set/ad/catalog/pixel/custom-audience creation) appeared in-session on 9/28 — origin not yet confirmed with Josh; nothing has been executed through it

## Proposed Facebook/Instagram Ad Campaign (drafted, not yet launched)
- Format: Lead-gen form ad (captures name/phone/email directly in Meta's native form)
- Targeting: job title (Business Owner, Small Business Owner, General Contractor) + industry interest (Construction, Home Improvement, Landscaping) + "Small Business Owners" behavior category
- Geography: matches current CRM footprint (nationwide, same cities as the email campaign) unless narrowed
- Budget: $30/day (~$900/mo) starting point, one ad set
- Ad copy: 3 variants drafted — pricing/risk-reversal hook, pain-point hook, outcome hook
- Blocked on: Josh creating a Facebook Business Page and a Meta Ads account with billing — required first, can't be created on his behalf
