# Svelte 5 Runes Reference

This document provides definitive guidance on utilizing Svelte 5 Runes for optimal performance and strict architectural adherence.

## State Management (`$state`)

The `$state` rune replaces `let` for reactive variables. It utilizes deeply reactive proxies.

```svelte
<script>
    let count = $state(0);
    let user = $state({ name: 'Alice', age: 30 });
</script>
```

- **Mutation**: Reassignment or deep property mutation triggers updates automatically.
- **Classes**: Use `$state` fields in class definitions within `.svelte.ts` files to encapsulate logic, separate concerns, and respect the Law of Demeter.

## Derived State (`$derived`)

The `$derived` rune replaces legacy `$: {}` blocks for computed values. It evaluates lazily and caches the result.

```svelte
<script>
    let count = $state(0);
    let double = $derived(count * 2);
</script>
```

- **Performance**: Use `$derived` to prevent unnecessary recalculations. Do not use `$effect` to compute state.

## Side Effects (`$effect`)

The `$effect` rune executes functions after the DOM has been updated, similar to `onMount` or legacy reactive statements that performed side effects.

```svelte
<script>
    let count = $state(0);
    
    $effect(() => {
        document.title = `Count: ${count}`;
        
        return () => {
            // Cleanup logic runs before the effect re-runs or component unmounts
        };
    });
</script>
```

- **Restriction**: Never use `$effect` to synchronize state. It is strictly for interacting with external systems (APIs, DOM, Canvas).

## Component Inputs (`$props`)

The `$props` rune replaces `export let`.

```svelte
<script>
    let { title, count = 0, onchange } = $props();
</script>
```

- **Event Passing**: Pass callback functions as props (e.g., `onchange`) instead of using `createEventDispatcher`.

## Snippets (`#snippet`)

Snippets replace `<slot>` for passing reusable markup chunks.

```svelte
{#snippet button(text)}
    <button class="btn">{text}</button>
{/snippet}

{@render button('Submit')}
```
