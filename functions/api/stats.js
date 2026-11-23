// Public daily totals for all three sites: GET /api/stats?days=30
export async function onRequestGet({ request, env }) {
  const h={'content-type':'application/json','cache-control':'no-store','access-control-allow-origin':'*'};
  if (!env.DB) return new Response(JSON.stringify({error:'counter not connected yet'}),{status:503,headers:h});
  const days=Math.min(400,Math.max(1,+new URL(request.url).searchParams.get('days')||30));
  const since=new Date(Date.now()-days*864e5).toLocaleDateString('en-CA',{timeZone:'America/Denver'});
  await env.DB.prepare('CREATE TABLE IF NOT EXISTS hits (day TEXT, site TEXT, event TEXT, n INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(day,site,event))').run();
  const {results}=await env.DB.prepare('SELECT day,site,event,n FROM hits WHERE day>=?1 ORDER BY day DESC,site,event').bind(since).all();
  return new Response(JSON.stringify({timezone:'America/Denver',since,rows:results}),{headers:h});
}
