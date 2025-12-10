package random

import (
	"math"
	"math/rand"
	"time"
)

func Exponential(lambda float64) float64 {
	u := rand.Float64()
	return -math.Log(1.0-u) / lambda
}

func ExponentialTime(lambda float64) time.Duration {
	return time.Duration(Exponential(lambda) * float64(time.Second))
}
