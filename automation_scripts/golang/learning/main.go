package main

import (
	"fmt"
	myreceiver "learning/myreceiver"
	mysender "learning/mysender"
	"time"
)

func main() {
	fmt.Println("Wowow")
	mysender.MySend()
	time.Sleep(30 * time.Second)
	myreceiver.MyReceive()

}
