package scenario_1

import (
	"fmt"
	"log"
	global "project/global"
	"strconv"
	"time"

	"github.com/streadway/amqp"
)

func RunProducerOptimized(params global.Scenario1Params) {
	conn, err := amqp.Dial("amqp://" + global.USER + ":" + global.USER + "@" + global.ADDR + ":" + strconv.Itoa(global.RABBITMQ_PORT) + "/")
	global.FailOnError(err, "Failed to connect to RabbitMQ")
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

	for i := 0; i < params.MessageAmount; i++ {

		body := fmt.Sprintf("Message %d:  %v", i, global.GenerateRandomString(20))
		err = ch.Publish(
			"",     // exchange
			q.Name, // routing key
			false,  // mandatory
			false,  // immediate
			amqp.Publishing{
				ContentType:  "text/plain",
				Body:         []byte(body),
				DeliveryMode: amqp.Persistent, // Make message persistent
			})

		global.FailOnError(err, "Failed to publish a message")

		log.Printf(" [x] Sent %s", body)
		time.Sleep(10 * time.Millisecond) // simulate some delay

	}

}
