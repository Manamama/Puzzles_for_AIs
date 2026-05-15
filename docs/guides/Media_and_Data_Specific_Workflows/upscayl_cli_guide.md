# Guide to the Upscayl Command-Line Tool

This document provides a comprehensive guide to using the `upscayl-cli` command-line tool for AI-powered image upscaling.

## 1. Overview

`upscayl-cli` is a powerful command-line interface that leverages AI models to enlarge images, enhance resolution, and improve quality. It provides granular control over the upscaling process, including model selection, scaling factors, output formats, and hardware acceleration. The primary executable is `upscayl-bin`, which is often aliased to `upscayl-cli` for ease of use.

## 2. Available Models

The tool comes with a variety of pre-trained models, each suited for different types of images. The models are located in `/opt/Upscayl/resources/models/`. To use a model, you must specify its name (without the `.bin` or `.param` extension) using the `-n` flag.

The following models are available in the current installation:

*   `digital-art-4x`
*   `high-fidelity-4x`
*   `remacri-4x`
*   `ultramix-balanced-4x`
*   `ultrasharp-4x`
*   `upscayl-lite-4x`
*   `upscayl-standard-4x`

All listed models are designed for a **4x** upscale.

## 3. Command-Line Options

The tool offers a range of options to customize the upscaling process.

| Option | Argument | Description |
| :--- | :--- | :--- |
| **Required** | | |
| `-i` | `input-path` | Path to the input image (jpg, png, webp) or a directory of images. |
| `-o` | `output-path` | Path for the output image or directory. |
| **Scaling & Sizing** | | |
| `-s` | `output-scale` | Custom output scale factor (e.g., 2, 3, 4). Defaults to 4. |
| `-z` | `model-scale` | Scale according to the model's native factor (e.g., 2, 3, 4). Defaults to 4. |
| `-r` | `resize` | Resize output to specific dimensions (e.g., `1920x1080`). Use `-r help` for more details. |
| `-w` | `width` | Resize the output to a specific width, maintaining aspect ratio. |
| **Model & Format** | | |
| `-m` | `model-path` | Folder path to the pre-trained models. Defaults to the installation's `models` directory. |
| `-n` | `model-name` | The name of the model to use (e.g., `remacri-4x`). |
| `-f` | `format` | Output image format (jpg, png, webp). Defaults to the original extension or png. |
| `-c` | `compress` | Compression level for the output image (0-100). 0 is lowest compression, 100 is highest. |
| **Performance** | | |
| `-g` | `gpu-id` | Specify the GPU device to use (e.g., 0, 1). `auto` is the default. |
| `-j` | `load:proc:save`| Thread count for loading, processing, and saving. Example: `1:2:2`. |
| `-t` | `tile-size` | Tile size for processing (>=32). `0` for auto. Can be set per GPU (e.g., `0,0,0`). |
| **Other** | | |
| `-h` | | Show the help message. |
| `-x` | | Enable TTA (Test-Time Augmentation) mode for potentially higher quality at the cost of speed. |
| `-v` | | Enable verbose output for detailed processing information. |

## 4. Practical Example

Here is an example of upscaling a JPEG image by 4x its original size using a specific model.

### Command
```bash
upscayl-cli -i /home/zezen/Pictures/uroboros.jpg -o /home/zezen/Pictures/uroboros_upscaled.png -m /opt/Upscayl/resources/models/ -n remacri-4x
```

### Analysis
1.  **Input File:** `/home/zezen/Pictures/uroboros.jpg`
    *   Dimensions: 399x424 pixels
2.  **Processing:** The `remacri-4x` model is explicitly selected to perform a 4x upscale.
3.  **Output File:** `/home/zezen/Pictures/uroboros_upscaled.png`
    *   Dimensions: 1596x1696 pixels (4 times the original)
    *   Format: PNG (lossless)

## 5. Context & Related Tools

While the `context7` tool did not find direct documentation for Upscayl, it revealed a rich ecosystem of tools for image manipulation, optimization, and processing. Understanding this context helps situate Upscayl's role.

Upscayl specializes in **super-resolution** (upscaling), a task distinct from simple resizing. It uses AI to intelligently add detail where none existed. Other related tool categories include:

*   **Image Optimization Services:** Tools like `imgproxy` and `Spatie Image Optimizer` focus on reducing file size and serving images efficiently, often with on-the-fly resizing and format conversion.
*   **Image Augmentation Libraries:** Libraries like `Albumentations` and `imgaug` are used in machine learning to create variations of images (rotating, flipping, color shifts) to train more robust models.
*   **General Image Processing Libraries:** Tools like `Spatie Image` (PHP) or `rs-image` (Rust) provide a broad set of functions for programmatic image manipulation (cropping, filtering, etc.).

Upscayl's specific niche is using pre-trained AI models to achieve high-quality enlargements, a task that these other tools generally do not perform.
