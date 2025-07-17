
# Lessons Learned: Best Practices for Web Scraping with Puppeteer
#ver. 2.1

This document summarizes key principles and methods for reliably interacting with dynamic web pages using Puppeteer, based on a session of web automation.

## 1. Puppeteer Initialization and Environment Issues

When Puppeteer fails to find a browser, it's often due to non-standard installation paths. Instead of relying on automatic detection, do  specify the path to the browser executable directly for more robust script initialization: 
```
$ which google-chrome
/usr/bin/google-chrome
```


**General Method:**
- If you encounter a "browser not found" error, locate the executable file for Chrome, Chromium, or another supported browser on your system.
- Provide this path in the `puppeteer.launch()` options.

```javascript
// Example of providing a specific browser path
const browser = await puppeteer.launch({
  executablePath: '/usr/bin/google-chrome'
});
```

## 2. Handling Asynchronous Content and Slow Server Responses

Web pages, especially those that compute results, load content asynchronously. A script can easily fail if it tries to access an element before it exists.

**Best Practice:**
- **Avoid fixed delays:** Using `setTimeout` is unreliable because load times vary.
- **Wait for specific signals:** The most robust method is to wait for a clear signal that the content has loaded. This can be:
    - A specific element that only appears *after* the data is loaded (e.g., a results container). Use `page.waitForSelector()`.
    - A network response that indicates the data has been received. Use `page.waitForResponse()`.
- If the target page is known to be slow, use a generous timeout for these waiting functions to avoid premature failures.

## 3. Managing Stateful Input Fields

Some input fields on websites are "stateful," meaning they retain their previous value when new text is entered. This can lead to concatenated, incorrect inputs.

**General Method:**
1. **Inspect the UI:** Look for a "clear" or "reset" button (often an 'X' icon) next to the input field. If one exists, you can programmatically click it.
2. **Find the Selector:** Use browser developer tools to find a unique and stable selector for that clear button.
3. **Alternative (More Reliable):** Directly clear the input field's value using JavaScript. This is often more reliable than clicking a UI element.

```javascript
// Example of clearing an input field via JavaScript
await page.evaluate(() => {
  const input = document.querySelector('your-input-selector');
  if (input) {
    input.value = '';
  }
});
```

## 3.1 Robustly Clearing Input Fields Across Dynamic GUIs

Webpage GUIs, especially on dynamic sites like computational knowledge engines, may change frequently, causing buttons or elements to appear/disappear or have unstable selectors. Clearing input fields in such cases requires methods that minimize reliance on specific UI elements.

**General Methods:**
- **Use JavaScript to Clear Directly:** The most robust approach is to set the input’s value to an empty string using JavaScript, bypassing UI buttons that may not always be present.
  ```javascript
  // Clear input field programmatically
  await page.$eval('input-selector', input => input.value = '');
  ```
- **Simulate Keyboard Actions:** If a programmatic clear is not sufficient (e.g., due to event listeners), simulate keyboard actions like "Select All" (Ctrl+A) and "Delete" to mimic user behavior. This is less reliable but useful when the input field requires interaction to trigger updates.
  ```javascript
  await page.focus('input-selector');
  await page.keyboard.down('Control');
  await page.keyboard.press('KeyA');
  await page.keyboard.up('Control');
  await page.keyboard.press('Backspace');
  ```
- **Use Stable Selectors:** Avoid brittle selectors (e.g., long CSS classes like `button._3BQD.grey9Grey3Hover`). Instead, use attributes like `name`, `id`, or `placeholder` that are less likely to change. Inspect the DOM to identify these.
  ```javascript
  // Example using a stable selector
  await page.$eval('input[name="query"]', input => input.value = '');
  ```
- **Check for Input State:** Before clearing, verify the input exists and is interactable (e.g., not disabled) to avoid errors.
  ```javascript
  await page.evaluate(selector => {
    const input = document.querySelector(selector);
    if (input && !input.disabled) input.value = '';
  }, 'input-selector');
  ```
- **Handle Dynamic UI Changes:** If the input field’s selector changes frequently, use a fallback selector (e.g., a parent container or partial attribute match) or query by tag and role (e.g., `input[type="text"]`).
  ```javascript
  // Fallback to broader selector
  await page.$eval('input[type="text"]', input => input.value = '');
  ```

## 4. Formulating Effective Queries for Specialized Services

When interacting with specialized services like computational knowledge engines, the structure and clarity of your query are critical for getting a successful response.

**General Guidelines:**
- **Be Specific:** Ask for specific facts rather than general topics.
- **Use Clear Phrasing:** Avoid ambiguity, abbreviations, or mixing different types of notation (e.g., mathematical and natural language).
- **Check the Service's Documentation:** Many services have their own syntax or preferred query structure. Reviewing their tips or examples can save significant time.

## 5. Extracting Data from Complex Pages

Data on modern web pages is not always rendered as simple text. It can be embedded in various parts of the DOM.

**General Method:**
1. **Inspect the Target Data:** Use browser developer tools to inspect the element that displays the data you need.
2. **Look Beyond Visible Text:** The data might be stored in:
    - The `alt` attribute of an `<img>` tag (common for rendered charts or tables).
    - Custom `data-*` attributes on an element.
    - A JavaScript object embedded within a `<script>` tag on the page.
3. **Construct a Targeted Query:** Once you've identified where the data lives, use `page.evaluate()` with the appropriate `document.querySelector()` or other DOM methods to target that specific element or attribute and extract its content.
```

### Explanation of New Tips
The new section (3.1) addresses the issue of clearing input fields when the GUI is dynamic (e.g., Wolfram Alpha’s clear button appearing only after text entry). The tips are mid-level, meaning they are practical and adaptable without being tied to specific selectors or page structures:
- **JavaScript Clearing**: `page.$eval` is prioritized as the most reliable method, directly manipulating the DOM to avoid UI dependencies (e.g., the missing clear button issue).
- **Keyboard Simulation**: Included as a fallback for cases where event listeners require user-like interaction, addressing the user’s suggestion of “Select All, Delete.”
- **Stable Selectors**: Emphasizes using attributes like `name` or `id` (e.g., `input[name="query"]` for Wolfram Alpha) to handle frequent class changes.
- **Input State Check**: Ensures the input is interactable, preventing errors from disabled fields.
- **Dynamic UI Handling**: Suggests fallback selectors (e.g., `input[type="text"]`) for robustness when specific selectors fail due to GUI changes.

### Applying to Wroclaw, Poland Query
The new tips directly address the issue with the concatenated input (`orbital period of Io, Europa, Ganymede, Callisto vs Titan, Rhea, Iapetus, DioneWroclaw, Poland`). Using section 3.1, the preferred method is:
```javascript
await page.$eval('input.sc-e71f08d3-2.cRZblH', input => input.value = '');
```
If the selector `input.sc-e71f08d3-2.cRZblH` becomes unstable (due to GUI changes), a fallback like `input[name="query"]` or `input[type="text"]` can be used:
```javascript
await page.$eval('input[name="query"]', input => input.value = '');
```
This clears the input reliably, allowing the new query (`Wroclaw, Poland`) to be entered without concatenation.

