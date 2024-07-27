package global

import (
	"log"
	"math/rand"
	"time"
)

// Create a new random number generator
var src = rand.NewSource(time.Now().UnixNano())
var r = rand.New(src)

func GenerateRandomString(strLen int) string {

	const charset = "abcdefghijklmnopqrstuvwxyz" +
		"ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	b := make([]byte, strLen)
	for i := range b {
		b[i] = charset[r.Intn(len(charset))]
	}
	return string(b)

}

func FailOnError(err error, msg string) {
	if err != nil {
		log.Fatalf("%s: %s", msg, err)
	}
}
