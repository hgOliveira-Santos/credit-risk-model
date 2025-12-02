package main

import (
	"log"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/hgOliveira-Santos/credit-risk-model/handlers"
)

func main() {
	// Criar servidor Gin
	server := gin.Default()

	// Configurar CORS para permitir requisições do frontend
	config := cors.DefaultConfig()
	config.AllowOrigins = []string{"http://localhost:5173", "http://localhost:3000"}
	config.AllowMethods = []string{"GET", "POST", "PUT", "DELETE", "OPTIONS"}
	config.AllowHeaders = []string{"Origin", "Content-Type", "Accept", "Authorization"}
	config.AllowCredentials = true
	server.Use(cors.New(config))

	// Rotas
	api := server.Group("/api")
	{
		api.POST("/upload", handlers.UploadFileHandler)
		// Adicionar outras rotas aqui quando necessário
	}

	// Iniciar servidor
	port := ":8080"
	log.Printf("Servidor iniciado na porta %s", port)
	log.Printf("Endpoint de upload disponível em: http://localhost%s/api/upload", port)

	if err := server.Run(port); err != nil {
		log.Fatal("Erro ao iniciar servidor:", err)
	}
}
