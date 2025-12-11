package kafka

import (
	"context"
	"log"
	"simulator/internal/config"
	"simulator/internal/models"
	"time"

	"github.com/segmentio/kafka-go"
)

type Consumer struct {
	reader         *kafka.Reader
	simulationChan chan models.Simulation
	cancelFunc     context.CancelFunc
	done           chan struct{}
	config         *config.Config
}

func NewConsumer(cfg *config.Config) *Consumer {
	reader := kafka.NewReader(kafka.ReaderConfig{
		Brokers:        cfg.KafkaBrokers,
		Topic:          cfg.KafkaSimConfigTopic,
		GroupID:        cfg.KafkaGroupID,
		CommitInterval: time.Second,
	})

	return &Consumer{
		reader:         reader,
		simulationChan: make(chan models.Simulation, cfg.NumberOfWorkers),
		done:           make(chan struct{}),
		config:         cfg,
	}
}

func (c *Consumer) Start(ctx context.Context) (<-chan models.Simulation, error) {
	ctx, cancel := context.WithCancel(ctx)
	c.cancelFunc = cancel

	go func() {
		defer close(c.done)
		defer close(c.simulationChan)

		log.Printf("Starting Kafka consumer for topic: %s\n", c.config.KafkaSimConfigTopic)

		for {
			select {
			case <-ctx.Done():
				log.Println("Kafka consumer shutting down")
				return
			default:
				msg, err := c.reader.ReadMessage(ctx)
				if err != nil {
					if ctx.Err() == context.Canceled {
						return
					}
					log.Printf("Error reading message: %v", err)
					time.Sleep(time.Second)
					continue
				}

				sim, err := models.SimulationFromJSON(msg.Value)
				if err != nil {
					log.Printf("Error unmarshaling simulation: %v", err)
					continue
				}

				select {
				case c.simulationChan <- *sim:
					// Message successfully sent to channel
				case <-ctx.Done():
					return
				}

				// c.processMessage(msg.Value)
			}
		}
	}()

	return c.simulationChan, nil
}

func (c *Consumer) Stop() error {
	c.cancelFunc()
	<-c.done
	return c.reader.Close()
}
