# daisyUI v5 component source subset

This build vendors an explicitly modified subset of MIT-licensed daisyUI v5 source so that the delivered HTML and CSS rebuild work without downloading the npm package. It is **not** the complete npm distribution, and is not the paid daisyUI Charts product.

Upstream: https://github.com/saadeghi/daisyui/tree/master/packages/daisyui/src/components
Retrieved 2026-09-21 through the GitHub connector. Source blob IDs:

| Component | Upstream blob |
|---|---|
| button.css | b78681e7ff633491dfa74d61f2804f5670dc52fe |
| card.css | 9122642e4327f493480c67c92fcb8dc82a976821 |
| badge.css | b4820f9e7f58668e5f49ef5c85bae12921bac53b |
| input.css | 17af9a0f1eb7f1bcb9fbe5b237b25bf5c0570e77 |

Local changes: preserve common component selectors, semantic variables and cascade layers; omit unused variants, card image/side behavior, decorative noise/shadows and special input types; generate repeated semantic color and size variants; use app-level light/dark themes. `@apply` is compiled using real Tailwind CSS. The blob IDs identify the original files, not hashes of this modified subset.

The normal npm manifest additionally declares daisyUI for future full-component development. The deterministic release CSS compiler uses this reviewed subset, not the npm plugin. The package installation was not possible in the delivery environment; no successful full-plugin installation is claimed. Do not add a new daisyUI component class without importing its source or enabling the full plugin.

License: [MIT](../licenses/daisyui-MIT.txt).
