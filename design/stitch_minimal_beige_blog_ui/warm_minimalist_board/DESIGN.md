---
name: Warm Minimalist Board
colors:
  surface: '#fbfbe2'
  surface-dim: '#dbdcc3'
  surface-bright: '#fbfbe2'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f5dc'
  surface-container: '#efefd7'
  surface-container-high: '#eaead1'
  surface-container-highest: '#e4e4cc'
  on-surface: '#1b1d0e'
  on-surface-variant: '#534340'
  inverse-surface: '#303221'
  inverse-on-surface: '#f2f2d9'
  outline: '#86736f'
  outline-variant: '#d9c1bd'
  surface-tint: '#8f4b3f'
  primary: '#89453a'
  on-primary: '#ffffff'
  primary-container: '#a65d50'
  on-primary-container: '#fff5f3'
  inverse-primary: '#ffb4a6'
  secondary: '#725a43'
  on-secondary: '#ffffff'
  secondary-container: '#ffdcbf'
  on-secondary-container: '#795f49'
  tertiary: '#645647'
  on-tertiary: '#ffffff'
  tertiary-container: '#7e6e5e'
  on-tertiary-container: '#fff4ed'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad4'
  primary-fixed-dim: '#ffb4a6'
  on-primary-fixed: '#3a0a04'
  on-primary-fixed-variant: '#723429'
  secondary-fixed: '#ffdcbf'
  secondary-fixed-dim: '#e1c1a5'
  on-secondary-fixed: '#291806'
  on-secondary-fixed-variant: '#59422d'
  tertiary-fixed: '#f4dfcb'
  tertiary-fixed-dim: '#d7c3b0'
  on-tertiary-fixed: '#241a0e'
  on-tertiary-fixed-variant: '#524436'
  background: '#fbfbe2'
  on-background: '#1b1d0e'
  surface-variant: '#e4e4cc'
typography:
  headline-xl:
    fontFamily: Be Vietnam Pro
    fontSize: 40px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Be Vietnam Pro
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.25'
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Be Vietnam Pro
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  body-lg:
    fontFamily: Be Vietnam Pro
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Be Vietnam Pro
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Be Vietnam Pro
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.4'
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Be Vietnam Pro
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.4'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  container-max: 720px
  gutter: 20px
---

## Brand & Style

This design system is built on the principles of **Warm Minimalism**. It aims to evoke a sense of calm, clarity, and approachability, moving away from the "clinical" feel of traditional white-space minimalism by utilizing a palette of organic, earthy tones. The target audience is readers and curators who value focus and intentionality.

The aesthetic leans into a "Digital Paper" feel—tactile and soft, yet structurally modern. The interface should feel like a physical journal or a well-curated board, emphasizing content over chrome. Visual noise is minimized through the use of soft-edged containers and a restricted color story.

## Colors

The palette is anchored by a two-tone beige foundation. The base background uses a clean off-white to maintain readability, while surfaces and containers use a warmer beige to create depth.

*   **Primary (Muted Terracotta):** Used for call-to-actions, active states, and highlights.
*   **Secondary (Soft Brown):** Used for metadata, secondary icons, and subtle borders.
*   **Neutrals:** A range of beige and off-white tones that prevent the high-contrast fatigue of pure black-and-white layouts.
*   **Text:** A deep, warm charcoal ensures high legibility while remaining softer than pure black.

## Typography

This design system utilizes **Be Vietnam Pro** across all levels to maintain a contemporary, approachable, and uniform look. 

The type scale is designed with an editorial focus. Headlines use tighter tracking and heavier weights to command attention, while body copy utilizes a generous line height (1.6) and a slightly larger base size to ensure a comfortable reading experience on both mobile and desktop. Labels utilize a medium weight and subtle letter spacing to provide clear hierarchy in metadata and functional UI elements.

## Layout & Spacing

The layout philosophy follows a **Fixed-Width Responsive** model. To maintain a "mobile-first" readability on desktop, the main content container is capped at 720px and centered. This mimics the width of a standard tablet or a large smartphone, ensuring that line lengths for blog posts remain optimal (60-75 characters).

Spacing follows a 4px-base rhythm. On desktop viewing, generous outer margins (32px+) are used to frame the content, creating a focused, "board-like" appearance. Grid gutters are kept at 20px to allow individual cards and posts enough room to breathe without feeling disconnected.

## Elevation & Depth

Hierarchy is established through **Ambient Shadows** and tonal layering. 

Rather than using harsh black shadows, this design system uses "tinted shadows"—shadows that incorporate a hint of the primary terracotta or secondary brown. This keeps the elevation feeling natural and warm. 

*   **Level 1 (Cards/Inputs):** A soft, highly diffused shadow (e.g., `0px 4px 12px rgba(60, 52, 49, 0.05)`).
*   **Level 2 (Hover states/Modals):** A slightly deeper, more pronounced shadow to indicate interactivity or priority.
*   **Surface Tiering:** Most interactive elements sit on the `#F5F5DC` surface, which itself rests on the `#FAF9F6` base background, providing a subtle "layered paper" effect without needing heavy borders.

## Shapes

The shape language is consistently **Rounded**, utilizing a base radius of 8px (0.5rem). This softens the overall aesthetic and reinforces the approachable brand personality.

*   **Buttons & Small Inputs:** 8px radius.
*   **Cards & Large Containers:** 12px to 16px radius.
*   **Chips/Pills:** Fully rounded (500px) to distinguish them from functional buttons.

Avoid sharp corners entirely; even progress bars and separators should feature rounded caps to maintain visual continuity.

## Components

### Buttons
*   **Primary:** Solid Terracotta (`#A65D50`) with white text. Rounded 8px.
*   **Secondary:** Muted Beige (`#F5F5DC`) with Soft Brown (`#8E735B`) text. 
*   **State Changes:** On hover, primary buttons should darken slightly; secondary buttons should gain a subtle 1px border of the accent color.

### Cards
Cards are the primary vehicle for the "board" aesthetic. They should feature a 12px corner radius, a Level 1 ambient shadow, and a 1px soft-beige border. Padding should be generous (24px) to emphasize the minimalist layout.

### Input Fields
Inputs should use the `#FAF9F6` background with an 8px corner radius. The border should be invisible or a very light beige unless the field is focused, at which point it transitions to a 1.5px Terracotta border.

### Chips & Tags
Used for categories and metadata. These should be pill-shaped with a background that is 10% opacity of the Primary color, using the Primary color for the text.

### Feed Items
Blog board items should follow a vertical stack: Featured Image (rounded 12px) → Category Label → Headline → Excerpt → Metadata. Use the secondary soft brown for metadata to reduce visual weight compared to the headline.