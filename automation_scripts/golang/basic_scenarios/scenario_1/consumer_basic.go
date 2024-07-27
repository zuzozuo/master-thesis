package scenario_1

import (
	"fmt"
	"strconv"
	"time"

	global "project/global"

	amqp "github.com/streadway/amqp"
)

func RunConsumerBasic() {
	conn, err := amqp.Dial("amqp://" + global.USER + ":" + global.USER + "@" + global.ADDR + ":" + strconv.Itoa(global.RABBITMQ_PORT) + "/")

	global.FailOnError(err, "Failed to connect to RabbitMQ")

	defer conn.Close()

	ch, err := conn.Channel()

	global.FailOnError(err, "Failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"test_queue",
		false,
		false,
		false,
		false,
		nil,
	)

	global.FailOnError(err, "Failed to declare queue")

	msgs, err := ch.Consume(
		q.Name,
		"",
		true,
		false,
		false,
		false,
		nil,
	)

	global.FailOnError(err, "Failed to register a consumer")

	forever := make(chan bool)

	go func() {
		for d := range msgs {
			fmt.Printf("Received: %s\n", d.Body)
			// Simulate work
			time.Sleep(1 * time.Second)
			fmt.Printf("Done")
		}
	}()

	fmt.Println("Waiting for messages. To exit press CTRL+C")
	<-forever
}
