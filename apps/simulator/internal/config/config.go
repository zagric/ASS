package config

import (
	"os"
	"strconv"
	"strings"

	"github.com/joho/godotenv"
)

type Config struct {
	KafkaBrokers        []string `env:"KAFKA_BROKERS"`
	KafkaSimConfigTopic string   `env:"KAFKA_SIM_CONFIG_TOPIC"`
	KafkaStatsTopic     string   `env:"KAFKA_STATS_TOPIC"`
	KafkaGroupID        string   `env:"KAFKA_GROUP_ID"`
	DBConnection        string   `env:"DB_CONNECTION"`
	NumberOfWorkers     int      `env:"WORKERS_COUNT"`
	ServerPort          string   `env:"SERVER_PORT"`
	LogLevel            string   `env:"LOG_LEVEL"`
}

func Load() (*Config, error) {
	godotenv.Load()

	return &Config{
		KafkaBrokers:        getEnvAsSlice("KAFKA_BROKERS", []string{"kafka:29092"}, ","),
		KafkaSimConfigTopic: getEnv("KAFKA_SIM_CONFIG_TOPIC", "new-simulation-created"),
		KafkaStatsTopic:     getEnv("KAFKA_STATS_TOPIC", "simulation-stats"),
		KafkaGroupID:        getEnv("KAFKA_GROUP_ID", "simulation-group"),
		DBConnection:        os.Getenv("DB_CONNECTION"),
		NumberOfWorkers:     getEnvAsInt("WORKERS_COUNT", 4),
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

func getEnvAsInt(key string, defaultValue int) int {
	valueStr := getEnv(key, "")
	if value, err := strconv.Atoi(valueStr); err == nil {
		return value
	}

	return defaultValue
}

func getEnvAsBool(key string, defaultValue bool) bool {
	valueStr := getEnv(key, "")
	if value, err := strconv.ParseBool(valueStr); err == nil {
		return value
	}

	return defaultValue
}

func getEnvAsSlice(key string, defaultValue []string, sep string) []string {
	valueStr := getEnv(key, "")
	if valueStr == "" {
		return defaultValue
	}

	return strings.Split(valueStr, sep)
}
