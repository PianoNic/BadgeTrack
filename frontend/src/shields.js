export const STYLES = [
  ['flat', 'Flat'],
  ['flat-square', 'Flat square'],
  ['plastic', 'Plastic'],
  ['for-the-badge', 'For the badge'],
  ['social', 'Social'],
];

// mirrors ShieldsBadgeUrlBuilder: shields.io splits on "-" and reads "_" as a space
const segment = (text) => encodeURIComponent(text.replaceAll('-', '--').replaceAll('_', '__'));

export function shieldsUrl({ label, color, style, logo }, count) {
  const query = new URLSearchParams({ style });
  if (logo) query.set('logo', logo);
  return `https://img.shields.io/badge/${segment(label)}-${count}-${segment(color)}.svg?${query}`;
}

export function trackingUrl({ tag, label, color, style, logo }) {
  const query = new URLSearchParams({ tag, label, color, style });
  if (logo) query.set('logo', logo);
  return new URL(`badge?${query}`, location.href).href;
}
