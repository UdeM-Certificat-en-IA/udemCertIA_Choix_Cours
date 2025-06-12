# PDF to Markdown Conversion

This project includes a `pdf_to_md` module that converts course PDFs into Markdown files. The converter first attempts to extract text with `pdfminer.six`. If no text is returned, the module falls back to OCR using `pdftoppm` and `tesseract`.

Usage:

```bash
python scripts/convert_pdf_to_md.py <path/to/pdf> <output_directory>
```

All converted files are saved with the same basename in the specified output directory.
