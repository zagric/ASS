package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"simulator/internal/config"
	"simulator/internal/kafka"
	"simulator/internal/worker"
	"sync"

	"syscall"
)

func main() {
	log.Println("Starting Queuing System Simulator")

	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	cfg, _ := config.Load()

	pool := worker.NewWorkerPool(cfg.NumberOfWorkers)
	pool.Start(ctx)

	var wg sync.WaitGroup

	consumer := kafka.NewConsumer(cfg)
	simChan, err := consumer.Start(ctx)
	if err != nil {
		log.Fatalf("Failed to start Kafka consumer: %v\n", err)
	}

	wg.Go(func() {
		for simulation := range simChan {
			if !pool.SubmitJob(simulation) {
				log.Printf("Worker pool is shutting down, stopped accepting simulations")
				break
			}
		}
	})

	<-sigChan
	log.Println("Shutdown signal received, initiating graceful shutdown")
	cancel()

	log.Println("Stopping Kafka consumer...")
	if err := consumer.Stop(); err != nil {
		log.Printf("Error stopping Kafka consumer: %v\n", err)
	}

	log.Println("Stopping working pool...")
	pool.Stop()

	wg.Wait()
	log.Println("Graceful shutdown completed")
}
