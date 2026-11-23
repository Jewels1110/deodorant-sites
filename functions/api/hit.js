// Counts page views and store-button clicks per site per day (America/Denver).
// No cookies, no IP addresses, no personal data: just a daily tally.
const SITES = ['simplebodydeodorant.com','allnaturaldeodorant.com','monthlydeodorant.com'];
const BOT = /bot|crawl|spider|slurp|preview|monitor|headless|lighthouse|facebookexternalhit|curl|wget|python/i;

function site(host){ host=(host||'').replace(/^www\./,''); if(SITES.includes(host)) return host;
  const m=host.match(/^([a-z]+)\.pages\.dev$/); return m ? m[1]+'.com' : null; }
function today(){ return new Date().toLocaleDateString('en-CA',{timeZone:'America/Denver'}); }

export async function onRequestPost({ request, env }) {
  const s = site(new URL(request.url).hostname);
  if (!env.DB || !s || BOT.test(request.headers.get('user-agent')||'')) return new Response(null,{status:204});
  let e='view'; try{ const b=await request.json(); if(b && b.e==='click') e='click'; }catch(_){}
  await env.DB.batch([
    env.DB.prepare('CREATE TABLE IF NOT EXISTS hits (day TEXT, site TEXT, event TEXT, n INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(day,site,event))'),
    env.DB.prepare('INSERT INTO hits(day,site,event,n) VALUES(?1,?2,?3,1) ON CONFLICT(day,site,event) DO UPDATE SET n=n+1').bind(today(),s,e)
  ]);
  return new Response(null,{status:204});
}
