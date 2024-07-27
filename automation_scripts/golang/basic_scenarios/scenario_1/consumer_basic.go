package scenario_1

import (
	"fmt"
	"log"
	"strconv"

	global "project/global"

	amqp "github.com/streadway/amqp"
)

func RunConsumerBasic() {
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

	msgs, err := ch.Consume(
		q.Name,
		"",
		true,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		log.Fatalf("Failed to register a consumer: %v", err)
	}

	forever := make(chan bool)

	go func() {
		for d := range msgs {
			fmt.Printf("Received: %s\n", d.Body)
		}
	}()

	fmt.Println("Waiting for messages. To exit press CTRL+C")
	<-forever
}
