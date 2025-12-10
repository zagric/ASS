package config

import (
	"os"
	"strings"

	"github.com/joho/godotenv"
)

type Config struct {
	KafkaBrokers        []string `env:"KAFKA_BROKERS"`
	KafkaSimConfigTopic string   `env:"KAFKA_SIM_CONFIG_TOPIC"`
	KafkaStatsTopic     string   `env:"KAFKA_STATS_TOPIC"`
	KafkaGroupID        string   `env:"KAFKA_GROUP_ID"`
	DBConnection        string   `env:"DB_CONNECTION"`
	ServerPort          string   `env:"SERVER_PORT"`
	LogLevel            string   `env:"LOG_LEVEL"`
}

func Load() (*Config, error) {
	godotenv.Load()

	brokers := os.Getenv("KAFKA_BROKERS")
	if brokers == "" {
		brokers = "kafka:29092"
	}

	return &Config{
		KafkaBrokers:        strings.Split(brokers, ","),
		KafkaSimConfigTopic: getEnv("KAFKA_SIM_CONFIG_TOPIC", "new-simulation-created"),
		KafkaStatsTopic:     getEnv("KAFKA_STATS_TOPIC", "simulation-stats"),
		KafkaGroupID:        getEnv("KAFKA_GROUP_ID", "simulation-group"),
		DBConnection:        os.Getenv("DB_CONNECTION"),
		ServerPort:          getEnv("SERVER_PORT", "8080"),
		LogLevel:            getEnv("LOG_LEVEL", "info"),
	}, nil
}

func getEnv(key, defaultValue string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return defaultValue
}
