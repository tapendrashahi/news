# Home Page News Grid Fix Plan

## Investigation Summary (Dec 7, 2025)

### Current Issues Identified:

1. **Hero section displays properly** ✓
2. **First news item after hero shows alone** (should be in grid)
3. **2-column grid is shifted right**
4. **News cards are too small**
5. **Cards not properly aligned**

---

## Root Causes

### 1. **Conflicting CSS Definitions**
**Location:** `frontend/src/pages/Home.css`

**Problem:** Two different `.content-wrapper` definitions exist:
- Line 582-592: Uses `padding: 0 20px` and `max-width: 100%`
- Previous edits tried to set `max-width: 1800px` but there's another definition overriding it

### 2. **Grid Container Width Constraints**
```css
/* Current (PROBLEMATIC) */
.content-wrapper {
  padding: 0 20px;        /* Too small padding */
  max-width: 100%;        /* No centering constraint */
  grid-template-columns: 1fr 350px;  /* Sidebar too wide */
}

.news-grid__items {
  gap: 24px;              /* Gap too small */
}
```

### 3. **Split Hero Section Width**
```css
.split-hero {
  padding: 0 20px;        /* Same small padding */
  max-width: 100%;        /* No proper width limit */
}
```

### 4. **News Card Sizing Issues**
```css
.news-card__image {
  height: 220px;          /* Too small */
}

.news-card__content {
  padding: 20px;          /* Could be larger */
}

.news-card__title {
  font-size: 1.15rem;     /* Too small */
}
```

---

## Fix Plan

### Phase 1: Container Alignment & Width

**File:** `frontend/src/pages/Home.css`

1. **Update .content-wrapper**
```css
.content-wrapper {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 300px;  /* Reduce sidebar */
  gap: 48px;                                     /* Increase gap */
  margin: 0 auto 60px;                          /* Center it */
  padding: 0 40px;                              /* Better padding */
  max-width: 1600px;                            /* Proper max-width */
  width: 100%;
}
```

2. **Update .split-hero to match**
```css
.split-hero {
  padding: 0 40px;          /* Match content-wrapper */
  max-width: 1600px;        /* Match content-wrapper */
  margin-left: auto;
  margin-right: auto;
}
```

### Phase 2: News Grid Enhancement

3. **Increase grid gap**
```css
.news-grid__items {
  gap: 32px;                /* From 24px */
}
```

4. **Enlarge news cards**
```css
.news-card__image {
  height: 280px;            /* From 220px */
}

.news-card__content {
  padding: 24px;            /* From 20px */
}

.news-card__title {
  font-size: 1.35rem;       /* From 1.15rem */
}

.news-card__excerpt {
  font-size: 1rem;          /* From 0.9rem */
}
```

5. **Enhance large cards**
```css
.news-card--large .news-card__image {
  height: 380px;            /* From 320px */
}

.news-card--large .news-card__title {
  font-size: 1.75rem;       /* From 1.5rem */
}
```

### Phase 3: Responsive Consistency

6. **Update responsive breakpoints** to match new widths
```css
@media (max-width: 1024px) {
  .content-wrapper,
  .split-hero {
    padding: 0 32px;
  }
}

@media (max-width: 768px) {
  .content-wrapper,
  .split-hero {
    padding: 0 24px;
  }
}
```

---

## Why Previous Changes Didn't Work

1. **Multiple CSS files conflict**: Global styles vs component styles
2. **Inline styles in JSX**: Some padding might be set in component
3. **CSS specificity**: Later definitions override earlier ones
4. **Missing !important where needed**: Some critical rules get overridden
5. **Cached styles**: Browser/webpack cache old CSS

---

## Implementation Order

1. ✅ Search and remove duplicate .content-wrapper definitions
2. ✅ Apply Phase 1 changes (containers)
3. ✅ Apply Phase 2 changes (grid & cards)
4. ✅ Apply Phase 3 changes (responsive)
5. ✅ Clear browser cache / hard refresh
6. ✅ Test on different screen sizes

---

## Files to Modify

1. **Primary:** `frontend/src/pages/Home.css`
2. **Check:** `frontend/src/styles/global.css` (if exists)
3. **Check:** `frontend/src/index.css` (for body/html constraints)
4. **Verify:** `frontend/src/pages/Home.jsx` (no inline styles interfering)

---

## Expected Result

- Hero section: Full width, properly centered
- Content wrapper: Centered, max 1600px, proper padding
- News grid: 2 columns, 32px gap, larger cards
- Large cards: Span both columns at indices 0 and 5
- All elements aligned consistently
- Sidebar: 300px width, proper spacing
- Cards: Bigger images (280px), larger text, better spacing

---

## Testing Checklist

- [ ] Hero section centered and full-width
- [ ] First article after hero (index 0) spans full grid width
- [ ] Grid properly aligned with hero above
- [ ] 2-column layout with proper spacing
- [ ] Cards are noticeably larger
- [ ] Sidebar aligned properly on right
- [ ] No horizontal scroll
- [ ] Responsive on tablet (768px)
- [ ] Responsive on mobile (480px)
