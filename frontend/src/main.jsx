import { render } from 'preact';
import { useEffect, useState } from 'preact/hooks';
import { Braces, Check, Copy, ExternalLink, IdCardLanyard, Monitor, Moon, Sun } from 'lucide-preact';
import '@fontsource-variable/archivo/wdth.css';
import { Lanyard } from './Lanyard';
import { STYLES, shieldsUrl, trackingUrl } from './shields';
import './style.css';

const COLORS = ['c8246b', 'e05d44', 'fe7d37', 'dfb317', '44cc11', '0f9d8a', '007ec6', '6f42c1', '555555'];
const THEMES = { system: Monitor, light: Sun, dark: Moon };
const NEXT_THEME = { system: 'light', light: 'dark', dark: 'system' };
const HEX = /^[0-9a-f]{6}$/i;

const hueToHex = (hue) => {
  const f = (n) => {
    const k = (n + hue / 30) % 12;
    const channel = 0.45 - 0.7 * Math.min(0.45, 0.55) * Math.max(-1, Math.min(k - 3, 9 - k, 1));
    return Math.round(channel * 255).toString(16).padStart(2, '0');
  };
  return `${f(0)}${f(8)}${f(4)}`;
};

// lucide 1.x dropped brand icons; this is its former GitHub outline (ISC) so it matches the rest
const GitHub = ({ size = 24 }) => (
  <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 3.5c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4" />
    <path d="M9 18c-4.51 2-5-2-7-2" />
  </svg>
);

const number = (value) => new Intl.NumberFormat().format(value);

// navigator.clipboard only exists on HTTPS and localhost; plain-HTTP self-hosts need the old way
async function copyText(text) {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch {
    const area = Object.assign(document.createElement('textarea'), { value: text });
    area.style.cssText = 'position:fixed;opacity:0';
    document.body.append(area);
    area.select();
    const copied = document.execCommand('copy');
    area.remove();
    return copied;
  }
}

function useTheme() {
  const [theme, setTheme] = useState(() => {
    try { return localStorage.getItem('theme') || 'system'; } catch { return 'system'; }
  });
  useEffect(() => {
    const media = matchMedia('(prefers-color-scheme: dark)');
    const apply = () => {
      document.documentElement.dataset.theme = theme === 'system' ? (media.matches ? 'dark' : 'light') : theme;
    };
    apply();
    try { localStorage.setItem('theme', theme); } catch {}
    media.addEventListener('change', apply);
    return () => media.removeEventListener('change', apply);
  }, [theme]);
  return [theme, () => setTheme(NEXT_THEME[theme])];
}

// reads the count without recording a visit, so previewing never touches the counter
function useVisitCount(tag) {
  const [count, setCount] = useState(null);
  useEffect(() => {
    if (!tag) return setCount(null);
    const timer = setTimeout(() => {
      fetch(`api/stats/${encodeURIComponent(tag)}`)
        .then((r) => (r.ok ? r.json() : null))
        .then((stats) => setCount(stats ? stats.visit_count : null))
        .catch(() => setCount(null));
    }, 300);
    return () => clearTimeout(timer);
  }, [tag]);
  return count;
}

