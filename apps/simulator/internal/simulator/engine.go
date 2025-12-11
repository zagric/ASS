package simulator

import (
	"fmt"
	"math"
	"math/rand"
	"simulator/internal/models"
	"simulator/pkg/random"
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

type SimulationEngine struct {
	Config            models.Simulation
	StartedAt         time.Time
	Buffer            Buffer
	Dispatchers       []Dispatcher
	Requests          []*Request
	Stats             Statistics
	CurrentTime       time.Duration
	CurrentDispatcher int
	Active            bool
	nextRequest       []time.Time
	nextReqID         int
	StepSnapshot      StepSnapshot
}

type Dispatcher struct {
	ID           int
	IsBusy       bool
	CurrentReq   *Request
	ServiceStart time.Time
	ServiceTime  time.Duration
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

type Statistics struct {
	TotalRequests       int
	Processed           int
	Rejected            int
	TotalWaitTime       time.Duration
	TotalServiceTime    time.Duration
	DispatchersBusyTime []time.Duration
}

type StepSnapshot struct {
	IsChanged           bool
	GeneratedRequests   []*Request
	RejectedRequests    []*Request
	FinishedRequests    []*Request
	BufferState         []*Request
	Dispatchers         []Dispatcher
	RejectionPercentage int
	Timestamp           time.Duration
}

func NewEngine(config models.Simulation) *SimulationEngine {
	engine := &SimulationEngine{
		Config:    config,
		StartedAt: time.Now(),
		Buffer: Buffer{
			Size:  config.BufferSize,
			Slots: make([]*Request, config.BufferSize),
		},
		Dispatchers: make([]Dispatcher, config.ConsumersCount),
		Stats: Statistics{
			DispatchersBusyTime: make([]time.Duration, config.ConsumersCount),
		},
	}

	engine.initRequestGenerator()

	for i := range engine.Dispatchers {
		engine.Dispatchers[i] = Dispatcher{
			ID:     i,
			IsBusy: false,
		}
	}

	return engine
}

func (e *SimulationEngine) Run() *Statistics {
	endTime := e.Config.SimulationDuration * time.Second
	const simulationStep = 1000 * time.Microsecond
	ticker := time.NewTicker(simulationStep)
	defer ticker.Stop()

	for e.CurrentTime < endTime {
		<-ticker.C
		snapshot := e.step()
		if snapshot.IsChanged {
			fmt.Println(snapshot)
		}
		e.CurrentTime += simulationStep
		e.StepSnapshot = StepSnapshot{}
	}

	return &e.Stats
}

func (e *SimulationEngine) step() StepSnapshot {
	e.generateRequests()
	e.processRequests()
	e.processDispatchers()

	if e.Stats.TotalRequests == 0 {
		e.StepSnapshot.RejectionPercentage = 0
	} else {
		e.StepSnapshot.RejectionPercentage = e.Stats.Rejected * 100 / e.Stats.TotalRequests
	}
	e.StepSnapshot.Timestamp = time.Since(e.StartedAt)
	e.StepSnapshot.BufferState = e.Buffer.Slots
	e.StepSnapshot.Dispatchers = e.Dispatchers

	return e.StepSnapshot
}

func (e *SimulationEngine) initRequestGenerator() {
	e.nextRequest = make([]time.Time, e.Config.ProducerCount)

	for i := 0; i < e.Config.ProducerCount; i++ {
		interval := random.ExponentialTime(e.Config.RequestRate)
		e.nextRequest[i] = time.Now().Add(interval)
	}
}

func (e *SimulationEngine) generateRequests() {
	now := time.Now()

	for i := 0; i < e.Config.ProducerCount; i++ {
		if now.After(e.nextRequest[i]) {
			source := rand.Intn(e.Config.ProducerCount)

			req := &Request{
				ID:          e.nextReqID,
				Source:      source,
				GeneratedAt: now,
			}
			e.nextReqID++
			e.StepSnapshot.GeneratedRequests = append(e.StepSnapshot.GeneratedRequests, req)
			e.StepSnapshot.IsChanged = true

			if e.addToBuffer(req) {
				req.Status = Buffered
				e.Requests = append(e.Requests, req)
			} else {
				req.Status = Rejected
				e.StepSnapshot.RejectedRequests = append(e.StepSnapshot.RejectedRequests, req)
				e.Requests = append(e.Requests, req)
				e.Stats.Rejected++
			}
			e.Stats.TotalRequests++

			interval := random.ExponentialTime(e.Config.RequestRate)
			e.nextRequest[i] = now.Add(interval)
		}
	}
}

func (e *SimulationEngine) addToBuffer(req *Request) bool {
	for i := 0; i < e.Buffer.Size; i++ {
		if e.Buffer.Slots[i] == nil {
			e.Buffer.Slots[i] = req
			e.Buffer.Count++
			return true
		}
	}

	minPriority := math.MaxInt
	minIndex := -1

	for i := 0; i < e.Buffer.Size; i++ {
		if e.Buffer.Slots[i].Source < minPriority {
			minPriority = e.Buffer.Slots[i].Source
			minIndex = i
		}
	}

	if minIndex != -1 {
		e.Buffer.Slots[minIndex].Status = Rejected

		e.StepSnapshot.RejectedRequests = append(e.StepSnapshot.RejectedRequests, e.Buffer.Slots[minIndex])

		e.Buffer.Slots[minIndex] = req
		e.Stats.Rejected++
		return true
	}

	return false
}

func (e *SimulationEngine) processRequests() {
	sources := make(map[int][]*Request)

	for i := 0; i < e.Buffer.Size; i++ {
		if e.Buffer.Slots[i] != nil {
			source := e.Buffer.Slots[i].Source
			sources[source] = append(sources[source], e.Buffer.Slots[i])
		}
	}

	for i := 0; i < e.Config.ProducerCount; i++ {
		for _, req := range sources[i] {
			if e.assignToDispatcher(req) {
				for i := 0; i < e.Buffer.Size; i++ {
					if e.Buffer.Slots[i] == req {
						e.Buffer.Slots[i] = nil
						e.Buffer.Count--
						break
					}
				}
			}
		}
	}
}

func (e *SimulationEngine) assignToDispatcher(req *Request) bool {
	for i := 0; i < len(e.Dispatchers); i++ {
		idx := (e.CurrentDispatcher + i) % len(e.Dispatchers)
		dispatcher := &e.Dispatchers[idx]

		if !dispatcher.IsBusy {
			dispatcher.IsBusy = true
			dispatcher.CurrentReq = req
			dispatcher.ServiceStart = time.Now()
			dispatcher.ServiceTime = random.ExponentialTime(1 + rand.Float64()*4)

			req.Status = Processing

			e.Stats.TotalWaitTime += time.Since(req.GeneratedAt)
			e.CurrentDispatcher = (idx + 1) % len(e.Dispatchers)

			return true
		}
	}

	return false
}

func (e *SimulationEngine) processDispatchers() {
	for i := range e.Dispatchers {
		if e.Dispatchers[i].IsBusy {
			if time.Since(e.Dispatchers[i].ServiceStart) >= e.Dispatchers[i].ServiceTime {
				e.Dispatchers[i].IsBusy = false
				e.Dispatchers[i].CurrentReq.Status = Finished
				e.StepSnapshot.FinishedRequests = append(e.StepSnapshot.FinishedRequests, e.Dispatchers[i].CurrentReq)
				e.StepSnapshot.IsChanged = true
				e.Dispatchers[i].CurrentReq = nil

				e.Stats.TotalServiceTime += time.Since(e.Dispatchers[i].ServiceStart)

				e.Stats.Processed++
			} else {
				e.Stats.DispatchersBusyTime[i] += 1000 * time.Microsecond
			}
		}
	}
}
