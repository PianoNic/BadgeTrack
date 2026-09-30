// Strap and clip the badge card hangs from. Width comes from CSS.
export function Lanyard(props) {
  return (
    <svg viewBox="0 0 140 230" aria-hidden="true" {...props}>
      <defs>
        <linearGradient id="lanyard-metal" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stop-color="#9aa1a8" />
          <stop offset="0.5" stop-color="#e3e6e9" />
          <stop offset="1" stop-color="#8d949b" />
        </linearGradient>
      </defs>
      <path d="M20 0 H44 L74 182 H62 Z" fill="var(--brand)" />
      <path d="M120 0 H96 L66 182 H78 Z" fill="var(--brand-deep)" />
      <circle cx="70" cy="188" r="9" fill="none" stroke="url(#lanyard-metal)" stroke-width="4" />
      <path d="M60 196 H80 L84 210 H56 Z" fill="url(#lanyard-metal)" />
      <rect x="62" y="208" width="16" height="22" rx="3" fill="url(#lanyard-metal)" />
    </svg>
  );
}