function App() {
  const [theme, cycleTheme] = useTheme();
  const [badge, setBadge] = useState({ tag: '', label: 'visits', color: 'c8246b', style: 'flat', logo: '' });
  const [totals, setTotals] = useState(null);
  const [info, setInfo] = useState(null);
  const tag = badge.tag.trim();
  const count = useVisitCount(tag);
  const set = (field) => (e) => setBadge({ ...badge, [field]: e.currentTarget.value });

  useEffect(() => {
    fetch('api/stats').then((r) => r.json()).then(setTotals).catch(() => {});
    fetch('api/app-info').then((r) => r.json()).then(setInfo).catch(() => {});
  }, []);

  const design = { ...badge, label: badge.label.trim() || 'visits', color: badge.color.trim() || 'c8246b', tag };
  const ThemeIcon = THEMES[theme];

  return (
    <>
      <header class="top">
        <a class="brand" href="./"><IdCardLanyard size={22} />BadgeTrack</a>
        <nav class="tools">
          <a href="docs" target="_blank" rel="noreferrer" title="API documentation" aria-label="API documentation"><Braces size={18} /></a>
          <a href="https://github.com/PianoNic/BadgeTrack" target="_blank" rel="noreferrer" title="GitHub" aria-label="GitHub"><GitHub size={18} /></a>
          <button onClick={cycleTheme} title={`Theme: ${theme}`} aria-label={`Theme: ${theme}. Switch to ${NEXT_THEME[theme]}`}>
            <ThemeIcon size={18} />
          </button>
        </nav>
      </header>

      <main class="page">
        <div class="left">
          <section class="intro">
            <h1>Visitor counters for your READMEs</h1>
            <p>
              Pick a tag, style the badge and paste the snippet. Each browser counts once per badge;
              a cookie remembers it and nothing else is stored.
            </p>
            {totals && (
              <p class="totals">
                <strong>{number(totals.total_visits)}</strong> visits counted on <strong>{number(totals.total_tracked_tags)}</strong> badges
              </p>
            )}
          </section>

            <form class="settings" onSubmit={(e) => e.preventDefault()}>
              <label class="field">
                <span>Tag</span>
                <input value={badge.tag} onInput={set('tag')} placeholder="my-project" maxLength={200} required autoFocus />
                <small>Unique to this badge. Every embed with the same tag shares one count.</small>
              </label>

              <label class="field">
                <span>Label</span>
                <input value={badge.label} onInput={set('label')} placeholder="visits" maxLength={20} />
              </label>

              <fieldset class="field">
                <legend>Colour</legend>
                <div class="swatches">
                  {COLORS.map((hex) => (
                    <button
                      type="button" key={hex} class="swatch" style={{ background: `#${hex}` }}
                      aria-pressed={design.color.toLowerCase() === hex} aria-label={`#${hex}`}
                      onClick={() => setBadge({ ...badge, color: hex })}
                    />
                  ))}
                </div>
                <div class="custom-colour">
                  <input
                    type="range" class="hue" min="0" max="359" aria-label="Pick any hue"
                    onInput={(e) => setBadge({ ...badge, color: hueToHex(Number(e.currentTarget.value)) })}
                  />
                  <span class="hex-field">
                    <i style={{ background: HEX.test(design.color) ? `#${design.color}` : design.color }} />
                    <input value={badge.color} onInput={set('color')} maxLength={20} aria-label="Colour as hex or shields.io name" />
                  </span>
                </div>
                <small>Tap a swatch, slide for any hue, or type a hex code or a shields.io colour name.</small>
              </fieldset>

              <fieldset class="field">
                <legend>Style</legend>
                <div class="styles">
                  {STYLES.map(([value, name]) => (
                    <label key={value} class="style-option">
                      <input type="radio" name="style" value={value} checked={badge.style === value} onChange={set('style')} />
                      <img src={shieldsUrl({ ...design, style: value }, count ?? 0)} alt="" height="20" />
                      <span>{name}</span>
                    </label>
                  ))}
                </div>
              </fieldset>

              <label class="field">
                <span>Logo <em>optional</em></span>
                <input value={badge.logo} onInput={set('logo')} placeholder="github" maxLength={20} />
                <small>
                  Any <a href="https://simpleicons.org" target="_blank" rel="noreferrer">Simple Icons<ExternalLink size={12} /></a> slug.
                </small>
              </label>
            </form>
        </div>

        <aside class="output">
          <div class="hanger">
            <Lanyard class="lanyard" />
            <article class="card">
              <div class="card-band"><span class="slot" />Visitor badge</div>
              <div class="card-body">
                <p class="card-name">{tag || 'your-tag'}</p>
                <img class="card-badge" src={shieldsUrl(design, count ?? 0)} alt={`${design.label} badge preview`} />
                <p class="card-count">
                  {!tag
                    ? 'Type a tag to see your badge.'
                    : count
                      ? `${number(count)} ${count === 1 ? 'visitor' : 'visitors'} so far`
                      : 'New tag. The first visit starts the count.'}
                </p>
              </div>
            </article>
          </div>

          <Snippets design={design} />
        </aside>
      </main>

      <footer class="bottom">
        <span>Only an anonymous cookie is stored, to count each browser once.</span>
        <span class="spacer" />
        <a href="https://github.com/PianoNic/BadgeTrack/blob/main/LICENSE" target="_blank" rel="noreferrer">MIT licence</a>
        {info && (
          <a href={`https://github.com/PianoNic/BadgeTrack/releases/tag/v${info.version.replace(/^v/i, '')}`} target="_blank" rel="noreferrer">
            {info.version} ({info.environment})
          </a>
        )}
      </footer>
    </>
  );
}

function Snippets({ design }) {
  const [copied, setCopied] = useState(null);
  if (!design.tag) {
    return <p class="snippets-empty">The embed code appears once the badge has a tag.</p>;
  }

  const url = trackingUrl(design);
  const snippets = [
    ['Markdown', `![${design.label}](${url})`],
    ['HTML', `<img src="${url}" alt="${design.label}">`],
    ['URL', url],
  ];
  const copy = async (name, text) => {
    if (await copyText(text)) {
      setCopied(name);
      setTimeout(() => setCopied(null), 1500);
    }
  };

  return (
    <div class="snippets">
      {snippets.map(([name, text]) => (
        <div class="snippet" key={name}>
          <span class="snippet-name">{name}</span>
          <code>{text}</code>
          <button type="button" class={copied === name ? 'is-done' : ''} onClick={() => copy(name, text)} aria-label={`Copy ${name}`} title={`Copy ${name}`}>
            {copied === name ? <Check size={16} /> : <Copy size={16} />}
          </button>
        </div>
      ))}
    </div>
  );
}

render(<App />, document.getElementById('app'));
