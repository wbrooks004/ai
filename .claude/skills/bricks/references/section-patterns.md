> **Version note.** Written against ACSS 3.x. On a 4.x site read `../../modern-web-standards/references/acss-4-alignment.md` first: several utility classes below are unconfirmed in 4.x, `xxl` is now `2xl`, and the `@media (max-width)` examples should become `@container` queries. The **variables** listed here remain the trustworthy part.

# Section patterns

Shapes to adapt, not templates to copy verbatim. The first entry shows the **full output format**; the
rest show markup only. Every example uses a `gg-` prefix as a stand-in — swap in the real client prefix.

## Contents

- [Full worked example: service grid](#full-worked-example-service-grid)
- [Hero](#hero)
- [FAQ](#faq)
- [CTA band](#cta-band)
- [Contact form](#contact-form)
- [Adapting these](#adapting-these)

---

## Full worked example: service grid

This is exactly what a response should look like.

### What this builds

A three-up service card grid that collapses to two columns on tablet and one on mobile. Assumed a
`gg-` prefix and placeholder icons — swap both.

### Paste into Bricks

```html
<style>
  .gg-service-card {
    display: flex;
    flex-direction: column;
    gap: var(--space-s);
    padding: var(--space-m);
    border-radius: var(--radius-m);
    background: var(--base-ultra-light);
  }

  .gg-service-card__icon {
    width: var(--space-l);
    height: var(--space-l);
  }

  @media (max-width: 991px) {
    .gg-service-grid { grid-template-columns: var(--grid-2); }
  }

  @media (max-width: 767px) {
    .gg-service-grid { grid-template-columns: var(--grid-1); }
  }
</style>

<section>
  <div class="container content-gap">
    <h2>Family law services across Montreal</h2>
    <p class="text--l">Straight answers and steady representation, in French and in English.</p>

    <div class="grid--3 grid-gap gg-service-grid">
      <article class="gg-service-card">
        <img class="gg-service-card__icon" src="/wp-content/uploads/icon-divorce.svg" alt="" width="48" height="48" loading="lazy">
        <h3>Divorce and separation</h3>
        <p>Filing, negotiation, and court representation for contested and uncontested matters.</p>
        <a href="/services/divorce/">Learn more</a>
      </article>

      <article class="gg-service-card">
        <img class="gg-service-card__icon" src="/wp-content/uploads/icon-custody.svg" alt="" width="48" height="48" loading="lazy">
        <h3>Child custody and support</h3>
        <p>Custody arrangements, support calculations, and modifications to existing orders.</p>
        <a href="/services/custody/">Learn more</a>
      </article>

      <article class="gg-service-card">
        <img class="gg-service-card__icon" src="/wp-content/uploads/icon-estate.svg" alt="" width="48" height="48" loading="lazy">
        <h3>Wills and estates</h3>
        <p>Drafting, probate, and estate disputes handled start to finish.</p>
        <a href="/services/estates/">Learn more</a>
      </article>
    </div>
  </div>
</section>
```

### New global classes this creates

| Class | Purpose |
|---|---|
| `.gg-service-card` | Card shell — padding, radius, background, internal gap |
| `.gg-service-card__icon` | Fixed icon sizing inside the card |
| `.gg-service-grid` | Responsive column overrides for the card grid |

### After pasting

1. Replace the three placeholder icon paths with real SVGs from the Media Library.
2. Point the three "Learn more" links at the real service pages.
3. If these cards will repeat across location pages, convert one card to a Bricks component and bind the
   fields — don't paste this section three more times.
4. Decorative icons carry empty `alt=""` deliberately. If an icon conveys meaning the heading doesn't,
   write real alt text.

---

## Hero

Note the single `<h1>`, the sizing coming from a text utility rather than a heading tag, and zero custom
CSS — a one-off hero rarely needs a global class.

```html
<section>
  <div class="container content-gap">
    <h1>Movers Toronto trusts with the hard jobs</h1>
    <p class="text--l">Stairs, pianos, tight downtown loading docks. Fixed quotes, no hourly surprises.</p>
    <div class="flex gap--s">
      <a href="/quote/" class="btn">Get a fixed quote</a>
      <a href="tel:+14165551234">(416) 555-1234</a>
    </div>
  </div>
</section>
```

If `.btn` is not confirmed on the site, replace it with `gg-hero__cta` and style it with variables.

## FAQ

Semantic `<details>` converts cleanly and works without JavaScript. Say so in the handoff notes — the
alternative is a Bricks Accordion element the user builds themselves, which is worth it if they want
schema markup and animation.

```html
<section>
  <div class="container content-gap">
    <h2>Common questions</h2>

    <details class="gg-faq__item">
      <summary>Do you charge by the hour or by the job?</summary>
      <p>By the job. You get a fixed written quote after a walkthrough, and it doesn't change on moving day.</p>
    </details>

    <details class="gg-faq__item">
      <summary>Are you insured?</summary>
      <p>Fully insured and licensed. Certificates are available on request before booking.</p>
    </details>
  </div>
</section>
```

## CTA band

```html
<style>
  .gg-cta {
    background: var(--primary);
    color: var(--base-ultra-light);
    border-radius: var(--radius-m);
    padding: var(--space-l);
    text-align: center;
  }
</style>

<section>
  <div class="container">
    <div class="gg-cta content-gap">
      <h2>Ready for a fixed quote?</h2>
      <p class="text--l">Most quotes come back the same day.</p>
      <a href="/quote/">Start your quote</a>
    </div>
  </div>
</section>
```

Check the contrast between the palette colour and the text colour before shipping — ACSS palettes are
configurable and `var(--primary)` is not guaranteed to be dark.

## Contact form

Emit a plain semantic form and hand the wiring to the user. Do **not** attempt to generate a Bricks Form
element's markup — form actions, validation, and submission handling are Bricks settings, not HTML, and
ACSS has a single-class form styling system that should own the appearance.

```html
<section>
  <div class="container content-gap">
    <h2>Request a quote</h2>
    <form>
      <label for="name">Name</label>
      <input type="text" id="name" name="name" required>

      <label for="email">Email</label>
      <input type="email" id="email" name="email" required>

      <label for="details">What do you need moved?</label>
      <textarea id="details" name="details" rows="4"></textarea>

      <button type="submit">Send request</button>
    </form>
  </div>
</section>
```

Handoff note to include: *"Rebuild this as a native Bricks Form element after paste so submissions, spam
protection, and the confirmation action work. Use it as the field list and label copy."*

## Adapting these

- Change the column count by changing `.grid--{n}` and the media query variables together — they must agree.
- Adding a second container to a section? Put `.container-gap` on the section.
- Adding more content elements inside a container? `.content-gap` on the container handles the rhythm; don't
  add margins.
- If a pattern needs more than about three custom classes, it is probably a component. Say so, and suggest
  building it once in Bricks and reusing it rather than pasting variants.
