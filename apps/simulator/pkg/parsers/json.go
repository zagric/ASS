package parsers

import (
	"fmt"
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
