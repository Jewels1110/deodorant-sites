# Simple Body deodorant sites: launch guide

There are three folders, one per domain. Each one is a complete static website: `index.html` plus an `img/` folder of product cutouts. You don't need a server, a database or another Shopify plan. The lifestyle photos load from your own Shopify CDN.

| Folder | Domain | Who it's for |
|---|---|---|
| `simplebodydeodorant.com/` | simplebodydeodorant.com | People who tried other natural deodorants and gave up. Reviews, the 4 ways natural deodorant fails, a one-question formula picker |
| `allnaturaldeodorant.com/` | allnaturaldeodorant.com | First-time switchers and label readers. Every ingredient explained, what's left out, sweat vs. smell, the first 30 days, aluminum |
| `monthlydeodorant.com/` | monthlydeodorant.com | Subscribers, households and couples. A subscription builder with a 12-month delivery calendar, plus a "reorder when empty" vs. subscribe comparison |

## How checkout works (one Shopify store)
Every "Add to cart" or "Start my subscription" button sends the shopper to a link like this:

`https://simplebodyproducts.com/cart/add?items[][id]=VARIANT&items[][quantity]=1&items[][selling_plan]=PLAN&utm_source=SITE&return_to=/cart`

- The items land in the regular simplebodyproducts.com cart, so your discounts, Yotpo points, upsells and checkout all work as usual.
- Subscription lines use your existing 30/60/90-day selling plans (10% off). This was tested on your live store: a subscription line and a one-time line were added together, then removed.
- Every link carries `utm_source=<the domain>`. In Shopify Analytics you can filter sales by UTM source to see which site sells.
- If you ever change variant or selling-plan IDs, edit the `P` and `PLAN` lists near the top of the script at the bottom of each `index.html`.

## Free hosting (about 15 minutes per domain)
**Cloudflare Pages (recommended, free):**
1. Create a free Cloudflare account, then go to Workers & Pages → Create → Pages → "Upload assets".
2. Name the project (e.g. `monthlydeodorant`) and drag in that site's folder, the one with `index.html` and `img/`.
3. In the project, open Custom domains → Set up a domain → enter `monthlydeodorant.com`. Cloudflare will tell you exactly which DNS records to add at your domain registrar, or offer to move the DNS for you.
4. Repeat for the other two folders.

Netlify ("Add new site → Deploy manually", then drag the folder in) works the same way and is also free.

## Before you launch: please check these
1. **Subscription changes and cancelling.** The sites don't promise "skip or cancel anytime", because I couldn't confirm what your subscription app lets customers do. If customers can manage their own subscriptions, add that line. It's a strong selling point.
2. **Ingredient label typo.** Your Shopify ingredient field says "melaleuca alternafolia". The correct spelling is *alternifolia*. The sites use the correct spelling.
3. **Original product description** lists 4 scents but leaves out Cedar + Clove, which is for sale.
4. **Keep each site's words unique.** Google treats near-copy sites as "doorway pages". These three were written to differ in audience, content and structure. Keep it that way: don't paste the same blog post on all three.
5. Shipping text says orders ship the same business day and are free over $75 (US only), taken from your shipping policy. Update all three sites if that changes.

## Files
- `index.html`: the page, with fonts built in
- `img/*.webp`: transparent product cutouts made from your Shopify renders
