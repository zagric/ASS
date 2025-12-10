package kafka

import (
	"context"
	"encoding/json"
	"log"
	"simulator/internal/config"
	"simulator/internal/simulation"
	"time"

	"github.com/segmentio/kafka-go"
)

type Consumer struct {
	reader *kafka.Reader
	config *config.Config
}

func NewConsumer(cfg *config.Config) (*Consumer, error) {
	reader := kafka.NewReader(kafka.ReaderConfig{
		Brokers:        cfg.KafkaBrokers,
		Topic:          cfg.KafkaSimConfigTopic,
		GroupID:        cfg.KafkaGroupID,
		CommitInterval: time.Second,
	})

	return &Consumer{
		reader: reader,
		config: cfg,
	}, nil
}

func (c *Consumer) Start(ctx context.Context) error {
	log.Printf("Consumer started")

	for {
		select {
		case <-ctx.Done():
			return nil
		default:
			msg, err := c.reader.ReadMessage(ctx)
			if err != nil {
				continue
			}

			c.processMessage(msg.Value)
		}
	}
}

func (c *Consumer) processMessage(data []byte) {
	var simMsg simulation.SimulationConfig
	if err := json.Unmarshal(data, &simMsg); err != nil {
		log.Printf("Error parsing message: %v", err)
		return
	}

	simConfig := simulation.SimulationConfig{
		EventID:            simMsg.EventID,
		OccurredAt:         simMsg.OccurredAt,
		SimulationOID:      simMsg.SimulationOID,
		SimulationDuration: simMsg.SimulationDuration,
		RequestRate:        simMsg.RequestRate,
		ProducerCount:      simMsg.ProducerCount,
		ConsumersCount:     simMsg.ConsumersCount,
		BufferSize:         simMsg.BufferSize,
	}

	engine := simulation.NewEngine(simConfig)
	log.Printf("Message: %v", simMsg)
	engine.Run()
}

func (c *Consumer) Close() error {
	if c.reader != nil {
		return c.reader.Close()
	}
	return nil
}
