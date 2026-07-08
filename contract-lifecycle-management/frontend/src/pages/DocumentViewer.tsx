import { useState, useEffect, useRef } from 'react';
import { Link, useParams } from 'react-router-dom';
import { contractsAPI, filesAPI } from '../services/api';
import { Document as DocumentType, FilesByType } from '../types';
import { Document, Page, pdfjs } from 'react-pdf';
import { renderAsync } from 'docx-preview';
import 'react-pdf/dist/esm/Page/AnnotationLayer.css';
import 'react-pdf/dist/esm/Page/TextLayer.css';

pdfjs.GlobalWorkerOptions.workerSrc = `//cdnjs.cloudflare.com/ajax/libs/pdf.js/${pdfjs.version}/pdf.worker.min.js`;

type ActiveTab = 'html' | 'pdf' | 'docx';

function DocumentViewer(): JSX.Element {
  const { contractId, documentId } = useParams<{ contractId: string; documentId: string }>();
  const [document, setDocument] = useState<DocumentType | null>(null);
  const [files, setFiles] = useState<FilesByType>({ html: null, docx: null, pdf: null, css: null });
  const [activeTab, setActiveTab] = useState<ActiveTab>('html');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [numPages, setNumPages] = useState<number | null>(null);
  const [pageNumber, setPageNumber] = useState<number>(1);
  const [docxLoading, setDocxLoading] = useState<boolean>(false);
  const docxContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    fetchDocument();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [contractId, documentId]);

  const fetchDocument = async (): Promise<void> => {
    if (!contractId || !documentId) return;

    try {
      setLoading(true);
      const response = await contractsAPI.getDocuments(contractId);
      const doc = response.data.find(d => d.document_id === parseInt(documentId));

      if (!doc) {
        setError('Document not found');
        return;
      }

      setDocument(doc);

      const filesByType: FilesByType = {
        html: doc.files.find(f => f.file_type === 'html') || null,
        docx: doc.files.find(f => f.file_type === 'docx') || null,
        pdf: doc.files.find(f => f.file_type === 'pdf') || null,
        css: doc.files.find(f => f.file_type === 'css') || null,
      };

      setFiles(filesByType);
      setError(null);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
      setError('Failed to load document: ' + errorMessage);
      console.error('Error fetching document:', err);
    } finally {
      setLoading(false);
    }
  };

  const onDocumentLoadSuccess = ({ numPages }: { numPages: number }): void => {
    setNumPages(numPages);
    setPageNumber(1);
  };

  const renderDocx = async (): Promise<void> => {
    if (!files.docx || !docxContainerRef.current) return;

    setDocxLoading(true);
    try {
      const response = await fetch(filesAPI.getFileUrl(files.docx.file_id));
      const blob = await response.blob();

      docxContainerRef.current.innerHTML = '';

      await renderAsync(blob, docxContainerRef.current, undefined, {
        className: 'docx-preview',
        inWrapper: true,
        ignoreWidth: false,
        ignoreHeight: false,
        ignoreFonts: false,
        breakPages: true,
        ignoreLastRenderedPageBreak: true,
        experimental: false,
        trimXmlDeclaration: true,
        useBase64URL: false,
        renderHeaders: true,
        renderFooters: true,
        renderFootnotes: true,
        renderEndnotes: true,
      });
    } catch (err) {
      console.error('Error rendering DOCX:', err);
      if (docxContainerRef.current) {
        docxContainerRef.current.innerHTML = '<p style="color: red;">Failed to render DOCX. Please download the file instead.</p>';
      }
    } finally {
      setDocxLoading(false);
    }
  };

  useEffect(() => {
    if (activeTab === 'docx' && files.docx) {
      renderDocx();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeTab, files.docx]);

  const renderFileViewer = (): JSX.Element => {
    switch (activeTab) {
      case 'html':
        if (!files.html) return <p>HTML file not found</p>;
        return (
          <div style={{
            border: '1px solid #ddd',
            borderRadius: '5px',
            backgroundColor: 'white',
            padding: '20px'
          }}>
            <iframe
              src={filesAPI.getFileUrl(files.html.file_id)}
              style={{
                width: '100%',
                height: '800px',
                border: 'none'
              }}
              title="HTML Document"
            />
            {files.css && (
              <p style={{ marginTop: '10px', fontSize: '12px', color: '#7f8c8d' }}>
                Styled with: {files.css.file_name}
              </p>
            )}
          </div>
        );

      case 'pdf':
        if (!files.pdf) return <p>PDF file not found</p>;
        return (
          <div style={{ textAlign: 'center' }}>
            <div style={{
              border: '1px solid #ddd',
              borderRadius: '5px',
              display: 'inline-block',
              backgroundColor: '#f5f5f5',
              padding: '20px'
            }}>
              <Document
                file={filesAPI.getFileUrl(files.pdf.file_id)}
                onLoadSuccess={onDocumentLoadSuccess}
                loading={<div>Loading PDF...</div>}
                error={<div>Failed to load PDF. <a href={filesAPI.getFileUrl(files.pdf.file_id)} download>Download instead</a></div>}
              >
                <Page
                  pageNumber={pageNumber}
                  renderTextLayer={true}
                  renderAnnotationLayer={true}
                  width={800}
                />
              </Document>
            </div>
            <div style={{
              marginTop: '15px',
              padding: '10px',
              backgroundColor: '#f8f9fa',
              borderRadius: '5px'
            }}>
              <button
                className="button"
                onClick={() => setPageNumber(prev => Math.max(prev - 1, 1))}
                disabled={pageNumber <= 1}
                style={{ marginRight: '10px' }}
              >
                Previous
              </button>
              <span style={{ margin: '0 15px', fontWeight: 'bold' }}>
                Page {pageNumber} of {numPages || '...'}
              </span>
              <button
                className="button"
                onClick={() => setPageNumber(prev => Math.min(prev + 1, numPages || prev))}
                disabled={pageNumber >= (numPages || 0)}
                style={{ marginLeft: '10px' }}
              >
                Next
              </button>
            </div>
            <div style={{ marginTop: '15px' }}>
              <a
                href={filesAPI.getFileUrl(files.pdf.file_id)}
                download
                className="button"
              >
                Download PDF
              </a>
            </div>
          </div>
        );

      case 'docx':
        if (!files.docx) return <p>DOCX file not found</p>;
        return (
          <div style={{
            border: '1px solid #ddd',
            borderRadius: '5px',
            backgroundColor: 'white',
            padding: '20px'
          }}>
            {docxLoading && (
              <div style={{ textAlign: 'center', padding: '20px' }}>
                <p>Loading DOCX preview...</p>
              </div>
            )}
            <div
              ref={docxContainerRef}
              style={{
                height: '800px',
                maxWidth: '100%',
                overflow: 'auto',
                backgroundColor: 'white'
              }}
            />
            <div style={{ marginTop: '15px', textAlign: 'center' }}>
              <a
                href={filesAPI.getFileUrl(files.docx.file_id)}
                download
                className="button"
              >
                Download DOCX File
              </a>
              <p style={{ marginTop: '10px', color: '#7f8c8d', fontSize: '14px' }}>
                File: {files.docx.file_name}
              </p>
            </div>
          </div>
        );

      default:
        return <p>Select a file type to view</p>;
    }
  };

  if (loading) {
    return <div className="loading">Loading document...</div>;
  }

  if (error) {
    return (
      <div>
        <div className="breadcrumb">
          <Link to="/" className="link">Contracts</Link>
          {' > '}
          <Link to={`/contracts/${contractId}/documents`} className="link">
            Contract {contractId} Documents
          </Link>
        </div>
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <div>
      <div className="breadcrumb">
        <Link to="/" className="link">Contracts</Link>
        {' > '}
        <Link to={`/contracts/${contractId}/documents`} className="link">
          Contract {contractId} Documents
        </Link>
        {' > '}
        <span>Document {documentId}</span>
      </div>

      <div className="card">
        <h2>Document Viewer</h2>
        <div style={{ marginBottom: '20px', padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '5px' }}>
          <p><strong>Contract ID:</strong> {contractId}</p>
          <p><strong>Document ID:</strong> {documentId}</p>
          <p><strong>Customer:</strong> {document?.customer_name}</p>
          <p><strong>Sites:</strong> {document?.sites_count}</p>
          <p><strong>Created:</strong> {document?.created_at ? new Date(document.created_at).toLocaleString() : 'N/A'}</p>
        </div>

        <div className="file-tabs">
          <button
            className={`file-tab ${activeTab === 'html' ? 'active' : ''}`}
            onClick={() => setActiveTab('html')}
            disabled={!files.html}
          >
            HTML
          </button>
          <button
            className={`file-tab ${activeTab === 'pdf' ? 'active' : ''}`}
            onClick={() => setActiveTab('pdf')}
            disabled={!files.pdf}
          >
            PDF
          </button>
          <button
            className={`file-tab ${activeTab === 'docx' ? 'active' : ''}`}
            onClick={() => setActiveTab('docx')}
            disabled={!files.docx}
          >
            DOCX
          </button>
        </div>

        <div className="file-viewer">
          {renderFileViewer()}
        </div>

        <div style={{ marginTop: '20px' }}>
          <h3>Available Files:</h3>
          <ul style={{ marginTop: '10px' }}>
            {document?.files?.map(file => (
              <li key={file.file_id} style={{ marginBottom: '5px' }}>
                <a
                  href={filesAPI.getFileUrl(file.file_id)}
                  className="link"
                  download
                >
                  {file.file_name}
                </a>
                {' '}
                ({file.file_type.toUpperCase()})
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}

export default DocumentViewer;
