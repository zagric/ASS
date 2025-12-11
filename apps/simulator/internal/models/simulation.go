package models

import (
	"encoding/json"
	"simulator/pkg/parsers"
	"time"
)

type Simulation struct {
	EventID            string           `json:"event_id"`
	OccurredAt         parsers.JsonTime `json:"occurred_at"`
	SimulationOID      string           `json:"simulation_oid"`
	SimulationDuration time.Duration    `json:"simulation_duration"`
	RequestRate        float64          `json:"request_rate"`
	ProducerCount      int              `json:"producers_count"`
	ConsumersCount     int              `json:"consumers_count"`
	BufferSize         int              `json:"buffer_size"`
}

type SimulationResult struct {
	SimulationOID         string `json:"simulation_oid"`
	RequestsGenerated     int    `json:"generated_requests"`
	RequestsRejected      int    `json:"rejected_requests"`
	RequestsProcessed     int    `json:"processed_requests"`
	AverageRejection      int    `json:"average_rejection"`
	AverageWaitingTime    int    `json:"average_waiting"`
	AverageProcessingTime int    `json:"average_processing"`
}

func SimulationFromJSON(data []byte) (*Simulation, error) {
	var simulation Simulation
	err := json.Unmarshal(data, &simulation)
	return &simulation, err
}

func (r *SimulationResult) ToJSON() ([]byte, error) {
	return json.Marshal(r)
}

func ResultFromJSON(data []byte) (*SimulationResult, error) {
	var result SimulationResult
	err := json.Unmarshal(data, &result)
	return &result, err
}
