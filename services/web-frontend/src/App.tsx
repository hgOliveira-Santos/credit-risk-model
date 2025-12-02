import React, { useState, useRef } from 'react';
import { UploadCloud, FileText, CheckCircle, XCircle, Loader2 } from 'lucide-react';

type Status = 'idle' | 'uploading' | 'success' | 'error';

const App: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [status, setStatus] = useState<Status>('idle');
  const [statusMessage, setStatusMessage] = useState<string>('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Validar extensão do arquivo
      const allowedExtensions = ['.csv', '.xlsx', '.xls'];
      const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
      
      if (allowedExtensions.includes(fileExtension)) {
        setSelectedFile(file);
        setStatus('idle');
        setStatusMessage('');
      } else {
        setStatus('error');
        setStatusMessage('Por favor, selecione um arquivo CSV ou Excel (.csv, .xlsx, .xls)');
        setSelectedFile(null);
      }
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();

    const file = event.dataTransfer.files?.[0];
    if (file) {
      const allowedExtensions = ['.csv', '.xlsx', '.xls'];
      const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
      
      if (allowedExtensions.includes(fileExtension)) {
        setSelectedFile(file);
        setStatus('idle');
        setStatusMessage('');
        // Atualizar o input file também
        if (fileInputRef.current) {
          const dataTransfer = new DataTransfer();
          dataTransfer.items.add(file);
          fileInputRef.current.files = dataTransfer.files;
        }
      } else {
        setStatus('error');
        setStatusMessage('Por favor, selecione um arquivo CSV ou Excel (.csv, .xlsx, .xls)');
        setSelectedFile(null);
      }
    }
  };

  const handleSubmit = async () => {
    if (!selectedFile) return;

    setStatus('uploading');
    setStatusMessage('');

    try {
      // Criar FormData
      const formData = new FormData();
      formData.append('file', selectedFile);

      // Chamada real para o backend Go
      const response = await fetch('http://localhost:8080/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || 'Falha no envio.');
      }

      const data = await response.json();
      
      setStatus('success');
      setStatusMessage(data.message || 'Arquivo recebido com sucesso!');
    } catch (error) {
      setStatus('error');
      setStatusMessage(error instanceof Error ? error.message : 'Falha no envio.');
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setStatus('idle');
    setStatusMessage('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl bg-white rounded-2xl shadow-lg p-8">
        <h1 className="text-3xl font-bold text-gray-800 text-center mb-8">
          Plataforma de Análise de Risco de Crédito
        </h1>

        {/* Área de Upload */}
        <div
          className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer transition-colors hover:border-blue-400 hover:bg-blue-50"
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv,.xlsx,.xls"
            onChange={handleFileSelect}
            className="hidden"
            id="file-upload"
          />
          
          {selectedFile ? (
            <div className="flex flex-col items-center space-y-3">
              <FileText className="w-12 h-12 text-blue-600" />
              <div className="flex flex-col items-center">
                <p className="text-lg font-semibold text-gray-700">
                  {selectedFile.name}
                </p>
                <p className="text-sm text-gray-500 mt-1">
                  {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleReset();
                }}
                className="text-sm text-red-600 hover:text-red-700 font-medium mt-2"
              >
                Remover arquivo
              </button>
            </div>
          ) : (
            <div className="flex flex-col items-center space-y-3">
              <UploadCloud className="w-12 h-12 text-gray-400" />
              <p className="text-gray-600 font-medium">
                Clique ou arraste o arquivo aqui
              </p>
              <p className="text-sm text-gray-400">
                Formatos aceitos: CSV, XLSX, XLS
              </p>
            </div>
          )}
        </div>

        {/* Botão de Envio */}
        <div className="mt-6 flex justify-center">
          <button
            onClick={handleSubmit}
            disabled={!selectedFile || status === 'uploading'}
            className="px-8 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center space-x-2 min-w-[160px] justify-center"
          >
            {status === 'uploading' ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Enviando...</span>
              </>
            ) : (
              <span>Enviar Arquivo</span>
            )}
          </button>
        </div>

        {/* Feedback de Status */}
        {statusMessage && (
          <div className="mt-6 flex items-center justify-center space-x-2">
            {status === 'success' ? (
              <>
                <CheckCircle className="w-5 h-5 text-green-600" />
                <p className="text-green-600 font-medium">{statusMessage}</p>
              </>
            ) : status === 'error' ? (
              <>
                <XCircle className="w-5 h-5 text-red-600" />
                <p className="text-red-600 font-medium">{statusMessage}</p>
              </>
            ) : null}
          </div>
        )}
      </div>
    </div>
  );
};

export default App;

