package simulation

import (
	"fmt"
	"math"
	"math/rand"
	"simulator/pkg/random"
	"strings"
	"time"
)

type JsonTime struct {
	time.Time
}

const layout = "2006-01-02T15:04:05.999999"

func (jt *JsonTime) UnmarshalJSON(b []byte) (err error) {
	s := strings.Trim(string(b), `"`)
	if s == "null" {
		return
	}
	jt.Time, err = time.Parse(layout, s)
	return
}

func (jt JsonTime) MarshalJSON() ([]byte, error) {
	if jt.Time.IsZero() {
		return nil, nil
	}
	return []byte(fmt.Sprintf(`"%s"`, jt.Time.Format(layout))), nil
}

func NewEngine(config SimulationConfig) *SimulationEngine {
	engine := &SimulationEngine{
		Config: config,
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

func (e *SimulationEngine) Run() {
	endTime := e.Config.SimulationDuration * time.Second
	const simulationStep = 1000 * time.Microsecond
	ticker := time.NewTicker(simulationStep)
	defer ticker.Stop()

	for e.CurrentTime < endTime {
		<-ticker.C
		e.step()
		e.CurrentTime += simulationStep
	}

	fmt.Println(e.Stats)
}

func (e *SimulationEngine) step() {
	e.generateRequests()
	e.processRequests()
	e.processDispatchers()
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

			if e.addToBuffer(req) {
				req.Status = Buffered
				e.Requests = append(e.Requests, req)
			} else {
				req.Status = Rejected
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
				e.Dispatchers[i].CurrentReq = nil

				e.Stats.Processed++
			} else {
				e.Stats.DispatchersBusyTime[i] += 1000 * time.Microsecond
			}
		}
	}
}
