package worker

import (
	"context"
	"fmt"
	"log"
	"simulator/internal/models"
	"simulator/internal/simulator"
	"sync"
)

type WorkerPool struct {
	numWorkers int
	jobs       chan models.Simulation
	results    chan models.SimulationResult
	done       chan struct{}
	workerWg   sync.WaitGroup
	cancelFunc context.CancelFunc
}

func NewWorkerPool(numWorkers int) *WorkerPool {
	return &WorkerPool{
		numWorkers: numWorkers,
		jobs:       make(chan models.Simulation, numWorkers),
		results:    make(chan models.SimulationResult, 100),
		done:       make(chan struct{}),
	}
}

func (p *WorkerPool) Start(ctx context.Context) {
	ctx, cancel := context.WithCancel(ctx)
	p.cancelFunc = cancel

	log.Printf("Starting worker pool with %d workers\n", p.numWorkers)

	p.workerWg.Add(p.numWorkers)
	for i := 0; i < p.numWorkers; i++ {
		workerId := i
		go p.worker(ctx, workerId)
	}

	go func() {
		<-ctx.Done()
		log.Println("Worker pool shutting down")
		close(p.jobs)
		p.workerWg.Wait()
		close(p.results)
		close(p.done)
	}()
}

func (p *WorkerPool) SubmitJob(simulation models.Simulation) bool {
	select {
	case p.jobs <- simulation:
		return true
	case <-p.done:
		return false
	}
}

func (p *WorkerPool) Stop() {
	p.cancelFunc()
	<-p.done
}

func (p *WorkerPool) worker(ctx context.Context, id int) {
	defer p.workerWg.Done()
	log.Printf("Worker %d started\n", id)

	for simulation := range p.jobs {
		select {
		case <-ctx.Done():
			return
		default:
			log.Printf("[Worker %d] Starting simulation with id: %s", id, simulation.SimulationOID)
			result := p.processSimulation(simulation)

			fmt.Println(result)

			select {
			case p.results <- result:
				// Result sent successfully
			case <-ctx.Done():
				return
			}
		}
	}

	log.Printf("Worker %d stopped\n", id)
}

func (p *WorkerPool) processSimulation(simulation models.Simulation) models.SimulationResult {
	engine := simulator.NewEngine(simulation)
	stats := engine.Run()

	return models.SimulationResult{
		SimulationOID:         engine.Config.SimulationOID,
		RequestsGenerated:     stats.TotalRequests,
		RequestsRejected:      stats.Rejected,
		RequestsProcessed:     stats.Processed,
		AverageRejection:      stats.Rejected * 100 / stats.TotalRequests,
		AverageWaitingTime:    int(stats.TotalWaitTime) / stats.Processed,
		AverageProcessingTime: int(stats.TotalServiceTime) / stats.Processed,
	}
}
