package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"simulator/internal/config"
	"simulator/internal/kafka"
	"syscall"
)

func main() {
	log.Println("Loading simulator...")
	_, startShutdown := signal.NotifyContext(context.Background(), os.Interrupt, os.Kill)
	defer startShutdown()

	cfg, err := config.Load()
	if err != nil {
		log.Fatalf("Error while loading configuration: %v", err)
	}

	consumer, err := kafka.NewConsumer(cfg)
	if err != nil {
		log.Fatalf("Error creating Kafka consumer: %v", err)
	}
	defer consumer.Close()

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	go func() {
		if err := consumer.Start(ctx); err != nil {
			log.Printf("Error in consumer: %v", err)
		}
	}()

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	<-sigChan
	log.Println("Получен сигнал завершения...")
	cancel()

	log.Println("Приложение завершено")
}
