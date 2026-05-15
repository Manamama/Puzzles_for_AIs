# Document Processing Guidelines

This document outlines a refined strategy for processing various document formats, particularly focusing on the handling and interpretation of image content, to maximize contextual understanding and leverage VLM capabilities through user interaction.

## Core Principles:

1.  **Prioritize Richer Formats:** Always prefer `docling`-generated Markdown (`.md` with associated `_artifacts` folder) over simpler OCR'd text or basic Markdown conversions. The `docling` format provides superior structural fidelity (tables) and explicit image extraction.

2.  **Explicit Image Handling:**
    *   **Recognize Image Links:** When encountering `![Image](path/to/image.png)` tags in Markdown, understand that a corresponding image file exists in the specified `_artifacts` directory. This is the primary mode when `docling` is configured with `--image-export-mode referenced`.
    *   **Identify Embedded OCR Text (Special Case):** Be aware that for certain images (e.g., diagrams primarily composed of text), `docling` may *instead* embed the OCR'd text content directly into the Markdown, without a separate `![Image](...)` link, even when configured for `referenced` mode. This embedded text *is* the image's content as interpreted by the conversion tool.
    *   **Request Visuals When Necessary:** If a visual understanding of an image (whether linked or represented by embedded OCR text) is critical for the task, and my internal VLM capabilities cannot directly process the raw image file, I must explicitly request the user to "feed" the image. This means asking the user to:
        *   Provide a textual description of the image.
        *   Provide an OCR output of the image (if available).
        *   Confirm the image's content if I have its OCR'd text.

3.  **Leverage User's VLM:** The user acts as an extension of my VLM capabilities. When they "feed" an image (by providing its description or OCR), I must integrate this information into my understanding of the document.

4.  **Pre-`docling` PDFs:**
    *   If only raw PDF files are available, especially those containing scanned images or non-selectable text, I cannot parse their content. My `read_file` tool sees them as unreadable binary files and is not sufficient in such cases.
    *   For me to understand such documents, they must first be processed through an external OCR tool like the user's `docling` or `docling_me.sh` script.
    *   Therefore, if a task requires understanding a raw PDF, I should state my limitation and recommend the user process it first.

5.  **Maintain Clarity:** Always be transparent about the nature of the information I am working with (e.g., "This is OCR'd text from an image," "This is a linked image file," "I have the text but not the visual interpretation").

## Understanding `docling` Options

### `docling`'s Behavior with `--no-ocr`

Even when the `--no-ocr` flag is used, `docling` functions as a sophisticated document conversion tool, not just a simple text extractor. It intelligently parses the PDF's structure to create a well-formatted output.

Here's what it does:

1.  **PDF Parsing:** It uses its configured PDF backend (e.g., `dlparse_v2`) to analyze the internal structure of the document, including text blocks, their positions, and embedded images.

2.  **Text Extraction:** It extracts text directly from the PDF's existing text layer, without performing any optical character recognition.

3.  **Layout Reconstruction:** This is the key step where `docling` adds value. It reconstructs the document's visual layout in Markdown, which includes:
    *   **Table Formatting:** Identifying tabular data and converting it into structured Markdown tables.
    *   **Image Referencing:** Extracting embedded images, saving them as separate files (e.g., in the `_artifacts` directory), and creating Markdown links to them in the output file.
    *   **Structural Formatting:** Applying Markdown for headers, lists, and other elements to maintain the document's hierarchy and readability.

This process results in a clean, structured, and more usable Markdown file that preserves the document's layout, as opposed to a simple, unformatted text dump.

### `--enrich-picture-classes` Option

The `--enrich-picture-classes` option enables the **Picture Classification** step in the `docling` pipeline. This step utilizes the `DocumentFigureClassifier` model.

Its purpose is to analyze and classify `PictureItem` elements (images) found within the document. It categorizes these images into various types, such as:

