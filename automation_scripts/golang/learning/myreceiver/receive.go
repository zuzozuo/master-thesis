package myreceiver

import (
	"fmt"
	"log"
	"strconv"

	consts "learning/configs"
	myutils "learning/myutils"

	amqp "github.com/rabbitmq/amqp091-go"
)

func MyReceive() {
	fmt.Println("Hihi odbijuuurrr")

	conn, err := amqp.Dial("amqp://" + consts.USERNAME + ":" + consts.PASSWORD + "@" + consts.CONN_STRING + ":" + strconv.Itoa(consts.CONN_PORT) + "/")
	myutils.FailOnError(err, "Failed to connect to RabbitMQ")
	defer conn.Close()

	ch, err := conn.Channel()
	myutils.FailOnError(err, "Failed to open a channel")
	defer ch.Close()

	q, err := ch.QueueDeclare(
		"hello", // name
		false,   // durable
		false,   // delete when unused
		false,   // exclusive
		false,   // no-wait
		nil,     // arguments
	)

	myutils.FailOnError(err, "Failed to declare a queue")

	msgs, err := ch.Consume(
		q.Name, // queue
		"",     // consumer
		true,   // auto-ack
		false,  // exclusive
		false,  // no-local
		false,  // no-wait
		nil,    // args
	)

	myutils.FailOnError(err, "Failed to register a consumer")

	var forever chan struct{}

	go func() {
		for d := range msgs {
			log.Printf("Received a message: %s", d.Body)
		}
	}()

	log.Printf(" [*] Waiting for messages. To exit press CTRL+C")
	<-forever

}