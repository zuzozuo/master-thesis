package scenario_1

import (
	"log"
	global "project/global"
	"strconv"
	"time"

	amqp "github.com/streadway/amqp"
)

func RunConsumerOptimized() {
	conn, err := amqp.Dial("amqp://" + global.USER + ":" + global.USER + "@" + global.ADDR + ":" + strconv.Itoa(global.RABBITMQ_PORT) + "/")

	global.FailOnError(err, "Failed to open a channel")

	defer conn.Close()
	ch, err := conn.Channel()
	global.FailOnError(err, "Failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"task_queue", // name
		true,         // durable
		false,        // delete when unused
		false,        // exclusive
		false,        // no-wait
		nil,          // arguments
	)
	global.FailOnError(err, "Failed to declare a queue")

	err = ch.Qos(
		1,     // prefetch count
		0,     // prefetch size
		false, // global
	)

	global.FailOnError(err, "Failed to set QoS")

	msgs, err := ch.Consume(
		q.Name, // queue
		"",     // consumer
		false,  // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)

	global.FailOnError(err, "Failed to register a consumer")

	forever := make(chan bool)

	go func() {
		for d := range msgs {
			log.Printf("Received a message: %s", d.Body)
			// Simulate work
			time.Sleep(1 * time.Second)
			log.Printf("Done")

			d.Ack(false)
		}
	}()

	log.Printf(" [*] Waiting for messages. To exit press CTRL+C")
	<-forever

}
