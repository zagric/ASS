package simulation

import (
	"time"
)

type RequestStatus int

const (
	Created RequestStatus = iota
	Buffered
	Processing
	Finished
	Rejected
)

type SimulationConfig struct {
	EventID            string        `json:"event_id"`
	OccurredAt         JsonTime      `json:"occurred_at"`
	SimulationOID      string        `json:"simulation_oid"`
	SimulationDuration time.Duration `json:"simulation_duration"`
	RequestRate        float64       `json:"request_rate"`
	ProducerCount      int           `json:"producers_count"`
	ConsumersCount     int           `json:"consumers_count"`
	BufferSize         int           `json:"buffer_size"`
}

type Request struct {
	ID          int
	Source      int
	GeneratedAt time.Time
	Status      RequestStatus
}

type Buffer struct {
	Size  int
	Slots []*Request
	Count int
}

type Dispatcher struct {
	ID           int
	IsBusy       bool
	CurrentReq   *Request
	ServiceStart time.Time
	ServiceTime  time.Duration
}

type SimulationEngine struct {
	Config            SimulationConfig
	Buffer            Buffer
	Dispatchers       []Dispatcher
	Requests          []*Request
	Stats             Statistics
	CurrentTime       time.Duration
	CurrentDispatcher int
	Active            bool
	nextRequest       []time.Time
	nextReqID         int
}

type Statistics struct {
	TotalRequests       int
	Processed           int
	Rejected            int
	TotalWaitTime       time.Duration
	TotalServiceTime    time.Duration
	DispatchersBusyTime []time.Duration
}
