# Svelte 5 Runes in Threlte

## Dependency Injection
Threlte v8 heavily relies on contexts. Svelte 5 introduces reactivity that safely integrates with context retrieval. Always utilize the native context APIs provided by Threlte (e.g., `useThrelte()`) at the top level of the component script.

## The `$state` and `$derived` Directives
Use `$state` for primitive values or objects that require UI reactivity.

```svelte
<script lang="ts">
  import { T } from '@threlte/core';
  
  let radius = $state(5);
  let geometryArgs = $derived([radius, 32, 32]);
</script>

<T.Mesh>
  <T.SphereGeometry args={geometryArgs} />
</T.Mesh>
```

## Avoid Reactive Statements (`$:`)
The `$: ` syntax is fully deprecated in Svelte 5. Any architectural blueprint utilizing legacy reactive assignments must be immediately refactored to `$derived` or `$effect`.

## Property Passing
Utilize `$props()` to enforce rigid parent-to-child data flow, respecting the Law of Demeter.

```svelte
<script lang="ts">
  let { position = [0, 0, 0] } = $props<{ position?: [number, number, number] }>();
</script>

<T.Mesh {position}>
  <T.BoxGeometry />
</T.Mesh>
```