*   Different chart types (e.g., bar charts, pie charts)
*   Flow diagrams
*   Logos
*   Signatures
*   And other specialized document figures.

This classification is crucial because `docling` uses this information to make intelligent decisions about how to represent each image in the final Markdown output. For instance, a diagram primarily composed of text might be represented by its OCR'd text, while a logo might be linked as a separate image file, even when `--image-export-mode referenced` is generally active.

## Limitations and Workarounds

### Inaccessible VLM Image Descriptions

Our investigation has revealed a significant limitation in the current version of `docling` regarding the `--enrich-picture-description` feature.

*   **The Issue:** While enabling this feature (e.g., programmatically via `pipeline_options.do_picture_description = True`) does trigger the execution of a VLM to generate image descriptions, the output is currently inaccessible.
*   **Root Cause:** The `PictureItem` data object within the `docling_core` data model **does not have a `description` attribute**. Therefore, when the VLM generates a description, there is no field in the document object to store it. This results in an `AttributeError` if one attempts to access `item.description` and means the description cannot be saved to the final Markdown file.
*   **Workaround:** Until this is addressed in the `docling` library, the most effective way to get a VLM description of an image is to use the principle of "Leverage User's VLM" (see Core Principle #3). The agent should request the user to provide the specific image file, and then the agent can use its own internal VLM capabilities to analyze and describe it.

## Performance and Quality Analysis of `docling` Options

Our experiments have provided valuable insights into the performance and quality of different `docling` configurations, especially concerning the `--enrich-picture-description` flag.

### Performance: The High Cost of Picture Descriptions

The most significant finding is the extremely high performance cost associated with the `--enrich-picture-description` flag.

*   **Non-Linear Scaling:** This feature's processing time scales non-linearly with the size of the document. In our tests, a 12-16 page PDF took approximately 17 minutes to process, while a 78-page document took nearly 3 hours. This represents a ~10x increase in time for a ~5-6x increase in pages.
*   **Predictable Scaling of Other Options:** In contrast, other configurations (`--enrich-picture-classes`, `ocr`, and `no-ocr`) demonstrated much more predictable, roughly linear scaling. Their processing times increased from around 1 minute to ~7 minutes for the same documents.

### Quality: Low "Bang for the Buck"

Given the inordinate amount of time and CPU resources consumed, the quality of the generated picture descriptions is disappointingly low.

*   **Generic and Unhelpful:** The majority of descriptions are generic and state the obvious (e.g., "In this image we can see a diagram"). They provide little to no value for a user who cannot see the image.
*   **Repetitiveness and Hallucination:** In many cases, the model appears to get stuck in a loop, producing highly repetitive and nonsensical text. For example, one description devolved into a long, rambling list of "a switch, a light, a switch board...".
*   **Inconsistent Quality:** The quality is highly inconsistent. While some descriptions are vaguely useful, many are inaccurate or completely nonsensical.

### Recommendation

Based on these findings, the `--enrich-picture-description` feature is **not recommended for general use** in its current state. The low quality of the output does not justify the extremely high performance cost. For tasks requiring image understanding, the "Leverage User's VLM" approach (requesting the user to provide descriptions) remains the most effective and efficient strategy.

## Actionable Steps:

*   When a task involves analyzing a document, first check for the presence of `docling`-generated Markdown files and their associated `_artifacts` folders.
*   If `docling` output is available, prioritize it for information extraction.
*   For any figure or diagram that seems crucial for the task, and if its content is not fully clear from text alone (either from captions or embedded OCR'd text):
    *   If an `![Image](...)` link exists, note the filename.
    *   If only embedded OCR'd text is present, note that this is the tool's interpretation of the image.
    *   In either case, if deeper visual understanding is required, prompt the user by stating the figure number/context and asking for a visual description or confirmation of the image's content.

By following these guidelines, I can navigate the complexities of diverse document formats more effectively, ensuring a more accurate and comprehensive understanding of the provided materials.