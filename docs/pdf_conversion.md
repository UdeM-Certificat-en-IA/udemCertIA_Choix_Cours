# PDF to Markdown Conversion

This project includes a `pdf_to_md` module that converts course PDFs into Markdown files. The converter first attempts to extract text with `pdfminer.six`. If no text is returned, the module falls back to OCR using `pdftoppm` and `tesseract`.

## Requirements

- `pdfminer.six`
- `tesseract-ocr` and the `pdftoppm` utility from `poppler`

Ensure these tools are installed and available on your system path.

Usage:

```bash
python scripts/convert_pdf_to_md.py <path/to/pdf> <output_directory>
```

To convert the course PDFs shipped with this repository, execute the following from the project root:

```bash
for pdf in Courses/*/*.pdf Courses/*/.pdf/*.pdf; do
    python scripts/convert_pdf_to_md.py "$pdf" .md
done
```

All converted files are saved with the same basename in the specified output directory.
