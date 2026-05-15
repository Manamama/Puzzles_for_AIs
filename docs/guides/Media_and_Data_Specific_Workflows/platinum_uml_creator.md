
## PlantUML Nesting Elements Tips

When creating diagrams in PlantUML, it's crucial to understand the proper nesting of elements to avoid syntax errors. Here are the key rules:

1. **Top-Level Use of `component`**:
   - The `component` element can only be used at the top level and cannot be nested inside other elements like `box` or `rectangle`.

2. **Nesting Inside `rectangle`**:
   - To nest elements inside a `rectangle`, you must use other `rectangle` elements or `box` elements.

3. **Restrictions on `box` Nesting**:
   - You cannot nest any elements, including `rectangle` or `box`, directly inside a `box` element.

4. **Alias Assignment**:
   - `box` elements cannot be assigned aliases using the `as` keyword. This is reserved for elements like `node`, `rectangle`, and `component`.

5. **Proper Nesting**:
   - When nesting elements, maintain consistency. If the outermost container is a `rectangle`, then the nested elements should also be `rectangle` elements (or other nestable elements like `node` or `component`).

6. **Grouping and Labeling with `box`**:
   - `box` elements are used for grouping and labeling purposes but cannot have aliases assigned using `as`, nor can they have other elements nested directly inside them.

For example, the following will cause a syntax error due to improper nesting and aliasing:

```plantuml
box "Container" {
    rectangle "Nested" as nested
}
```

However, these examples follow the correct syntax:

```plantuml
rectangle "Container" {
    rectangle "Nested" as nested
}
```

```plantuml
rectangle "Container" {
    box "Nested"
}
```

By understanding and applying these rules, you can avoid syntax errors and create well-structured PlantUML diagrams. Remember that `box` elements cannot be treated like other nestable elements and should be used appropriately within the diagram's hierarchy.
