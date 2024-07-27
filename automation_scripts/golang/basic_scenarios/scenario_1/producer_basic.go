package scenario_1

import (
	"fmt"
	"log"
	"project/global"
	"strconv"
	"time"

	"github.com/streadway/amqp"
)

func RunProducerBasic(params global.Scenario1Params) {
	conn, err := amqp.Dial("amqp://" + global.USER + ":" + global.USER + "@" + global.ADDR + ":" + strconv.Itoa(global.RABBITMQ_PORT) + "/")
	if err != nil {
		log.Fatalf("Failed to connect to RabbitMQ: %v", err)
	}
	defer conn.Close()

	ch, err := conn.Channel()
	if err != nil {
		log.Fatalf("Failed to open a channel: %v", err)
	}
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"test_queue",
		false,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		log.Fatalf("Failed to declare a queue: %v", err)
	}

	for i := 0; i < params.MessageAmount; i++ {
		body := fmt.Sprintf("Message %d", i)
		err = ch.Publish(
			"",
			q.Name,
			false,
			false,
			amqp.Publishing{
				ContentType: "text/plain",
				Body:        []byte(body),
			})
		if err != nil {
			log.Fatalf("Failed to publish a message: %v", err)
		}
		fmt.Printf("Sent: %s\n", body)
		time.Sleep(10 * time.Millisecond) // simulate some delay
	}
}
