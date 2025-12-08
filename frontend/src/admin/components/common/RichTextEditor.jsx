import React, { useMemo, useRef } from 'react';
import ReactQuill, { Quill } from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import './RichTextEditor.css';

// Import Quill modules for additional features
const Size = Quill.import('formats/size');
Size.whitelist = ['small', 'medium', 'large', 'huge'];
Quill.register(Size, true);

// Custom image handler for inserting images
const ImageHandler = (quillRef) => {
  const input = document.createElement('input');
  input.setAttribute('type', 'file');
  input.setAttribute('accept', 'image/*');
  input.click();

  input.onchange = async () => {
    const file = input.files[0];
    if (file) {
      // Check file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        alert('Image size must be less than 5MB');
        return;
      }

      // Convert to base64
      const reader = new FileReader();
      reader.onload = (e) => {
        const quill = quillRef.current?.getEditor();
        if (quill) {
          const range = quill.getSelection(true);
          quill.insertEmbed(range.index, 'image', e.target.result);
          quill.setSelection(range.index + 1);
        }
      };
      reader.readAsDataURL(file);
    }
  };
};

const RichTextEditor = ({ value, onChange, placeholder = 'Write your article content...' }) => {
  const quillRef = useRef(null);

  // Custom toolbar configuration (WordPress-like)
  const modules = useMemo(
    () => ({
      toolbar: {
        container: [
          // Text formatting
          [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
          [{ 'size': ['small', false, 'large', 'huge'] }],
          ['bold', 'italic', 'underline', 'strike'],
          
          // Text color and background
          [{ 'color': [] }, { 'background': [] }],
          
          // Lists and alignment
          [{ 'list': 'ordered'}, { 'list': 'bullet' }],
          [{ 'indent': '-1'}, { 'indent': '+1' }],
          [{ 'align': [] }],
          
          // Links, images, videos
          ['link', 'image', 'video'],
          
          // Block elements
          ['blockquote', 'code-block'],
          
          // Text direction
          [{ 'direction': 'rtl' }],
          
          // Font family
          [{ 'font': [] }],
          
          // Clean formatting
          ['clean']
        ],
        handlers: {
          image: () => ImageHandler(quillRef)
        }
      },
      clipboard: {
        matchVisual: false,
      },
    }),
    []
  );

  // Formats allowed in the editor
  const formats = [
    'header',
    'font',
    'size',
    'bold',
    'italic',
    'underline',
    'strike',
    'blockquote',
    'list',
    'bullet',
    'indent',
    'link',
    'image',
    'video',
    'color',
    'background',
    'align',
    'code-block',
    'direction'
  ];

  return (
    <div className="rich-text-editor">
      <ReactQuill
        ref={quillRef}
        theme="snow"
        value={value || ''}
        onChange={onChange}
        modules={modules}
        formats={formats}
        placeholder={placeholder}
      />
    </div>
  );
};

export default RichTextEditor;
