package handlers

import (
	"fmt"
	"io"
	"os"
	"path/filepath"
	"time"

	"github.com/gin-gonic/gin"
)

func UploadFileHandler(c *gin.Context) {
	file, err := c.FormFile("file")
	if err != nil {
		c.JSON(400, gin.H{
			"error":   "Nenhum arquivo foi enviado",
			"message": err.Error(),
		})
		return
	}

	allowedExtensions := map[string]bool{
		".csv":  true,
		".xlsx": true,
		".xls":  true,
	}

	ext := filepath.Ext(file.Filename)
	if !allowedExtensions[ext] {
		c.JSON(400, gin.H{
			"error":   "Tipo de arquivo não permitido",
			"message": "Apenas arquivos CSV e Excel (.csv, .xlsx, .xls) são aceitos",
		})
		return
	}

	uploadDir := "uploads"
	if err := os.MkdirAll(uploadDir, 0755); err != nil {
		c.JSON(500, gin.H{
			"error":   "Erro ao criar diretório de uploads",
			"message": err.Error(),
		})
		return
	}

	timestamp := time.Now().Format("20060102-150405")
	baseName := filepath.Base(file.Filename)

	nameWithoutExt := baseName[:len(baseName)-len(ext)]
	filename := fmt.Sprintf("%s-%s%s", timestamp, nameWithoutExt, ext)
	filePath := filepath.Join(uploadDir, filename)

	src, err := file.Open()
	if err != nil {
		c.JSON(500, gin.H{
			"error":   "Erro ao abrir arquivo",
			"message": err.Error(),
		})
		return
	}
	defer src.Close()

	dst, err := os.Create(filePath)
	if err != nil {
		c.JSON(500, gin.H{
			"error":   "Erro ao criar arquivo",
			"message": err.Error(),
		})
		return
	}
	defer dst.Close()

	if _, err := io.Copy(dst, src); err != nil {
		c.JSON(500, gin.H{
			"error":   "Erro ao salvar arquivo",
			"message": err.Error(),
		})
		return
	}

	c.JSON(200, gin.H{
		"message":  "Arquivo recebido com sucesso!",
		"filename": filename,
		"path":     filePath,
		"size":     file.Size,
	})
}
