// Supabase GIẢ nhớ trong bộ nhớ, chỉ đủ cho ban-tin-gui/index.ts (test). Dữ liệu nằm ở globalThis.__FAKE.db.
// Được nối vào bằng import map (tools/mau_gui/import_map.json) thay cho https://esm.sh/@supabase/supabase-js@2.
type Row = Record<string, any>;
const F = () => (globalThis as any).__FAKE;

class Q implements PromiseLike<{ data: any; error: any }> {
  f: ((r: Row) => boolean)[] = []; op = 'select'; pl: any = null; one = false;
  constructor(public t: string) {}
  select() { return this; }
  eq(c: string, v: any) { this.f.push((r) => r[c] === v); return this; }
  is(c: string, v: any) { this.f.push((r) => (r[c] ?? null) === v); return this; }
  maybeSingle() { this.one = true; return this; }
  insert(p: any) { this.op = 'insert'; this.pl = p; return this; }
  update(p: any) { this.op = 'update'; this.pl = p; return this; }
  then<A, B>(ok?: (v: { data: any; error: any }) => A, ko?: (e: any) => B) { return Promise.resolve(this.chay()).then(ok, ko); }
  chay() {
    const f = F(); f.nhatKy.push(`${this.op} ${this.t}`);
    const loi = f.loiBang?.[`${this.op}:${this.t}`];
    if (loi) return { data: null, error: { message: loi } };
    const D: Row[] = (f.db[this.t] ||= []);
    const m = D.filter((r) => this.f.every((x) => x(r)));
    if (this.op === 'insert') {
      for (const r of [].concat(this.pl)) {
        if (this.t === 'ban_tin' && D.some((x) => x.ngay === (r as Row).ngay)) return { data: null, error: { message: 'duplicate key value (ngay)' } };
        D.push({ telegram_luc: null, loi: null, ...(r as Row) });
      }
      return { data: null, error: null };
    }
    if (this.op === 'update') { m.forEach((r) => Object.assign(r, this.pl)); return { data: null, error: null }; }
    const out = JSON.parse(JSON.stringify(m));
    return { data: this.one ? (out[0] ?? null) : out, error: null };
  }
}
export function createClient(_url: string, _key: string, opts?: any) {
  const auth = opts?.global?.headers?.Authorization;
  return {
    from: (t: string) => new Q(t),
    rpc: async (_n: string) => ({ data: auth ? F().laChu : null, error: null }),
  };
}
