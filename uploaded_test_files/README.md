# 📁 Uploaded Test Files Directory

This directory contains real files for testing the invoice upload functionality.

## 📋 How to Use:

1. **Add your test files here** - Upload any invoice files you want to test:
   - ✅ PDF invoices
   - ✅ Image files (JPG, PNG)  
   - ✅ Document files (DOC, DOCX)
   - ✅ Hebrew language invoices
   - ✅ Any real invoice formats

2. **File naming suggestions**:
   - `invoice_hebrew_alpha_computers.pdf` - Your Hebrew Alpha.A invoice
   - `invoice_english_sample.pdf` - English invoice sample
   - `invoice_large_file.pdf` - Large file for testing limits
   - `invoice_special_chars.pdf` - Files with special characters
   - `invalid_file.xyz` - Invalid format for error testing

3. **The test will automatically**:
   - Scan this directory for files
   - Use them for upload testing
   - Test duplicate prevention
   - Test file deletion (C8010)
   - Support multiple file formats

## 🔧 Test Integration:

The upload tests (`test_upload_invoice_file`) will:
- **Auto-detect** files in this directory
- **Upload** each file type
- **Verify** successful upload
- **Test** duplicate prevention
- **Clean up** uploaded files

## 📝 Example Files to Add:

```
uploaded_test_files/
├── invoice_hebrew_alpha.pdf          # Your Hebrew invoice
├── invoice_english_sample.pdf        # Standard English invoice  
├── invoice_image.jpg                 # Image format test
├── invoice_large.pdf                 # Large file test
├── invoice_special_chars_#@$.pdf     # Special characters test
└── invalid_format.xyz               # Invalid format test
```

## 🎯 Benefits:

✅ **Real file testing** - Use actual invoice files  
✅ **Multiple formats** - Test PDF, images, documents  
✅ **Hebrew support** - Test international invoices  
✅ **Flexible** - Add/remove files as needed  
✅ **Realistic** - Tests real-world scenarios  

**Simply add your files here and run the tests!** 🚀 